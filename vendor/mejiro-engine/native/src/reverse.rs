//! Shared desktop/WebAssembly reverse lookup transport.
use mejiro_engine::ffi::CRule;
use mejiro_engine::reverse::{self, GrammarSpan, Kind};
use mejiro_engine::{Context, RuleKind, RuleStore};
use std::format;
use std::string::String;

#[repr(C)]
#[derive(Clone, Copy)]
pub struct CGrammarSpan {
    pub start: u16,
    pub end: u16,
    pub kind: u8,
    pub lemma_len: u8,
    pub lemma: [u8; 32],
}

fn kind(value: u8) -> Option<Kind> {
    Some(match value {
        0 => Kind::Basic,
        1 => Kind::Particle,
        2 => Kind::Verb,
        3 => Kind::General,
        4 => Kind::User,
        5 => Kind::Minor,
        _ => return None,
    })
}
fn kind_id(value: Kind) -> u8 {
    match value {
        Kind::Basic => 0,
        Kind::Particle => 1,
        Kind::Verb => 2,
        Kind::General => 3,
        Kind::User => 4,
        Kind::Minor => 5,
    }
}
fn context(value: u8) -> Option<Context> {
    Context::from_name(match value {
        0 => "unknown",
        1 => "nominalizable",
        2 => "incomplete",
        3 => "attributive_na",
        4 => "question_predicate",
        5 => "noun",
        6 => "place",
        7 => "indefinite_noun",
        8 => "question_particle",
        _ => return None,
    })
    .ok()
}

fn escape_json(text: &str) -> String {
    let mut escaped = String::new();
    for c in text.chars() {
        match c {
            '"' => escaped.push_str("\\\""),
            '\\' => escaped.push_str("\\\\"),
            '\n' => escaped.push_str("\\n"),
            '\r' => escaped.push_str("\\r"),
            '\t' => escaped.push_str("\\t"),
            c if c <= '\u{001f}' => escaped.push_str(&format!("\\u{:04x}", c as u32)),
            c => escaped.push(c),
        }
    }
    escaped
}

/// Returns the JSON byte length (excluding NUL), -1 for invalid arguments,
/// or -2 when the provided output capacity is insufficient. No output is
/// written on failure. The rule array uses the existing 144-byte CRule layout.
/// # Safety
/// All pointers with nonzero lengths must refer to readable/writable storage.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_reverse_lookup(
    input: *const u8,
    input_len: usize,
    grammar: *const CGrammarSpan,
    grammar_len: usize,
    rules: *const CRule,
    rule_len: usize,
    output: *mut u8,
    capacity: usize,
) -> i32 {
    if input.is_null()
        || output.is_null()
        || grammar_len > 32
        || rule_len > 96
        || (grammar_len != 0 && grammar.is_null())
        || (rule_len != 0 && rules.is_null())
    {
        return -1;
    }
    let Ok(text) = core::str::from_utf8(unsafe { core::slice::from_raw_parts(input, input_len) })
    else {
        return -1;
    };
    let grammar = if grammar_len == 0 {
        &[][..]
    } else {
        unsafe { core::slice::from_raw_parts(grammar, grammar_len) }
    };
    let rules = if rule_len == 0 {
        &[][..]
    } else {
        unsafe { core::slice::from_raw_parts(rules, rule_len) }
    };
    let mut spans = std::vec::Vec::new();
    for span in grammar {
        let Some(k) = kind(span.kind) else { return -1 };
        if span.start >= span.end || span.end as usize > text.chars().count() || span.lemma_len > 32
        {
            return -1;
        }
        let lemma = if span.lemma_len == 0 {
            None
        } else {
            let Ok(s) = core::str::from_utf8(&span.lemma[..span.lemma_len as usize]) else {
                return -1;
            };
            Some(s.to_owned())
        };
        spans.push(GrammarSpan {
            start: span.start as usize,
            end: span.end as usize,
            kind: k,
            lemma,
        });
    }
    let mut overlay = RuleStore::new();
    for rule in rules {
        let Ok(k) = RuleKind::try_from(rule.kind) else {
            return -1;
        };
        let Some(c) = context(rule.context) else {
            return -1;
        };
        if rule.key_len as usize > 32
            || rule.value_len as usize > 96
            || rule.row_len as usize > 8
            || rule.reserved != [0, 0]
        {
            return -1;
        }
        let Ok(key) = core::str::from_utf8(&rule.key[..rule.key_len as usize]) else {
            return -1;
        };
        let Ok(value) = core::str::from_utf8(&rule.value[..rule.value_len as usize]) else {
            return -1;
        };
        let Ok(row) = core::str::from_utf8(&rule.row[..rule.row_len as usize]) else {
            return -1;
        };
        let applied = if rule.hidden != 0 {
            overlay.hide(k, key)
        } else {
            overlay.set(k, key, value, row, c)
        };
        if applied.is_err() {
            return -1;
        }
    }
    let result = match reverse::lookup(text, &spans, &overlay) {
        Ok(value) => value,
        Err(reverse::ReverseError::InputTooLong) => return -3,
        Err(reverse::ReverseError::SearchLimit) => return -4,
    };
    let mut json = String::from("{\"all\":[");
    for (name, entries) in [
        ("all", &result.all),
        ("basic_and_particle", &result.basic_and_particle),
    ] {
        if name != "all" {
            json.push_str("],\"basic_and_particle\":[");
        }
        for (i, entry) in entries.iter().enumerate() {
            if i > 0 {
                json.push(',');
            }
            json.push_str(&format!(
                "{{\"strokes\":\"{}\",\"stroke_count\":{},\"segments\":[",
                entry.strokes, entry.stroke_count
            ));
            for (j, segment) in entry.segments.iter().enumerate() {
                if j > 0 {
                    json.push(',');
                }
                json.push_str(&format!(
                    "[{}, {}, {}, \"{}\"]",
                    segment.start,
                    segment.end,
                    kind_id(segment.kind),
                    escape_json(segment.lemma.as_deref().unwrap_or(""))
                ));
            }
            json.push_str("]}");
        }
    }
    json.push_str(&format!("],\"truncated\":{}}}", result.truncated));
    if json.len() + 1 > capacity || json.len() > i32::MAX as usize {
        return -2;
    }
    unsafe {
        core::ptr::copy_nonoverlapping(json.as_ptr(), output, json.len());
        *output.add(json.len()) = 0;
    }
    json.len() as i32
}

/// Allocate a temporary buffer for direct WebAssembly calls.
#[unsafe(no_mangle)]
pub extern "C" fn mejiro_reverse_alloc(capacity: usize) -> *mut u8 {
    if capacity == 0 || capacity > 1_048_576 {
        return core::ptr::null_mut();
    }
    let bytes = std::vec![0u8; capacity].into_boxed_slice();
    std::boxed::Box::into_raw(bytes) as *mut u8
}
/// # Safety
/// Pointer must come from `mejiro_reverse_alloc` with the same capacity.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_reverse_free(ptr: *mut u8, capacity: usize) {
    if !ptr.is_null() && capacity > 0 && capacity <= 1_048_576 {
        let slice = core::ptr::slice_from_raw_parts_mut(ptr, capacity);
        drop(unsafe { std::boxed::Box::from_raw(slice) });
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn grammar_span_layout_and_json_escaping() {
        assert_eq!(core::mem::size_of::<CGrammarSpan>(), 38);
        assert_eq!(escape_json("a\"\\\n"), "a\\\"\\\\\\n");
    }
}
