"""Run with: python -m unittest discover -s tests -v (requires Plover)."""

import contextlib
import configparser
import io
from importlib.metadata import EntryPoint, entry_points
from pathlib import Path
import unittest

from plover import system
from plover.dictionary.json_dict import JsonDictionary
from plover.formatting import Formatter
from plover.registry import registry
from plover.steno import Stroke
from plover.steno_dictionary import StenoDictionary, StenoDictionaryCollection
from plover.translation import Translation, Translator
from plover_python_dictionary import PythonDictionary

from Mejiro import engine as native
from Mejiro.formatting import NativeFormatter
from Mejiro.dictionaries.default import func, recording
from Mejiro.dictionaries.default.settings import COMMA, PARTICLE_KEY_LIST
from Mejiro.dictionaries.default.translate import kana_to_typing_output
from Mejiro.dictionaries.default.verb import (
    AUXILIARY_VERB_EXCEPTION_MAP, AUXILIARY_VERB_LEFT_MAP,
    AUXILIARY_VERB_RIGHT_MAP, DESU_CONJUGATE_MAP,
)

ROOT = Path(__file__).resolve().parents[1]
DICTIONARIES = ROOT / "Mejiro/dictionaries/default"


class Output:
    def __init__(self):
        self.text = ""
        self.combos = []

    def send_string(self, text):
        self.text += text

    def send_backspaces(self, count):
        self.text = self.text[:-count]

    def send_key_combination(self, combo):
        self.combos.append(combo)
        if combo == "BackSpace":
            self.text = self.text[:-1]


class ParticleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load real entry points without importing optional Qt GUI plugins.
        for group in ("meta", "macro"):
            for entry in entry_points(group="plover." + group):
                registry.register_plugin(group, entry.name, entry.load())
        config = configparser.ConfigParser()
        config.read(ROOT / "setup.cfg")
        for group in ("system", "meta", "macro"):
            value = config["options.entry_points"]["plover." + group].strip()
            for entry in value.splitlines():
                name, target = map(str.strip, entry.split("=", 1))
                plugin = EntryPoint(name=name, value=target, group="plover." + group)
                registry.register_plugin(group, name, plugin.load())
        system.setup("Mejiro")
        cls.dictionary = PythonDictionary.load(str(DICTIONARIES / "mejiro.py"))
        cls.commands = JsonDictionary.load(str(DICTIONARIES / "mejiro_commands.json"))

    def setUp(self):
        self.module = native
        self.module.is_typing_mode = False
        self.module.typing_mode = 0
        func.LAST_VOWEL_STROKE = ""
        recording.active_recording_macros.clear()
        recording.recording_macro_order.clear()
        recording.macro_values.update({key: "" for key in recording.macro_KEYS})
        self.make_engine()

    def make_engine(self, extra=None):
        self.output = Output()
        self.formatter = Formatter()
        self.formatter.set_output(self.output)
        self.translator = Translator()
        dictionaries = ([extra] if extra is not None else []) + [self.commands, self.dictionary]
        self.translator.set_dictionary(StenoDictionaryCollection(dictionaries))
        self.translator.set_min_undo_length(100)
        self.adapter = NativeFormatter(self.formatter)
        self.translator.add_listener(self.adapter.format)

    def stroke(self, *strokes):
        with contextlib.redirect_stdout(io.StringIO()):
            for raw in strokes:
                self.translator.translate(Stroke(raw))
        return self.output.text

    def test_one_hand_switching_and_opposite_hand_fallback(self):
        self.assertEqual(self.stroke("#STKNYIAUntk-", "#KAU-"), "こと")
        self.assertEqual(self.stroke("-STKNYIAUntk*", "-TAU*", "-U"), "ことところう")
        self.assertEqual(self.stroke("KA-TA", "-U"), "ことところう")
        self.assertEqual(self.stroke("KA-"), "ことところうか")

    def test_one_hand_i_and_ia_are_phonetic_without_symbol(self):
        for switch, strokes in [
            ("#STKNYIAUntk-", ["KI-", "KIA-", "KIn-", "KIAt-", "#KI-", "#KIA-"]),
            ("-STKNYIAUntk*", ["-KI", "-KIA", "-KIn", "-KIAt", "-KI*", "-KIA*"]),
        ]:
            with self.subTest(switch=switch):
                self.make_engine()
                self.assertEqual(self.stroke(switch, *strokes), "きけきんけつときけす")

    def test_left_symbol_key_is_the_one_hand_abbreviation_key(self):
        self.assertEqual(self.stroke("#STKNYIAUntk-", "#-", "#n-", "#KAUntk-"), "するしないことは")

    def test_one_hand_romaji_keeps_pending_sokuon_across_switch(self):
        native.is_typing_mode = True
        self.assertEqual(self.stroke("#STKNYIAUntk-", "KAtk-"), "ka")
        self.assertEqual(self.stroke("-STKNYIAUntk*", "-KA"), "kakka")
        erased = []
        self.adapter.output.output = self.adapter.output.output._replace(send_backspaces=erased.append)
        self.stroke("#STKNYIAUntk-STKNYIAUntk*", "-U", "TA-")
        self.assertEqual(erased, [2])
        self.assertEqual(self.translator.get_state().translations[-1]._mejiro_body, "った")

    def test_stn_without_vowel_keeps_only_extra_sound(self):
        for raw, expected in (("STN-", ""), ("STNtk-", "っ"),
                              ("STNntk-", "ー"), ("KAntk-STNtk", "かーっ")):
            with self.subTest(raw=raw):
                self.make_engine()
                self.assertEqual(self.stroke(raw), expected)

    def test_requested_examples(self):
        self.assertEqual(self.stroke("n-*", "k-k"), "しているのが")
        self.make_engine()
        self.assertEqual(self.stroke("-k*", "k-k"), "しますのが")

    def test_visible_conjugation_examples(self):
        examples = {
            "-*": "する", "-n*": "しない", "-t*": "した", "-nt*": "しなかった",
            "-nk*": "しません", "-tk*": "しました", "t-*": "させる",
            "k-*": "される", "nk-*": "してしまう", "nt-*": "しやすい",
            "nt-n*": "しにくい", "nt-t*": "したい", "nt-nt*": "してほしい",
            "n-n*": "していない", "n-t*": "していた", "n-k*": "しています",
            "TAtk-STA*": "はたらける",
        }
        for raw, text in examples.items():
            with self.subTest(raw=raw):
                self.make_engine()
                self.assertEqual(self.stroke(raw, "k-k"), text + "のが")

    def test_every_conjugation_for_each_verb_class(self):
        right_keys = ("", "n", "t", "k", "nt", "nk", "tk", "ntk")
        complete = ("のが",) * 7 + ("な",)
        expectations = {
            "": complete, "n": complete, "t": complete, "k": complete, "nk": complete,
            "nt": ("のが", "のが", "のが", "な", "のが", "な", "な", "な"),
            "tk": complete, "ntk": ("な",) * 8,
        }
        # Coverage must be revisited when the actual conjugation tables grow.
        self.assertEqual(set(right_keys), set(AUXILIARY_VERB_RIGHT_MAP))
        self.assertEqual(set(expectations), {"", *AUXILIARY_VERB_LEFT_MAP,
                                            *(key.split("-")[0] for key in AUXILIARY_VERB_EXCEPTION_MAP)})
        self.assertEqual(set(AUXILIARY_VERB_EXCEPTION_MAP), {
            left + "-" + right for left in ("nt", "tk", "ntk") for right in right_keys
        })
        for stem in ("-", "K-", "I-K", "A-ST", "TKA-TA", "SI-SNI", "TN-KIA", "TA-SKNA"):
            left_stem, right_stem = stem.split("-")
            for left, suffixes in expectations.items():
                for right, suffix in zip(right_keys, suffixes):
                    raw = left_stem + left + "-" + right_stem + right + "*"
                    with self.subTest(stroke=raw):
                        self.make_engine()
                        before = self.stroke(raw)
                        self.assertTrue(before)
                        self.assertEqual(self.stroke("k-k"), before + suffix)

    def test_implicit_verbs_without_asterisk(self):
        for raw in ("KA-K", "-SKNI", "-TNIA"):
            with self.subTest(raw=raw):
                self.make_engine()
                before = self.stroke(raw)
                self.assertTrue(before)
                self.assertEqual(self.stroke("k-k"), before + "のが")

    def test_all_desu_forms(self):
        for right in DESU_CONJUGATE_MAP:
            with self.subTest(right=right):
                self.make_engine()
                before = self.stroke("-TN" + right)
                suffix = "のが" if right in ("", "t") else "な"
                self.assertEqual(self.stroke("k-k"), before + suffix)

    def test_all_particle_combinations(self):
        for left in PARTICLE_KEY_LIST:
            for right in PARTICLE_KEY_LIST:
                if not left and not right:
                    continue
                with self.subTest(left=left, right=right):
                    self.make_engine()
                    # A prior verb must never leak through an intervening particle.
                    before = self.stroke("n-*", left + "-" + right)
                    self.assertEqual(self.stroke("k-k"), before + "な")

    def test_comma_variant_and_boundary(self):
        self.assertEqual(self.stroke("n-*", "k-nk"), "しているのが" + COMMA)
        self.assertEqual(self.stroke("k-k"), "しているのが" + COMMA + "な")
        self.make_engine()
        self.assertEqual(self.stroke("k-nk", "k-k"), "な" + COMMA + "な")
        self.make_engine()
        self.assertEqual(self.stroke("k-k", "k-nk"), "なのが" + COMMA)

    def test_unknown_kana_does_not_guess_part_of_speech(self):
        for raw, text in (("KA-STU", "かる"), ("KI-STIA", "きれ"), ("NA-", "な")):
            with self.subTest(raw=raw):
                self.make_engine()
                self.assertEqual(self.stroke("n-*", raw, "k-k"), "している" + text + "な")

    def test_undo_restores_context(self):
        self.assertEqual(self.stroke("n-*", "k-k", "-U", "k-nk"), "しているのが" + COMMA)
        self.make_engine()
        self.assertEqual(self.stroke("k-k", "n-*", "-U", "k-k"), "なのが")
        self.make_engine()
        self.assertEqual(self.stroke("n-*", "KA-", "-U", "k-k"), "しているのが")

    def test_undo_without_history_erases_two_characters(self):
        self.output.text = "abcd"
        self.assertEqual(self.stroke("-U"), "ab")
        self.assertEqual(self.stroke("-U"), "")
        self.output.text = "xyz"
        self.assertEqual(self.stroke("KA-", "-U"), "xyz")
        self.assertEqual(self.stroke("-U"), "x")

    def test_state_reset_drops_context(self):
        self.stroke("n-*")
        self.translator.clear_state()
        self.assertEqual(self.stroke("k-k"), "しているな")

    def test_lookups_do_not_change_grammar(self):
        self.stroke("n-*")
        with contextlib.redirect_stdout(io.StringIO()):
            for raw in ("k-k", "-nt", "-k", "KA-", "ntk-t*", "k-nk") * 3:
                self.dictionary.get((raw,))
        self.assertEqual(self.stroke("k-k"), "しているのが")

    def test_same_stroke_word_particle_uses_local_context(self):
        self.assertEqual(self.stroke("n-*", "KAk-k"), "しているかな")
        self.assertEqual(self.stroke("k-k"), "しているかなのが")
        self.make_engine()
        self.assertEqual(self.stroke("NAk-k", "k-k"), "なのがな")

    def test_abstract_copula(self):
        for raw, expected in (("Kn-T", "ことであるのが"), ("Kn-Tn", "ことだったのが"),
                              ("K-Tn", "ことだな"), ("Kk-Tk", "ことなのが")):
            with self.subTest(raw=raw):
                self.make_engine()
                self.assertEqual(self.stroke(raw, "k-k"), expected)

    def test_typing_modes(self):
        for mode in (0, 1):
            with self.subTest(mode=mode):
                self.make_engine()
                self.module.typing_mode = mode
                self.module.is_typing_mode = True
                expected = kana_to_typing_output("しているのが" + COMMA, mode)
                self.assertEqual(self.stroke("n-*", "k-nk"), expected)

    def test_typing_mode_switch_preserves_context(self):
        self.assertEqual(self.stroke("n-*", "#-n", "k-k"), "しているnoga")

    def test_macro_records_resolved_particle(self):
        self.stroke("#n*", "n-*", "k-k", "#-*")
        self.assertEqual(recording.macro_values["n"], "しているのが")
        self.assertEqual(self.stroke("#n"), "しているのがしているのが")

    def test_empty_macro_controls_preserve_context(self):
        self.stroke("n-*", "#n*")
        self.assertEqual(self.stroke("k-k"), "しているのが")
        self.assertEqual(recording.macro_values["n"], "のが")

    def test_unrendered_auto_particle_does_not_record(self):
        self.stroke("#n*")
        self.dictionary.get(("k-k",))
        self.assertEqual(recording.macro_values["n"], "")

    def test_user_dictionary_overrides_are_unknown(self):
        override = StenoDictionary()
        override[("n-*",)] = "{^しいたけ^}"
        self.make_engine(override)
        self.assertEqual(self.stroke("n-*", "k-k"), "しいたけな")

    def test_user_multistroke_dictionary_still_works(self):
        override = StenoDictionary()
        override[("n-*", "k-k")] = "{^登録済みの語句^}"
        self.make_engine(override)
        self.assertEqual(self.stroke("n-*", "k-k"), "登録済みの語句")
        self.assertEqual(self.stroke("k-k"), "登録済みの語句な")

    def test_user_map_override_is_unknown(self):
        self.module.USERS_MAP["n-*"] = "きれい"
        try:
            self.assertEqual(self.stroke("n-*", "k-k"), "きれいな")
        finally:
            del self.module.USERS_MAP["n-*"]

    def test_cursor_operation_breaks_context(self):
        self.assertEqual(self.stroke("n-*", "-A", "k-k"), "しているな")
        self.assertEqual(self.output.combos, ["Left"])

    def test_native_vowels_undo_and_lookup_are_isolated(self):
        self.assertEqual(self.stroke("KI-"), "き")
        for raw in ("KU-", "TNYIUtk-", "#n*", "#-n"):
            self.dictionary.get((raw,))
        self.assertFalse(native.is_typing_mode)
        self.assertFalse(recording.active_recording_macros)
        self.assertEqual(self.stroke("STKN-"), "きふぃ")
        self.assertEqual(self.stroke("KU-", "-U", "STKN-"), "きふぃふぃ")

    def test_native_user_map_typing_uses_rust(self):
        native.USERS_MAP["n-*"] = "あめりか"
        native.is_typing_mode = True
        try:
            self.assertEqual(self.stroke("n-*"), "amerika")
        finally:
            del native.USERS_MAP["n-*"]

    def test_native_repeater_is_recorded(self):
        self.stroke("#n*", "n-*", "#-", "#-*")
        self.assertEqual(recording.macro_values["n"], "しているしている")
        self.assertEqual(self.stroke("#n"), "しているしているしているしている")

    def test_native_pending_sokuon_undo(self):
        native.is_typing_mode = True
        self.stroke("KAtk-")
        self.assertEqual(self.output.text, "ka")
        self.assertEqual(self.translator.get_state().translations[-1]._mejiro_body, "か")
        self.assertTrue(self.translator.get_state().translations[-1]._mejiro_state.pending_sokuon)
        self.dictionary.get(("KI-",))
        self.stroke("KA-")
        self.assertEqual(self.output.text, "kakka")
        self.assertEqual(self.translator.get_state().translations[-1]._mejiro_body, "っか")
        erased = []
        self.adapter.output.output = self.adapter.output.output._replace(send_backspaces=erased.append)
        self.stroke("-U", "TA-")
        self.assertEqual(erased, [2])
        self.assertEqual(self.translator.get_state().translations[-1]._mejiro_body, "った")

    def test_romaji_undo_counts_kana_not_sent_keys(self):
        native.is_typing_mode = True
        sent, erased = [], []
        self.adapter.output.output = self.adapter.output.output._replace(
            send_string=sent.append, send_backspaces=erased.append)
        native.USERS_MAP["KA"] = "では"
        try:
            self.stroke("KA")
            self.assertEqual(self.translator.get_state().translations[-1]._mejiro_body, "では")
            self.stroke("-U")
        finally:
            del native.USERS_MAP["KA"]
        self.assertEqual(sent, ["deha"])
        self.assertEqual(erased, [2])

    def test_romaji_multistroke_revision_and_undo_use_kana_suffix(self):
        native.is_typing_mode = True
        extra = StenoDictionary()
        extra[("KA", "KI")] = self.dictionary.get(("TA",))
        self.make_engine(extra)
        sent, erased = [], []
        self.adapter.output.output = self.adapter.output.output._replace(
            send_string=sent.append, send_backspaces=erased.append)
        native.USERS_MAP.update({"KA": "では", "TA": "である"})
        try:
            self.stroke("KA", "KI")
            self.assertEqual(sent, ["deha", "aru"])
            self.assertEqual(erased, [1])
            self.stroke("-U")
            self.assertEqual(sent, ["deha", "aru", "ha"])
            self.assertEqual(erased, [1, 2])
        finally:
            del native.USERS_MAP["KA"]
            del native.USERS_MAP["TA"]

    def test_typing_literal_user_dictionary_is_not_transliterated(self):
        native.is_typing_mode = True
        extra = StenoDictionary()
        extra[("KA",)] = "{^では^}"
        self.make_engine(extra)
        self.assertEqual(self.stroke("KA"), "では")

    def test_typing_toggle_in_one_batch_uses_each_translation_mode(self):
        native.is_typing_mode = True
        sent = []
        self.adapter.output.output = self.adapter.output.output._replace(send_string=sent.append)
        translations = [Translation([Stroke(raw)], self.dictionary.get((raw,)))
                        for raw in ("KA-", "#-n", "KA-")]
        self.adapter.format([], translations, [])
        self.assertEqual(sent, ["ka", "か"])

    def test_native_vowel_revision_through_plover(self):
        for raw, expected in (("STKNYk-", "ゔぁ"), ("STKNIUntk-", "てゅー"),
                              ("STKNYIUntk-", "ゔゅー"), ("TNYIUntk-", "どぅー"),
                              ("TNYIAUntk-", "づぉー"), ("STNYk-", "ぅぁ")):
            with self.subTest(stroke=raw):
                self.make_engine()
                self.assertEqual(self.stroke(raw), expected)

    def test_plain_particle_conversion_is_stateless(self):
        for _ in range(3):
            self.assertEqual(func.joshi("k", "k"), "な")
            self.assertEqual(func.joshi("k", "nk"), "な" + COMMA)

    def test_macro_records_logical_kana_in_typing_mode(self):
        self.module.is_typing_mode = True
        self.stroke("#n*", "n-*", "k-nk", "#-*")
        self.assertEqual(recording.macro_values["n"], "しているのが" + COMMA)

    def test_multiple_translations_in_one_format_call(self):
        with contextlib.redirect_stdout(io.StringIO()):
            translations = [Translation([Stroke(raw)], self.dictionary.get((raw,)))
                            for raw in ("n-*", "k-k")]
        self.adapter.format([], translations, [])
        self.assertEqual(self.output.text, "しているのが")
        # Plover logs must also be able to display the custom action.
        self.assertTrue(hasattr(translations[-1], "_mejiro_state"))

    def test_repeater_repeats_resolved_particle(self):
        self.assertEqual(self.stroke("k-k", "#-", "#-"), "ななな")
        self.assertEqual(self.stroke("k-k"), "なななのが")
        self.make_engine()
        self.assertEqual(self.stroke("n-*", "k-k", "#-", "#-"), "しているのがのがのが")
        self.assertEqual(self.stroke("k-k"), "しているのがのがのがな")

    def test_repeater_still_repeats_normal_output(self):
        self.assertEqual(self.stroke("n-*", "#-", "k-k"), "しているしているのが")

    def test_he_ka_visible_examples(self):
        examples = {
            "n-*": "しているか", "-k*": "しますか", "-nk*": "しませんか",
            "nt-t*": "したいか", "ntk-k*": "しましょうか", "ntk-ntk*": "しようか",
            "-TN": "ですか", "-TNt": "でしたか", "-TNk": "でしょうか",
            "K-T": "ことか", "SKN-N": "ものか", "K-KAU": "ここへ",
            "T-ST": "ところへ", "N-N": "なにか", "NA-N": "なんか",
            "TN-STIA": "どれか", "KA-": "かへ",
        }
        for raw, expected in examples.items():
            with self.subTest(stroke=raw):
                self.make_engine()
                self.assertEqual(self.stroke(raw, "ntk-"), expected)

    def test_he_ka_every_verb_conjugation(self):
        right_keys = ("", "n", "t", "k", "nt", "nk", "tk", "ntk")
        complete = ("か",) * 7 + ("へ",)
        expectations = {
            "": complete, "n": complete, "t": complete, "k": complete, "nk": complete,
            "nt": ("か", "か", "か", "へ", "か", "へ", "へ", "へ"),
            "tk": complete, "ntk": ("へ", "へ", "へ", "か", "へ", "へ", "へ", "か"),
        }
        for stem in ("-", "K-", "I-K", "A-ST", "TKA-TA", "SI-SNI", "TN-KIA", "TA-SKNA"):
            left_stem, right_stem = stem.split("-")
            for left, suffixes in expectations.items():
                for right, suffix in zip(right_keys, suffixes):
                    raw = left_stem + left + "-" + right_stem + right + "*"
                    with self.subTest(stroke=raw):
                        self.make_engine()
                        before = self.stroke(raw)
                        self.assertEqual(self.stroke("ntk-"), before + suffix)

    def test_he_ka_all_right_suffixes(self):
        # Nominal modifiers distinguish ことへの / 何かの / しているかのよう.
        he = ("へ", "へ、", "へは", "への", "へも", "へは、", "への、", "へも、")
        ka = ("か", "か、", "かは", "への", "かも", "かは、", "への、", "かも、")
        indefinite = ("か", "か、", "かは", "かの", "かも", "かは、", "かの、", "かも、")
        for raw, suffixes in (("KA-", he), ("K-KAU", he), ("K-T", ka),
                              ("n-*", indefinite), ("N-N", indefinite)):
            for right, suffix in zip(PARTICLE_KEY_LIST, suffixes):
                with self.subTest(stroke=raw, right=right):
                    self.make_engine()
                    before = self.stroke(raw)
                    self.assertEqual(self.stroke("ntk-" + right), before + suffix)

    def test_abstract_attached_and_separate_particles_agree(self):
        for stem in ("K-T", "SKN-N", "K-KAU", "T-ST", "N-N", "NA-N", "TN-STIA",
                     "-SKNAU*", "-TAU*", "K-STN*", "Y-STN*", "S-NA"):
            for left, rights in (("ntk", PARTICLE_KEY_LIST), ("k", ("k", "nk"))):
                for right in rights:
                    with self.subTest(stem=stem, left=left, right=right):
                        self.make_engine()
                        separate = self.stroke(stem, left + "-" + right)
                        asterisk = "*" if stem.endswith("*") else ""
                        left_stem, right_stem = stem.removesuffix("*").split("-")
                        attached = left_stem + left + "-" + right_stem + right + asterisk
                        self.make_engine()
                        self.assertEqual(self.stroke(attached), separate)

    def test_abstract_places_and_modifiers(self):
        for raw, expected in (("Kntk-KAU", "ここへ"), ("Kntk-Tk", "ことへの"),
                              ("Nntk-Nk", "なにかの"), ("-TAU*", "あのところ"),
                              ("K-STN*", "この")):
            with self.subTest(stroke=raw):
                self.make_engine()
                self.assertEqual(self.stroke(raw), expected)
        for raw in ("K-NA", "S-NA", "TN-NA", "Y-STN*"):
            with self.subTest(stroke=raw):
                self.make_engine()
                before = self.stroke(raw)
                self.assertEqual(self.stroke("k-k"), before + "のが")

    def test_he_ka_after_other_particles(self):
        for raw, suffix in (("k-", "か"), ("nt-", "か"), ("-tk", "か"), ("ST-", "か"),
                            ("TN-ST", "か"), ("TN-K", "か"), ("t-", "へ"),
                            ("-t", "へ"), ("-k", "へ"), ("tk-k", "へ"), ("k-k", "へ")):
            with self.subTest(stroke=raw):
                self.make_engine()
                before = self.stroke(raw)
                self.assertEqual(self.stroke("ntk-"), before + suffix)
        self.make_engine()
        self.assertEqual(self.stroke("n-*", "k-", "ntk-"), "しているのか")
        self.make_engine()
        self.assertEqual(self.stroke("K-T", "nt-", "ntk-"), "こととか")
        self.make_engine()
        self.assertEqual(self.stroke("n-*", "ntk-k", "STN-YI*"), "しているかのよう")

    def test_he_ka_boundaries(self):
        for raw in ("-nt", "-nk", "n-", "-n", "n-n", "-A"):
            with self.subTest(stroke=raw):
                self.make_engine()
                before = self.stroke("n-*", raw)
                self.assertEqual(self.stroke("ntk-"), before + "へ")
        self.make_engine()
        self.assertEqual(self.stroke("n-*", "ntk-n", "ntk-"), "しているか、へ")

    def test_he_ka_undo_and_cross_particle_context(self):
        self.assertEqual(self.stroke("K-T", "K-KAU", "-U", "ntk-"), "ことか")
        self.make_engine()
        self.assertEqual(self.stroke("n-*", "ntk-", "-U", "k-k"), "しているのが")
        self.make_engine()
        self.assertEqual(self.stroke("K-KAU", "k-k", "-U", "ntk-"), "ここへ")
        self.make_engine()
        self.stroke("n-*")
        self.translator.clear_state()
        self.assertEqual(self.stroke("ntk-"), "しているへ")

    def test_he_ka_typing_recording_and_repeater(self):
        for mode in (0, 1):
            with self.subTest(mode=mode):
                self.make_engine()
                self.module.is_typing_mode = True
                self.module.typing_mode = mode
                self.stroke("#n*", "n-*", "ntk-n", "#-*")
                self.assertEqual(self.output.text, kana_to_typing_output("しているか、", mode))
                self.assertEqual(recording.macro_values["n"], "しているか、")
        self.module.is_typing_mode = False
        self.make_engine()
        self.assertEqual(self.stroke("n-*", "ntk-", "#-", "#-"), "しているかかか")
        self.make_engine()
        self.assertEqual(self.stroke("K-KAU", "ntk-", "#-", "#-"), "ここへへへ")

    def test_he_ka_override_and_lookup_safety(self):
        override = StenoDictionary()
        override[("n-*",)] = "{^している^}"
        self.make_engine(override)
        self.assertEqual(self.stroke("n-*", "ntk-"), "しているへ")
        override[("n-*", Stroke("ntk-").rtfcre)] = "{^登録語^}"
        self.make_engine(override)
        self.assertEqual(self.stroke("n-*", "ntk-"), "登録語")
        self.make_engine()
        self.stroke("n-*")
        with contextlib.redirect_stdout(io.StringIO()):
            for raw in ("K-T", "ntk-", "K-KAU", "ntk-k", "k-k"):
                self.dictionary.get((raw,))
        self.assertEqual(self.stroke("ntk-"), "しているか")

    def test_he_ka_same_batch(self):
        for raw, expected in (("n-*", "しているか"), ("K-KAU", "ここへ")):
            with self.subTest(stroke=raw):
                self.make_engine()
                with contextlib.redirect_stdout(io.StringIO()):
                    translations = [Translation([Stroke(s)], self.dictionary.get((s,)))
                                    for s in (raw, "ntk-")]
                self.adapter.format([], translations, [])
                self.assertEqual(self.output.text, expected)


if __name__ == "__main__":
    unittest.main()
