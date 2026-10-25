use super::*;
fn particle_index(p: &str) -> usize {
    PARTICLE_KEY_LIST.iter().position(|s| *s == p).unwrap()
}
fn base_kana(consonant: &str, vowel: &str, particle: Option<&str>, fallback: &str) -> Result<Text> {
    let cv = small_key(&[consonant, vowel])?;
    let empty = cv.as_str().is_empty() || cv.as_str() == "STN";
    if empty {
        return Text::of(
            particle
                .map(|p| SECOND_SOUND_LIST[particle_index(p)])
                .unwrap_or(""),
        );
    }
    let current = if vowel.is_empty() { fallback } else { vowel };
    let minor_key = small_key(&[current, particle.unwrap_or("")])?;
    let minor = particle.and_then(|_| get(MINOR_DIPHTHONGS, minor_key.as_str()));
    if minor.is_none()
        && let Some(kana) = get(EXCEPTION_KANA, cv.as_str())
    {
        return join(&[
            kana,
            particle
                .map(|p| SECOND_SOUND_LIST[particle_index(p)])
                .unwrap_or(""),
        ]);
    }
    let (v, suffix, extra) = if let Some(row) = minor {
        (row[0], row[1], "")
    } else if let Some(row) = get(DIPHTHONGS, current) {
        (
            row[0],
            row[1],
            particle
                .map(|p| SECOND_SOUND_LIST[particle_index(p)])
                .unwrap_or(""),
        )
    } else {
        (
            value(VOWELS, current),
            "",
            particle
                .map(|p| SECOND_SOUND_LIST[particle_index(p)])
                .unwrap_or(""),
        )
    };
    let index = ["a", "i", "u", "e", "o", "ya", "yu", "yo"]
        .iter()
        .position(|x| *x == v)
        .ok_or(Error::InvalidStroke)?;
    let consonant = value(CONSONANTS, consonant);
    let row = get(KANA, consonant).ok_or(Error::InvalidStroke)?;
    join(&[row[index], suffix, extra])
}
fn choose_he(context: Context, right: &str) -> &'static str {
    let ka = if matches!(right, "k" | "nk") {
        matches!(context, Context::Nominalizable | Context::IndefiniteNoun)
    } else {
        matches!(
            context,
            Context::Nominalizable
                | Context::QuestionPredicate
                | Context::Noun
                | Context::IndefiniteNoun
                | Context::QuestionParticle
        )
    };
    if ka { "か" } else { "へ" }
}
pub fn particle(left: &str, right: &str, context: Context) -> Result<Output> {
    if !PARTICLE_KEY_LIST.contains(&left) || !PARTICLE_KEY_LIST.contains(&right) {
        return Err(Error::InvalidStroke);
    }
    let mut out = Output::new();
    let key = small_key(&[left, "-", right])?;
    match key.as_str() {
        "-n" => out.push_key(Key::Return)?,
        "n-" => out.push_key(Key::Space)?,
        "n-n" => out.push_key(Key::Tab)?,
        _ => {
            if let Some(text) = get(PARTICLE_EXCEPTIONS, key.as_str()) {
                out.push_text(text)?;
            } else {
                let l = if left == "ntk" {
                    choose_he(context, right)
                } else {
                    L_PARTICLE[particle_index(left)]
                };
                let r = R_PARTICLE[particle_index(right.strip_prefix('n').unwrap_or(right))];
                if matches!(left, "n" | "") && right == "ntk" {
                    out.push_text(R_PARTICLE[particle_index(right)])?;
                    if left == "n" {
                        out.push_text("、")?;
                    }
                } else if left == "n" && !right.is_empty() {
                    out.push_text(r)?;
                    out.push_text("、")?;
                } else if !left.is_empty() && matches!(right, "k" | "nk") {
                    if matches!(left, "nt" | "ntk") {
                        out.push_text(l)?;
                        out.push_text("の")?;
                    } else {
                        out.push_text("の")?;
                        out.push_text(l)?;
                    }
                    if out.text.as_str() == "のの" {
                        out.text = Text::of(
                            if matches!(context, Context::Nominalizable | Context::AttributiveNa) {
                                "のが"
                            } else {
                                "な"
                            },
                        )?;
                    }
                    if right.contains('n') {
                        out.push_text("、")?;
                    }
                } else {
                    out.push_text(l)?;
                    out.push_text(r)?;
                    if right.contains('n') {
                        out.push_text("、")?;
                    }
                }
            }
        }
    }
    out.context = particle_context(out.text.as_str());
    Ok(out)
}
fn particle_context(text: &str) -> Context {
    if text == "な" {
        Context::AttributiveNa
    } else if QUESTION_PARTICLES.contains(&text) {
        Context::QuestionParticle
    } else {
        Context::Incomplete
    }
}
fn attached_context(left: &str, right: &str, p: &Output, base: Context) -> Context {
    if left.is_empty() && right.is_empty() {
        base
    } else if left == "n" && matches!(right, "" | "n") {
        Context::Nominalizable
    } else {
        particle_context(p.text.as_str())
    }
}
fn verb_context(left: &str, right: &str, desu: bool) -> Context {
    if desu {
        return if right == "k" {
            Context::QuestionPredicate
        } else if matches!(right, "" | "t") {
            Context::Nominalizable
        } else {
            Context::Incomplete
        };
    }
    if left == "ntk" && matches!(right, "k" | "ntk") {
        return Context::QuestionPredicate;
    }
    if matches!(left, "nt" | "tk" | "ntk") {
        let is_complete = NOMINALIZABLE_EXCEPTIONS
            .iter()
            .any(|key| key.split_once('-') == Some((left, right)));
        if is_complete {
            Context::Nominalizable
        } else {
            Context::Incomplete
        }
    } else if right != "ntk" {
        Context::Nominalizable
    } else {
        Context::Incomplete
    }
}
fn abstract_word(s: &Stroke<'_>, key: &str) -> Result<Option<(Text, Context)>> {
    let full = small_key(&[key, if s.star { "*" } else { "" }])?;
    let lk = small_key(&[s.left.consonant, s.left.vowel])?;
    let rk = small_key(&[s.right.consonant, s.right.vowel])?;
    let (word, head, context) = if let Some(word) = get(ABSTRACT_MAP, full.as_str()) {
        (Text::of(word)?, *word, None)
    } else if s.star {
        if let (Some(l), Some(r)) = (
            get(ABSTRACT_MAP_LEFT, lk.as_str()),
            get(ABSTRACT_MAP_RIGHT, rk.as_str()),
        ) {
            let text = join(&[l, r])?;
            let text = replace(text.as_str(), "のふう", "んなふう")?;
            (
                text,
                *r,
                if r.is_empty() {
                    Some(if ATTRIBUTIVE_NA_WORDS.contains(l) {
                        Context::AttributiveNa
                    } else {
                        Context::Incomplete
                    })
                } else {
                    None
                },
            )
        } else {
            return Ok(None);
        }
    } else {
        return Ok(None);
    };
    // Empty composite abbreviations fall through in the Python reference too.
    if word.as_str().is_empty() {
        return Ok(None);
    }
    let context = context.unwrap_or_else(|| {
        if PLACE_WORDS.contains(&head) {
            Context::Place
        } else if INDEFINITE_WORDS.contains(&head) {
            Context::IndefiniteNoun
        } else if ATTRIBUTIVE_NA_WORDS.contains(&head) {
            Context::AttributiveNa
        } else if QUESTION_PARTICLES.contains(&head) {
            Context::QuestionParticle
        } else if head == "ただ" {
            Context::Incomplete
        } else {
            Context::Noun
        }
    });
    Ok(Some((word, context)))
}
fn conjugate(
    row: &[(&str, &[&str])],
    consonant: &str,
    index: usize,
    suffix: &str,
    voiced: bool,
) -> Result<Text> {
    let base = get(row, consonant).ok_or(Error::InvalidStroke)?[index];
    let text = join(&[base, suffix])?;
    if voiced && index == 6 {
        let choices = if consonant == "g" {
            [("いて", "いで"), ("いた", "いだ")]
        } else if matches!(consonant, "n" | "b" | "m") {
            [("んて", "んで"), ("んた", "んだ")]
        } else {
            [("", ""), ("", "")]
        };
        for (from, to) in choices {
            if !from.is_empty()
                && let Some(tail) = text.as_str().strip_prefix(from)
            {
                return join(&[to, tail]);
            }
        }
    }
    Ok(text)
}
fn verb(s: &Stroke<'_>, key: &str, left: &str, left_syllable: &str, right: &str) -> Result<Text> {
    let l = s.left.particle;
    let r = s.right.particle;
    let (i, suffix) = AUXILIARIES[particle_index(l) * 8 + particle_index(r)];
    let rc = value(CONSONANTS, s.right.consonant);
    let rc = if rc.is_empty() { "w" } else { rc };
    if s.right.consonant == "TN" && s.right.vowel.is_empty() {
        return join(&[left_syllable, value(DESU, r)]);
    }
    let special = match key {
        "I-K" => Some(IKU_LIST),
        "A-ST" => Some(ARU_LIST),
        "K-" => Some(KAHEN_LIST),
        _ => None,
    };
    if let Some(row) = special {
        return join(&[row[i], suffix]);
    }
    if left.is_empty() && l.is_empty() {
        if s.right.vowel == "I" && get(CONJUGATE_KAMI_MAP, rc).is_some() {
            return conjugate(CONJUGATE_KAMI_MAP, rc, i, suffix, false);
        }
        if s.right.vowel == "IA" && get(CONJUGATE_SIMO_MAP, rc).is_some() {
            return conjugate(CONJUGATE_SIMO_MAP, rc, i, suffix, false);
        }
    }
    if s.right.vowel.is_empty()
        && !s.right.consonant.is_empty()
        && get(CONJUGATE_GODAN_MAP, rc).is_some()
    {
        let tail = conjugate(CONJUGATE_GODAN_MAP, rc, i, suffix, true)?;
        return join(&[left, tail.as_str()]);
    }
    if !s.star {
        return Ok(Text::new());
    }
    for (registered, row, voiced) in [
        (VERB_GODAN_MAP, CONJUGATE_GODAN_MAP, true),
        (VERB_KAMI_MAP, CONJUGATE_KAMI_MAP, false),
        (VERB_SIMO_MAP, CONJUGATE_SIMO_MAP, false),
    ] {
        if let Some(entry) = get(registered, key) {
            let tail = conjugate(row, entry[1], i, suffix, voiced)?;
            let text = join(&[entry[0], tail.as_str()])?;
            return if voiced {
                replace(text.as_str(), "くださり", "ください")
            } else {
                Ok(text)
            };
        }
    }
    if s.right.vowel == "IU" && s.right.consonant.is_empty() {
        let tail = conjugate(CONJUGATE_GODAN_MAP, "w", i, suffix, false)?;
        return join(&[left, "い", tail.as_str()]);
    }
    if right.is_empty() {
        return join(&[left, SAHEN_LIST[i], suffix]);
    }
    if s.right.vowel == "I" && get(CONJUGATE_KAMI_MAP, rc).is_some() {
        let tail = conjugate(CONJUGATE_KAMI_MAP, rc, i, suffix, false)?;
        return join(&[left, tail.as_str()]);
    }
    if s.right.vowel == "IA" && get(CONJUGATE_SIMO_MAP, rc).is_some() {
        let tail = conjugate(CONJUGATE_SIMO_MAP, rc, i, suffix, false)?;
        return join(&[left, tail.as_str()]);
    }
    let tail = conjugate(CONJUGATE_GODAN_MAP, "r", i, suffix, false)?;
    let text = join(&[left, right, tail.as_str()])?;
    let text = replace(text.as_str(), "ござり", "ござい")?;
    replace(text.as_str(), "なさり", "なさい")
}

/// A request is classified before expensive kana/verb work. Controls never
/// mutate vowels just because a dictionary was probed.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Request {
    Output,
    Undo,
    Repeat,
    ToggleTyping,
    ToggleRecording(u8),
    StopRecording,
    Replay(u8),
}
#[derive(Clone, Copy, Debug)]
pub struct Translation {
    pub output: Output,
    pub next: State,
    pub request: Request,
    pub dynamic_particle: bool,
}
fn control(s: &Stroke<'_>, raw: &str) -> Option<Request> {
    match raw {
        "-U" => return Some(Request::Undo),
        "#-" | "#" => return Some(Request::Repeat),
        "#-n" => return Some(Request::ToggleTyping),
        _ => {}
    }
    let pure = s.left.consonant.is_empty()
        && s.left.vowel.is_empty()
        && s.right.consonant.is_empty()
        && s.right.vowel.is_empty()
        && s.right.particle.is_empty();
    if s.hash && pure {
        if let Some(i) = MACRO_KEYS.iter().position(|p| *p == s.left.particle) {
            if s.star {
                return Some(Request::ToggleRecording(i as u8));
            }
            if !s.hyphen {
                return Some(Request::Replay(i as u8));
            }
        }
        if s.left.particle.is_empty() && s.hyphen && s.star {
            return Some(Request::StopRecording);
        }
    }
    None
}
fn command(raw: &str) -> Option<(&'static str, Key, Key)> {
    use Key::*;
    Some(match raw {
        "#-k" => ("", SelectAlternateSystem, ImeOff),
        "#-t" => ("", ImeOn, None),
        "#n-n" => ("", ShiftReturn, None),
        "#-nk" => ("", CtrlReturn, None),
        "-AU" => ("", Backspace, None),
        "-IU" => ("", Delete, None),
        "-A" => ("", Left, None),
        "-N" => ("", Down, None),
        "-K" => ("", Right, None),
        "-Y" => ("", Up, None),
        "-I" => ("", Home, None),
        "-T" => ("", End, None),
        "-An" => ("", ShiftLeft, None),
        "-Nn" => ("", ShiftDown, None),
        "-Kn" => ("", ShiftRight, None),
        "-Yn" => ("", ShiftUp, None),
        "-In" => ("", ShiftHome, None),
        "-Tn" => ("", ShiftEnd, None),
        "-YI" => ("（", None, None),
        "-TY" => ("）", None, None),
        "-SYI" => ("【", None, None),
        "-STY" => ("】", None, None),
        "-TYI" => ("（）", Left, None),
        "-STYI" => ("【】", Left, None),
        "-NA" => ("「", None, None),
        "-KN" => ("」", None, None),
        "-SNA" => ("『", None, None),
        "-SKN" => ("』", None, None),
        "-KNA" => ("「」", Left, None),
        "-SKNA" => ("『』", Left, None),
        "-NYIA" => ("〈", None, None),
        "-TKNY" => ("〉", None, None),
        "-SNYIA" => ("《", None, None),
        "-STKNY" => ("》", None, None),
        "-TKNYIA" => ("〈〉", Left, None),
        "-STKNYIA" => ("《》", Left, None),
        "-YA" => ("\"", None, None),
        "-SYA" => ("\"\"", Left, None),
        "-TK" => ("|", None, None),
        "-TKIA" => ("||", None, None),
        "-IA" => (":", None, None),
        "-NY" => ("・", None, None),
        "-SNY" => ("＊", None, None),
        "-KY" => ("※", None, None),
        "-KA" => ("…", None, None),
        "-SKA" => ("～", None, None),
        "-TNI" => ("↓", None, None),
        "-KYA" => ("↑", None, None),
        "-IAU" => ("←", None, None),
        "-STK" => ("→", None, None),
        _ => return core::option::Option::None,
    })
}

/// Translate a committed-state snapshot without changing it. Set
/// `include_commands=false` to compare the procedural Plover dictionary beneath
/// its higher-priority command dictionary.
pub fn translate(raw: &str, state: State, include_commands: bool) -> Result<Translation> {
    let s = Stroke::parse(raw)?;
    let mut next = state;
    let mut output = Output::new();
    if let Some(request) = control(&s, raw) {
        return Ok(Translation {
            output,
            next,
            request,
            dynamic_particle: false,
        });
    }
    if include_commands && let Some((text, k1, k2)) = command(raw) {
        output.push_text(text)?;
        if k1 != Key::None {
            output.push_key(k1)?;
        }
        if k2 != Key::None {
            output.push_key(k2)?;
        }
        // Command dictionary entries bypass typing conversion and vowel updates.
        next.context = Context::Unknown;
        return Ok(Translation {
            output,
            next,
            request: Request::Output,
            dynamic_particle: false,
        });
    }
    let l = s.left;
    let r = s.right;
    // Explicitly reproduce the reference's vowel inheritance, without four
    // writes to a global. Its left syllable sees an explicit right vowel.
    let lv = if l.vowel.is_empty() {
        state.last_vowel()
    } else {
        l.vowel
    };
    let rv = if r.vowel.is_empty() { lv } else { r.vowel };
    let lsv = if l.vowel.is_empty() { rv } else { l.vowel };
    let rsv = if r.vowel.is_empty() { lsv } else { r.vowel };
    next = next.with_vowel(rsv)?;
    output = convert(&s, raw, state.context, [lv, rv, lsv, rsv])?;
    if raw == "#STKNYIAUntk-STKNYIAUntk*" {
        output = Output::new();
        if next.mode != Mode::Kana {
            next.pending_sokuon = false;
        }
    }
    let dynamic = s.dynamic_particle();
    // STN without a vowel represents no kana. When its extra sound is a
    // terminal small-tsu, emit it now; ordinary trailing small-tsu still
    // waits so the next consonant can be doubled in typing modes.
    let terminal_stn_tsu = output.text.as_str().ends_with('っ')
        && ((r.consonant == "STN" && r.vowel.is_empty() && r.particle == "tk")
            || (r.consonant.is_empty()
                && r.vowel.is_empty()
                && r.particle.is_empty()
                && l.consonant == "STN"
                && l.vowel.is_empty()
                && l.particle == "tk"));
    // Empty formatting preserves context; real output carries its explicit
    // classification, as Plover's confirmed formatting actions do.
    render(&mut output, &mut next)?;
    if terminal_stn_tsu && next.pending_sokuon {
        output.push_text(if next.mode == Mode::Romaji {
            "ltsu"
        } else {
            "Z"
        })?;
        next.pending_sokuon = false;
    }
    if !output.is_empty() {
        next.context = output.context;
    }
    Ok(Translation {
        output,
        next,
        request: Request::Output,
        dynamic_particle: dynamic,
    })
}
/// Priority is explicit: user word → particle → general abbreviation → verb
/// → left kana with particle → ordinary syllables. Each successful branch
/// returns immediately; fallback kana/syllable work is performed only as needed.
fn convert(s: &Stroke<'_>, raw: &str, context: Context, vowels: [&str; 4]) -> Result<Output> {
    let [lv, rv, lsv, rsv] = vowels;
    let l = s.left;
    let r = s.right;
    let mut output = Output::new();
    if let Some(user) = get(USERS_MAP, raw) {
        output.push_text(user)?;
        return Ok(output);
    }
    let no_kana = l.consonant.is_empty()
        && l.vowel.is_empty()
        && r.consonant.is_empty()
        && r.vowel.is_empty();
    if no_kana && !s.star {
        let p = particle(l.particle, r.particle, context)?;
        if !p.is_empty() {
            return Ok(p);
        }
    }
    let key = s.kana_key()?;
    if let Some((word, base)) = abstract_word(s, key.as_str())? {
        let p = particle(l.particle, r.particle, base)?;
        output.context = attached_context(l.particle, r.particle, &p, base);
        output.push_text(word.as_str())?;
        append_attached(&mut output, &p)?;
        return Ok(output);
    }
    let lk = base_kana(l.consonant, l.vowel, None, lv)?;
    let rk = base_kana(r.consonant, r.vowel, None, rv)?;
    let desu = r.consonant == "TN" && r.vowel.is_empty();
    let left_syllable = if desu {
        base_kana(l.consonant, l.vowel, Some(l.particle), lsv)?
    } else {
        Text::new()
    };
    let word = verb(
        s,
        key.as_str(),
        lk.as_str(),
        left_syllable.as_str(),
        rk.as_str(),
    )?;
    if !word.as_str().is_empty() {
        output.text = word;
        output.context = verb_context(l.particle, r.particle, desu);
        return Ok(output);
    }
    if !lk.as_str().is_empty()
        && r.consonant.is_empty()
        && r.vowel.is_empty()
        && !(l.particle == "ntk" && r.particle == "n")
        && !r.particle.is_empty()
    {
        let local = if lk.as_str() == "な" {
            Context::AttributiveNa
        } else {
            Context::Unknown
        };
        let p = particle(l.particle, r.particle, local)?;
        output.context = attached_context(l.particle, r.particle, &p, Context::Unknown);
        output.text = lk;
        append_attached(&mut output, &p)?;
        return Ok(output);
    }
    let undefined_right = l.consonant.is_empty()
        && l.vowel.is_empty()
        && l.particle.is_empty()
        && !rk.as_str().is_empty()
        && r.particle.is_empty();
    if undefined_right {
        return Ok(output);
    }
    output.text = base_kana(l.consonant, l.vowel, Some(l.particle), lsv)?;
    let rs = base_kana(r.consonant, r.vowel, Some(r.particle), rsv)?;
    output.push_text(rs.as_str())?;
    if s.hash {
        let copy = output;
        output.append(&copy)?;
    }
    Ok(output)
}

fn append_attached(out: &mut Output, p: &Output) -> Result<()> {
    if p.count == 1 {
        match p.operations[0].key {
            Key::Space => out.push_text("である")?,
            Key::Return => out.push_text("だ")?,
            Key::Tab => out.push_text("だった")?,
            _ => out.append(p)?,
        }
    } else {
        out.append(p)?;
    }
    Ok(())
}
