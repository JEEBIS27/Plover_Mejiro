from Mejiro.dictionaries.default.settings import COMMA, DOT
from Mejiro.dictionaries.default.abbreviations import VERB_KAMI_MAP, VERB_SIMO_MAP, VERB_GODAN_MAP

CONJUGATE_GODAN_MAP = { # (五段活用限定)
    #行: [0.ない形, 1.使役形, 2.受身形, 3.ます形, 4.辞書形, 5.て・た形, 6.意向形, 7.仮定形, 8.可能形, 9.命令形]
    'k': ['か', 'か', 'か', 'き', 'く', 'い', 'こう', 'け', 'け', 'け'],
    'g': ['が', 'が', 'が', 'ぎ', 'ぐ', 'い', 'ごう', 'げ', 'げ', 'げ'],
    's': ['さ', 'さ', 'さ', 'し', 'す', 'し', 'そう', 'せ', 'せ', 'せ'],
    't': ['た', 'た', 'た', 'ち', 'つ', 'っ', 'とう', 'て', 'て', 'て'],
    'n': ['な', 'な', 'な', 'に', 'ぬ', 'ん', 'のう', 'ね', 'ね', 'ね'],
    'b': ['ば', 'ば', 'ば', 'び', 'ぶ', 'ん', 'ぼう', 'べ', 'べ', 'べ'],
    'm': ['ま', 'ま', 'ま', 'み', 'む', 'ん', 'もう', 'め', 'め', 'め'],
    'r': ['ら', 'ら', 'ら', 'り', 'る', 'っ', 'ろう', 'れ', 'れ', 'れ'],
    'w': ['わ', 'わ', 'わ', 'い', 'う', 'っ', 'おう', 'え', 'え', 'え'],
}
CONJUGATE_KAMI_MAP = { # (上一段活用限定)
    #行: [0.ない形, 1.使役形, 2.受身形, 3.ます形, 4.辞書形, 5.て・た形, 6.意向形, 7.仮定形, 8.可能形, 9.命令形]
    'k': ['き', 'きさ', 'きら', 'き', 'きる', 'き', 'きよう', 'きれ', 'きれ', 'きろ'],
    'g': ['ぎ', 'ぎさ', 'ぎら', 'ぎ', 'ぎる', 'ぎ', 'ぎよう', 'ぎれ', 'ぎれ', 'ぎろ'],
    'z': ['じ', 'じさ', 'じら', 'じ', 'じる', 'じ', 'じよう', 'じれ', 'じれ', 'じろ'],
    't': ['ち', 'ちさ', 'ちら', 'ち', 'ちる', 'ち', 'ちよう', 'ちれ', 'ちれ', 'ちろ'],
    'n': ['に', 'にさ', 'にら', 'に', 'にる', 'に', 'によう', 'にれ', 'にれ', 'にろ'],
    'b': ['び', 'びさ', 'びら', 'び', 'びる', 'び', 'びよう', 'びれ', 'びれ', 'びろ'],
    'm': ['み', 'みさ', 'みら', 'み', 'みる', 'み', 'みよう', 'みれ', 'みれ', 'みろ'],
    'r': ['り', 'りさ', 'りら', 'り', 'りる', 'り', 'りよう', 'りれ', 'りれ', 'りろ'],
    'w': ['い', 'いさ', 'いら', 'い', 'いる', 'い', 'いよう', 'いれ', 'いれ', 'いろ'],
}
CONJUGATE_SIMO_MAP = { # (下一段活用限定)
    #行: [0.ない形, 1.使役形, 2.受身形, 3.ます形, 4.辞書形, 5.て・た形, 6.意向形, 7.仮定形, 8.可能形, 9.命令形]
    'k': ['け', 'けさ', 'けら', 'け', 'ける', 'け', 'けよう', 'けれ', 'けれ', 'けろ'],
    'g': ['げ', 'げさ', 'げら', 'げ', 'げる', 'げ', 'げよう', 'げれ', 'げれ', 'げろ'],
    's': ['せ', 'せさ', 'せら', 'せ', 'せる', 'せ', 'せよう', 'せれ', 'せれ', 'せろ'],
    'z': ['ぜ', 'ぜさ', 'ぜら', 'ぜ', 'ぜる', 'ぜ', 'ぜよう', 'ぜれ', 'ぜれ', 'ぜろ'],
    't': ['て', 'てさ', 'てら', 'て', 'てる', 'て', 'てよう', 'てれ', 'てれ', 'てろ'],
    'd': ['で', 'でさ', 'でら', 'で', 'でる', 'で', 'でよう', 'でれ', 'でれ', 'でろ'],
    'n': ['ね', 'ねさ', 'ねら', 'ね', 'ねる', 'ね', 'ねよう', 'ねれ', 'ねれ', 'ねろ'],
    'h': ['へ', 'へさ', 'へら', 'へ', 'へる', 'へ', 'へよう', 'へれ', 'へれ', 'へろ'],
    'b': ['べ', 'べさ', 'べら', 'べ', 'べる', 'べ', 'べよう', 'べれ', 'べれ', 'べろ'],
    'm': ['め', 'めさ', 'めら', 'め', 'める', 'め', 'めよう', 'めれ', 'めれ', 'めろ'],
    'r': ['れ', 'れさ', 'れら', 'れ', 'れる', 'れ', 'れよう', 'れれ', 'れれ', 'れろ'],
    'w': ['え', 'えさ', 'えら', 'え', 'える', 'え', 'えよう', 'えれ', 'えれ', 'えろ'],
}
CONJUGATE_MAP = {
    '五': CONJUGATE_GODAN_MAP,
    '上': CONJUGATE_KAMI_MAP,
    '下': CONJUGATE_SIMO_MAP,
}
SAHEN_LIST =  ['し', 'さ', 'さ', 'し', 'する', 'し', 'しよう', 'すれ', 'でき', 'しろ'] # "*"
KAHEN_LIST =  ['こ', 'こさ', 'こら', 'き', 'くる', 'き', 'こよう', 'くれ', 'これ', 'こい'] # "K-*"
IKU_LIST =    ['いか', 'いか', 'いか', 'いき', 'いく', 'いっ', 'いこう', 'いけ', 'いけ', 'いけ'] # "I-K*"
ARU_LIST =    ['', 'あら', 'あら', 'あり', 'ある', 'あっ', 'あろう', 'あれ', 'ありえ', 'あれ'] # "A-*"
GOZARU_LIST = ['ござら', 'ござら', 'ござら', 'ござい', 'ござる', 'ござっ', 'ござろう', 'ござれ', 'ござれ', 'ござれ'] # "KNAU-SNA*"

# 文語調の活用
AUXILIARY_VERB_LEFT_MAP = { # ストローク: [活用形, 補助動詞の語幹, 活用段, 活用行]
    'n' : [5, "て", '上', 'w'], # ～ている
    't' : [1, ""  , '下', 's'], # ～させる
    'k' : [2, ""  , '下', 'r'], # ～られる
    'nt': [5, "てもら", '五', 'w'], # ～てもらう
    'nk': [5, "てしま", '五', 'w'], # ～てしまう
}
AUXILIARY_VERB_RIGHT_MAP = { # ストローク: [活用形, 助動詞]
    ''   : [4, ""],
    'n'  : [0, "ない"],
    't'  : [5, "た"],
    'k'  : [3, "ます"],
    'nt' : [0, "なかった"],
    'nk' : [3, "ません"],
    'tk' : [3, "ました"],
    'ntk': [5, "て"],
}
AUXILIARY_VERB_EXCEPTION_MAP = { # 例外
    'tk-'    : [8, "る"], # 可能
    'tk-n'   : [8, "れない"], # 可能+否定
    'tk-t'   : [8, "た"], # 可能+過去
    'tk-k'   : [8, "ます"], # 可能+丁寧
    'tk-nt'  : [8, "なかった"], # 可能+否定+過去
    'tk-nk'  : [8, "ません"], # 可能+否定+丁寧
    'tk-tk'  : [8, "ました"], # 可能+過去+丁寧
    'tk-ntk' : [8, "て"], # 可能+て
    'ntk-'   : [3, ""], # 連用
    'ntk-n'  : [0, "ず"], # 否定
    'ntk-t'  : [7, "ば"], # 仮定
    'ntk-k'  : [6, ""], # 意向
    'ntk-nt' : [0, "なければ"], # 否定+仮定
    'ntk-nk' : [0, "なく"], # 否定+連用
    'ntk-tk' : [5, "てください"], # 丁寧命令
    'ntk-ntk': [9, ""], # 命令 
}
DESU_CONJUGATE_MAP = { # ですの活用形
    '':"です",
    'n':"でして",
    't':"でした",
    'k':"でしょう",
    'nt':"です",
    'nk':"ですが",
    'tk':"ですか?",
    'ntk':"ですね",
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

def translate_ta_te_form(string: str, auxiliary: list, conso: list) -> str:
    return string.replace("て", "で").replace("た", "だ") if conso in ['g', 'n', 'b', 'm'] and auxiliary == 5 else string

def stroke_to_verb(left_kana_list, right_kana_list, stroke_list) -> str:
    left_kana, left_extra_sound, left_conso, left_vowel = left_kana_list
    right_kana, right_extra_sound, right_conso, right_vowel = right_kana_list
    left_conso_stroke, left_vowel_stroke, left_particle_stroke, right_conso_stroke, right_vowel_stroke, right_particle_stroke = stroke_list[0], stroke_list[1], stroke_list[2], stroke_list[4], stroke_list[5], stroke_list[6]
    main_kana = left_kana + right_kana
    kana_stroke = left_conso_stroke + left_vowel_stroke + '-' + right_conso_stroke + right_vowel_stroke

    output = ""
    
    # 活用を取得
    auxiliary_list = stroke_to_conjugate(left_particle_stroke, right_particle_stroke)

    # 登録された五段活用
    if kana_stroke in VERB_GODAN_MAP:
        verb_list = VERB_GODAN_MAP[kana_stroke]
        output = verb_list[0] + translate_ta_te_form(CONJUGATE_GODAN_MAP[verb_list[1]][auxiliary_list[0]], auxiliary_list[0], verb_list[1]) + auxiliary_list[1]
    # 登録された上一段活用
    elif kana_stroke in VERB_KAMI_MAP:
        verb_list = VERB_KAMI_MAP[kana_stroke]
        output = verb_list[0] + CONJUGATE_KAMI_MAP[verb_list[1]][auxiliary_list[0]] + auxiliary_list[1]
    # 登録された下一段活用
    elif kana_stroke in VERB_SIMO_MAP:
        verb_list = VERB_SIMO_MAP[kana_stroke]
        output = verb_list[0] + CONJUGATE_SIMO_MAP[verb_list[1]][auxiliary_list[0]] + auxiliary_list[1]
    # 行く
    elif kana_stroke == "I-K":
        output += IKU_LIST[auxiliary_list[0]] + auxiliary_list[1]
    # ある
    elif kana_stroke == "A-":
        output += ARU_LIST[auxiliary_list[0]] + auxiliary_list[1]
    # ござる
    elif kana_stroke == "KNAU-SNA":
        output += GOZARU_LIST[auxiliary_list[0]] + auxiliary_list[1]
    # カ変活用
    elif kana_stroke == "K-":
        output += KAHEN_LIST[auxiliary_list[0]] + auxiliary_list[1]
    # サ変活用
    elif not right_kana:
        output = main_kana + SAHEN_LIST[auxiliary_list[0]] + auxiliary_list[1]
        output = output.replace("しず", "せず")
    # ～です
    elif right_conso_stroke == 'TN' and right_vowel_stroke == '':
        output = left_kana + left_extra_sound + DESU_CONJUGATE_MAP[right_particle_stroke]
    # 五段活用
    elif right_vowel_stroke == "" and right_conso in ['k', 'g', 's', 't', 'n', 'b', 'm', 'r', 'w']:
        output = left_kana + translate_ta_te_form(CONJUGATE_GODAN_MAP[right_conso][auxiliary_list[0]], auxiliary_list[0], right_conso) + auxiliary_list[1]
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
    return output
