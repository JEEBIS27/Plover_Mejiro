use mejiro_engine::{Key, Output, Result, Text};
pub fn plover_body(output: &Output) -> Result<Text<2048>> {
    let mut out = Text::new();
    let mut from = 0;
    for op in output.operations() {
        out.push(&output.text.as_str()[from..op.byte_offset])?;
        let name = match op.key {
            Key::Return => "Return",
            Key::Space => "Space",
            Key::Tab => "Tab",
            Key::Backspace => "BackSpace",
            Key::Delete => "Delete",
            Key::Left => "Left",
            Key::Down => "Down",
            Key::Right => "Right",
            Key::Up => "Up",
            Key::Home => "Home",
            Key::End => "End",
            Key::ShiftLeft => "Shift_L(Left)",
            Key::ShiftDown => "Shift_L(Down)",
            Key::ShiftRight => "Shift_L(Right)",
            Key::ShiftUp => "Shift_L(Up)",
            Key::ShiftHome => "Shift_L(Home)",
            Key::ShiftEnd => "Shift_L(End)",
            Key::ShiftReturn => "Shift_L(Return)",
            Key::CtrlReturn => "Ctrl_L(Return)",
            Key::F13 => "F13",
            Key::F14 => "F14",
            Key::Shift0 => "Shift(0)",
            Key::SelectAlternateSystem => {
                out.push("}{PLOVER:MEJIRO_ALTERNATE:Phonetix}{")?;
                from = op.byte_offset;
                continue;
            }
            Key::ImeOn | Key::ImeOff => {
                out.push(if op.key == Key::ImeOn {
                    "}{PLOVER:MEJIRO_IME:on}{"
                } else {
                    "}{PLOVER:MEJIRO_IME:off}{"
                })?;
                from = op.byte_offset;
                continue;
            }
            Key::None => continue,
        };
        out.push("}{#")?;
        out.push(name)?;
        out.push("}{")?;
        from = op.byte_offset;
    }
    out.push(&output.text.as_str()[from..])?;
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;
    use mejiro_engine::{State, translate};

    #[test]
    fn ime_commands_select_optional_system_before_off() {
        for (stroke, expected) in [
            ("#-t", "}{PLOVER:MEJIRO_IME:on}{"),
            (
                "#-k",
                "}{PLOVER:MEJIRO_ALTERNATE:Phonetix}{}{PLOVER:MEJIRO_IME:off}{",
            ),
        ] {
            let translation = translate(stroke, State::default(), true).unwrap();
            assert_eq!(plover_body(&translation.output).unwrap().as_str(), expected);
        }
    }
}
