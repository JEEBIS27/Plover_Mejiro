CONJUGATE_GODAN_MAP = { # (五段活用限定)
    #行: [ない形, ます形, 辞書形, て・た形, 意向形, 仮定形, 命令形]
    'k': ['か', 'き', 'く', 'い', 'こ', 'け', 'けろ'],
    'g': ['が', 'ぎ', 'ぐ', 'い', 'ご', 'げ', 'げろ'],
    's': ['さ', 'し', 'す', 'し', 'そ', 'せ', 'せろ'],
    't': ['た', 'ち', 'つ', 'っ', 'と', 'て', 'てろ'],
    'n': ['な', 'に', 'ぬ', 'ん', 'の', 'ね', 'ねろ'],
    'b': ['ば', 'び', 'ぶ', 'ん', 'ぼ', 'べ', 'べろ'],
    'm': ['ま', 'み', 'む', 'ん', 'も', 'め', 'めろ'],
    'r': ['ら', 'り', 'る', 'っ', 'ろ', 'れ', 'れろ'],
    'w': ['わ', 'い', 'う', 'っ', 'お', 'え', 'えろ'],
}
CONJUGATE_KAMI_MAP = { # (上一段活用限定)
    #行: [ない形, ます形, 辞書形, て・た形, 意向形, 仮定形, 命令形]
    'k': ['き', 'き', 'きる', 'き', 'きよ', 'きれ', 'きろ'],
    'g': ['ぎ', 'ぎ', 'ぎる', 'ぎ', 'ぎよ', 'ぎれ', 'ぎろ'],
    'z': ['じ', 'じ', 'じる', 'じ', 'じよ', 'じれ', 'じろ'],
    't': ['ち', 'ち', 'ちる', 'ち', 'ちよ', 'ちれ', 'ちろ'],
    'n': ['に', 'に', 'にる', 'に', 'によ', 'にれ', 'にろ'],
    'b': ['び', 'び', 'びる', 'び', 'びよ', 'びれ', 'びろ'],
    'm': ['み', 'み', 'みる', 'み', 'みよ', 'みれ', 'みろ'],
    'r': ['り', 'り', 'りる', 'り', 'りよ', 'りれ', 'りろ'],
    'w': ['い', 'い', 'いる', 'い', 'いよ', 'いれ', 'いろ'],
}
CONJUGATE_SIMO_MAP = { # (下一段活用限定)
    #行: [ない形, ます形, 辞書形, て・た形, 意向形, 仮定形, 命令形]
    'k': ['け', 'け', 'ける', 'け', 'けよ', 'けれ', 'けろ'],
    'g': ['げ', 'げ', 'げる', 'げ', 'げよ', 'げれ', 'げろ'],
    's': ['せ', 'せ', 'せる', 'せ', 'せよ', 'せれ', 'せろ'],
    'z': ['ぜ', 'ぜ', 'ぜる', 'ぜ', 'ぜよ', 'ぜれ', 'ぜろ'],
    't': ['て', 'て', 'てる', 'て', 'てよ', 'てれ', 'てろ'],
    'd': ['で', 'で', 'でる', 'で', 'でよ', 'でれ', 'でろ'],
    'n': ['ね', 'ね', 'ねる', 'ね', 'ねよ', 'ねれ', 'ねろ'],
    'h': ['へ', 'へ', 'へる', 'へ', 'へよ', 'へれ', 'へろ'],
    'b': ['べ', 'べ', 'べる', 'べ', 'べよ', 'べれ', 'べろ'],
    'm': ['め', 'め', 'める', 'め', 'めよ', 'めれ', 'めろ'],
    'r': ['れ', 'れ', 'れる', 'れ', 'れよ', 'れれ', 'れろ'],
    'w': ['え', 'え', 'える', 'え', 'えよ', 'えれ', 'えろ'],
}
SAHEN_LIST = ['し', 'し', 'する', 'し', 'しよ', 'すれ', 'しろ']
VERB_GODAN_MAP = { # ストローク: [語幹, 行]
    "-KA": ["", 'k'],
    "-KNA": ["", 'g'],
    "-SA": ["", 's'],
    "-TA": ["", 't'],
    "-NA": ["", 'n'],
    "-TKNA": ["", 'b'],
    "-SKNA": ["", 'm'],
    "-STA": ["", 'r'],
    "-A": ["", 'w'],
    "TN-S": ["で", 's'],
    "SKN-S": ["ま", 's'],
    "TA-T": ["たた", 'k'],
    "TU-K": ["つ", 'k'],
    "KI-KNA": ["きがつ", 'k'],
    "KI-TNU": ["きづ", 'k'],
    "I-SAU": ["いそ", 'g'],
    "KA-K": ["かか", 's'],
    "TKA-N": ["はな", 's'],
    "SI-N": ["し", 'n'],
    "SKNA-N": ["まな", 'b'],
    "TKA-S": ["はさ", 'm'],
    "TKU-K": ["ふく", 'm'],
    "I-ST": ["い", 'r'],
    "KNA-TKN": ["がんば", 'r'],
    "SI-ST": ["し", 'r'],
    "SI-SKNA": ["しま", 'w'],
    "TAU-SKN": ["ともな", 'w'],
    "NA-ST": ["な", 'r'],
    "SKA-K": ["わか", 'r'],
    "AU-SKN": ["おも", 'w'],
    "SI-SKNIAU": ["しま", 'w'],
}
VERB_KAMI_MAP = { # ストローク: [語幹, 行]
    "-KI": ["", 'k'],
    "-KNI": ["", 'g'],
    "-SI": ["", 's'],
    "-TI": ["", 't'],
    "-NI": ["", 'n'],
    "-TKNI": ["", 'b'],
    "-SKNI": ["", 'm'],
    "-STI": ["", 'r'],
    "-I": ["", 'w'],
    "I-K": ["い", 'k'],
    "TNIA-KI": ["で", 'k'],
    "AU-TI": ["お", 't'],
    "KA-SNI": ["かん", 'z'],
}
VERB_SIMO_MAP = { # ストローク: [語幹, 行]
    "-KIA": ["", 'k'],
    "-KNIA": ["", 'g'],
    "-SIA": ["", 's'],
    "-TIA": ["", 't'],
    "-NIA": ["", 'n'],
    "-TKNIA": ["", 'b'],
    "-SKNIA": ["", 'm'],
    "-STIA": ["", 'r'],
    "-IA": ["", 'w'],
    "SA-S": ["ささ", 'w'],
    "KA-KN": ["かんが", 'w'],
}
AUXILIARY_VERB_LEFT_MAP = { # ストローク: [活用形, 助動詞]
    "": [None, ""],
    "n": [3, "てい"],
    "t": [0, "せ"],
    "k": [0, "れ"],
    "nt": [0, "せてい"],
    "nk": [0, "れてい"],
    "tk": [0, "せられ"],
}
AUXILIARY_VERB_RIGHT_MAP = { # ストローク: [活用形, 助動詞]
    "": [2, ""],
    "n": [0, "ない"],
    "t": [3, "た"],
    "k": [1, "ます"],
    "nk": [1, "ません"],
    "nt": [0, "なかった"],
    "tk": [1, "ました"],
    "ntk": [1, ""],
}
AUXILIARY_VERB_EXCEPTION_MAP = { # 左がntkのときの例外処理
    "": [3, "て"],
    "n": [0, "ん"],
    "t": [4, "う"],
    "k": [5, ""],
    "nt": [6, ""],
    "nk": [5, "ない"],
    "tk": [1, "ましょう"],
    "ntk": [1, "まして"],
}
def stroke_to_verb(kana_stroke, left_particle_stroke, right_particle_stroke, asterisk):
    print(f"動詞変換処理: '{kana_stroke}' + '{left_particle_stroke}' + '{right_particle_stroke}' + '{asterisk}'")
    auxiliary_list = [None, ""]
    if left_particle_stroke == "ntk":
        auxiliary_list = AUXILIARY_VERB_EXCEPTION_MAP[right_particle_stroke]
        print(f"例外処理: {auxiliary_list}")
    else:
        auxiliary_list[0] = AUXILIARY_VERB_LEFT_MAP[left_particle_stroke][0] if left_particle_stroke else AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][0]
        auxiliary_list[1] = AUXILIARY_VERB_LEFT_MAP[left_particle_stroke][1] + AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][1]
        if left_particle_stroke and not right_particle_stroke:
            auxiliary_list[1] += "る"

    if kana_stroke == '-' and asterisk: # 例外処理：「-＊」は「する」
        print("サ行変格活用")
        output = SAHEN_LIST[auxiliary_list[0]] + auxiliary_list[1]
        output = output.replace("しせ", "させ").replace("しれ", "され")
    elif kana_stroke in VERB_GODAN_MAP:
        print("五段活用")
        verb_list = VERB_GODAN_MAP[kana_stroke]
        output = verb_list[0] + CONJUGATE_GODAN_MAP[verb_list[1]][auxiliary_list[0]]
        output += auxiliary_list[1].replace("て", "で").replace("た", "だ") if verb_list[1] in ['g', 'n', 'b', 'm'] and auxiliary_list[0] == 3 else auxiliary_list[1]
    elif kana_stroke in VERB_KAMI_MAP:
        print("上一段活用")
        verb_list = VERB_KAMI_MAP[kana_stroke]
        output = verb_list[0] + CONJUGATE_KAMI_MAP[verb_list[1]][auxiliary_list[0]]
        if left_particle_stroke != "ntk" and ('t' in left_particle_stroke or 'k' in left_particle_stroke):
            output += "さ" if 't' in left_particle_stroke else "ら"
        output += auxiliary_list[1]
    elif kana_stroke in VERB_SIMO_MAP:
        print("下一段活用")
        verb_list = VERB_SIMO_MAP[kana_stroke]
        output = verb_list[0] + CONJUGATE_SIMO_MAP[verb_list[1]][auxiliary_list[0]]
        if left_particle_stroke != "ntk" and ('t' in left_particle_stroke or 'k' in left_particle_stroke):
            output += "さ" if 't' in left_particle_stroke else "ら"
        output += auxiliary_list[1]
    else:
        print(f"動詞ストローク '{kana_stroke}' が見つかりません")
        output = None
    print(f"動詞: '{output}'")
    return output
