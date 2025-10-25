from Mejiro.dictionaries.default.settings import COMMA, DOT
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
    "-K": ["", 'k'],# ～く
    "-KA": ["", 'k'],# ～く
    "-KN": ["", 'g'],# ～ぐ
    "-KNA": ["", 'g'],# ～ぐ
    "-S": ["", 's'],# ～す
    "-SA": ["", 's'],# ～す
    "-T": ["", 't'],# ～つ
    "-TA": ["", 't'],# ～つ
    "-N": ["", 'n'],# ～ぬ
    "-NA": ["", 'n'],# ～ぬ
    "-TKN": ["", 'b'],# ～ぶ
    "-TKNA": ["", 'b'],# ～ぶ
    "-SKN": ["", 'm'],# ～む
    "-SKNA": ["", 'm'],# ～む
    "-ST": ["", 'r'],# ～る
    "-STA": ["", 'r'],# ～る
    "-SK": ["", 'w'],# ～う
    "-ASK": ["", 'w'],# ～う
    "-TN": ["で", 's'],# です
    "-SKNA": ["ま", 's'],# ます
    "I-K": ["い", 'k'],# 行く
    "AU-K": ["お", 'k'],# 置く
    "KA-K": ["か", 'k'],# 書く
    "KI-KNA": ["きがつ", 'k'],# 気が付く
    "KI-TNU": ["きづ", 'k'],# 気付く
    "TA-T": ["たた", 'k'],# 叩く
    "TU-K": ["つ", 'k'],# 付く
    "NA-K": ["な", 'k'],# 泣く
    "TKA-T": ["はたら", 'k'],# 働く
    "TKI-K": ["ひ", 'k'],# 引く
    "I-SAU": ["いそ", 'g'],# 急ぐ
    "KA-S": ["かか", 's'],# 欠かす
    "TKA-N": ["はな", 's'],# 話す
    "SKNIA-S": ["め", 's'],# 召す
    "TA-T": ["た", 't'],# 立つ
    "SI-N": ["し", 'n'],# 死ぬ
    "SKNA-N": ["まな", 'b'],# 学ぶ
    "TKA-S": ["はさ", 'm'],# 挟む
    "TKU-K": ["ふく", 'm'],# 吹く
    "A-": ["あ", 'r'],# 有る
    "A-KN": ["あが", 'r'],# 上がる
    "I-ST": ["い", 'r'],# 要る
    "-YA": ["や", 'r'],# やる
    "KNA-TKN": ["がんば", 'r'],# 頑張る
    "SI-ST": ["し", 'r'],# 知る
    "SI-SKNA": ["しま", 'r'],# 閉まる
    "NA-ST": ["な", 'r'],# 成る
    "TKY-ST": ["はい", 'r'],# 入る
    "TKI-KA": ["ひか", 'r'],# 光る
    "SKA-K": ["わか", 'r'],# 分かる
    "-A": ["あ", 'w'],# 会う
    "I-": ["い", 'w'],# 言う
    "AU-SKN": ["おも", 'w'],# 思う
    "SI-SKNIAU": ["しま", 'w'],# 仕舞う
    "TU-KA": ["つか", 'w'],# 使う
    "TAU-SKN": ["ともな", 'w'],# 伴う
    "SKNAU-STA": ["もら", 'w'],# 貰う
}
VERB_KAMI_MAP = { # ストローク: [語幹, 行]
    "-KI": ["", 'k'],# ～きる
    "-KNI": ["", 'g'],# ～ぎる
    "-SI": ["", 's'],# ～しる
    "-TI": ["", 't'],# ～ちる
    "-NI": ["", 'n'],# ～にる
    "-TKNI": ["", 'b'],# ～びる
    "-SKNI": ["", 'm'],# ～みる
    "-STI": ["", 'r'],# ～りる
    "-I": ["", 'w'],# ～いる
    "I-KI": ["い", 'k'],# 生きる
    "AU-KI": ["お", 'k'],# 起きる
    "TNIA-KI": ["で", 'k'],# 出来る
    "AU-TI": ["お", 't'],# 落ちる
    "KA-SNI": ["かん", 'z'],# 感じる
    "KIAU-SNI": ["こう", 'z'],# 講じる
    "SIY-SNI": ["しょう", 'z'],# 生じる
    "SI-SNI": ["しん", 'z'],# 信じる
    "SIAU-SNI": ["そう", 'z'],# 総じる
    "TIAU-SNI": ["とう", 'z'],# 投じる
}
VERB_SIMO_MAP = { # ストローク: [語幹, 行]
    "-KIA": ["", 'k'],# ～ける
    "-KNIA": ["", 'g'],# ～げる
    "-SIA": ["", 's'],# ～せる
    "-TIA": ["", 't'],# ～てる
    "-TNIA": ["", 'd'],# ～でる
    "-NIA": ["", 'n'],# ～ねる
    "-TKNIA": ["", 'b'],# ～べる
    "-SKNIA": ["", 'm'],# ～める
    "-STIA": ["", 'r'],# ～れる
    "-IA": ["", 'w'],# ～える
    "TU-TN": ["つづ", 'k'],# 続ける
    "KA-IA": ["かえ", 'k'],# 変える
    "KAU-KNIA": ["こ", 'g'],# 焦げる
    "TKA-SNI": ["はじ", 'm'],# 始める
    "KA-KN": ["かんが", 'w'],# 考える
    "KI-IA": ["き", 'w'],# 消える
    "SA-S": ["ささ", 'w'],# 支える
}
# 文語調の活用
AUXILIARY_VERB_LEFT_MAP = { # ストローク: [活用形, 助動詞]
    "": [[None, ""], [None, ""]],
    "n": [[3, "てい"], [3, "て"]],
    "t": [[0, "せ"], [3, "てみ"]],
    "k": [[0, "れ"], [5, "れ"]],
    "nt": [[0, "せていただ"], [0, "せて"]],
    "nk": [[0, "れてい"], [5, "れて"]],
    "tk": [[0, "せられ"], [0, "せれ"]],
}
AUXILIARY_VERB_RIGHT_MAP = { # ストローク: [活用形, 助動詞]
    "": [[2, ""], [1, ""]],
    "n": [[0, "ない"], [0, "ん"]],
    "t": [[3, "た"], [3, "たら"]],
    "k": [[1, "ます"], [4, "う"]],
    "nk": [[1, "ません"], [3, "てほしい"]],
    "nt": [[0, "なかった"], [0, "なかったら"]],
    "tk": [[1, "ました"], [1, "ましたら"]],
    "ntk": [[3, "て"], [1, "まして"]],
}
AUXILIARY_VERB_EXCEPTION_MAP = { # 左がntkのときの例外処理
    "": [[3, "て" + COMMA], [2, DOT]],
    "n": [[1, "ながら"], [0, "ぬ"]],
    "t": [[5, "ば"], [1, "つつ"]],
    "k": [[1, "ましょう"], [1, "かた"]],
    "nt": [[0, "なければ"], [2, "ので"]],
    "nk": [[2, "ことができる"], [0, "なかった"]],
    "tk": [[2, "ことができます"], [1, "ますか"]],
    "ntk": [[3, "てください"], [1, "ませんか"]],
}
def stroke_to_verb(left_kana_stroke, right_kana_stroke, left_particle_stroke, right_particle_stroke, main_kana, hyphen, asterisk):
    kana_stroke = left_kana_stroke + '-' + right_kana_stroke
    print(f"動詞変換処理: '{kana_stroke}' + '{left_particle_stroke}' + '{right_particle_stroke}' + '{main_kana}' + '{asterisk}'")
    auxiliary_list = [None, ""]
    hash_num = 1 if hyphen == "#" else 0
    if left_particle_stroke == "ntk":
        auxiliary_list = AUXILIARY_VERB_EXCEPTION_MAP[right_particle_stroke][hash_num]
        print(f"例外処理: {auxiliary_list}")
    else:
        auxiliary_list[0] = AUXILIARY_VERB_LEFT_MAP[left_particle_stroke][hash_num][0] if left_particle_stroke else AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][hash_num][0]
        auxiliary_list[1] = AUXILIARY_VERB_LEFT_MAP[left_particle_stroke][hash_num][1]
        if hyphen != "#" and left_particle_stroke == "nt": # させていただk
            auxiliary_list[1] += CONJUGATE_GODAN_MAP['k'][AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][hash_num][0]]
        if left_particle_stroke:
            auxiliary_list[1] += AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][0][1]
            if (left_particle_stroke != "nt" or hyphen == "#") and not right_particle_stroke:
                auxiliary_list[1] += "る"
        else:
            auxiliary_list[1] += AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][hash_num][1]
    print(f"活用形: {auxiliary_list}")

    if kana_stroke in VERB_GODAN_MAP:
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
    elif not right_kana_stroke:
        print("サ行変格活用")
        output = main_kana + SAHEN_LIST[auxiliary_list[0]] + auxiliary_list[1]
        output = output.replace("しせ", "させ").replace("しれ", "され")
    else:
        """print("～る(造語動詞)")
        output = main_kana + CONJUGATE_GODAN_MAP['r'][auxiliary_list[0]]
        output += auxiliary_list[1]
        """
        print("この動詞は登録されていません")
        output = None
    print(f"動詞: '{output}'")
    return output
