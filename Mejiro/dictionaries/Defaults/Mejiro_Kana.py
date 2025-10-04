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
#Mejiro Kana
import re

LONGEST_KEY = 1

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

    LAST_VOWEL_STROKE = "A"  # 初期値として'A'を設定

    # Key: ストローク, Value: (基本母音ローマ字, 長音文字)
    # YIAU
    DIPHTHONG_MAPPING = {
        "Y": ("a", "い"),
        "YI": ("yo", "う"),
        "YIA": ("e", "い"),
        "YIU": ("yu", "う"),
        "YIAU": ("u", "う"),
        "IU": ("u", "い"),
        "IAU": ("o", "う"),
    }

    # ストローク（子音・母音）からローマ字の行段アルファベットへの対応表
    # STKN
    conso_stroke_to_roma = [
        ["", ''], ["S", 's'], ["T", 't'], ["K", 'k'], ["N", 'n'], 
        ["ST", 'r'], ["SK", 'm'], ["TK", 'h'],
        ["SN", 'z'], ["TN", 'd'], ["KN", 'g'], ["TKN", 'b'],
        ["STK", 'p'], ["STN", 'f'], ["SKN", 'w'], ["STKN", 'l']
    ]

    # 基本母音ストロークの定義 (二重母音は除外)
    # ストローク -> 基本母音 (a, i, u, e, o, ya, yu, yo)
    vowel_stroke_to_roma = [
        ['A', 'a'], ['I', 'i'], ['U', 'u'], ['IA', 'e'], ['AU', 'o'],
        ["YA", 'ya'], ["YU", 'yu'], ["YAU", 'yo']
    ]

    # 行段のアルファベットからひらがなへのマッピング (変更なし)
    ROMA_TO_KANA_MAP = {
        '':  ['あ', 'い', 'う', 'え', 'お', 'や', 'ゆ', 'よ'],
        'k': ['か', 'き', 'く', 'け', 'こ', 'きゃ', 'きゅ', 'きょ'],
        's': ['さ', 'し', 'す', 'せ', 'そ', 'しゃ', 'しゅ', 'しょ'],
        't': ['た', 'ち', 'つ', 'て', 'と', 'ちゃ', 'ちゅ', 'ちょ'],
        'n': ['な', 'に', 'ぬ', 'ね', 'の', 'にゃ', 'にゅ', 'にょ'],
        'h': ['は', 'ひ', 'ふ', 'へ', 'ほ', 'ひゃ', 'ひゅ', 'ひょ'],
        'm': ['ま', 'み', 'む', 'め', 'も', 'みゃ', 'みゅ', 'みょ'],
        'r': ['ら', 'り', 'る', 'れ', 'ろ', 'りゃ', 'りゅ', 'りょ'],
        'w': ['わ', 'うぃ', 'ゔ', 'うぇ', 'を', 'やあ', 'いう', 'いぇ'],
        'g': ['が', 'ぎ', 'ぐ', 'げ', 'ご', 'ぎゃ', 'ぎゅ', 'ぎょ'],
        'z': ['ざ', 'じ', 'ず', 'ぜ', 'ぞ', 'じゃ', 'じゅ', 'じょ'],
        'd': ['だ', 'ぢ', 'づ', 'で', 'ど', 'でぃ', 'てぃ', 'どぅ'],
        'b': ['ば', 'び', 'ぶ', 'べ', 'ぼ', 'びゃ', 'びゅ', 'びょ'],
        'p': ['ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ', 'ぴゃ', 'ぴゅ', 'ぴょ'],
        'f': ['ふぁ', 'ふぃ', 'ふ', 'ふぇ', 'ふぉ', 'じぇ', 'しぇ', 'ちぇ'],
        'l': ['ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'ゃ', 'ゅ', 'ょ']
    }

    # 母音のローマ字と対応するインデックス（段）のマッピング (変更なし)
    VOWEL_INDEX_MAP = {
        'a': 0, 'i': 1, 'u': 2, 'e': 3, 'o': 4,
        'ya': 5, 'yu': 6, 'yo': 7
    }

    # --- 関数内のロジック変更 ---

    def stroke_to_kana(Consonant_stroke: str, Vowel_stroke: str) -> str:
        
        global LAST_VOWEL_STROKE 

        # 1. 母音ストロークの決定と更新
        if not Vowel_stroke:
            if not LAST_VOWEL_STROKE:
                print("key error no last vowel")
                raise KeyError
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
        if current_vowel_stroke in DIPHTHONG_MAPPING:
            vowel_roma, suffix = DIPHTHONG_MAPPING[current_vowel_stroke]
        # b. 基本母音マッピングをチェック
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

    PARTICLE_MAP = {
        "": "", "n": "ん", "t": "つ", "k": "く", 
        "tk": "っ", "nt": "ち", "nk": "き", "ntk": "ー"
    }

    def second_sound(particle_stroke: str) -> str:
        # 辞書から直接対応する文字列を取得。キーが存在しない場合は空文字列を返す。
        return PARTICLE_MAP.get(particle_stroke, "")
    LIST_PARTICLE_KEYS = ["", "n", "t", "k", "tk", "nt", "nk", "ntk"] 

    # 左側の助詞文字列のリスト
    L_PARTICLE = ["", "、", "に", "の", "で", "と", "を", "か"]

    # 右側の助詞文字列のリスト
    R_PARTICLE = ["", "、", "は", "が", "も", "は、", "が、", "も、"]

    # 助詞の置換ルール { 助詞in: 助詞out }
    JOSHI_IN_MAP = {
        "は、": ".", "が、": ",", "も、": "ー",  
        "、は": "は、", "、が": "が、", "、も": "も、", 
        "、は、": "!", "、が、": "?", "、も、": "ん",
        "にが": "のに", "にが、": "のに、", 
        "でが": "ので", "でが、": "ので、",
        "かが": "のか", "かが、": "のか、",
        "をが": "のを", "をが、": "のを、"
    }

    def joshi(LeftParticle: str, RightParticle: str) -> str:
        # 1. 左右の助詞キーからインデックスを取得
        try:
            # LIST_PARTICLE_KEYS (外部定数) からインデックスを取得
            l_index = LIST_PARTICLE_KEYS.index(LeftParticle)
            r_index = LIST_PARTICLE_KEYS.index(RightParticle)
        except ValueError:
            # LeftParticleやRightParticleが定義されたキーに含まれない場合、空文字列を返す
            return ""

        # 2. 左右の助詞文字列を生成
        # L_PARTICLE/R_PARTICLE (外部定数) をインデックスで参照
        left_joshi = L_PARTICLE[l_index]
        right_joshi = R_PARTICLE[r_index]
        generated_joshi = left_joshi + right_joshi
        
        # 3. 助詞の置換ルールを適用 (JOSHI_IN_MAPを参照)
        # .get() を使用し、キーが存在しない場合は生成した助詞をそのまま返す
        # 例: "のが" -> "のが" (置換なし), "は、" -> "." (置換あり)
        return JOSHI_IN_MAP.get(generated_joshi, generated_joshi)

    # メインの変換処理
    result = (stroke_to_kana(LeftConsonant, LeftVowel) + second_sound(LeftParticle)
          + stroke_to_kana(RightConsonant, RightVowel) + second_sound(RightParticle))

    if Asterisk and result[-1] == "ん" and result[-2] in ["い", "き","し","ち","に","ひ","み","り","ぎ","じ","ぢ","び","ぴ","ぃ"]:
        result += "ぐ"

    if Fingers and Hyphen == "#":
        result *= 2
    
    if not Fingers:
        result = joshi(LeftParticle, RightParticle)
    print("{^" + result + "^}")
    return "{^" + result + "^}"