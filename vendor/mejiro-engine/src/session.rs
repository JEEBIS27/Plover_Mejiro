use super::*;
use crate::recording::ExternalLog;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum EventKind {
    Emit,
    Undo,
    Control,
}
#[derive(Clone, Copy, Debug)]
pub struct Event {
    pub kind: EventKind,
    /// For Undo, this is the output being removed, not text to emit.
    pub output: Output,
    /// Adapter-supplied erase units, never inferred from UTF-8 bytes.
    pub erase_units: u32,
    pub ticket: Option<u64>,
}
#[derive(Clone, Copy)]
struct Entry {
    before: State,
    output: Output,
    receipt: Option<u32>,
    ticket: u64,
}
const EMPTY_ENTRY: Entry = Entry {
    before: State {
        context: Context::Unknown,
        mode: Mode::Kana,
        vowel: 0,
        pending_sokuon: false,
    },
    output: Output::new(),
    receipt: None,
    ticket: 0,
};

/// Firmware-style runtime. Plover may instead use `translate` and keep snapshots
/// in its own confirmed formatting history. H is the maximum undo depth.
/// Recording controls and mode toggles do not themselves become undo entries.
/// Macro contents are an explicit recording log; undo does not edit that log.
pub struct Session<const H: usize = 20> {
    state: State,
    history: [Entry; H],
    start: usize,
    len: usize,
    serial: u64,
    macros: [Output; 7],
    external: [ExternalLog; 7],
    replayed_external: ExternalLog,
    active: [bool; 7],
    order: [u8; 7],
    order_len: usize,
    typing_mode: Mode,
}
impl<const H: usize> Default for Session<H> {
    fn default() -> Self {
        Self::new()
    }
}
impl<const H: usize> Session<H> {
    pub const fn new() -> Self {
        Self {
            state: EMPTY_ENTRY.before,
            history: [EMPTY_ENTRY; H],
            start: 0,
            len: 0,
            serial: 0,
            macros: [Output::new(); 7],
            external: [ExternalLog::new(); 7],
            replayed_external: ExternalLog::new(),
            active: [false; 7],
            order: [0; 7],
            order_len: 0,
            typing_mode: Mode::Romaji,
        }
    }
    pub fn state(&self) -> State {
        self.state
    }
    pub fn history_len(&self) -> usize {
        self.len
    }
    pub fn recording(&self, index: usize) -> Option<bool> {
        self.active.get(index).copied()
    }
    pub fn recorded(&self, index: usize) -> Option<&Output> {
        self.macros.get(index)
    }
    pub fn recorded_external(&self, index: usize) -> Option<&[RecordedEvent]> {
        self.external.get(index).map(ExternalLog::as_slice)
    }
    pub fn replayed_external(&self) -> &[RecordedEvent] {
        self.replayed_external.as_slice()
    }
    /// Append already-sent keyboard output to every active recorder, atomically.
    /// No host output, linguistic translation, or replay happens here.
    pub fn record_external(&mut self, events: &[HidEvent]) -> Result<()> {
        if events.iter().any(|e| !e.valid()) {
            return Err(Error::InvalidState);
        }
        for i in 0..7 {
            if self.active[i] && !self.external[i].fits(events.len()) {
                return Err(Error::Capacity);
            }
        }
        for i in 0..7 {
            if self.active[i] {
                for event in events {
                    self.external[i].push(RecordedEvent {
                        byte_offset: self.macros[i].text.len as u16,
                        operation_index: self.macros[i].count as u8,
                        reserved: 0,
                        event: *event,
                    });
                }
            }
        }
        Ok(())
    }
    /// Fail closed after a host-side recording overflow; never replay a prefix
    /// as if it were the complete recording. Unrelated saved macros survive.
    pub fn abort_recordings(&mut self) {
        for i in 0..7 {
            if self.active[i] {
                self.macros[i] = Output::new();
                self.external[i] = ExternalLog::new();
                self.stop(i);
            }
        }
    }
    /// Select the typing-game mode. Toggling typing uses this selection.
    pub fn set_typing_mode(&mut self, mode: Mode) -> Result<()> {
        if mode == Mode::Kana {
            return Err(Error::InvalidState);
        }
        self.typing_mode = mode;
        if self.state.mode != Mode::Kana {
            self.state.mode = mode;
        }
        Ok(())
    }
    /// Explicit boundary when external editing/IME changes make receipts stale.
    /// Keep recorded macros and user mode settings; clear linguistic state.
    pub fn reset(&mut self) {
        self.state.context = Context::Unknown;
        self.state.vowel = 0;
        self.state.pending_sokuon = false;
        self.start = 0;
        self.len = 0;
    }
    pub fn acknowledge(&mut self, ticket: u64, erase_units: u32) -> Result<()> {
        if self.len == 0 {
            return Err(Error::InvalidState);
        }
        let entry = &mut self.history[(self.start + self.len - 1) % H];
        if entry.ticket != ticket || entry.receipt.is_some() {
            return Err(Error::InvalidState);
        }
        entry.receipt = Some(erase_units);
        Ok(())
    }
    fn stop(&mut self, index: usize) {
        self.active[index] = false;
        if let Some(pos) = self.order[..self.order_len]
            .iter()
            .position(|n| *n as usize == index)
        {
            self.order.copy_within(pos + 1..self.order_len, pos);
            self.order_len -= 1;
        }
    }
    fn emit(&mut self, output: Output, next: State) -> Result<Event> {
        self.emit_recorded(output, next, &[], None)
    }
    fn emit_recorded(
        &mut self,
        output: Output,
        next: State,
        external: &[RecordedEvent],
        exclude: Option<usize>,
    ) -> Result<Event> {
        // Validate every active recorder before changing any state.
        let mut updated = [None; 7];
        for (i, slot) in updated.iter_mut().enumerate() {
            if self.active[i] && exclude != Some(i) {
                if !self.external[i].fits(external.len()) {
                    return Err(Error::Capacity);
                }
                let mut value = self.macros[i];
                value.append(&output)?;
                *slot = Some(value);
            }
        }
        let before = self.state;
        let barrier = !external.is_empty()
            || output
                .operations()
                .iter()
                .any(|op| !matches!(op.key, Key::Shift0 | Key::Return | Key::Space | Key::Tab));
        let changed = !output.is_empty() || next != before;
        let ticket = if changed && !barrier && H > 0 {
            self.serial = self.serial.wrapping_add(1);
            let entry = Entry {
                before,
                output,
                receipt: if output.is_empty() { Some(0) } else { None },
                ticket: self.serial,
            };
            if self.len == H {
                self.history[self.start] = entry;
                self.start = (self.start + 1) % H;
            } else {
                self.history[(self.start + self.len) % H] = entry;
                self.len += 1;
            }
            Some(self.serial)
        } else {
            None
        };
        if barrier {
            self.start = 0;
            self.len = 0;
        }
        self.state = next;
        for (i, value) in updated.into_iter().enumerate() {
            if let Some(v) = value {
                self.external[i].append(external, self.macros[i].text.len, self.macros[i].count);
                self.macros[i] = v;
            }
        }
        Ok(Event {
            kind: EventKind::Emit,
            output,
            erase_units: 0,
            ticket,
        })
    }
    /// A host dictionary override is literal text with unknown grammar. It
    /// still participates in typing conversion, undo, repeat, and recording.
    pub fn process_override(&mut self, text: &str) -> Result<Event> {
        self.replayed_external = ExternalLog::new();
        let mut output = Output::new();
        output.push_text(text)?;
        let mut next = self.state;
        render(&mut output, &mut next)?;
        if !output.is_empty() {
            next.context = Context::Unknown;
        }
        self.emit(output, next)
    }
    /// Process a real input. Dictionary searches must call `translate`, not this.
    /// Before undo the host must acknowledge the number of units it can erase.
    pub fn process(&mut self, raw: &str) -> Result<Event> {
        self.replayed_external = ExternalLog::new();
        let t = translate(raw, self.state, true)?;
        let control = Event {
            kind: EventKind::Control,
            output: Output::new(),
            erase_units: 0,
            ticket: None,
        };
        match t.request {
            Request::Output => self.emit(t.output, t.next),
            Request::Undo => {
                if self.len == 0 {
                    // The host may still contain text after our bounded history
                    // was exhausted or cleared. Preserve the user's erase key.
                    self.reset();
                    return Ok(Event {
                        kind: EventKind::Undo,
                        output: Output::new(),
                        erase_units: 2,
                        ticket: None,
                    });
                }
                let entry = self.history[(self.start + self.len - 1) % H];
                let erase_units = entry.receipt.ok_or(Error::Unacknowledged)?;
                let mode = self.state.mode;
                self.state = entry.before;
                self.state.mode = mode;
                self.len -= 1;
                Ok(Event {
                    kind: EventKind::Undo,
                    output: entry.output,
                    erase_units,
                    ticket: None,
                })
            }
            Request::Repeat => {
                if self.len == 0 {
                    return Ok(control);
                }
                let output = self.history[(self.start + self.len - 1) % H].output;
                let mut next = self.state;
                next.context = output.context;
                self.emit(output, next)
            }
            Request::ToggleTyping => {
                self.state.mode = if self.state.mode == Mode::Kana {
                    self.typing_mode
                } else {
                    Mode::Kana
                };
                Ok(control)
            }
            Request::ToggleRecording(i) => {
                let i = i as usize;
                if self.active[i] {
                    self.stop(i);
                } else {
                    self.macros[i] = Output::new();
                    self.external[i] = ExternalLog::new();
                    self.active[i] = true;
                    self.order[self.order_len] = i as u8;
                    self.order_len += 1;
                }
                Ok(control)
            }
            Request::StopRecording => {
                if self.order_len > 0 {
                    let i = self.order[self.order_len - 1] as usize;
                    self.stop(i);
                }
                Ok(control)
            }
            Request::Replay(i) => {
                let mut output = self.macros[i as usize];
                let external = self.external[i as usize];
                // A recording is literal already-rendered output, not a fresh
                // linguistic analysis of the last word it happens to contain.
                output.context = Context::Unknown;
                let mut next = self.state;
                if !output.is_empty() || !external.as_slice().is_empty() {
                    next.context = Context::Unknown;
                }
                let result =
                    self.emit_recorded(output, next, external.as_slice(), Some(i as usize));
                if result.is_ok() {
                    self.replayed_external = external;
                }
                result
            }
        }
    }
}
