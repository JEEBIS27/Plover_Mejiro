use super::*;
/// Render one output while carrying a final small-tsu across strokes. Keys are
/// never transliterated. The state is returned only after successful conversion.
pub fn render(output: &mut Output, state: &mut State) -> Result<()> {
    if state.mode == Mode::Kana {
        return Ok(());
    }
    let old = *output;
    let mut new = Output::new();
    new.context = old.context;
    let mut from = 0;
    let mut pending = state.pending_sokuon;
    for op in old.operations() {
        render_text(
            &old.text.as_str()[from..op.byte_offset],
            state.mode,
            &mut pending,
            &mut new,
        )?;
        // A real key operation terminates the text run. The reference emits
        // a pending small-tsu before that operation, rather than carrying it
        // across Return/Space/Tab into unrelated text.
        if pending {
            new.push_text(if state.mode == Mode::Romaji {
                "ltsu"
            } else {
                "Z"
            })?;
            pending = false;
        }
        new.push_key(op.key)?;
        from = op.byte_offset;
    }
    render_text(
        &old.text.as_str()[from..],
        state.mode,
        &mut pending,
        &mut new,
    )?;
    *output = new;
    state.pending_sokuon = pending;
    Ok(())
}
fn render_text(text: &str, mode: Mode, pending: &mut bool, out: &mut Output) -> Result<()> {
    let mut working: Text = Text::new();
    if *pending {
        working.push("っ")?;
    }
    working.push(text)?;
    *pending = false;
    if working.as_str().ends_with('っ') {
        *pending = true;
        working.pop_char();
    }
    if mode == Mode::Jis {
        for c in working.as_str().chars() {
            if c == 'を' {
                out.push_key(Key::Shift0)?;
            } else {
                let mut buf = [0; 4];
                let key = c.encode_utf8(&mut buf);
                out.push_text(get(JIS, key).copied().unwrap_or(key))?;
            }
        }
        return Ok(());
    }
    let mut raw: Text = Text::new();
    let mut rest = working.as_str();
    while !rest.is_empty() {
        let mut chars = rest.char_indices();
        let (_, first) = chars.next().unwrap();
        let n1 = first.len_utf8();
        let n2 = chars.next().map(|(i, c)| i + c.len_utf8());
        if let Some(n) = n2
            && let Some(roma) = get(ROMAJI, &rest[..n])
        {
            raw.push(roma)?;
            rest = &rest[n..];
            continue;
        }
        raw.push(get(ROMAJI, &rest[..n1]).copied().unwrap_or(&rest[..n1]))?;
        rest = &rest[n1..];
    }
    let mut doubled: Text = Text::new();
    let mut chars = raw.as_str().chars().peekable();
    while let Some(c) = chars.next() {
        if c == 'Q'
            && let Some(&next) = chars.peek()
            && "bcdfghjklmnpqrstvwxyz".contains(next)
        {
            let mut b = [0; 4];
            doubled.push(next.encode_utf8(&mut b))?;
            continue;
        }
        let mut b = [0; 4];
        doubled.push(c.encode_utf8(&mut b))?;
    }
    let mut chars = doubled.as_str().chars().peekable();
    while let Some(c) = chars.next() {
        if c == 'N' {
            out.push_text(
                if chars
                    .peek()
                    .is_some_and(|c| "bcdfghjklmpqrstvwxzQ".contains(*c))
                {
                    "n"
                } else {
                    "nn"
                },
            )?;
        } else if c == 'Q' {
            out.push_text("ltsu")?;
        } else {
            let mut b = [0; 4];
            out.push_text(c.encode_utf8(&mut b))?;
        }
    }
    Ok(())
}
