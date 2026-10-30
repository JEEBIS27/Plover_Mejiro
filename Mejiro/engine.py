"""ctypes transport for the authoritative Rust Mejiro engine.

No kana, conjugation, particle or transliteration rules live in this module.
"""
import ctypes as c
from dataclasses import dataclass
import os
from pathlib import Path
import sys


class State(c.Structure):
    _fields_ = [("vowel", c.c_uint8), ("context", c.c_uint8),
                ("mode", c.c_uint8), ("pending_sokuon", c.c_uint8)]

    def clone(self):
        return State.from_buffer_copy(bytes(self))


@dataclass(frozen=True)
class Preview:
    body: str
    state: State
    request: int
    argument: int


class Engine:
    def __init__(self, path=None):
        name = ("mejiro_native.dll" if sys.platform == "win32" else
                "libmejiro_native.dylib" if sys.platform == "darwin" else
                "libmejiro_native.so")
        path = path or os.environ.get("MEJIRO_ENGINE_LIBRARY") or Path(__file__).with_name("_native") / name
        try:
            self.library = c.CDLL(str(path))
            self.library.mejiro_abi_version.restype = c.c_uint32
            if self.library.mejiro_abi_version() != 1:
                raise RuntimeError("Unsupported Mejiro engine ABI")
            self.preview_fn = self.library.mejiro_plover_preview
        except (OSError, AttributeError) as error:
            raise RuntimeError(
                "Mejiro Rust engine is missing or outdated. Rebuild/reinstall Mejiro "
                "with Rust, or set MEJIRO_ENGINE_LIBRARY to the new native library."
            ) from error
        self.preview_fn.argtypes = [c.c_char_p, c.c_size_t, c.POINTER(State),
                                    c.c_void_p, c.c_size_t, c.POINTER(State),
                                    c.POINTER(c.c_uint8), c.POINTER(c.c_uint8)]
        self.preview_fn.restype = c.c_int32
        self.override_fn = self.library.mejiro_plover_override
        self.override_fn.argtypes = [c.c_char_p, c.c_size_t, c.POINTER(State),
                                     c.c_void_p, c.c_size_t, c.POINTER(State)]
        self.override_fn.restype = c.c_int32

    def override(self, text, state):
        raw = text.encode("utf-8")
        output, next_state = c.create_string_buffer(2048), State()
        rc = self.override_fn(raw, len(raw), c.byref(state),
                              output, len(output), c.byref(next_state))
        if rc:
            raise RuntimeError(f"Mejiro native override failed: {rc}")
        return Preview(output.value.decode("utf-8"), next_state, 0, 0)

    def preview(self, stroke, state=None):
        state = state if state is not None else State()
        raw = stroke.encode("ascii")
        output = c.create_string_buffer(2048)
        next_state, request, argument = State(), c.c_uint8(), c.c_uint8()
        rc = self.preview_fn(raw, len(raw), c.byref(state), output, len(output),
                             c.byref(next_state), c.byref(request), c.byref(argument))
        if rc == -1:
            raise KeyError(stroke)
        if rc:
            raise RuntimeError(f"Mejiro native preview failed: {rc}")
        return Preview(output.value.decode("utf-8"), next_state, request.value, argument.value)


_engine = None
# Host preferences and optional overrides; these contain no language rules.
typing_mode = 0
is_typing_mode = True
USERS_MAP = {}


def engine():
    global _engine
    if _engine is None:
        _engine = Engine()
    return _engine


def lookup(key):
    if len(key) != 1:
        raise KeyError(key)
    raw = key[0]
    if raw in ("#U", "#U-", "-U*"):
        # These are Undo only in the corresponding one-hand mode.
        return "=mejiro_undo:" + raw
    preview = engine().preview(raw)
    if preview.request == 1:
        return "=mejiro_undo"
    if preview.request == 2:
        return "=mejiro_repeat_last_output"
    return "{:mejiro_engine:" + raw + "}"


def require_extension(ctx, argument):
    raise RuntimeError(
        "Enable the 'mejiro_engine' extension in Plover Configure > Plugins. "
        "Mejiro strokes must be resolved before Plover formatting."
    )
