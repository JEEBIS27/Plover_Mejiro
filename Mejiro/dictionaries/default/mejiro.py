"""Plover dictionary adapter. All language rules live in the Rust engine."""
from Mejiro.engine import engine, lookup

LONGEST_KEY = 1


def reverse_lookup(text):
    result = engine().reverse_lookup(text)
    return [tuple(candidate["strokes"].split("/")) for candidate in result["all"]]
