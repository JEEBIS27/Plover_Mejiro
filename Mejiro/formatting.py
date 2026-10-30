"""Resolve Rust previews only when Plover commits a translation.

Each Translation owns a state snapshot, so undo and multistroke replacement
restore the same vowels, grammatical context and pending small-tsu.
"""
import re

from plover.translation import Translation
from plover.formatting import Formatter

from Mejiro import engine as native
from Mejiro.dictionaries.default import recording

MARKER = re.compile(r"\A\{:mejiro_engine:([#A-Za-z*\-]+)\}\Z")


class ImeOutput:
    """Keep Plover's diff in kana; transliterate only the emitted suffix."""

    def __init__(self, output):
        self.output = output
        self.mode = 0

    def send_string(self, text):
        if not self.mode:
            self.output.send_string(text)
            return
        state = native.State()
        state.mode = self.mode
        rendered = native.engine().override(text, state)
        body = rendered.body
        # A standalone small-tsu explicitly emitted by the shared engine (STN)
        # or flushed at a key boundary must still be sent. Ordinary trailing
        # small-tsu is kept out of the history by NativeFormatter until later.
        if rendered.state.pending_sokuon:
            body += "ltsu" if self.mode == 1 else "Z"
        # The Rust JIS renderer can also return key operations (e.g. Shift+0).
        formatter = Formatter()
        formatter.set_output(self.output)
        formatter.format([], [Translation([], "{^" + body + "^}")], [])

    def send_backspaces(self, count):
        self.output.send_backspaces(count)

    def send_key_combination(self, combo):
        self.output.send_key_combination(combo)

    def send_engine_command(self, command):
        self.output.send_engine_command(command)


class NativeFormatter:
    def __init__(self, formatter):
        self.formatter = formatter
        if formatter is not None:
            self.output = ImeOutput(formatter._output)
            formatter.set_output(self.output)

    @staticmethod
    def previous_state(translations):
        boundary = False
        for translation in reversed(translations or ()):
            state = getattr(translation, "_mejiro_state", None)
            if state is not None:
                state = state.clone()
                if boundary:
                    state.context = 0
                    state.pending_sokuon = 0
                return state
            if translation.english:
                boundary = True
        return native.State()

    def resolve(self, translation, state):
        marker = MARKER.fullmatch(getattr(translation, "_mejiro_source", translation.english or ""))
        if marker is None:
            if hasattr(translation, "_mejiro_state"):
                return translation._mejiro_state.clone()
            # Foreign dictionaries/commands invalidate grammatical context.
            state = state.clone()
            state.context = 0
            state.pending_sokuon = 0
            return state
        translation._mejiro_source = marker.group(0)
        raw = marker.group(1)
        state = state.clone()
        selected_mode = native.typing_mode + 1 if native.is_typing_mode else 0
        if state.mode != selected_mode:
            state.pending_sokuon = 0
        typing_state = state.clone()
        typing_state.mode = selected_mode
        typed = native.engine().preview(raw, typing_state)
        # Store canonical kana in Plover, including in typing modes. The
        # selected physical output mode belongs to the translation separately.
        state.mode = 0
        state.pending_sokuon = 0
        result = native.engine().preview(raw, state)
        next_state = result.state
        body = result.body
        committed = getattr(translation, "_mejiro_committed", False)
        if raw in native.USERS_MAP:
            override = native.engine().override(native.USERS_MAP[raw], state)
            body, next_state = override.body, override.state
            typed = native.engine().override(native.USERS_MAP[raw], typing_state)
        elif result.request == 3:
            if not committed:
                native.is_typing_mode = not native.is_typing_mode
            next_state.mode = native.typing_mode + 1 if native.is_typing_mode else 0
            next_state.pending_sokuon = 0
        elif result.request in (4, 5):
            if not committed:
                if result.request == 4:
                    key = recording.macro_KEYS[result.argument]
                    if key in recording.active_recording_macros:
                        recording.active_recording_macros.remove(key)
                        recording.recording_macro_order.remove(key)
                    else:
                        recording.macro_values[key] = ""
                        recording.active_recording_macros.add(key)
                        recording.recording_macro_order.append(key)
                elif recording.recording_macro_order:
                    recording.active_recording_macros.discard(recording.recording_macro_order.pop())
        elif result.request == 6:
            key = recording.macro_KEYS[result.argument]
            body = recording.macro_values[key]
            next_state.context = 0
            typed = native.engine().override(body, typing_state)
        elif result.request:
            raise RuntimeError(f"Unexpected Mejiro control in formatter: {result.request}")
        if selected_mode and result.request != 3:
            # Use the shared renderer's pending flag (including its explicit
            # STN flush), but associate the delayed kana with the next visible
            # output. Undo then deletes only kana that actually reached the IME
            # and restores the preceding snapshot's pending small-tsu.
            has_body = bool(body)
            if typed.state.pending_sokuon and body.endswith("っ"):
                body = body[:-1]
            if typing_state.pending_sokuon and has_body:
                body = "っ" + body
            next_state.pending_sokuon = typed.state.pending_sokuon
        if not committed and body:
            recording.record_output(body)
        translation._mejiro_control_only = result.request in (3, 4, 5) or raw.replace("-", "") in (
            "#STKNYIAUntk", "STKNYIAUntk*", "#STKNYIAUntkSTKNYIAUntk*",
        )
        translation._mejiro_committed = True
        translation._mejiro_mode = selected_mode
        if result.request != 3:
            next_state.mode = selected_mode
        translation._mejiro_state = next_state.clone()
        translation._mejiro_body = body
        translation.english = "{^" + body + "^}"
        return next_state

    def format(self, undo, do, prev):
        state = self.previous_state(prev)
        history = list(prev or ())
        pending_undo = undo
        for translation in do:
            state = self.resolve(translation, state)
            self.output.mode = getattr(translation, "_mejiro_mode", 0)
            self.formatter.format(pending_undo, [translation], history)
            pending_undo = []
            history.append(translation)
        if pending_undo:
            # Deleted text is already counted in logical kana units.
            self.output.mode = getattr(history[-1], "_mejiro_mode", 0) if history else 0
            self.formatter.format(pending_undo, [], history)


class EngineExtension:
    def __init__(self, engine):
        self.engine = engine
        self.adapter = NativeFormatter(engine._formatter)

    def start(self):
        native.engine()  # Fail before altering the listener list.
        self.engine._formatter.set_output(self.adapter.output)
        self.engine._translator.remove_listener(self.engine._formatter.format)
        self.engine._translator.add_listener(self.adapter.format)

    def stop(self):
        self.engine._translator.remove_listener(self.adapter.format)
        self.engine._formatter.set_output(self.adapter.output.output)
        self.engine._translator.add_listener(self.engine._formatter.format)


def repeat_last_output(translator, stroke, argument):
    """Repeat resolved Plover output, including ordinary user dictionaries."""
    assert not argument
    history = translator.get_state().translations
    state = NativeFormatter.previous_state(history)
    preview = native.engine().preview("#", state)
    if preview.request != 2:
        # The left symbol key is the abbreviation key in left-hand mode.
        translator.translate_translation(Translation([stroke], "{:mejiro_engine:#}"))
        return
    for previous in reversed(history):
        if not previous.has_undo():
            continue
        repeated = Translation([stroke], previous.english)
        state = getattr(previous, "_mejiro_state", None)
        if state is not None:
            repeated._mejiro_state = state.clone()
            # The left # key returns one-hand input to ordinary input.
            repeated._mejiro_state.vowel &= 0x0f
            repeated._mejiro_body = previous._mejiro_body
            repeated._mejiro_mode = previous._mejiro_mode
            recording.record_output(repeated._mejiro_body)
        translator.translate_translation(repeated)
        return


def mejiro_undo(translator, stroke, argument):
    raw = argument or "-U"
    history = translator.get_state().translations
    state = NativeFormatter.previous_state(history)
    preview = native.engine().preview(raw, state)
    if preview.request != 1:
        # In right-hand mode this is the ordinary U vowel, not Undo.
        translator.translate_translation(Translation([stroke], "{:mejiro_engine:" + raw + "}"))
        return
    def keep_input_mode():
        for previous in reversed(translator.get_state().translations):
            remaining = getattr(previous, "_mejiro_state", None)
            if remaining is not None:
                remaining.vowel = (remaining.vowel & 0x0f) | (preview.state.vowel & 0xf0)
                return
        # An invisible state anchor survives even when no text history remains.
        # Plover's flush(extra_translations) emits keys but does not save state.
        anchor = Translation([stroke], "{^}")
        anchor._mejiro_state = native.State()
        anchor._mejiro_state.vowel = preview.state.vowel & 0xf0
        anchor._mejiro_state.mode = state.mode
        anchor._mejiro_mode = state.mode
        anchor._mejiro_control_only = True
        translator.translate_translation(anchor)

    for translation in reversed(tuple(history)):
        translator.untranslate_translation(translation)
        if translation.has_undo() and not getattr(translation, "_mejiro_control_only", False):
            keep_input_mode()
            return
    keep_input_mode()
    translator.flush([Translation([stroke], "{#BackSpace}{#BackSpace}{^}")])
