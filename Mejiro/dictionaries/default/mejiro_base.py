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
from Mejiro.dictionaries.default.settings import (DOT, COMMA, conso_stroke_to_roma)
from Mejiro.dictionaries.default.func import (stroke_to_kana, joshi)
from Mejiro.dictionaries.default.abbreviations import USERS_MAP, ABSTRACT_MAP
from Mejiro.dictionaries.default.verb import stroke_to_verb, VERB_KAMI_MAP
from Mejiro.dictionaries.default.translate import kana_to_typing_output

# ファイル構成
# Mejiro ┬ system.py
#        └ dictionaries ─ default ┬ mejiro_base.py
#                                 ├ mejiro_commands.json
#                                 ├ mejiro_users.json
#                                 ├ settings.py
#                                 ├ func.py
#                                 ├ abbreviations.py
#                                 ├ verb.py
#                                 └ translate.py

# グローバル変数の定義
LONGEST_KEY = 1
LAST_VOWEL_STROKE = "A"
is_typing_mode = False
is_found_exception = [False, False]

# タイピングゲーム時の入力法設定
typing_mode = 0 # 0: ローマ字入力, 1: JISかな入力

# メインの関数
def lookup(key):
    global LONGEST_KEY
    global LAST_VOWEL_STROKE
    global typing_mode
    global is_typing_mode
    global is_found_exception
    assert len(key) <= LONGEST_KEY
    stroke = key[0]

    if stroke == "n#":
        print("typing mode off")
        is_typing_mode = False
    if stroke == "#n":
        print("typing mode on")
        is_typing_mode = True
    
    regex = re.compile(r"(S?T?K?N?)(Y?I?A?U?)(n?t?k?)(\-?#?)(S?T?K?N?)(Y?I?A?U?)(n?t?k?)(\*?)")
    regex_groups = re.search(regex, stroke)

    left_conso_stroke = regex_groups.group(1)
    left_vowel_stroke = regex_groups.group(2)
    left_particle_stroke = regex_groups.group(3)
    hyphen = regex_groups.group(4)
    right_conso_stroke = regex_groups.group(5)
    right_vowel_stroke = regex_groups.group(6)
    right_particle_stroke = regex_groups.group(7)
    asterisk = regex_groups.group(8)
    kana_stroke = left_conso_stroke + left_vowel_stroke + '-' + right_conso_stroke + right_vowel_stroke
    main_stroke = left_conso_stroke + left_vowel_stroke + left_particle_stroke + '-' + right_conso_stroke + right_vowel_stroke + right_particle_stroke

    is_found_exception = [False, False] # 初期化
    result = "" # 初期化

    # 左右のかなを変数に格納
    left_kana_list = stroke_to_kana(left_conso_stroke, left_vowel_stroke, left_particle_stroke, asterisk)
    right_kana_list = stroke_to_kana(right_conso_stroke, right_vowel_stroke, right_particle_stroke, asterisk)
    left_kana, left_extra_sound, left_conso, left_vowel = left_kana_list
    right_kana, right_extra_sound, right_conso, right_vowel = right_kana_list
    main_kana = left_kana + right_kana
    # 基本形を変数に格納
    main_base = left_kana + left_extra_sound + right_kana + right_extra_sound
    # 主要助詞を変数に格納
    main_joshi = joshi(left_particle_stroke, right_particle_stroke)
    # 動詞変換処理
    verb = stroke_to_verb(kana_stroke, right_conso, right_vowel_stroke, left_particle_stroke, right_particle_stroke, left_kana, right_kana, hyphen, asterisk)

    message = ""
    # メインの変換処理
    if main_stroke in USERS_MAP and asterisk: # ユーザー略語
        result = USERS_MAP[main_stroke]
        message = "ユーザー辞書"
    elif kana_stroke in ABSTRACT_MAP and asterisk: # 一般略語
        result = ABSTRACT_MAP[kana_stroke]
        result += (main_joshi.replace("や" + COMMA, "です" + DOT).replace("や", "です"))
        message = "一般略語"
    elif not main_kana and main_joshi and not asterisk: # 助詞
        result = main_joshi
        message = "助詞"
    elif verb and not left_kana and right_kana and not left_extra_sound: # 動詞略語(*省略)
        result = verb
        message = "動詞略語"
    elif asterisk:
        # 特殊略語：～ing
        if len(main_base) > 2 and not kana_stroke in VERB_KAMI_MAP and main_kana[-1] in ['い', 'き', 'し', 'ち', 'に', 'ひ', 'み', 'り', 'ぎ', 'じ', 'ぢ', 'び', 'ぴ', 'ぃ'] and main_base[-1] == 'ん':
            result = (main_base + 'ぐ')
            message = "特殊略語：～ing"
        # 動詞略語
        elif verb:
            result = verb
            message = "動詞略語"
        # 通常
        else:
            message = "通常出力"
            result = main_base * (2 if hyphen == "#" else 1)
    # 通常
    else:
        message = "通常出力"
        result = main_base * (2 if hyphen == "#" else 1)

    # タイピングゲーム時の変換処理
    if is_typing_mode:
        translated_result = kana_to_typing_output(result, typing_mode)
        result = translated_result

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