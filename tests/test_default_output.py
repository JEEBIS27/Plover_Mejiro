"""Check startup output in a fresh process, without test mode overrides."""
import subprocess
import sys
import unittest
from pathlib import Path


class DefaultOutputTests(unittest.TestCase):
    def test_startup_romaji_and_explicit_kana_toggle(self):
        subprocess.run([sys.executable, "-c", """
from plover.translation import Translation
from Mejiro.engine import State, lookup
from Mejiro.formatting import NativeFormatter
from plover.formatting import Formatter
from types import SimpleNamespace
from plover.registry import registry
from plover.meta.attach import meta_attach
registry.register_plugin('meta', 'attach', meta_attach)

output = []
base = Formatter()
base.set_output(SimpleNamespace(send_string=output.append))
formatter = NativeFormatter(base)
history = []
for stroke, expected in [('KA-', 'ka'), ('#-n', ''), ('KA-', 'か')]:
    output.clear()
    translation = Translation([], lookup((stroke,)))
    formatter.format([], [translation], history)
    history.append(translation)
    assert ''.join(output) == expected, (stroke, output)
"""], cwd=Path(__file__).resolve().parents[1], check=True)
