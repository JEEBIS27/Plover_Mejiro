use crate::{Context, Error, Result, Stroke, Text};

/// Fixed-size, allocation-free overlay for editable dictionary entries.
/// A hidden entry masks a built-in entry; removing the overlay restores it.
pub const RULE_CAPACITY: usize = 96;
pub const RULE_KEY_CAPACITY: usize = 32;
pub const RULE_VALUE_CAPACITY: usize = 96;
pub const RULE_ROW_CAPACITY: usize = 8;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum RuleKind {
    User = 0,
    General = 1,
    GeneralLeft = 2,
    GeneralRight = 3,
    Verb = 4,
}

impl TryFrom<u8> for RuleKind {
    type Error = Error;
    fn try_from(value: u8) -> Result<Self> {
        match value {
            0 => Ok(Self::User),
            1 => Ok(Self::General),
            2 => Ok(Self::GeneralLeft),
            3 => Ok(Self::GeneralRight),
            4 => Ok(Self::Verb),
            _ => Err(Error::InvalidState),
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct RuleEntry {
    pub kind: RuleKind,
    pub key: Text<RULE_KEY_CAPACITY>,
    pub value: Text<RULE_VALUE_CAPACITY>,
    /// Verb inflection row, empty for other kinds.
    pub row: Text<RULE_ROW_CAPACITY>,
    /// Explicit grammar for General, or Unknown to infer from its word.
    pub context: Context,
    pub hidden: bool,
}

const EMPTY: RuleEntry = RuleEntry {
    kind: RuleKind::User,
    key: Text::new(),
    value: Text::new(),
    row: Text::new(),
    context: Context::Unknown,
    hidden: false,
};

#[derive(Clone, Copy)]
pub struct RuleStore {
    entries: [RuleEntry; RULE_CAPACITY],
    len: usize,
}

impl Default for RuleStore {
    fn default() -> Self {
        Self::new()
    }
}

impl RuleStore {
    pub const fn new() -> Self {
        Self {
            entries: [EMPTY; RULE_CAPACITY],
            len: 0,
        }
    }

    pub fn len(&self) -> usize {
        self.len
    }
    pub fn entries(&self) -> &[RuleEntry] {
        &self.entries[..self.len]
    }

    pub fn find(&self, kind: RuleKind, key: &str) -> Option<&RuleEntry> {
        self.entries()
            .iter()
            .find(|e| e.kind == kind && e.key.as_str() == key)
    }

    fn validate_key(kind: RuleKind, key: &str) -> Result<()> {
        if (key.is_empty() && kind != RuleKind::GeneralLeft)
            || key.len() > RULE_KEY_CAPACITY
            || !key.is_ascii()
        {
            return Err(Error::InvalidStroke);
        }
        if key.is_empty() {
            return Ok(());
        }
        match kind {
            RuleKind::User => {
                Stroke::parse(key)?;
                if crate::rules::reserved_stroke(key) {
                    return Err(Error::InvalidStroke);
                }
            }
            RuleKind::General | RuleKind::Verb => {
                let s = Stroke::parse(key)?;
                if !s.hyphen
                    || s.hash
                    || (kind == RuleKind::Verb && s.star)
                    || !s.left.particle.is_empty()
                    || !s.right.particle.is_empty()
                {
                    return Err(Error::InvalidStroke);
                }
            }
            RuleKind::GeneralLeft | RuleKind::GeneralRight => {
                let s = Stroke::parse(key)?;
                if s.hash
                    || s.star
                    || s.hyphen
                    || !s.left.particle.is_empty()
                    || !s.right.consonant.is_empty()
                    || !s.right.vowel.is_empty()
                    || !s.right.particle.is_empty()
                {
                    return Err(Error::InvalidStroke);
                }
            }
        }
        Ok(())
    }

    /// Add or replace an overlay. `row` is required only for verbs.
    /// Failed operations leave the store unchanged.
    pub fn set(
        &mut self,
        kind: RuleKind,
        key: &str,
        value: &str,
        row: &str,
        context: Context,
    ) -> Result<()> {
        Self::validate_key(kind, key)?;
        if value.is_empty() && kind != RuleKind::GeneralLeft && kind != RuleKind::GeneralRight {
            return Err(Error::InvalidState);
        }
        if kind == RuleKind::Verb {
            if !valid_row(row) {
                return Err(Error::InvalidState);
            }
        } else if !row.is_empty() {
            return Err(Error::InvalidState);
        }
        if kind != RuleKind::General && context != Context::Unknown {
            return Err(Error::InvalidState);
        }
        let entry = RuleEntry {
            kind,
            key: Text::of(key)?,
            value: Text::of(value)?,
            row: Text::of(row)?,
            context,
            hidden: false,
        };
        self.put(entry)
    }

    /// Hide a built-in or edited entry without changing the compiled table.
    pub fn hide(&mut self, kind: RuleKind, key: &str) -> Result<()> {
        Self::validate_key(kind, key)?;
        self.put(RuleEntry {
            kind,
            key: Text::of(key)?,
            hidden: true,
            ..EMPTY
        })
    }

    /// Remove the overlay, restoring the compiled entry if it exists.
    pub fn clear(&mut self, kind: RuleKind, key: &str) -> Result<bool> {
        Self::validate_key(kind, key)?;
        if let Some(i) = self
            .entries()
            .iter()
            .position(|e| e.kind == kind && e.key.as_str() == key)
        {
            self.entries.copy_within(i + 1..self.len, i);
            self.len -= 1;
            self.entries[self.len] = EMPTY;
            Ok(true)
        } else {
            Ok(false)
        }
    }

    pub fn clear_all(&mut self) {
        *self = Self::new();
    }

    fn put(&mut self, entry: RuleEntry) -> Result<()> {
        if let Some(i) = self
            .entries()
            .iter()
            .position(|e| e.kind == entry.kind && e.key == entry.key)
        {
            self.entries[i] = entry;
        } else {
            if self.len == RULE_CAPACITY {
                return Err(Error::Capacity);
            }
            self.entries[self.len] = entry;
            self.len += 1;
        }
        Ok(())
    }
}

fn valid_row(row: &str) -> bool {
    if matches!(row, "sh" | "kh") {
        return true;
    }
    let (table, consonant) = if let Some(c) = row.strip_suffix('i') {
        (crate::CONJUGATE_KAMI_MAP, c)
    } else if let Some(c) = row.strip_suffix('e') {
        (crate::CONJUGATE_SIMO_MAP, c)
    } else {
        (crate::CONJUGATE_GODAN_MAP, row)
    };
    crate::get(table, consonant).is_some()
}
