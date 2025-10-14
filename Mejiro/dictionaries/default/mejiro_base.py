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
from Mejiro.dictionaries.default.settings import (DIPHTHONG_MAPPING, COMPLEX_DIPHTHONG_MAPPING,
                                                  conso_stroke_to_roma, vowel_stroke_to_roma, ROMA_TO_KANA_MAP,
                                                  PARTICLE_KEY_LIST, SECOND_SOUND_LIST,
                                                  L_PARTICLE, R_PARTICLE,
                                                  henkan_command, EXCEPTION_STROKE_MAP,
                                                  ABSTRACT_ABBREVIATIONS_MAP)

LONGEST_KEY = 1
LAST_VOWEL_STROKE = "A"
is_found_exception = []

def lookup(key):
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

    # --- 関数内のロジック変更 ---

    def stroke_to_kana(conso_stroke: str, vowel_stroke: str, particle_stroke: str) -> str:
        
        global LAST_VOWEL_STROKE
        global is_found_exception

        # 1. 母音ストロークの決定と更新
        if not vowel_stroke:
            if not LAST_VOWEL_STROKE:
                LAST_VOWEL_STROKE = "A"
            current_vowel_stroke = LAST_VOWEL_STROKE
        else:
            current_vowel_stroke = vowel_stroke
            LAST_VOWEL_STROKE = vowel_stroke

        # 2. 子音ストロークからローマ字の子音（行）を取得
        conso_roma = next((roma for stroke, roma in conso_stroke_to_roma if conso_stroke == stroke), None)
        if conso_roma is None:
            print(f"子音ストローク '{conso_stroke}' が見つかりません")
            raise KeyError

        # 3. 母音ストロークからローマ字の基本母音（段）と長音文字を決定
        
        vowel_roma = None
        suffix = "" # 長音文字

        # a. 特殊な二重母音マッピングをチェック
        if current_vowel_stroke + particle_stroke in COMPLEX_DIPHTHONG_MAPPING:
            vowel_roma, suffix = COMPLEX_DIPHTHONG_MAPPING[current_vowel_stroke + particle_stroke]
            vowel_index = [item[1] for item in vowel_stroke_to_roma].index(vowel_roma)
            is_found_exception = [True, is_found_exception[0]] # 例外フラグを右向きに更新
        # b. 基本の二重母音マッピングをチェック
        elif current_vowel_stroke in DIPHTHONG_MAPPING:
            vowel_roma, suffix = DIPHTHONG_MAPPING[current_vowel_stroke]
            vowel_index = [item[1] for item in vowel_stroke_to_roma].index(vowel_roma)
            is_found_exception = [False, is_found_exception[0]] # 例外フラグを右向きに更新
        # c. それ以外の場合、基本母音ストロークから取得
        else:
            vowel_tuple = next(((i, roma) for i, (stroke, roma) in enumerate(vowel_stroke_to_roma) if current_vowel_stroke == stroke), None)
            if vowel_tuple is not None:
                vowel_index, vowel_roma = vowel_tuple
            suffix = "" # 基本母音には長音文字なし
            is_found_exception = [False, is_found_exception[0]] # 例外フラグを右向きに更新
            
        if vowel_roma is None:
            print(f"母音ストローク '{current_vowel_stroke}' が見つかりません")
            raise KeyError

        try:
            base_kana = ROMA_TO_KANA_MAP[conso_roma][vowel_index]
        except IndexError:
            print(f"無効な組み合わせ: 子音'{conso_roma}' + 母音'{vowel_roma}'")
            raise KeyError

        if conso_stroke + vowel_stroke == "":
            return ""  # 両方空の場合は空文字を返す
        else:
            # 5. 長音文字を付加して返す
            return base_kana + suffix

    def extra_sound(particle_stroke: str) -> str:
        # 辞書から直接対応する文字列を取得。
        return SECOND_SOUND_LIST[PARTICLE_KEY_LIST.index(particle_stroke)]

    def joshi(left_particle_stroke: str, right_particle_stroke: str) -> str:
        # ストロークを直接置換するため、'ｰ'をつける。
        particle_stroke = left_particle_stroke + '-' + right_particle_stroke
        if particle_stroke in EXCEPTION_STROKE_MAP:
            print("例外助詞")
            joshi = EXCEPTION_STROKE_MAP[particle_stroke]
        else:
            # right_particle_strokeからnを取り除く
            right_particle_tk = right_particle_stroke.split("n", 1)[-1]
            # PARTICLE_KEY_LISTからインデックスを取得
            l_index = PARTICLE_KEY_LIST.index(left_particle_stroke)
            r_index = PARTICLE_KEY_LIST.index(right_particle_tk)
            # L_PARTICLE/R_PARTICLEをインデックスで参照
            left_joshi = L_PARTICLE[l_index]
            right_joshi = R_PARTICLE[r_index]
            if left_particle_stroke == "n":
                joshi = right_joshi + '、' + henkan_command
            elif right_particle_stroke in ["k", "nk"] and left_joshi not in ["", "の", "と"]:
                joshi = "の" + left_joshi
                if "n" in right_particle_stroke:
                    joshi += '、' + henkan_command
            else:
                joshi = left_joshi + right_joshi
                if "n" in right_particle_stroke :
                    joshi += '、' + henkan_command
        return joshi

    global is_found_exception
    is_found_exception = [False, False] # 初期化
    result = "" # 初期化

    # 左右のかなを変数に格納
    left_kana = stroke_to_kana(left_conso_stroke, left_vowel_stroke, left_particle_stroke)
    right_kana = stroke_to_kana(right_conso_stroke, right_vowel_stroke, right_particle_stroke)
    main_kana = left_kana + right_kana
    print("main_kana: " + str(main_kana))
    # 左右の追加音を変数に格納
    left_extra_sound = "" if is_found_exception[0] else extra_sound(left_particle_stroke)
    right_extra_sound = "" if is_found_exception[1] else extra_sound(right_particle_stroke)
    # 基本形を変数に格納
    main_base = left_kana + left_extra_sound + right_kana + right_extra_sound
    print("main_base: " + str(main_base))
    # 主要助詞を変数に格納
    main_joshi = joshi(left_particle_stroke, right_particle_stroke)
    print("main_joshi: " + str(main_joshi))

    # メインの変換処理
    if not main_kana and main_joshi:
        result = main_joshi
        print("助詞")
    elif asterisk:
        if main_kana in ABSTRACT_ABBREVIATIONS_MAP or not main_kana:
            result = ABSTRACT_ABBREVIATIONS_MAP[main_kana] * (2 if hyphen == "#" else 1)
            result += (main_joshi.replace("ー", "です").replace("ん", "です。" + henkan_command))
            print("略語「" + result + "」")
        elif main_kana[-1] in ['い', 'き', 'し', 'ち', 'に', 'ひ', 'み', 'り', 'ぎ', 'じ', 'ぢ', 'び', 'ぴ', 'ぃ'] and main_base[-1] == 'ん':
            result = (main_base + 'ぐ') * (2 if hyphen == "#" else 1)
            print("～ing")
        elif main_base[-1] == 'し':
            result = main_base + 'て'
            print("～して")
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