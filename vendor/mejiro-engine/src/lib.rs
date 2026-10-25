//! Deterministic Mejiro rules, independent of keyboard firmware and Plover.
//! `translate` is a side-effect-free preview. `Session` commits inputs and owns
//! bounded history, repeat, recording, and all linguistic/typing state.
#![no_std]

pub mod ffi;
mod tables;
pub const MACRO_KEYS: &[&str] = &["n", "t", "k", "nt", "nk", "tk", "ntk"];
mod recording;
mod render;
mod rules;
mod session;
use core::fmt;
pub use recording::{EXTERNAL_CAPACITY, HidEvent, RecordedEvent};
pub use render::render;
pub use rules::{Request, Translation, particle, translate};
pub use session::{Event, EventKind, Session};
use tables::*;

pub const TEXT_CAPACITY: usize = 512;
const MAX_OPERATIONS: usize = 8;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Error {
    InvalidStroke,
    Capacity,
    InvalidState,
    Unacknowledged,
}
pub type Result<T> = core::result::Result<T, Error>;

/// UTF-8, checked capacity, no allocation or silent truncation.
#[derive(Clone, Copy, PartialEq, Eq)]
pub struct Text<const N: usize = TEXT_CAPACITY> {
    bytes: [u8; N],
    len: usize,
}
impl<const N: usize> Default for Text<N> {
    fn default() -> Self {
        Self::new()
    }
}
impl<const N: usize> Text<N> {
    pub const fn new() -> Self {
        Self {
            bytes: [0; N],
            len: 0,
        }
    }
    pub fn as_str(&self) -> &str {
        core::str::from_utf8(&self.bytes[..self.len]).unwrap()
    }
    pub fn push(&mut self, text: &str) -> Result<()> {
        let end = self.len.checked_add(text.len()).ok_or(Error::Capacity)?;
        if end > N {
            return Err(Error::Capacity);
        }
        self.bytes[self.len..end].copy_from_slice(text.as_bytes());
        self.len = end;
        Ok(())
    }
    fn of(text: &str) -> Result<Self> {
        let mut out = Self::new();
        out.push(text)?;
        Ok(out)
    }
    fn pop_char(&mut self) {
        if let Some((i, _)) = self.as_str().char_indices().next_back() {
            self.len = i;
        }
    }
}
impl<const N: usize> fmt::Debug for Text<N> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.as_str().fmt(f)
    }
}
fn join(parts: &[&str]) -> Result<Text> {
    let mut out = Text::new();
    for p in parts {
        out.push(p)?;
    }
    Ok(out)
}
fn small_key(parts: &[&str]) -> Result<Text<32>> {
    let mut out = Text::new();
    for p in parts {
        out.push(p)?;
    }
    Ok(out)
}
fn replace(text: &str, from: &str, to: &str) -> Result<Text> {
    let mut out = Text::new();
    let mut remaining = text;
    while let Some(i) = remaining.find(from) {
        out.push(&remaining[..i])?;
        out.push(to)?;
        remaining = &remaining[i + from.len()..];
    }
    out.push(remaining)?;
    Ok(out)
}
fn get<'a, T>(table: &'a [(&str, T)], key: &str) -> Option<&'a T> {
    table
        .binary_search_by(|(k, _)| k.cmp(&key))
        .ok()
        .map(|i| &table[i].1)
}
fn value(table: &[(&str, &'static str)], key: &str) -> &'static str {
    get(table, key).copied().unwrap_or("")
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Default)]
#[repr(u8)]
pub enum Context {
    #[default]
    Unknown,
    Nominalizable,
    Incomplete,
    AttributiveNa,
    QuestionPredicate,
    Noun,
    Place,
    IndefiniteNoun,
    QuestionParticle,
}
impl Context {
    pub fn name(self) -> &'static str {
        match self {
            Self::Unknown => "unknown",
            Self::Nominalizable => "nominalizable",
            Self::Incomplete => "incomplete",
            Self::AttributiveNa => "attributive_na",
            Self::QuestionPredicate => "question_predicate",
            Self::Noun => "noun",
            Self::Place => "place",
            Self::IndefiniteNoun => "indefinite_noun",
            Self::QuestionParticle => "question_particle",
        }
    }
    pub fn from_name(name: &str) -> Result<Self> {
        [
            Self::Unknown,
            Self::Nominalizable,
            Self::Incomplete,
            Self::AttributiveNa,
            Self::QuestionPredicate,
            Self::Noun,
            Self::Place,
            Self::IndefiniteNoun,
            Self::QuestionParticle,
        ]
        .into_iter()
        .find(|c| c.name() == name)
        .ok_or(Error::InvalidState)
    }
}
#[derive(Clone, Copy, Debug, PartialEq, Eq, Default)]
#[repr(u8)]
pub enum Mode {
    #[default]
    Kana,
    Romaji,
    Jis,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct State {
    pub context: Context,
    pub mode: Mode,
    vowel: u8,
    pending_sokuon: bool,
}
const VOWEL_STROKES: &[&str] = &[
    "A", "I", "U", "IA", "AU", "YA", "YU", "YAU", "Y", "YI", "YIA", "YIU", "YIAU", "IU", "IAU",
];
impl Default for State {
    fn default() -> Self {
        Self {
            context: Context::Unknown,
            mode: Mode::Kana,
            vowel: 0,
            pending_sokuon: false,
        }
    }
}
impl State {
    pub fn last_vowel(self) -> &'static str {
        VOWEL_STROKES[self.vowel as usize]
    }
    pub fn pending_sokuon(self) -> bool {
        self.pending_sokuon
    }
    pub fn with_pending_sokuon(mut self, pending: bool) -> Self {
        self.pending_sokuon = pending;
        self
    }
    pub fn with_vowel(mut self, vowel: &str) -> Result<Self> {
        self.vowel = VOWEL_STROKES
            .iter()
            .position(|v| *v == vowel)
            .ok_or(Error::InvalidState)? as u8;
        Ok(self)
    }
}

/// Text and key operations in execution order. Operation offsets are UTF-8 byte
/// boundaries in `text`, not erase counts. Hosts acknowledge actual emitted units.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum Key {
    None,
    Return,
    Space,
    Tab,
    Backspace,
    Delete,
    Left,
    Down,
    Right,
    Up,
    Home,
    End,
    ShiftLeft,
    ShiftDown,
    ShiftRight,
    ShiftUp,
    ShiftHome,
    ShiftEnd,
    ShiftReturn,
    CtrlReturn,
    F13,
    F14,
    Shift0,
    SelectAlternateSystem, // Select an available alternate system; otherwise do nothing.
    ImeOn,
    ImeOff,
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Operation {
    pub byte_offset: usize,
    pub key: Key,
}
const EMPTY_OPERATION: Operation = Operation {
    byte_offset: 0,
    key: Key::None,
};
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Output {
    pub text: Text,
    operations: [Operation; MAX_OPERATIONS],
    count: usize,
    pub context: Context,
}
impl Default for Output {
    fn default() -> Self {
        Self::new()
    }
}
impl Output {
    pub const fn new() -> Self {
        Self {
            text: Text::new(),
            operations: [EMPTY_OPERATION; MAX_OPERATIONS],
            count: 0,
            context: Context::Unknown,
        }
    }
    pub fn operations(&self) -> &[Operation] {
        &self.operations[..self.count]
    }
    pub fn is_empty(&self) -> bool {
        self.text.len == 0 && self.count == 0
    }
    pub fn push_text(&mut self, text: &str) -> Result<()> {
        self.text.push(text)
    }
    pub fn push_key(&mut self, key: Key) -> Result<()> {
        if self.count == MAX_OPERATIONS {
            return Err(Error::Capacity);
        }
        self.operations[self.count] = Operation {
            byte_offset: self.text.len,
            key,
        };
        self.count += 1;
        Ok(())
    }
    fn append(&mut self, other: &Self) -> Result<()> {
        if self.count + other.count > MAX_OPERATIONS {
            return Err(Error::Capacity);
        }
        let offset = self.text.len;
        self.text.push(other.text.as_str())?;
        for op in other.operations() {
            self.operations[self.count] = Operation {
                byte_offset: offset + op.byte_offset,
                key: op.key,
            };
            self.count += 1;
        }
        Ok(())
    }
}

#[derive(Clone, Copy, Debug)]
pub struct Hand<'a> {
    pub consonant: &'a str,
    pub vowel: &'a str,
    pub particle: &'a str,
}
#[derive(Clone, Copy, Debug)]
pub struct Stroke<'a> {
    pub hash: bool,
    pub star: bool,
    pub hyphen: bool,
    pub left: Hand<'a>,
    pub right: Hand<'a>,
}
impl<'a> Stroke<'a> {
    /// Ordered scan, no regex, no allocation. Both explicit `-` and Plover's
    /// canonical omitted-hyphen form are accepted. Reject trailing junk.
    pub fn parse(raw: &'a str) -> Result<Self> {
        fn group<'a>(s: &'a str, pos: &mut usize, order: &[u8]) -> &'a str {
            let start = *pos;
            for b in order {
                if s.as_bytes().get(*pos) == Some(b) {
                    *pos += 1;
                }
            }
            &s[start..*pos]
        }
        fn hand<'a>(s: &'a str, p: &mut usize) -> Hand<'a> {
            Hand {
                consonant: group(s, p, b"STKN"),
                vowel: group(s, p, b"YIAU"),
                particle: group(s, p, b"ntk"),
            }
        }
        if raw.is_empty() || !raw.is_ascii() {
            return Err(Error::InvalidStroke);
        }
        let mut p = 0;
        let hash = raw.starts_with('#');
        if hash {
            p += 1;
        }
        let left = hand(raw, &mut p);
        let hyphen = raw.as_bytes().get(p) == Some(&b'-');
        if hyphen {
            p += 1;
        }
        let right = hand(raw, &mut p);
        let star = raw.as_bytes().get(p) == Some(&b'*');
        if star {
            p += 1;
        }
        if p != raw.len() {
            return Err(Error::InvalidStroke);
        }
        Ok(Self {
            hash,
            star,
            hyphen,
            left,
            right,
        })
    }
    fn kana_key(&self) -> Result<Text<32>> {
        small_key(&[
            self.left.consonant,
            self.left.vowel,
            "-",
            self.right.consonant,
            self.right.vowel,
        ])
    }
    pub fn dynamic_particle(&self) -> bool {
        self.left.consonant.is_empty()
            && self.left.vowel.is_empty()
            && self.right.consonant.is_empty()
            && self.right.vowel.is_empty()
            && !self.star
            && ((self.left.particle == "k" && matches!(self.right.particle, "k" | "nk"))
                || self.left.particle == "ntk")
    }
}
