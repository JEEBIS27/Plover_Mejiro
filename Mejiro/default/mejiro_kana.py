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
from Mejiro.dictionaries.default.settings import (DIPHTHONG_MAPPING, COMPLEX_DIPHTHONG_MAPPING, exception_particle,
                                                  conso_stroke_to_roma, vowel_stroke_to_roma,
                                                  ROMA_TO_KANA_MAP, VOWEL_INDEX_MAP,
                                                  PARTICLE_KEY_LIST, SECOND_SOUND_LIST,
                                                  L_PARTICLE, R_PARTICLE,
                                                  henkan_command, EXCEPTION_STROKE_MAP)

LONGEST_KEY = 1
LAST_VOWEL_STROKE = "A"

def lookup(key):
    assert len(key) <= LONGEST_KEY
    stroke = key[0]

    if stroke == "#":
        print("key error*")
        raise KeyError

    regex = re.compile(r"(S?T?K?N?)(Y?I?A?U?)(n?t?k?)(\-?#?)(S?T?K?N?)(Y?I?A?U?)(n?t?k?)(\*?)")
    regex_groups = re.search(regex, stroke)

    LeftConsonant = regex_groups.group(1)
    LeftVowel = regex_groups.group(2)
    LeftParticle = regex_groups.group(3)
    Hyphen = regex_groups.group(4)
    RightConsonant = regex_groups.group(5)
    RightVowel = regex_groups.group(6)
    RightParticle = regex_groups.group(7)
    Asterisk = regex_groups.group(8)

    Fingers = LeftConsonant + LeftVowel + RightConsonant + RightVowel + Asterisk

    print("LeftConsonant\tLeftVowel\tLeftParticle\tHyphen")
    print(LeftConsonant + "\t\t" + LeftVowel + "\t\t" + LeftParticle + "\t\t" + Hyphen)

    print("RightConsonant\tRightVowel\tRightParticle\tAsterisk")
    print(RightConsonant + "\t\t" + RightVowel + "\t\t" + RightParticle + "\t\t" + Asterisk)

    print(stroke)

    global LAST_VOWEL_STROKE

    # --- 関数内のロジック変更 ---

    def stroke_to_kana(Consonant_stroke: str, Vowel_stroke: str, Particle_stroke: str) -> str:
        
        global LAST_VOWEL_STROKE 

        # 1. 母音ストロークの決定と更新
        if not Vowel_stroke:
            if not LAST_VOWEL_STROKE:
                LAST_VOWEL_STROKE = "A"
            current_vowel_stroke = LAST_VOWEL_STROKE
        else:
            current_vowel_stroke = Vowel_stroke
            LAST_VOWEL_STROKE = Vowel_stroke 
            
        # 2. 子音ストロークからローマ字の子音（行）を取得
        conso_roma = next((roma for stroke, roma in conso_stroke_to_roma if Consonant_stroke == stroke), None)
        if conso_roma is None:
            print(f"子音ストローク '{Consonant_stroke}' が見つかりません")
            raise KeyError

        # 3. 母音ストロークからローマ字の基本母音（段）と長音文字を決定
        
        vowel_roma = None
        suffix = "" # 長音文字
        
        # a. 二重母音マッピングをチェック (優先)
        if current_vowel_stroke + Particle_stroke in COMPLEX_DIPHTHONG_MAPPING:
            vowel_roma, suffix = COMPLEX_DIPHTHONG_MAPPING[current_vowel_stroke + Particle_stroke]
        # b. 基本母音マッピングをチェック
        elif current_vowel_stroke in DIPHTHONG_MAPPING:
            vowel_roma, suffix = DIPHTHONG_MAPPING[current_vowel_stroke]
        else:
            vowel_roma = next((roma for stroke, roma in vowel_stroke_to_roma if current_vowel_stroke == stroke), None)
            suffix = "" # 基本母音には長音文字なし
            
        if vowel_roma is None:
            print(f"母音ストローク '{current_vowel_stroke}' が見つかりません")
            raise KeyError

        # 4. ひらがなを特定
        if conso_roma not in ROMA_TO_KANA_MAP or vowel_roma not in VOWEL_INDEX_MAP:
            print(f"対応するひらがなの行または段が見つかりません")
            raise KeyError

        vowel_index = VOWEL_INDEX_MAP[vowel_roma]
        
        try:
            base_kana = ROMA_TO_KANA_MAP[conso_roma][vowel_index]
        except IndexError:
            print(f"無効な組み合わせ: 子音'{conso_roma}' + 母音'{vowel_roma}'")
            raise KeyError
        
        if Consonant_stroke + Vowel_stroke == "":
            return ""  # 両方空の場合は空文字を返す
        else:
            # 5. 長音文字を付加して返す
            return base_kana + suffix

    def second_sound(vowel_stroke: str, particle_stroke: str) -> str:
        # 辞書から直接対応する文字列を取得。キーが存在しない場合は空文字列を返す。
        if vowel_stroke + particle_stroke in exception_particle:
            return ""
        else:
            return SECOND_SOUND_LIST[PARTICLE_KEY_LIST.index(particle_stroke)]

    def joshi(LeftParticle: str, RightParticle: str) -> str:
        # ストロークを直接置換するため、'ｰ'をつける。
        joshi = EXCEPTION_STROKE_MAP.get(LeftParticle + '-' + RightParticle,False)
        if joshi:
            return joshi
        else:
            # RightParticleをn以外に分割
            RightParticle_tk = RightParticle.split("n",1)[-1]
            # PARTICLE_KEY_LIST (外部定数) からインデックスを取得
            l_index = PARTICLE_KEY_LIST.index(LeftParticle)
            r_index = PARTICLE_KEY_LIST.index(RightParticle_tk)
            # L_PARTICLE/R_PARTICLE (外部定数) をインデックスで参照
            left_joshi = L_PARTICLE[l_index]
            right_joshi = R_PARTICLE[r_index]
            if LeftParticle == "n":
                joshi = right_joshi + ',' + henkan_command
            elif RightParticle in ["k","nk"] and left_joshi not in ["の","と",""]:
                joshi = "の" + left_joshi
                if "n" in RightParticle:
                    joshi += ',' + henkan_command
            else:
                joshi = left_joshi + right_joshi
                if "n" in RightParticle:
                    joshi += ',' + henkan_command
            return joshi
    
    # メインの変換処理
    if not Fingers:
        result = joshi(LeftParticle, RightParticle)
    else:
        result = (stroke_to_kana(LeftConsonant, LeftVowel, LeftParticle) + second_sound(LeftVowel, LeftParticle)
                + stroke_to_kana(RightConsonant, RightVowel, RightParticle))

    # 左の音があって、右の音がないかつ、右の助詞がある場合
    if RightParticle not in ["","n"] and (LeftConsonant or LeftVowel) and not RightConsonant and not RightVowel and not Asterisk:
        result += joshi("", RightParticle)
    elif Fingers:  # 何かしらのキーが押されている場合
        result += second_sound(RightVowel, RightParticle)
        # ～ingの処理
        if Asterisk and result[-1] == "ん" and result[-2] in ["い","き","し","ち","に","ひ","み","り","ぎ","じ","ぢ","び","ぴ","ぃ"]:
            result += "ぐ"

    # ハイフンがある場合、結果を二回繰り返す
    if Fingers and Hyphen == "#":
        result *= 2

    # 結果の出力(両端に{^ ^}をつけることで、英語の自動スペースを防ぐ)
    print("{^" + result + "^}")
    return "{^" + result + "^}"