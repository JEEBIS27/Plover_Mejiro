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
from Mejiro.dictionaries.default.settings import (exception_particle, henkan_command, ABSTRACT_ABBREVIATIONS_MAP)
from Mejiro.dictionaries.default.func import (stroke_to_kana, extra_sound, joshi)
from Mejiro.dictionaries.default.verb import stroke_to_verb

LONGEST_KEY = 1
LAST_VOWEL_STROKE = "A"
is_found_exception = [False, False]

def lookup(key):
    global LONGEST_KEY
    global LAST_VOWEL_STROKE
    global is_found_exception
    assert len(key) <= LONGEST_KEY
    stroke = key[0]

    if stroke == "#":
        print("key error*")
        raise KeyError
    
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

    print("LeftConsonant\tLeftVowel\tLeftParticle\tHyphen")
    print(left_conso_stroke + "\t\t" + left_vowel_stroke + "\t\t" + left_particle_stroke + "\t\t" + hyphen)

    print("RightConsonant\tRightVowel\tRightParticle\tAsterisk")
    print(right_conso_stroke + "\t\t" + right_vowel_stroke + "\t\t" + right_particle_stroke + "\t\t" + asterisk)

    print(stroke)

    is_found_exception = [False, False] # 初期化
    result = "" # 初期化
    # 左右のかなを変数に格納
    left_kana = stroke_to_kana(left_conso_stroke, left_vowel_stroke, left_particle_stroke)
    right_kana = stroke_to_kana(right_conso_stroke, right_vowel_stroke, right_particle_stroke)
    main_kana = left_kana + right_kana
    # 左右の追加音を変数に格納
    left_extra_sound = ("" if left_vowel_stroke + left_particle_stroke in exception_particle else extra_sound(left_particle_stroke))
    right_extra_sound = ("" if right_vowel_stroke + right_particle_stroke in exception_particle else extra_sound(right_particle_stroke))
    # 基本形を変数に格納
    main_base = (left_kana + left_extra_sound + right_kana + right_extra_sound)
    # 主要助詞を変数に格納
    main_joshi = joshi(left_particle_stroke, right_particle_stroke)
    # 動詞変換処理
    verb = stroke_to_verb(left_conso_stroke + left_vowel_stroke + '-' + right_conso_stroke + right_vowel_stroke, left_particle_stroke, right_particle_stroke, asterisk)

    # メインの変換処理
    if not main_kana and main_joshi and not asterisk:
        result = main_joshi
        print("助詞")
    elif verb and not left_kana and right_kana and not left_extra_sound:
        result = verb * (2 if hyphen == "#" else 1)
        print("動詞")
    elif asterisk:
        if verb:
            result = verb * (2 if hyphen == "#" else 1)
        elif main_kana in ABSTRACT_ABBREVIATIONS_MAP:
            result = ABSTRACT_ABBREVIATIONS_MAP[main_kana] * (2 if hyphen == "#" else 1)
            result += (main_joshi.replace("ー", "です").replace("ん", "です。" + henkan_command))
            print("略語「" + result + "」")
        elif main_kana[-1] in ['い', 'き', 'し', 'ち', 'に', 'ひ', 'み', 'り', 'ぎ', 'じ', 'ぢ', 'び', 'ぴ', 'ぃ'] and main_base[-1] == 'ん':
            result = (main_base + 'ぐ') * (2 if hyphen == "#" else 1)
            print("～ing")
        elif main_base[-1] == 'し':
            result = main_base + 'て'
            print("～して")
        elif main_base[-1] == 'ま':
            result = main_base + 'す'
            print("～ます")
        else:
            result = main_kana * (2 if hyphen == "#" else 1)
            result += (main_joshi.replace("ー", "です").replace("ん", "です。" + henkan_command)) if main_joshi else "する"
            print(main_kana + "(" + stroke + ")の略語は登録されていません")
            
    elif right_particle_stroke not in ["","n"] and (left_conso_stroke or left_vowel_stroke) and not right_conso_stroke and not right_vowel_stroke:
        result = left_kana + left_extra_sound + joshi("", right_particle_stroke)
        print("左+助詞")
    else:
        result = main_base * (2 if hyphen == "#" else 1)

    # 結果の出力(両端に{^ ^}をつけることで、英語の自動スペースを防ぐ)
    print("{^" + result + "^}")
    return "{^" + result + "^}"
