from Mejiro.dictionaries.default.settings import (DIPHTHONG_MAPPING, COMPLEX_DIPHTHONG_MAPPING, exception_particle,
                                                  conso_stroke_to_roma, vowel_stroke_to_roma, ROMA_TO_KANA_MAP,
                                                  PARTICLE_KEY_LIST, SECOND_SOUND_LIST,
                                                  L_PARTICLE, R_PARTICLE,
                                                  COMMA, henkan_command, EXCEPTION_STROKE_MAP)

def stroke_to_kana(conso_stroke: str, vowel_stroke: str, particle_stroke: str) -> str:
    
    global LAST_VOWEL_STROKE
    global conso_stroke_to_roma
    global vowel_stroke_to_roma
    global DIPHTHONG_MAPPING
    global COMPLEX_DIPHTHONG_MAPPING
    global ROMA_TO_KANA_MAP
    global PARTICLE_KEY_LIST
    global SECOND_SOUND_LIST

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
        extra_sound = ""  # 追加音はなし
    # b. 基本の二重母音マッピングをチェック
    elif current_vowel_stroke in DIPHTHONG_MAPPING:
        vowel_roma, suffix = DIPHTHONG_MAPPING[current_vowel_stroke]
        vowel_index = [item[1] for item in vowel_stroke_to_roma].index(vowel_roma)
        # 辞書から直接対応する文字列を取得。
        extra_sound = SECOND_SOUND_LIST[PARTICLE_KEY_LIST.index(particle_stroke)]
    # c. それ以外の場合、基本母音ストロークから取得
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
    except IndexError:
        print(f"無効な組み合わせ: 子音'{conso_roma}' + 母音'{vowel_roma}'")
        raise KeyError

    if conso_stroke + vowel_stroke == "":
        return '', '', '', ''  # 両方空の場合は空文字を返す
    else:
        # 5. 長音文字を付加して返す
        return base_kana + suffix, extra_sound, conso_roma, vowel_roma
    
def joshi(left_particle_stroke: str, right_particle_stroke: str) -> str:
    global exception_particle
    global EXCEPTION_STROKE_MAP
    global L_PARTICLE
    global R_PARTICLE
    global henkan_command
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
        elif right_particle_stroke in ["k", "nk"] and left_joshi:
            joshi = "の" + left_joshi
            if "n" in right_particle_stroke:
                joshi += COMMA
        else:
            joshi = left_joshi + right_joshi
            if "n" in right_particle_stroke :
                joshi += COMMA
    return joshi
