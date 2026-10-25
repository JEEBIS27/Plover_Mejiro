"""IME ON/OFF の意味を、ホストの専用キーへ変換する。"""

import sys

from plover import log
from plover.registry import registry


def select_alternate(engine, argument):
    """登録済みの切り替え先だけを選ぶ。未導入なら何もしない。"""
    target = argument or "Phonetix"
    try:
        plugin = registry.get_plugin("system", target)
    except KeyError:
        return
    try:
        if engine.config["system_name"] != plugin.name:
            engine.config = {"system_name": plugin.name}
    except Exception:
        # 切り替え失敗で、後続のIME OFFまで止めない。
        log.error("Unable to select alternate system: %s", target, exc_info=True)


def set_ime(engine, argument):
    if argument not in ("on", "off"):
        raise ValueError("MEJIRO_IME expects on or off")
    enabled = argument == "on"
    if sys.platform.startswith("linux"):
        # XKB のUS/JP配列の両方にある専用キー。Fキーやトグルは使わない。
        engine._send_key_combination("Hiragana" if enabled else "Muhenkan")
    elif sys.platform == "win32":
        # Plover の標準キー名表には VK_IME_ON/OFF がないため、既存の
        # Windows送信機で仮想キーを直接押下・解放する。
        key = 0x16 if enabled else 0x1A  # VK_IME_ON / VK_IME_OFF
        engine._keyboard_emulation._key_event(key, True)
        engine._keyboard_emulation._key_event(key, False)
    elif sys.platform == "darwin":
        from Quartz import CGEventCreateKeyboardEvent, CGEventPost, kCGHIDEventTap

        key = 104 if enabled else 102  # JIS Kana / Eisu
        for pressed in (True, False):
            CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, key, pressed))
    else:
        raise RuntimeError(f"Unsupported IME host: {sys.platform}")
