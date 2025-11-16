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
#mejiro_kana
import re
from Mejiro.dictionaries.default.settings import (exception_particle, DOT, COMMA, ABSTRACT_ABBREVIATIONS_MAP, conso_stroke_to_roma)
from Mejiro.dictionaries.default.func import (stroke_to_kana, extra_sound, joshi)
from Mejiro.dictionaries.default.verb import stroke_to_verb
from Mejiro.dictionaries.default.translate import kana_to_typing_output

LONGEST_KEY = 1
LAST_VOWEL_STROKE = "A"
is_typing_mode = False
is_found_exception = [False, False]

# タイピングゲーム時の入力法設定
typing_mode = 1 # 0: ローマ字入力, 1: JISかな入力

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

    is_found_exception = [False, False] # 初期化
    result = "" # 初期化
    # 左右のかなを変数に格納
    left_kana_list = stroke_to_kana(left_conso_stroke, left_vowel_stroke, left_particle_stroke)
    right_kana_list = stroke_to_kana(right_conso_stroke, right_vowel_stroke, right_particle_stroke)
    left_kana, left_conso, left_vowel = left_kana_list
    right_kana, right_conso, right_vowel = right_kana_list
    main_kana = left_kana + right_kana
    # 左右の追加音を変数に格納
    left_extra_sound = ("" if left_vowel_stroke + left_particle_stroke in exception_particle else extra_sound(left_particle_stroke))
    right_extra_sound = ("" if right_vowel_stroke + right_particle_stroke in exception_particle else extra_sound(right_particle_stroke))
    # 基本形を変数に格納
    main_base = (left_kana + left_extra_sound + right_kana + right_extra_sound)
    # 主要助詞を変数に格納
    main_joshi = joshi(left_particle_stroke, right_particle_stroke)
    # 動詞変換処理
    verb = stroke_to_verb(left_conso_stroke + left_vowel_stroke + '-' + right_conso_stroke + right_vowel_stroke, right_conso, right_vowel_stroke, left_particle_stroke, right_particle_stroke, left_kana, right_kana, hyphen, asterisk)

    message = ""
    # メインの変換処理
    if not main_kana and main_joshi and not asterisk:
        result = main_joshi
        message = "助詞"
    elif verb and not left_kana and right_kana and not left_extra_sound:
        result = verb
        message = "動詞略語(*省略)"
    elif asterisk:
        if verb:
            result = verb
            message = "動詞略語"
        elif main_kana in ABSTRACT_ABBREVIATIONS_MAP:
            result = ABSTRACT_ABBREVIATIONS_MAP[main_kana]
            result += (main_joshi.replace("や" + COMMA, "です" + DOT).replace("や", "です"))
            message = "一般略語"
        elif main_kana[-1] in ['い', 'き', 'し', 'ち', 'に', 'ひ', 'み', 'り', 'ぎ', 'じ', 'ぢ', 'び', 'ぴ', 'ぃ'] and main_base[-1] == 'ん':
            result = (main_base + 'ぐ')
            message = "特殊略語：～ing"
        else:
            message = "かな+助詞"
            result = main_kana
            result += (main_joshi.replace("や" + COMMA, "である").replace("や", "だ")) if main_joshi else "です"
    elif right_particle_stroke not in ["","n"] and (left_conso_stroke or left_vowel_stroke) and not right_conso_stroke and not right_vowel_stroke:
        message = "左かな+助詞(*省略)"
        result = left_kana + left_extra_sound + joshi("", right_particle_stroke)
    else:
        message = "通常出力"
        result = main_base * (2 if hyphen == "#" else 1)

    # タイピングゲーム時の変換処理
    if is_typing_mode:
        translated_result = kana_to_typing_output(result, typing_mode)
        result = translated_result

    print("|\t" + stroke + "\t|\t" + result + "\t|\t" + message + "\t|\t" + ("on" if is_typing_mode else "off") + "\t|")

    # 結果の出力(両端に{^ ^}をつけることで、英語の自動スペースを防ぐ)
    return "{^" + result + "^}"

# Optional: return an array of stroke tuples that would translate back
# to <text> (an empty array if not possible).
def reverse_lookup(text):
    result = ""
    string = kana_to_typing_output(text, 0) # ローマ字に変換してから解析
    conso_stroke = next((stroke for roma, stroke in conso_stroke_to_roma if roma == string), None)
    if text == "きき":
        return [("KI-KI", ), ("KInk-", ), ("KI-", "KI-")]
    
    return []