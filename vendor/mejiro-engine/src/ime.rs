//! Forward, pre-render analysis for IME adapters. Existing translation/FFI APIs
//! remain unchanged. Ranges are UTF-8 byte offsets into `canonical_text`.
//! User literals are surfaces, NOT inferred readings. General abbreviations
//! retain Engine context; adapters must not invent a part of speech from kana.
use crate::{Context, Error, Result, RuleStore, State, Text, Translation};

pub const SEGMENT_CAPACITY: usize = 16;
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum SegmentKind {
    Sound,
    Particle,
    GeneralAbbreviation,
    Verb,
    Copula,
    UserLiteral,
    CommandLiteral,
    Unknown,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum VerbClass {
    GodanK,
    GodanG,
    GodanS,
    GodanT,
    GodanN,
    GodanB,
    GodanM,
    GodanR,
    GodanW,
    IchidanUpper,
    IchidanLower,
    Iku,
    Aru,
    Suru,
    Kuru,
    Desu,
}
impl VerbClass {
    pub(crate) fn row(row: &str) -> Option<Self> {
        Some(match row {
            "k" => Self::GodanK,
            "g" => Self::GodanG,
            "s" => Self::GodanS,
            "t" => Self::GodanT,
            "n" => Self::GodanN,
            "b" => Self::GodanB,
            "m" => Self::GodanM,
            "r" => Self::GodanR,
            "w" => Self::GodanW,
            "sh" => Self::Suru,
            "kh" => Self::Kuru,
            r if r.ends_with('i') => Self::IchidanUpper,
            r if r.ends_with('e') => Self::IchidanLower,
            _ => return None,
        })
    }
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct VerbInfo {
    pub class: Option<VerbClass>,
    /// Relative byte boundary between the actual emitted stem and inflection.
    /// None means an irregular stem cannot be aligned safely.
    pub stem_bytes: Option<usize>,
    /// Index into the Engine conjugation table; not a dictionary POS ID.
    pub form: u8,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Segment {
    pub start: usize,
    pub end: usize,
    pub kind: SegmentKind,
    pub context: Context,
    pub verb: Option<VerbInfo>,
}
const EMPTY: Segment = Segment {
    start: 0,
    end: 0,
    kind: SegmentKind::Unknown,
    context: Context::Unknown,
    verb: None,
};
#[derive(Clone, Debug)]
pub struct Analysis {
    pub translation: Translation,
    /// Text immediately before output encoding, including literal surfaces.
    /// Consult segment kinds before treating any part as a kana reading.
    pub canonical_text: Text,
    segments: [Segment; SEGMENT_CAPACITY],
    len: usize,
}
impl Analysis {
    pub fn segments(&self) -> &[Segment] {
        &self.segments[..self.len]
    }
}
#[derive(Default)]
pub(crate) struct Trace {
    text: Text,
    segments: [Segment; SEGMENT_CAPACITY],
    len: usize,
}
impl Default for Segment {
    fn default() -> Self {
        EMPTY
    }
}
impl Trace {
    pub(crate) fn push(
        &mut self,
        start: usize,
        end: usize,
        kind: SegmentKind,
        context: Context,
        verb: Option<VerbInfo>,
    ) -> Result<()> {
        if start == end {
            return Ok(());
        }
        if self.len == SEGMENT_CAPACITY {
            return Err(Error::Capacity);
        }
        self.segments[self.len] = Segment {
            start,
            end,
            kind,
            context,
            verb,
        };
        self.len += 1;
        Ok(())
    }
    pub(crate) fn capture(&mut self, text: &Text) {
        self.text = *text;
    }
}
pub(crate) fn mark(
    trace: &mut Option<&mut Trace>,
    start: usize,
    end: usize,
    kind: SegmentKind,
    context: Context,
    verb: Option<VerbInfo>,
) -> Result<()> {
    if let Some(t) = trace {
        t.push(start, end, kind, context, verb)?;
    }
    Ok(())
}
pub(crate) fn capture(trace: &mut Option<&mut Trace>, text: &Text) {
    if let Some(t) = trace {
        t.capture(text);
    }
}
/// Same rules/state transition as `translate_with_rules`, plus information
/// emitted by the successful rule branches. Does not mutate a Session.
pub fn analyze(
    raw: &str,
    state: State,
    include_commands: bool,
    rules: &RuleStore,
) -> Result<Analysis> {
    let mut trace = Trace::default();
    let translation =
        crate::rules::translate_observed(raw, state, include_commands, rules, Some(&mut trace))?;
    let n = trace.text.as_str().len();
    let mut end = 0;
    for span in &trace.segments[..trace.len] {
        if span.start != end || span.end > n || !trace.text.as_str().is_char_boundary(span.end) {
            return Err(Error::InvalidState);
        }
        end = span.end;
    }
    if end != n {
        return Err(Error::InvalidState);
    }
    Ok(Analysis {
        translation,
        canonical_text: trace.text,
        segments: trace.segments,
        len: trace.len,
    })
}
