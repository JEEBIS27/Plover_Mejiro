//! Desktop-only C ABI. Firmware links the no_std core directly (RMK) or adds
//! target-specific staticlib/panic glue (QMK), without this std crate.
mod plover;
use mejiro_engine::{State, translate};

use mejiro_engine::ffi::CState as NativeState;
/// ABI version for adapters to reject incompatible binaries.
#[unsafe(no_mangle)]
pub extern "C" fn mejiro_abi_version() -> u32 {
    1
}

/// Plover preview including control classification. Formatting history, rather
/// than dictionary probes, owns the returned state. ABI 1 uses four state bytes
/// and request/argument bytes matching the core CTranslation contract.
///
/// # Safety
/// All pointers must be valid and non-overlapping; output has capacity bytes.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_plover_preview(
    stroke: *const u8,
    stroke_len: usize,
    state: *const NativeState,
    output: *mut u8,
    capacity: usize,
    next_state: *mut NativeState,
    request: *mut u8,
    argument: *mut u8,
) -> i32 {
    if stroke.is_null()
        || state.is_null()
        || output.is_null()
        || next_state.is_null()
        || request.is_null()
        || argument.is_null()
    {
        return -1;
    }
    let Ok(raw) = core::str::from_utf8(unsafe { core::slice::from_raw_parts(stroke, stroke_len) })
    else {
        return -1;
    };
    let Ok(state) = State::try_from(unsafe { *state }) else {
        return -1;
    };
    let t = match translate(raw, state, true) {
        Ok(t) => t,
        Err(mejiro_engine::Error::Capacity) => return -2,
        Err(_) => return -1,
    };
    let body = match plover::plover_body(&t.output) {
        Ok(body) => body,
        Err(_) => return -2,
    };
    let bytes = body.as_str().as_bytes();
    if bytes.len() + 1 > capacity {
        return -2;
    }
    let classified = mejiro_engine::ffi::CTranslation::from(t);
    unsafe {
        core::ptr::copy_nonoverlapping(bytes.as_ptr(), output, bytes.len());
        *output.add(bytes.len()) = 0;
        *next_state = classified.next;
        *request = classified.request;
        *argument = classified.argument;
    }
    0
}

/// Render a host dictionary override using the same typing rules as firmware.
///
/// # Safety
/// Pointers must be valid and non-overlapping; output has capacity bytes.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_plover_override(
    text: *const u8,
    text_len: usize,
    state: *const NativeState,
    output: *mut u8,
    capacity: usize,
    next_state: *mut NativeState,
) -> i32 {
    if text.is_null() || state.is_null() || output.is_null() || next_state.is_null() {
        return -1;
    }
    let Ok(text) = core::str::from_utf8(unsafe { core::slice::from_raw_parts(text, text_len) })
    else {
        return -1;
    };
    let Ok(mut next) = State::try_from(unsafe { *state }) else {
        return -1;
    };
    let mut rendered = mejiro_engine::Output::new();
    if rendered.push_text(text).is_err() || mejiro_engine::render(&mut rendered, &mut next).is_err()
    {
        return -2;
    }
    next.context = mejiro_engine::Context::Unknown;
    let Ok(body) = plover::plover_body(&rendered) else {
        return -2;
    };
    let bytes = body.as_str().as_bytes();
    if bytes.len() + 1 > capacity {
        return -2;
    }
    unsafe {
        core::ptr::copy_nonoverlapping(bytes.as_ptr(), output, bytes.len());
        *output.add(bytes.len()) = 0;
        *next_state = next.into();
    }
    0
}

/// Pure preview. UTF-8 body is NUL terminated. All output arguments remain
/// unchanged on error. Returns 0 on success, -1 invalid input, -2 capacity,
/// -3 control request (use Session in the core for runtime controls).
///
/// # Safety
/// Pointers must reference valid, non-overlapping memory of stated lengths;
/// output parameters must be writable. `stroke` is not NUL terminated.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mejiro_translate(
    stroke: *const u8,
    stroke_len: usize,
    state: *const NativeState,
    include_commands: bool,
    output: *mut u8,
    capacity: usize,
    next_state: *mut NativeState,
    output_context: *mut u8,
) -> i32 {
    if stroke.is_null()
        || state.is_null()
        || output.is_null()
        || next_state.is_null()
        || output_context.is_null()
    {
        return -1;
    }
    let raw = match core::str::from_utf8(unsafe { core::slice::from_raw_parts(stroke, stroke_len) })
    {
        Ok(s) => s,
        Err(_) => return -1,
    };
    let Ok(state) = State::try_from(unsafe { *state }) else {
        return -1;
    };
    let t = match translate(raw, state, include_commands) {
        Ok(t) => t,
        Err(mejiro_engine::Error::Capacity) => return -2,
        Err(_) => return -1,
    };
    if t.request != mejiro_engine::Request::Output {
        return -3;
    }
    let body = match plover::plover_body(&t.output) {
        Ok(s) => s,
        Err(_) => return -2,
    };
    let text = body.as_str().as_bytes();
    if text.len() + 1 > capacity {
        return -2;
    }
    unsafe {
        core::ptr::copy_nonoverlapping(text.as_ptr(), output, text.len());
        *output.add(text.len()) = 0;
        *next_state = t.next.into();
        *output_context = t.output.context as u8;
    }
    0
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn plover_preview_reports_controls_and_atomic_errors() {
        for (raw, expected, control) in [("TNYIUntk-", "どぅー", 0), ("#", "", 2), ("#n*", "", 4)]
        {
            let state = NativeState::default();
            let mut next = state;
            let mut output = [0u8; 2048];
            let (mut request, mut argument) = (255, 255);
            let rc = unsafe {
                mejiro_plover_preview(
                    raw.as_ptr(),
                    raw.len(),
                    &state,
                    output.as_mut_ptr(),
                    output.len(),
                    &mut next,
                    &mut request,
                    &mut argument,
                )
            };
            assert_eq!(rc, 0);
            assert_eq!(request, control);
            assert_eq!(&output[..expected.len()], expected.as_bytes());
            assert_eq!(output[expected.len()], 0);
        }
        let raw = "KA-";
        let state = NativeState::default();
        let mut next = NativeState { vowel: 14, ..state };
        let (mut request, mut argument) = (255, 255);
        let mut output = [127u8; 1];
        assert_eq!(
            unsafe {
                mejiro_plover_preview(
                    raw.as_ptr(),
                    raw.len(),
                    &state,
                    output.as_mut_ptr(),
                    output.len(),
                    &mut next,
                    &mut request,
                    &mut argument,
                )
            },
            -2
        );
        assert_eq!(output, [127]);
        assert_eq!(next.vowel, 14);
        assert_eq!((request, argument), (255, 255));
    }
    #[test]
    fn native_capacity_errors_do_not_write_partial_state() {
        let raw = b"K-T";
        let state = NativeState::default();
        let mut next = NativeState { vowel: 14, ..state };
        let mut context = 255;
        let mut bytes = [0x7f; 2];
        let rc = unsafe {
            mejiro_translate(
                raw.as_ptr(),
                raw.len(),
                &state,
                false,
                bytes.as_mut_ptr(),
                bytes.len(),
                &mut next,
                &mut context,
            )
        };
        assert_eq!(rc, -2);
        assert_eq!(bytes, [0x7f; 2]);
        assert_eq!(next.vowel, 14);
        assert_eq!(context, 255);
    }
}
