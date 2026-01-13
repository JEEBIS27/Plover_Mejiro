import re
from Mejiro.dictionaries.default.settings import (DIPHTHONG_MAPPING, COMPLEX_DIPHTHONG_MAPPING, EXCEPTION_KANA_MAP,
                                                  conso_stroke_to_roma, vowel_stroke_to_roma, ROMA_TO_KANA_MAP,
                                                  PARTICLE_KEY_LIST, SECOND_SOUND_LIST,
                                                  L_PARTICLE, R_PARTICLE,
                                                  COMMA, EXCEPTION_STROKE_MAP)
from Mejiro.dictionaries.default.abbreviations import ABSTRACT_MAP, ABSTRACT_MAP_LEFT, ABSTRACT_MAP_RIGHT

global LAST_VOWEL_STROKE
LAST_VOWEL_STROKE = ''

def stroke_to_kana(conso_stroke: str, vowel_stroke: str, particle_stroke: str, asterisk: str) -> str:
    
    global LAST_VOWEL_STROKE
    global conso_stroke_to_roma
    global vowel_stroke_to_roma
    global DIPHTHONG_MAPPING
    global COMPLEX_DIPHTHONG_MAPPING
    global ROMA_TO_KANA_MAP
    global PARTICLE_KEY_LIST
    global SECOND_SOUND_LIST
    global is_first_input

    if not LAST_VOWEL_STROKE:
        LAST_VOWEL_STROKE = "A"
    # 母音ストロークの決定と更新
    if not vowel_stroke:
        current_vowel_stroke = LAST_VOWEL_STROKE
    else:
        current_vowel_stroke = vowel_stroke
        LAST_VOWEL_STROKE = vowel_stroke

    if conso_stroke + vowel_stroke + particle_stroke == "":
        return ['', '', '', '']  # すべてのストロークが空の場合、空文字を返す
    elif conso_stroke + vowel_stroke == "":
        extra_sound = SECOND_SOUND_LIST[PARTICLE_KEY_LIST.index(particle_stroke)]
        return ['', extra_sound, '', '']  # 子音と母音が空の場合、空文字と追加音を返す
    elif conso_stroke + vowel_stroke in EXCEPTION_KANA_MAP and not asterisk and current_vowel_stroke + particle_stroke not in COMPLEX_DIPHTHONG_MAPPING: # 例外的なかなのマッピングをチェック
        base_kana = EXCEPTION_KANA_MAP[conso_stroke + vowel_stroke]
        extra_sound = SECOND_SOUND_LIST[PARTICLE_KEY_LIST.index(particle_stroke)]
        return [base_kana, extra_sound, '', '']
    else:
        # 子音ストロークからローマ字の子音（行）を取得
        conso_roma = next((roma for stroke, roma in conso_stroke_to_roma if conso_stroke == stroke), None)
        if conso_roma is None:
            print(f"子音ストローク '{conso_stroke}' が見つかりません")
            raise KeyError

        # 母音ストロークからローマ字の基本母音（段）と長音文字を決定
        
        vowel_roma = None
        suffix = "" # 長音文字

        # 英語フラグをリセット
        is_english = False

        # 英語母音マッピングをチェック
        if not asterisk and current_vowel_stroke + particle_stroke in COMPLEX_DIPHTHONG_MAPPING:
            vowel_roma, suffix = COMPLEX_DIPHTHONG_MAPPING[current_vowel_stroke + particle_stroke]
            vowel_index = [item[1] for item in vowel_stroke_to_roma].index(vowel_roma)
            extra_sound = ""  # 追加音はなし
            is_english = True # 英語モードフラグを立てる
        # 基本の二重母音マッピングをチェック
        elif current_vowel_stroke in DIPHTHONG_MAPPING:
            vowel_roma, suffix = DIPHTHONG_MAPPING[current_vowel_stroke]
            vowel_index = [item[1] for item in vowel_stroke_to_roma].index(vowel_roma)
            # 辞書から直接対応する文字列を取得。
            extra_sound = SECOND_SOUND_LIST[PARTICLE_KEY_LIST.index(particle_stroke)]
        # それ以外の場合、基本母音ストロークから取得
        else:
            vowel_tuple = next(((i, roma) for i, (stroke, roma) in enumerate(vowel_stroke_to_roma) if current_vowel_stroke == stroke), None)
            if vowel_tuple is not None:
                vowel_index, vowel_roma = vowel_tuple
            suffix = "" # 基本母音には長音文字なし
            # 辞書から直接対応する文字列を取得。
            extra_sound = SECOND_SOUND_LIST[PARTICLE_KEY_LIST.index(particle_stroke)]
            
        if vowel_roma is None:
            print(f"母音ストローク '{current_vowel_stroke}' が見つかりません")
            raise KeyError

        try:
            base_kana = ROMA_TO_KANA_MAP[conso_roma][vowel_index]
            if is_english:
                base_kana = base_kana.replace('ち', 'てぃ').replace('ぢ', 'でぃ')
        except IndexError:
            print(f"無効な組み合わせ: 子音'{conso_roma}' + 母音'{vowel_roma}'")
            raise KeyError

        # [CV, C, C, V]
        return [base_kana + suffix, extra_sound, conso_roma, vowel_roma]
    
def joshi(left_particle_stroke: str, right_particle_stroke: str) -> str:
    global exception_particle
    global EXCEPTION_STROKE_MAP
    global L_PARTICLE
    global R_PARTICLE
    # ストロークを直接置換するため、'ｰ'をつける。
    particle_stroke = left_particle_stroke + '-' + right_particle_stroke
    if particle_stroke in EXCEPTION_STROKE_MAP:
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
            joshi = right_joshi + COMMA
        elif right_particle_stroke in ["k", "nk"] and left_particle_stroke not in ["", "k", "ntk"]:
            joshi = "の" + left_joshi
            if "n" in right_particle_stroke:
                joshi += COMMA
        else:
            joshi = left_joshi + right_joshi
            if "n" in right_particle_stroke :
                joshi += COMMA
    return joshi

def abstract_abbreviation_lookup(left_kana_stroke: str, right_kana_stroke: str) -> str:
    if left_kana_stroke + '-' + right_kana_stroke in ABSTRACT_MAP:
        output = ABSTRACT_MAP[left_kana_stroke + '-' + right_kana_stroke]
    elif left_kana_stroke in ABSTRACT_MAP_LEFT and right_kana_stroke in ABSTRACT_MAP_RIGHT:
        output = ABSTRACT_MAP_LEFT[left_kana_stroke] + ABSTRACT_MAP_RIGHT[right_kana_stroke]
    else:
        output = ""
    return output