//! Host-neutral HID output events, anchored between rendered text/key actions.

pub const EXTERNAL_CAPACITY: usize = 128;

/// HID usage page 7 (keyboard), 12 (consumer), or 1 (system control).
/// Kind 0 changes modifiers only; 1 presses a usage; 2 releases it.
/// Modifiers use the standard eight HID bits. This records output, not timing.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
#[repr(C)]
pub struct HidEvent {
    pub usage: u16,
    pub page: u8,
    pub mods: u8,
    pub kind: u8,
    pub reserved: u8,
}
impl HidEvent {
    pub fn valid(self) -> bool {
        self.reserved == 0
            && match self.kind {
                0 => self.page == 7 && self.usage == 0,
                1 | 2 => {
                    matches!(self.page, 1 | 7 | 12)
                        && self.usage != 0
                        && (self.page != 7 || self.usage < 256)
                }
                _ => false,
            }
    }
}

/// Execute after `operation_index` semantic key actions and `byte_offset` text
/// bytes of the corresponding Output. Offsets always refer to UTF-8 boundaries.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
#[repr(C)]
pub struct RecordedEvent {
    pub byte_offset: u16,
    pub operation_index: u8,
    pub reserved: u8,
    pub event: HidEvent,
}

#[derive(Clone, Copy)]
pub(crate) struct ExternalLog {
    events: [RecordedEvent; EXTERNAL_CAPACITY],
    len: usize,
}
impl ExternalLog {
    pub const fn new() -> Self {
        Self {
            events: [RecordedEvent {
                byte_offset: 0,
                operation_index: 0,
                reserved: 0,
                event: HidEvent {
                    usage: 0,
                    page: 7,
                    mods: 0,
                    kind: 0,
                    reserved: 0,
                },
            }; EXTERNAL_CAPACITY],
            len: 0,
        }
    }
    pub fn as_slice(&self) -> &[RecordedEvent] {
        &self.events[..self.len]
    }
    pub fn fits(&self, count: usize) -> bool {
        count <= EXTERNAL_CAPACITY - self.len
    }
    pub fn push(&mut self, event: RecordedEvent) {
        self.events[self.len] = event;
        self.len += 1;
    }
    pub fn append(&mut self, events: &[RecordedEvent], bytes: usize, operations: usize) {
        for event in events {
            self.push(RecordedEvent {
                byte_offset: event.byte_offset + bytes as u16,
                operation_index: event.operation_index + operations as u8,
                ..*event
            });
        }
    }
}
