//! Allocation-free C interface for a target-specific QMK static library.
//! Rust firmware should prefer the safe native API.
use super::*;

/// Import already-emitted host events into all active recorders, without IO.
/// Safety: session is exclusively owned; events references count initialized
/// HidEvent values. A zero count permits a null events pointer.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_core_session_record_external(
    session: *mut u8,
    events: *const HidEvent,
    count: usize,
) -> i32 {
    if session.is_null() || (events.is_null() && count != 0) {
        return -1;
    }
    if count > EXTERNAL_CAPACITY {
        return -2;
    }
    let events = if count == 0 {
        &[]
    } else {
        unsafe { core::slice::from_raw_parts(events, count) }
    };
    match unsafe { &mut *session.cast::<FirmwareSession>() }.record_external(events) {
        Ok(()) => 0,
        Err(Error::Capacity) => -2,
        Err(_) => -1,
    }
}
/// Return the most recent replay's anchored events. A null output with capacity
/// zero queries the count. No copy occurs on insufficient capacity.
/// Safety: session is initialized; output has capacity writable elements.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_core_session_replayed_external(
    session: *const u8,
    output: *mut RecordedEvent,
    capacity: usize,
) -> i32 {
    if session.is_null() {
        return -1;
    }
    let events = unsafe { &*session.cast::<FirmwareSession>() }.replayed_external();
    if output.is_null() && capacity == 0 {
        return events.len() as i32;
    }
    if capacity < events.len() {
        return -2;
    }
    if !events.is_empty() {
        if output.is_null() {
            return -1;
        }
        unsafe { core::ptr::copy_nonoverlapping(events.as_ptr(), output, events.len()) };
    }
    events.len() as i32
}
/// Abort and erase only macros which are currently recording after host failure.
/// Safety: session is initialized and exclusively owned.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_core_session_abort_recordings(session: *mut u8) -> i32 {
    if session.is_null() {
        return -1;
    }
    unsafe { &mut *session.cast::<FirmwareSession>() }.abort_recordings();
    0
}

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
#[repr(C)]
pub struct CState {
    pub vowel: u8,
    pub context: u8,
    pub mode: u8,
    pub pending_sokuon: u8,
}
impl TryFrom<CState> for State {
    type Error = Error;
    fn try_from(raw: CState) -> Result<Self> {
        let contexts = [
            Context::Unknown,
            Context::Nominalizable,
            Context::Incomplete,
            Context::AttributiveNa,
            Context::QuestionPredicate,
            Context::Noun,
            Context::Place,
            Context::IndefiniteNoun,
            Context::QuestionParticle,
        ];
        let mut state = State {
            context: *contexts
                .get(raw.context as usize)
                .ok_or(Error::InvalidState)?,
            mode: match raw.mode {
                0 => Mode::Kana,
                1 => Mode::Romaji,
                2 => Mode::Jis,
                _ => return Err(Error::InvalidState),
            },
            vowel: raw.vowel,
            pending_sokuon: false,
        };
        if raw.vowel as usize >= VOWEL_STROKES.len() || raw.pending_sokuon > 1 {
            return Err(Error::InvalidState);
        }
        state.pending_sokuon = raw.pending_sokuon != 0;
        Ok(state)
    }
}
impl From<State> for CState {
    fn from(state: State) -> Self {
        Self {
            vowel: state.vowel,
            context: state.context as u8,
            mode: state.mode as u8,
            pending_sokuon: state.pending_sokuon as u8,
        }
    }
}
#[derive(Clone, Copy, Debug, Default)]
#[repr(C)]
pub struct COperation {
    pub byte_offset: u16,
    pub key: u8,
    pub reserved: u8,
}
#[derive(Clone, Copy)]
#[repr(C)]
pub struct CTranslation {
    pub next: CState,
    pub text: [u8; TEXT_CAPACITY],
    pub text_len: u16,
    pub operations: [COperation; MAX_OPERATIONS],
    pub operation_count: u8,
    pub output_context: u8,
    /// 0 output, 1 undo, 2 repeat, 3 toggle typing, 4 toggle recording,
    /// 5 stop recording, 6 replay macro. Macro key index is in `argument`.
    pub request: u8,
    pub argument: u8,
    pub dynamic_particle: u8,
    pub reserved: u8,
}
impl From<Translation> for CTranslation {
    fn from(t: Translation) -> Self {
        let (request, argument) = match t.request {
            Request::Output => (0, 0),
            Request::Undo => (1, 0),
            Request::Repeat => (2, 0),
            Request::ToggleTyping => (3, 0),
            Request::ToggleRecording(i) => (4, i),
            Request::StopRecording => (5, 0),
            Request::Replay(i) => (6, i),
        };
        let mut operations = [COperation::default(); MAX_OPERATIONS];
        for (i, op) in t.output.operations().iter().enumerate() {
            operations[i] = COperation {
                byte_offset: op.byte_offset as u16,
                key: op.key as u8,
                reserved: 0,
            };
        }
        Self {
            next: t.next.into(),
            text: t.output.text.bytes,
            text_len: t.output.text.len as u16,
            operations,
            operation_count: t.output.count as u8,
            output_context: t.output.context as u8,
            request,
            argument,
            dynamic_particle: t.dynamic_particle as u8,
            reserved: 0,
        }
    }
}

/// Preview: 0 success, -1 invalid input/state, -2 capacity. Does not commit IO.
/// `include_commands` must be 0 or 1. No output writes occur on failure.
///
/// # Safety
/// `stroke` must reference `len` readable bytes. `state` must be readable and
/// aligned; `output` writable, aligned, and non-overlapping with other arguments.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_core_translate(
    stroke: *const u8,
    len: usize,
    state: *const CState,
    include_commands: u8,
    output: *mut CTranslation,
) -> i32 {
    if stroke.is_null() || state.is_null() || output.is_null() || include_commands > 1 {
        return -1;
    }
    let raw = match core::str::from_utf8(unsafe { core::slice::from_raw_parts(stroke, len) }) {
        Ok(s) => s,
        Err(_) => return -1,
    };
    let state = match State::try_from(unsafe { *state }) {
        Ok(s) => s,
        Err(_) => return -1,
    };
    match translate(raw, state, include_commands != 0) {
        Ok(t) => {
            unsafe { output.write(t.into()) };
            0
        }
        Err(Error::Capacity) => -2,
        Err(_) => -1,
    }
}

/// Opaque, caller-owned runtime storage. Its layout is not a C API.
type FirmwareSession = Session<20>;
#[derive(Clone, Copy)]
#[repr(C)]
pub struct CEvent {
    pub translation: CTranslation,
    pub erase_units: u32,
    pub ticket: u64,
    /// 0 emit, 1 undo, 2 control. Undo output describes what is removed.
    pub kind: u8,
    pub has_ticket: u8,
    pub reserved: [u8; 6],
}
#[unsafe(no_mangle)]
pub extern "C" fn mejiro_core_session_size() -> usize {
    core::mem::size_of::<FirmwareSession>()
}
#[unsafe(no_mangle)]
pub extern "C" fn mejiro_core_session_align() -> usize {
    core::mem::align_of::<FirmwareSession>()
}

/// Initialize suitably aligned storage without allocating. Returns 0 or -1.
/// Re-initialization resets the complete session, including macros and mode.
///
/// # Safety
/// Storage must be writable for `capacity` bytes and exclusively owned for the
/// lifetime of the session. A process/ack/reset pointer must originate here.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_core_session_init(storage: *mut u8, capacity: usize) -> i32 {
    if storage.is_null()
        || !storage.addr().is_multiple_of(mejiro_core_session_align())
        || capacity < mejiro_core_session_size()
    {
        return -1;
    }
    unsafe {
        storage
            .cast::<FirmwareSession>()
            .write(FirmwareSession::new())
    };
    0
}
/// Process one real input. 0 success, -1 invalid, -2 capacity, -4 missing receipt.
///
/// # Safety
/// `session` must reference an initialized, exclusively owned session. `stroke`
/// must be readable for `len` bytes and `output` writable/aligned. Arguments
/// must not overlap. The same session cannot be used concurrently.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_core_session_process(
    session: *mut u8,
    stroke: *const u8,
    len: usize,
    output: *mut CEvent,
) -> i32 {
    if session.is_null() || stroke.is_null() || output.is_null() {
        return -1;
    }
    let raw = match core::str::from_utf8(unsafe { core::slice::from_raw_parts(stroke, len) }) {
        Ok(s) => s,
        Err(_) => return -1,
    };
    let s = unsafe { &mut *session.cast::<FirmwareSession>() };
    let e = match s.process(raw) {
        Ok(e) => e,
        Err(Error::Capacity) => return -2,
        Err(Error::Unacknowledged) => return -4,
        Err(_) => return -1,
    };
    let translation = Translation {
        output: e.output,
        next: s.state(),
        request: if e.kind == EventKind::Undo {
            Request::Undo
        } else {
            Request::Output
        },
        dynamic_particle: false,
    };
    let kind = match e.kind {
        EventKind::Emit => 0,
        EventKind::Undo => 1,
        EventKind::Control => 2,
    };
    unsafe {
        output.write(CEvent {
            translation: translation.into(),
            erase_units: e.erase_units,
            ticket: e.ticket.unwrap_or(0),
            kind,
            has_ticket: e.ticket.is_some() as u8,
            reserved: [0; 6],
        })
    };
    0
}
/// Acknowledge the newest output's actual erase units. 0 success, -1 invalid.
/// Empty output with a ticket is internally acknowledged with zero units.
///
/// # Safety
/// `session` must be initialized and exclusively owned.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_core_session_ack(
    session: *mut u8,
    ticket: u64,
    erase_units: u32,
) -> i32 {
    if session.is_null() {
        return -1;
    }
    let s = unsafe { &mut *session.cast::<FirmwareSession>() };
    if s.acknowledge(ticket, erase_units).is_ok() {
        0
    } else {
        -1
    }
}
/// Reset linguistic state/history when an external edit invalidates receipts.
///
/// # Safety
/// `session` must be initialized and exclusively owned.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_core_session_reset(session: *mut u8) -> i32 {
    if session.is_null() {
        return -1;
    }
    unsafe { &mut *session.cast::<FirmwareSession>() }.reset();
    0
}

/// Configure typing-game output (1 Romaji, 2 JIS). 0 success, -1 invalid.
///
/// # Safety
/// `session` must be initialized and exclusively owned.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_core_session_set_typing_mode(session: *mut u8, mode: u8) -> i32 {
    if session.is_null() {
        return -1;
    }
    let mode = match mode {
        1 => Mode::Romaji,
        2 => Mode::Jis,
        _ => return -1,
    };
    let s = unsafe { &mut *session.cast::<FirmwareSession>() };
    if s.set_typing_mode(mode).is_ok() {
        0
    } else {
        -1
    }
}
