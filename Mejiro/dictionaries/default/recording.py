"""辞書とフォーマッターが共有するマクロ記録先。"""

macro_KEYS = ("n", "t", "k", "nt", "nk", "tk", "ntk")
macro_values = {key: "" for key in macro_KEYS}
active_recording_macros = set()
recording_macro_order = []


def record_output(text):
    for key in active_recording_macros:
        macro_values[key] += text
