import configparser
from importlib.metadata import EntryPoint
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from plover.formatting import Formatter
from plover.meta.command import meta_command
from plover.meta.attach import meta_attach
from plover.registry import registry
from plover.translation import Translation

from Mejiro.ime import select_alternate, set_ime
from Mejiro.engine import engine

ROOT = Path(__file__).resolve().parents[1]


class ImeTests(unittest.TestCase):
    def test_dictionary_emits_ordered_semantic_commands(self):
        registry.register_plugin("meta", "command", meta_command)
        commands = {raw: "{^" + engine().preview(raw).body + "^}" for raw in ("#-t", "#-k")}
        for stroke, mode in (("#-t", "on"), ("#-k", "off")):
            with self.subTest(stroke=stroke):
                prefix = "{PLOVER:MEJIRO_ALTERNATE:Phonetix}" if mode == "off" else ""
                self.assertIn("{PLOVER:MEJIRO_IME:" + mode + "}", commands[stroke])
                if prefix:
                    self.assertLess(commands[stroke].index(prefix), commands[stroke].index("{PLOVER:MEJIRO_IME:"))
                # Exercise real Plover formatting, without sending host keys.
                output = SimpleNamespace(send_engine_command=Mock())
                registry.register_plugin("meta", "attach", meta_attach)
                formatter = Formatter()
                formatter.set_output(output)
                translation = Translation([], commands[stroke])
                formatter.format([], [translation], [])
                expected = [(("MEJIRO_IME:" + mode,),)]
                if mode == "off":
                    expected.insert(0, (("MEJIRO_ALTERNATE:Phonetix",),))
                self.assertEqual(output.send_engine_command.call_args_list, expected)

    def test_entry_point_is_registered(self):
        config = configparser.ConfigParser()
        config.read(ROOT / "setup.cfg")
        for line in config["options.entry_points"]["plover.command"].strip().splitlines():
            name, value = map(str.strip, line.split("=", 1))
            entry = EntryPoint(name=name, value=value, group="plover.command")
            expected = {"mejiro_ime": set_ime, "mejiro_alternate": select_alternate}[name]
            self.assertIs(entry.load(), expected)
            registry.register_plugin("command", name, entry.load())
            self.assertIs(registry.get_plugin("command", name).obj, expected)

    def test_optional_system_selection_then_ime_off(self):
        # Exercise actual formatting and both command handlers in execution order.
        commands = {raw: "{^" + engine().preview(raw).body + "^}" for raw in ("#-t", "#-k")}
        registry.register_plugin("meta", "attach", meta_attach)
        for available, fails, current in ((False, False, "Mejiro"),
                                           (True, False, "Mejiro"),
                                           (True, True, "Mejiro"),
                                           (True, False, "Phonetix")):
            with self.subTest(available=available, fails=fails, current=current):
                events = []

                class Engine:
                    @property
                    def config(self):
                        return {"system_name": current}

                    @config.setter
                    def config(self, value):
                        events.append(("switch", value["system_name"]))
                        if fails:
                            raise RuntimeError("cannot load system")

                    def _send_key_combination(self, key):
                        events.append(("key", key))

                    def send_engine_command(self, command):
                        name, argument = command.split(":", 1)
                        {"MEJIRO_ALTERNATE": select_alternate,
                         "MEJIRO_IME": set_ime}[name](self, argument)

                def lookup(kind, name):
                    self.assertEqual((kind, name), ("system", "Phonetix"))
                    if not available:
                        raise KeyError(name)
                    return SimpleNamespace(name="Phonetix")

                registry.register_plugin("meta", "command", meta_command)
                formatter = Formatter()
                formatter.set_output(Engine())
                original_lookup = registry.get_plugin
                def dispatch(kind, name):
                    return lookup(kind, name) if kind == "system" else original_lookup(kind, name)
                with patch("Mejiro.ime.registry.get_plugin", side_effect=dispatch), \
                     patch("Mejiro.ime.sys.platform", "linux"), \
                     patch("Mejiro.ime.log.error") as error:
                    formatter.format([], [Translation([], commands["#-k"])], [])
                    self.assertEqual(error.call_count, int(fails))
                expected = [("switch", "Phonetix")] if available and current != "Phonetix" else []
                self.assertEqual(events, expected + [("key", "Hangul_Hanja")])

    def test_alternate_target_can_be_named(self):
        engine = SimpleNamespace(config={"system_name": "Mejiro"})
        with patch("Mejiro.ime.registry.get_plugin", return_value=SimpleNamespace(name="English")) as lookup:
            select_alternate(engine, "English")
        lookup.assert_called_once_with("system", "English")
        self.assertEqual(engine.config, {"system_name": "English"})

    def test_linux_uses_dedicated_keys(self):
        for mode, key in (("on", "Hangul"), ("off", "Hangul_Hanja")):
            engine = Mock()
            with patch("Mejiro.ime.sys.platform", "linux"):
                set_ime(engine, mode)
            engine._send_key_combination.assert_called_once_with(key)
            engine._keyboard_emulation.assert_not_called()

    def test_windows_uses_language_virtual_keys(self):
        for mode, key in (("on", 0x15), ("off", 0x19)):
            engine = Mock()
            with patch("Mejiro.ime.sys.platform", "win32"):
                set_ime(engine, mode)
            self.assertEqual(engine._keyboard_emulation._key_event.call_args_list,
                             [((key, True),), ((key, False),)])
            engine._send_key_combination.assert_not_called()

    def test_macos_uses_jis_kana_eisu(self):
        quartz = SimpleNamespace(CGEventCreateKeyboardEvent=Mock(side_effect=lambda *args: args),
                                 CGEventPost=Mock(), kCGHIDEventTap=0)
        with patch("Mejiro.ime.sys.platform", "darwin"), patch.dict("sys.modules", Quartz=quartz):
            set_ime(Mock(), "on")
            set_ime(Mock(), "off")
        self.assertEqual(quartz.CGEventCreateKeyboardEvent.call_args_list,
                         [((None, 104, True),), ((None, 104, False),),
                          ((None, 102, True),), ((None, 102, False),)])
        self.assertEqual(quartz.CGEventPost.call_count, 4)

    def test_invalid_modes_do_not_emit_keys(self):
        engine = Mock()
        with self.assertRaises(ValueError):
            set_ime(engine, "toggle")
        self.assertEqual(engine.mock_calls, [])
