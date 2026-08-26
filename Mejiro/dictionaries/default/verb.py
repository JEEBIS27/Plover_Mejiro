from Mejiro.dictionaries.default.settings import DOT, COMMA
from Mejiro.dictionaries.default.func import get_conso
from Mejiro.dictionaries.default.abbreviations import VERB_KAMI_MAP, VERB_SIMO_MAP, VERB_GODAN_MAP

CONJUGATE_GODAN_MAP = { # (五段活用限定)
    #行: [0.ない形, 1.否定形（～ず）, 2.使役形, 3.受身形, 4.ます形, 5.辞書形, 6.て・た形, 7.意向形, 8.仮定形, 9.可能形]
    'k': ['か', 'か', 'か', 'か', 'き', 'く', 'い', 'こう', 'け', 'け'],
    'g': ['が', 'が', 'が', 'が', 'ぎ', 'ぐ', 'い', 'ごう', 'げ', 'げ'],
    's': ['さ', 'さ', 'さ', 'さ', 'し', 'す', 'し', 'そう', 'せ', 'せ'],
    't': ['た', 'た', 'た', 'た', 'ち', 'つ', 'っ', 'とう', 'て', 'て'],
    'n': ['な', 'な', 'な', 'な', 'に', 'ぬ', 'ん', 'のう', 'ね', 'ね'],
    'b': ['ば', 'ば', 'ば', 'ば', 'び', 'ぶ', 'ん', 'ぼう', 'べ', 'べ'],
    'm': ['ま', 'ま', 'ま', 'ま', 'み', 'む', 'ん', 'もう', 'め', 'め'],
    'r': ['ら', 'ら', 'ら', 'ら', 'り', 'る', 'っ', 'ろう', 'れ', 'れ'],
    'w': ['わ', 'わ', 'わ', 'わ', 'い', 'う', 'っ', 'おう', 'え', 'え'],
}
CONJUGATE_KAMI_MAP = { # (上一段活用限定)
    #行: [0.ない形, 1.否定形（～ず）, 2.使役形, 3.受身形, 4.ます形, 5.辞書形, 6.て・た形, 7.意向形, 8.仮定形, 9.可能形]
    'k': ['き', 'き', 'きさ', 'きら', 'き', 'きる', 'き', 'きよう', 'きれ', 'きれ', 'きろ'],
    'g': ['ぎ', 'ぎ', 'ぎさ', 'ぎら', 'ぎ', 'ぎる', 'ぎ', 'ぎよう', 'ぎれ', 'ぎれ', 'ぎろ'],
    'z': ['じ', 'じ', 'じさ', 'じら', 'じ', 'じる', 'じ', 'じよう', 'じれ', 'じれ', 'じろ'],
    't': ['ち', 'ち', 'ちさ', 'ちら', 'ち', 'ちる', 'ち', 'ちよう', 'ちれ', 'ちれ', 'ちろ'],
    'n': ['に', 'に', 'にさ', 'にら', 'に', 'にる', 'に', 'によう', 'にれ', 'にれ', 'にろ'],
    'b': ['び', 'び', 'びさ', 'びら', 'び', 'びる', 'び', 'びよう', 'びれ', 'びれ', 'びろ'],
    'm': ['み', 'み', 'みさ', 'みら', 'み', 'みる', 'み', 'みよう', 'みれ', 'みれ', 'みろ'],
    'r': ['り', 'り', 'りさ', 'りら', 'り', 'りる', 'り', 'りよう', 'りれ', 'りれ', 'りろ'],
    'w': ['い', 'い', 'いさ', 'いら', 'い', 'いる', 'い', 'いよう', 'いれ', 'いれ', 'いろ'],
}
CONJUGATE_SIMO_MAP = { # (下一段活用限定)
    #行: [0.ない形, 1.否定形（～ず）, 2.使役形, 3.受身形, 4.ます形, 5.辞書形, 6.て・た形, 7.意向形, 8.仮定形, 9.可能形]
    'k': ['け', 'け', 'けさ', 'けら', 'け', 'ける', 'け', 'けよう', 'けれ', 'けれ', 'けろ'],
    'g': ['げ', 'げ', 'げさ', 'げら', 'げ', 'げる', 'げ', 'げよう', 'げれ', 'げれ', 'げろ'],
    's': ['せ', 'せ', 'せさ', 'せら', 'せ', 'せる', 'せ', 'せよう', 'せれ', 'せれ', 'せろ'],
    'z': ['ぜ', 'ぜ', 'ぜさ', 'ぜら', 'ぜ', 'ぜる', 'ぜ', 'ぜよう', 'ぜれ', 'ぜれ', 'ぜろ'],
    't': ['て', 'て', 'てさ', 'てら', 'て', 'てる', 'て', 'てよう', 'てれ', 'てれ', 'てろ'],
    'd': ['で', 'で', 'でさ', 'でら', 'で', 'でる', 'で', 'でよう', 'でれ', 'でれ', 'でろ'],
    'n': ['ね', 'ね', 'ねさ', 'ねら', 'ね', 'ねる', 'ね', 'ねよう', 'ねれ', 'ねれ', 'ねろ'],
    'h': ['へ', 'へ', 'へさ', 'へら', 'へ', 'へる', 'へ', 'へよう', 'へれ', 'へれ', 'へろ'],
    'b': ['べ', 'べ', 'べさ', 'べら', 'べ', 'べる', 'べ', 'べよう', 'べれ', 'べれ', 'べろ'],
    'm': ['め', 'め', 'めさ', 'めら', 'め', 'める', 'め', 'めよう', 'めれ', 'めれ', 'めろ'],
    'r': ['れ', 'れ', 'れさ', 'れら', 'れ', 'れる', 'れ', 'れよう', 'れれ', 'れれ', 'れろ'],
    'w': ['え', 'え', 'えさ', 'えら', 'え', 'える', 'え', 'えよう', 'えれ', 'えれ', 'えろ'],
}
CONJUGATE_MAP = {
    '五': CONJUGATE_GODAN_MAP,
    '上': CONJUGATE_KAMI_MAP,
    '下': CONJUGATE_SIMO_MAP,
}
SAHEN_LIST =  ['し',   'せ',   'さ',   'さ',   'し',   'する', 'し',   'しよう', 'すれ', 'でき',   'しろ'] # "*"
KAHEN_LIST =  ['こ',   'こ',   'こさ', 'こら', 'き',   'くる', 'き',   'こよう', 'くれ', 'これ',   'こい'] # "K-*"
IKU_LIST =    ['いか', 'いか', 'いか', 'いか', 'いき', 'いく', 'いっ', 'いこう', 'いけ', 'いけ',   'いけ'] # "I-K*"
ARU_LIST =    ['',     'あら', 'あら', 'あら', 'あり', 'ある', 'あっ', 'あろう', 'あれ', 'ありえ', 'あれ'] # "A-ST"

# 文語調の活用
AUXILIARY_VERB_LEFT_MAP = { # ストローク: [活用形, 補助動詞の語幹, 活用段, 活用行]
    'n' : [6, "て", '上', 'w'], # ～ている
    't' : [2, ""  , '下', 's'], # ～させる
    'k' : [3, ""  , '下', 'r'], # ～られる
    'nk': [6, "てしま", '五', 'w'], # ～てしまう
}
AUXILIARY_VERB_RIGHT_MAP = { # ストローク: [活用形, 助動詞]
    ''   : [5, ""],
    'n'  : [0, "ない"],
    't'  : [6, "た"],
    'k'  : [4, "ます"],
    'nt' : [0, "なかった"],
    'nk' : [4, "ません"],
    'tk' : [4, "ました"],
    'ntk': [6, "て"],
}
AUXILIARY_VERB_EXCEPTION_MAP = { # 例外
    'nt-'    : [4, "やすい"], # ～やすい
    'nt-k'   : [4, "やすく"], # ～やすく
    'nt-n'   : [4, "にくい"], # ～にくい
    'nt-nk'  : [4, "にくく"], # ～にくく
    'nt-t'   : [4, "たい"], # ～たい
    'nt-tk'  : [4, "たく"], # ～たく
    'nt-nt'  : [6, "てほしい"], # ～てほしい
    'nt-ntk' : [6, "てください"], # ～てください
    'tk-'    : [9, "る"], # 可能
    'tk-n'   : [9, "ない"], # 可能+否定
    'tk-t'   : [9, "た"], # 可能+過去
    'tk-k'   : [9, "ます"], # 可能+丁寧
    'tk-nt'  : [9, "なかった"], # 可能+否定+過去
    'tk-nk'  : [9, "ません"], # 可能+否定+丁寧
    'tk-tk'  : [9, "ました"], # 可能+過去+丁寧
    'tk-ntk' : [9, "て"], # 可能+て
    'ntk-'   : [4, ""], # 連用
    'ntk-n'  : [1, "ず"], # 否定
    'ntk-t'  : [8, "ば"], # 仮定
    'ntk-k'  : [4, "ましょう"], # 提案
    'ntk-nt' : [0, "なければ"], # 否定+仮定
    'ntk-nk' : [0, "なく"], # 否定+連用
    'ntk-tk' : [4, "ながら"], # ～ながら
    'ntk-ntk'  : [7, ""], # 意向
}
DESU_CONJUGATE_MAP = { # ですの活用形
    '':"です",
    'n':"ですね",
    't':"でした",
    'k':"でしょう",
    'nt':"です" + DOT,
    'nk':"ですが" + COMMA,
    'tk':"ですか?",
    'ntk':"でして" + COMMA,
}

def stroke_to_conjugate(left_particle_stroke: str, right_particle_stroke: str) -> list:
    auxiliary_list = [None, ""]
    if left_particle_stroke + '-' + right_particle_stroke in AUXILIARY_VERB_EXCEPTION_MAP:
        auxiliary_list = AUXILIARY_VERB_EXCEPTION_MAP[left_particle_stroke + '-' + right_particle_stroke]
    elif left_particle_stroke:
        auxiliary_list[0] = AUXILIARY_VERB_LEFT_MAP[left_particle_stroke][0]
        auxiliary_list[1] = AUXILIARY_VERB_LEFT_MAP[left_particle_stroke][1]
        auxiliary_list[1] += CONJUGATE_MAP[AUXILIARY_VERB_LEFT_MAP[left_particle_stroke][2]][AUXILIARY_VERB_LEFT_MAP[left_particle_stroke][3]][AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][0]]
        auxiliary_list[1] += AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][1]
    else:
        auxiliary_list[0] = AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][0]
        auxiliary_list[1] = AUXILIARY_VERB_RIGHT_MAP[right_particle_stroke][1]
    return auxiliary_list

def translate_ta_te_form(string: str, auxiliary: int, conso: str) -> str:
    if auxiliary == 6 and conso in ['g', 'n', 'b', 'm']:
        if conso == 'g':
            if string.startswith("いて"):
                string = "いで" + string[2:]
            elif string.startswith("いた"):
                string = "いだ" + string[2:]
        else:  # n, b, m
            if string.startswith("んて"):
                string = "んで" + string[2:]
            elif string.startswith("んた"):
                string = "んだ" + string[2:]
    return string

def stroke_to_verb(left_kana, left_syllable, right_kana, stroke_list) -> str:
    left_conso_stroke, left_vowel_stroke, left_particle_stroke, right_conso_stroke, right_vowel_stroke, right_particle_stroke, asterisk = stroke_list[0], stroke_list[1], stroke_list[2], stroke_list[4], stroke_list[5], stroke_list[6], stroke_list[7]
    main_kana = left_kana + right_kana
    kana_stroke = left_conso_stroke + left_vowel_stroke + '-' + right_conso_stroke + right_vowel_stroke

    right_conso = get_conso(right_conso_stroke)

    output = ""

    # 活用を取得
    auxiliary_list = stroke_to_conjugate(left_particle_stroke, right_particle_stroke)

    # ～です
    if right_conso_stroke == 'TN' and right_vowel_stroke == '':
        output = left_syllable + DESU_CONJUGATE_MAP[right_particle_stroke]
    # 行く
    elif kana_stroke == "I-K":
        output += IKU_LIST[auxiliary_list[0]] + auxiliary_list[1]
    # ある
    elif kana_stroke == "A-ST":
        output += ARU_LIST[auxiliary_list[0]] + auxiliary_list[1]
    # カ変活用
    elif kana_stroke == "K-":
        output += KAHEN_LIST[auxiliary_list[0]] + auxiliary_list[1]
    # 上一段活用
    elif not left_kana and not left_particle_stroke and right_vowel_stroke == "I" and right_conso in ['k', 'g', 'z', 't', 'n', 'b', 'm', 'r', 'w', '']:
        if right_conso == '':
            right_conso = 'w'
        output = CONJUGATE_KAMI_MAP[right_conso][auxiliary_list[0]] + auxiliary_list[1]
    # 下一段活用
    elif not left_kana and not left_particle_stroke and right_vowel_stroke == "IA" and right_conso in ['k', 'g', 's', 'z', 't', 'd', 'n', 'h', 'b', 'm', 'r', 'w', '']:
        if right_conso == '':
            right_conso = 'w'
        output = CONJUGATE_SIMO_MAP[right_conso][auxiliary_list[0]] + auxiliary_list[1]
    # 五段活用
    elif right_vowel_stroke == "" and right_conso in ['k', 'g', 's', 't', 'n', 'b', 'm', 'r', 'w']:
        output = left_kana + translate_ta_te_form(CONJUGATE_GODAN_MAP[right_conso][auxiliary_list[0]] + auxiliary_list[1], auxiliary_list[0], right_conso)
    elif asterisk:
        # 登録された五段活用
        if kana_stroke in VERB_GODAN_MAP:
            verb_list = VERB_GODAN_MAP[kana_stroke]
            output = verb_list[0] + translate_ta_te_form(CONJUGATE_GODAN_MAP[verb_list[1]][auxiliary_list[0]] + auxiliary_list[1], auxiliary_list[0], verb_list[1])
            output = output.replace("くださり", "ください")
        # 登録された上一段活用
        elif kana_stroke in VERB_KAMI_MAP:
            verb_list = VERB_KAMI_MAP[kana_stroke]
            output = verb_list[0] + CONJUGATE_KAMI_MAP[verb_list[1]][auxiliary_list[0]] + auxiliary_list[1]
        # 登録された下一段活用
        elif kana_stroke in VERB_SIMO_MAP:
            verb_list = VERB_SIMO_MAP[kana_stroke]
            output = verb_list[0] + CONJUGATE_SIMO_MAP[verb_list[1]][auxiliary_list[0]] + auxiliary_list[1]
        # ～いう
        elif right_vowel_stroke == 'IU' and not right_conso_stroke:
            output = left_kana + "い" + CONJUGATE_GODAN_MAP['w'][auxiliary_list[0]] + auxiliary_list[1]
        # サ変活用
        elif not right_kana:
            output = main_kana + SAHEN_LIST[auxiliary_list[0]] + auxiliary_list[1]
        # 上一段活用
        elif right_vowel_stroke == "I" and right_conso in ['k', 'g', 'z', 't', 'n', 'b', 'm', 'r', 'w', '']:
            if right_conso == '':
                right_conso = 'w'
            output = left_kana + CONJUGATE_KAMI_MAP[right_conso][auxiliary_list[0]] + auxiliary_list[1]
        # 下一段活用
        elif right_vowel_stroke == "IA" and right_conso in ['k', 'g', 's', 'z', 't', 'd', 'n', 'h', 'b', 'm', 'r', 'w', '']:
            if right_conso == '':
                right_conso = 'w'
            output = left_kana + CONJUGATE_SIMO_MAP[right_conso][auxiliary_list[0]] + auxiliary_list[1]
        # 「～る」動詞(五段活用)
        else:
            output = main_kana + CONJUGATE_GODAN_MAP['r'][auxiliary_list[0]] + auxiliary_list[1]
            output = output.replace("ござり", "ござい")
            output = output.replace("なさり", "なさい")
    return output
