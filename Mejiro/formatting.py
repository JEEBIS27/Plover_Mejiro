"""Resolve Rust previews only when Plover commits a translation.

Each Translation owns a state snapshot, so undo and multistroke replacement
restore the same vowels, grammatical context and pending small-tsu.
"""
import re

from plover.translation import Translation

from Mejiro import engine as native
from Mejiro.dictionaries.default import recording

MARKER = re.compile(r"\A\{:mejiro_engine:([#A-Za-z*\-]+)\}\Z")


class NativeFormatter:
    def __init__(self, formatter):
        self.formatter = formatter

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
        state.mode = selected_mode
        result = native.engine().preview(raw, state)
        next_state = result.state
        body = result.body
        committed = getattr(translation, "_mejiro_committed", False)
        if raw in native.USERS_MAP:
            override = native.engine().override(native.USERS_MAP[raw], state)
            body, next_state = override.body, override.state
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
        elif result.request:
            raise RuntimeError(f"Unexpected Mejiro control in formatter: {result.request}")
        if not committed and body:
            recording.record_output(body)
        translation._mejiro_committed = True
        translation._mejiro_state = next_state.clone()
        translation._mejiro_body = body
        translation.english = "{^" + body + "^}"
        return next_state

    def format(self, undo, do, prev):
        state = self.previous_state(prev)
        for translation in do:
            state = self.resolve(translation, state)
        self.formatter.format(undo, do, prev)


class EngineExtension:
    def __init__(self, engine):
        self.engine = engine
        self.adapter = NativeFormatter(engine._formatter)

    def start(self):
        native.engine()  # Fail before altering the listener list.
        self.engine._translator.remove_listener(self.engine._formatter.format)
        self.engine._translator.add_listener(self.adapter.format)

    def stop(self):
        self.engine._translator.remove_listener(self.adapter.format)
        self.engine._translator.add_listener(self.engine._formatter.format)


def repeat_last_output(translator, stroke, argument):
    """Repeat resolved Plover output, including ordinary user dictionaries."""
    assert not argument
    for previous in reversed(translator.get_state().translations):
        if not previous.has_undo():
            continue
        repeated = Translation([stroke], previous.english)
        state = getattr(previous, "_mejiro_state", None)
        if state is not None:
            repeated._mejiro_state = state.clone()
            repeated._mejiro_body = previous._mejiro_body
            recording.record_output(repeated._mejiro_body)
        translator.translate_translation(repeated)
        return


def mejiro_undo(translator, stroke, argument):
    assert not argument
    for translation in reversed(translator.get_state().translations):
        translator.untranslate_translation(translation)
        if translation.has_undo():
            return
    translator.flush([Translation([stroke], "{#BackSpace}{#BackSpace}{^}")])
