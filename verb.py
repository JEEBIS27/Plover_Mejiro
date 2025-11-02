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
SAHEN_LIST = ['し', 'し', 'する', 'し', 'しよ', 'すれ', 'しろ'] # "*"
KAHEN_LIST = ['こ', 'き', 'くる', 'き', 'こよ', 'くれ', 'こい'] # "K-", "-KAU"
VERB_GODAN_MAP = { # ストローク: [語幹, 行]
    "SI-SU": ["しめ", 's'],# 示す
    "-TN": ["で", 's'],# です
    "TA-TNA": ["いただ", 'k'],# 頂く
    "KI-TU": ["きがつ", 'k'],# 気が付く
    "KI-TNU": ["きづ", 'k'],# 気付く
    "TA-TA": ["たた", 'k'],# 叩く
    "TKA-TA": ["はたら", 'k'],# 働く
    "I-SAU": ["いそ", 'g'],# 急ぐ
    "I-KA": ["いか", 's'],# 活かす
    "AU-TAU": ["おと", 's'],# 落とす
    "KA-KA": ["かか", 's'],# 欠かす
    "TKA-NA": ["はな", 's'],# 話す
    "SKNI-NA": ["みな", 's'],# 見なす
    "SKNA-NA": ["まな", 'b'],# 学ぶ
    "TKA-SA": ["はさ", 'm'],# 挟む
    "TKU-KU": ["ふく", 'm'],# 吹く
    "A-": ["あ", 'r'],# ある
    "A-KNA": ["あが", 'r'],# 上がる
    "A-TA": ["あた", 'r'],# 当る
    "AU-SKA": ["おわ", 'r'],# 終わる
    "KA-SKA": ["かわ", 'r'],# 変わる
    "KNA-TKNA": ["がんば", 'r'],# 頑張る
    "SI-SKNA": ["しま", 'r'],# 閉まる
    "TU-SKNAU": ["つも", 'r'],# 積もる
    "TAU-AU": ["とお", 'r'],# 通る
    "NA-": ["な", 'r'],# なる
    "TKA-KA": ["はか", 'r'],# 計る
    "TKA-TKIA": ["はべ", 'r'],# 侍る
    "TKI-KA": ["ひか", 'r'],# 光る
    "YA-": ["や", 'r'],# やる
    "-YA": ["や", 'r'],# やる
    "SKA-KA": ["わか", 'r'],# 分かる
    "SKA-TA": ["わた", 'r'],# 渡る
    "-A": ["あ", 'w'],# 会う
    "I-": ["い", 'w'],# 言う
    "AU-SKNAU": ["おも", 'w'],# 思う
    "SI-SKNIAU": ["しま", 'w'],# 仕舞う
    "TU-KA": ["つか", 'w'],# 使う
    "TAU-SKNAU": ["ともな", 'w'],# 伴う
    "SKNA-TAU": ["まと", 'w'],# 纏う
    "SKNAU-STA": ["もら", 'w'],# 貰う
    "TKA-STA": ["はら", 'w'],# 払う
    "SKA-STA": ["わら", 'w'],# 笑う
}
VERB_KAMI_MAP = { # ストローク: [語幹, 行]
    "SI-SNI": ["しん", 'z'],# 信じる
    "KA-SNI": ["かん", 'z'],# 感じる
    "KI-SNI": ["きん", 'z'],# 禁じる
    "TNA-SNI": ["だん", 'z'],# 断じる
    "KA-SKNI": ["かんが", 'm'],# 鑑みる
}
VERB_SIMO_MAP = { # ストローク: [語幹, 行]
    "TU-TN": ["つづ", 'k'],# 続ける
    "TKA-SNI": ["はじ", 'm'],# 始める
    "SKNAU-TAU": ["もと", 'm'],# 求める
    "KA-KNA": ["かんが", 'w'],# 考える
    "SA-SA": ["ささ", 'w'],# 支える
}
# 文語調の活用
AUXILIARY_VERB_LEFT_MAP = { # ストローク: [活用形, 助動詞]
    "": [[None, ""], [None, ""]],
    "n": [[3, "てい"], [3, "て"]],
    "t": [[0, "せ"], [3, "ちゃ"]],
    "k": [[0, "れ"], [5, ""]],
    "nt": [[0, "せていただ"], [0, "せて"]],
    "nk": [[0, "れてい"], [5, "て"]],
    "tk": [[0, "せられ"], [0, "せれ"]],
}
AUXILIARY_VERB_RIGHT_MAP = { # ストローク: [活用形, 助動詞]
    "": [[2, ""], [3, "て"]],
    "n": [[0, "ない"], [0, "ん"]],
    "t": [[3, "た"], [3, "たら"]],
    "k": [[1, "ます"], [4, "う"]],
    "nt": [[0, "なかった"], [0, "なかったら"]],
    "nk": [[1, "ません"], [3, "てほしい"]],
    "tk": [[1, "ました"], [1, "ましたら"]],
    "ntk": [[1, ""], [1, "まして"]],
}
AUXILIARY_VERB_EXCEPTION_MAP = { # 左がntkのときの例外処理
    "": [[1, "たい"], [2, "ので"]],
    "n": [[1, "ながら"], [0, "ず"]],
    "t": [[5, "ば"], [1, "つつ"]],
    "k": [[1, "ましょう"], [1, "かた"]],
    "nt": [[0, "なければ"], [2, "かどうか"]],
    "nk": [[2, "ために"], [0, "なくても"]],
    "tk": [[2, "こと"], [1, "ますか"]],
    "ntk": [[3, "てください"], [1, "ませんか"]],
}
def stroke_to_verb(kana_stroke, right_conso, right_vowel_stroke, left_particle_stroke, right_particle_stroke, left_kana, right_kana, hyphen, asterisk):
    main_kana = left_kana + right_kana
    print(f"動詞変換処理: '{kana_stroke}' + '{left_particle_stroke}' + '{right_particle_stroke}' + '{main_kana}' + '{hyphen}' + '{asterisk}'")
    auxiliary_list = [None, ""]
    hash_num = 1 if hyphen == "#" else 0
    if left_particle_stroke == "ntk":
        auxiliary_list = AUXILIARY_VERB_EXCEPTION_MAP[right_particle_stroke][hash_num]
        print(f"例外処理: {auxiliary_list}")
    else:
        auxiliary_list[0] = AUXILIARY_VERB_LEFT_MAP[left_particle_stroke][hash_num][0] if left_particle_stroke else AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][hash_num][0]
        auxiliary_list[1] = AUXILIARY_VERB_LEFT_MAP[left_particle_stroke][hash_num][1]
        if hyphen != "#" and left_particle_stroke == "nt": # させていただk
            auxiliary_list[1] += CONJUGATE_GODAN_MAP['k'][AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][0][0]]
        elif hyphen == "#" and left_particle_stroke == "t": # ちゃw
            auxiliary_list[1] += CONJUGATE_GODAN_MAP['w'][AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][0][0]]
        if left_particle_stroke:
            auxiliary_list[1] += AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][0][1]
            if not (hyphen != "#" and left_particle_stroke == "nt" or hyphen == "#" and left_particle_stroke == "t") and not right_particle_stroke:
                auxiliary_list[1] += "る"
        else:
            auxiliary_list[1] += AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][hash_num][1]
    print(f"活用形: {auxiliary_list}")

    if kana_stroke in VERB_GODAN_MAP:
        print("五段活用")
        verb_list = VERB_GODAN_MAP[kana_stroke]
        output = verb_list[0] + CONJUGATE_GODAN_MAP[verb_list[1]][auxiliary_list[0]]
        output += auxiliary_list[1].replace("て", "で").replace("た", "だ") if verb_list[1] in ['g', 'n', 'b', 'm'] and auxiliary_list[0] == 3 else auxiliary_list[1]
        output = output.replace("あらな", "な")
    elif kana_stroke in VERB_KAMI_MAP:
        print("上一段活用")
        verb_list = VERB_KAMI_MAP[kana_stroke]
        output = verb_list[0] + CONJUGATE_KAMI_MAP[verb_list[1]][auxiliary_list[0]]
        if hyphen != "#" and left_particle_stroke != "ntk" and ('t' in left_particle_stroke or 'k' in left_particle_stroke) or hyphen == "#" and left_particle_stroke == "tk":
            output += "さ" if 't' in left_particle_stroke else "ら"
        output += auxiliary_list[1]
    elif kana_stroke in VERB_SIMO_MAP:
        print("下一段活用")
        verb_list = VERB_SIMO_MAP[kana_stroke]
        output = verb_list[0] + CONJUGATE_SIMO_MAP[verb_list[1]][auxiliary_list[0]]
        if hyphen != "#" and left_particle_stroke != "ntk" and ('t' in left_particle_stroke or 'k' in left_particle_stroke) or hyphen == "#" and left_particle_stroke == "tk":
            output += "さ" if 't' in left_particle_stroke else "ら"
        output += auxiliary_list[1]
    elif kana_stroke in ["K-", "-KAU"]:
        print("カ行変格活用")
        output = KAHEN_LIST[auxiliary_list[0]] + auxiliary_list[1]
        if hyphen != "#" and left_particle_stroke != "ntk" and ('t' in left_particle_stroke or 'k' in left_particle_stroke) or hyphen == "#" and left_particle_stroke == "tk":
            output += "さ" if 't' in left_particle_stroke else "ら"
    elif not right_kana:
        print("サ行変格活用")
        output = main_kana + (SAHEN_LIST[auxiliary_list[0]] if (hyphen != "#" or left_particle_stroke not in ['k', 'nk']) else "でき") + auxiliary_list[1]
        output = output.replace("しせ", "させ").replace("しれ", "され").replace("しず", "せず")
    elif right_vowel_stroke == "" and right_conso in ['k', 'g', 's', 't', 'n', 'b', 'm', 'r', 'w']:
        print("五段活用(特殊)")
        output = left_kana + CONJUGATE_GODAN_MAP[right_conso][auxiliary_list[0]]
        output += auxiliary_list[1].replace("て", "で").replace("た", "だ") if right_conso in ['g', 'n', 'b', 'm'] and auxiliary_list[0] == 3 else auxiliary_list[1]
        output = output.replace("あらな", "な")
    elif right_vowel_stroke == "I" and right_conso in ['k', 'g', 'z', 't', 'n', 'b', 'm', 'r', 'w', '']:
        print("上一段活用(特殊)")
        if right_conso == '':
            right_conso = 'w'
        output = left_kana + CONJUGATE_KAMI_MAP[right_conso][auxiliary_list[0]]
        if hyphen != "#" and left_particle_stroke != "ntk" and ('t' in left_particle_stroke or 'k' in left_particle_stroke) or hyphen == "#" and left_particle_stroke == "tk":
            output += "さ" if 't' in left_particle_stroke else "ら"
        output += auxiliary_list[1]
    elif right_vowel_stroke == "IA" and right_conso in ['k', 'g', 's', 'z', 't', 'd', 'n', 'h', 'b', 'm', 'r', 'w', '']:
        print("下一段活用(特殊)")
        if right_conso == '':
            right_conso = 'w'
        output = left_kana + CONJUGATE_SIMO_MAP[right_conso][auxiliary_list[0]]
        if hyphen != "#" and left_particle_stroke != "ntk" and ('t' in left_particle_stroke or 'k' in left_particle_stroke) or hyphen == "#" and left_particle_stroke == "tk":
            output += "さ" if 't' in left_particle_stroke else "ら"
        output += auxiliary_list[1]
    else:
        print("この動詞は登録されていません")
        output = None
    print(f"動詞: '{output}'")
    return output
