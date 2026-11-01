"""The Plover dictionary delegates reverse lookup to the shared Rust engine."""
import unittest

from Mejiro.dictionaries.default.mejiro import reverse_lookup


class ReverseLookupTests(unittest.TestCase):
    def test_reverse_lookup_returns_single_and_multistroke_candidates(self):
        single = reverse_lookup("いって")
        self.assertIn(("I-SKntk",), single)
        phrase = reverse_lookup("とはいっても")
        self.assertTrue(phrase)
        self.assertTrue(all(isinstance(candidate, tuple) and candidate for candidate in phrase))
        self.assertTrue(all(all("/" not in stroke for stroke in candidate) for candidate in phrase))


    def test_reverse_lookup_rejects_non_hiragana(self):
        self.assertEqual(reverse_lookup("hello"), [])
