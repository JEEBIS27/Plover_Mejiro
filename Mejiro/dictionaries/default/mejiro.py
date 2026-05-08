#                             [STKNYIAUntk#STKNYIAUntk*]
# ┌─────┬─────┬─────┬─────┬─────┬─────┐        ┌─────┬─────┬─────┬─────┬─────┬─────┐
# │     │     │  T  │  Y  │  I  │     │        │     │  I  │  Y  │  T  │     │     │
# │  #  │  S  ├─────┼─────┼─────┤  U  │        │  U  ├─────┼─────┼─────┤  S  │  *  │
# │     │     │  K  │  N  │  A  │     │        │     │  A  │  N  │  K  │     │     │
# └─────┴─────┴─────┴─────┴─────┴─────┘        └─────┴─────┴─────┴─────┴─────┴─────┘
#                         ┌───────────┐        ┌───────────┐
#                         │     n     │        │     n     │
#                         ├─────┬─────┤        ├─────┬─────┤
#                         │  t  │  k  │        │  k  │  t  │
#                         └─────┴─────┘        └─────┴─────┘

import re
from Mejiro.dictionaries.default.settings import (conso_stroke_to_roma)
from Mejiro.dictionaries.default.func import (stroke_to_kana, stroke_to_syllable, joshi, abstract_abbreviation_lookup)
from Mejiro.dictionaries.default.abbreviations import USERS_MAP
from Mejiro.dictionaries.default.verb import stroke_to_verb
from Mejiro.dictionaries.default.translate import kana_to_typing_output

# ファイル構成
# Mejiro ┬ system.py
#        └ dictionaries ─ default ┬ mejiro.py
#                                 ├ mejiro_commands.json
#                                 ├ mejiro_users.json
#                                 ├ settings.py
#                                 ├ func.py
#                                 ├ abbreviations.py
#                                 ├ verb.py
#                                 └ translate.py

# グローバル変数の定義
LONGEST_KEY = 1
is_typing_mode = False
REGISTER_KEYS = ("n", "t", "k", "nt", "nk", "tk", "ntk")
register_values = {key: "" for key in REGISTER_KEYS}
active_recording_registers = set()
recording_register_order = []

# タイピングゲーム時の入力法設定
typing_mode = 0 # 0: ローマ字入力, 1: JISかな入力

# メインの関数
def lookup(key):
    global LONGEST_KEY
    global typing_mode
    global is_typing_mode
    global register_values
    global active_recording_registers
    global recording_register_order
    assert len(key) <= LONGEST_KEY
    stroke = key[0]

    if stroke == "#-n":
        if is_typing_mode:
            print("typing mode off")
        else:
            print("typing mode on")
        is_typing_mode = not is_typing_mode
        return ""

    regex = re.compile(r"(#?)(S?T?K?N?)(Y?I?A?U?)(n?t?k?)(\-?)(S?T?K?N?)(Y?I?A?U?)(n?t?k?)(\*?)")
    regex_groups = re.search(regex, stroke)

    hash = regex_groups.group(1)
    left_conso_stroke = regex_groups.group(2)
    left_vowel_stroke = regex_groups.group(3)
    left_particle_stroke = regex_groups.group(4)
    hyphen = regex_groups.group(5)
    right_conso_stroke = regex_groups.group(6)
    right_vowel_stroke = regex_groups.group(7)
    right_particle_stroke = regex_groups.group(8)
    asterisk = regex_groups.group(9)
    left_kana_stroke = left_conso_stroke + left_vowel_stroke
    right_kana_stroke = right_conso_stroke + right_vowel_stroke
    left_stroke = left_conso_stroke + left_vowel_stroke + left_particle_stroke
    right_stroke = right_conso_stroke + right_vowel_stroke + right_particle_stroke
    kana_stroke = left_kana_stroke + '-' + right_kana_stroke
    main_stroke = left_stroke + '-' + right_stroke
    stroke_list = [left_conso_stroke, left_vowel_stroke, left_particle_stroke, hyphen, right_conso_stroke, right_vowel_stroke, right_particle_stroke, asterisk]
    result = "" # 初期化

    is_pure_left_particle = (
        not left_conso_stroke
        and not left_vowel_stroke
        and not right_conso_stroke
        and not right_vowel_stroke
        and not right_particle_stroke
    )
    is_register_target = is_pure_left_particle and left_particle_stroke in REGISTER_KEYS
    is_register_record_start = hash and is_register_target and not hyphen and asterisk
    is_register_record_stop_specific = hash and is_register_target and hyphen and asterisk
    is_register_record_stop_generic = hash and not left_particle_stroke and hyphen and asterisk and not right_stroke
    is_register_replay = hash and is_register_target and not hyphen and not asterisk

    # 左右のかなを変数に格納
    left_kana = stroke_to_kana(left_conso_stroke, left_vowel_stroke)
    right_kana = stroke_to_kana(right_conso_stroke, right_vowel_stroke)

    # 左右の音節を変数に格納
    left_syllable = stroke_to_syllable(left_conso_stroke, left_vowel_stroke, left_particle_stroke)
    right_syllable = stroke_to_syllable(right_conso_stroke, right_vowel_stroke, right_particle_stroke)
    main_syllable = left_syllable + right_syllable
    # 主要助詞を変数に格納
    main_joshi = joshi(left_particle_stroke, right_particle_stroke)
    abstract = abstract_abbreviation_lookup(left_kana_stroke, right_kana_stroke, asterisk)
    verb = stroke_to_verb(left_kana, left_syllable, right_kana, stroke_list)

    message = ""
    # メインの変換処理
    if is_register_record_start:
        target = left_particle_stroke
        if target in active_recording_registers:
            active_recording_registers.remove(target)
            if target in recording_register_order:
                recording_register_order.remove(target)
            message = f"レジストリ記録停止:{target}"
        else:
            register_values[target] = ""
            active_recording_registers.add(target)
            recording_register_order.append(target)
            message = f"レジストリ記録開始:{target}"
        result = ""
    elif is_register_record_stop_specific:
        target = left_particle_stroke
        if target in active_recording_registers:
            active_recording_registers.remove(target)
            if target in recording_register_order:
                recording_register_order.remove(target)
            message = f"レジストリ記録停止:{target}"
        else:
            register_values[target] = ""
            active_recording_registers.add(target)
            recording_register_order.append(target)
            message = f"レジストリ記録開始:{target}(#-*)"
        result = ""
    elif is_register_record_stop_generic:
        if recording_register_order:
            target = recording_register_order.pop()
            active_recording_registers.discard(target)
            message = f"レジストリ記録停止:#-*->{target}"
        else:
            message = "レジストリ記録停止:#-* (未記録)"
        result = ""
    elif is_register_replay:
        target = left_particle_stroke
        result = register_values[target]
        message = f"レジストリ再生:{target}" if result else f"レジストリ空:{target}"
    elif stroke in USERS_MAP: # ユーザー略語
        print(stroke)
        result = USERS_MAP[stroke]
        message = "ユーザー辞書"
    elif kana_stroke == '-' and main_joshi and not asterisk: # 助詞
        result = main_joshi
        message = "助詞"
    # 一般略語変換処理
    elif abstract:
        result = abstract
        result += (main_joshi.replace("}{#Space}{", "である").replace("}{#Return}{", "だ").replace("}{#Tab}{", "だった").replace("}{#F8}{", "でした").replace("}{#F7}{", "です"))
        message = "一般略語"
    # 動詞変換処理
    elif verb:
        result = verb
        message = "動詞略語"
    # 左+助詞
    elif left_kana and not right_kana_stroke and left_particle_stroke + '-' + right_particle_stroke != "ntk-n" and right_particle_stroke:
        message = "左+助詞"
        result = left_kana + main_joshi
    # 通常
    elif not left_stroke and right_kana and not right_particle_stroke:
        message = "未定義の右手略語"
        result = ''
    else :
        message = "通常出力"
        result = main_syllable * (2 if hash else 1)

    # タイピングゲーム時の変換処理
    if is_typing_mode:
        translated_result = kana_to_typing_output(result, typing_mode)
        result = translated_result

    if stroke == "#STKNYIAUntk-STKNYIAUntk*":
        message = "出力取止"
        result = ""

    for register_key in active_recording_registers:
        register_values[register_key] += result
    # デバッグ画面に入力と結果を表示
    print("|\t" + stroke + "\t|\t" + result + "\t|\t" + message + "\t|\t" + ("on" if is_typing_mode else "off") + "\t|")

    # 結果の出力(両端に{^ ^}をつけることで、英語の自動スペースを防ぐ)
    return "{^" + result + "^}"

# 逆引き関数（ストローク検索用）
def reverse_lookup(text):
    result = ""
    string = kana_to_typing_output(text, 0) # ローマ字に変換してから解析
    conso_stroke = next((stroke for roma, stroke in conso_stroke_to_roma if roma == string), None)
    # 一例
    if text == "きき":
        return [("KI-KI", ), ("KInk-", ), ("KI-", "KI-")]

    return []
