import re
HEPBURN_ROMA_MAP = {
    'きゃ':'kya', 'きゅ':'kyu', 'きょ':'kyo', 'きぇ':'kye',
    'ぎゃ':'gya', 'ぎゅ':'gyu', 'ぎょ':'gyo', 'ぎぇ':'gye',
    'くぁ':'qa',  'くぃ':'qi',  'くぇ':'qe',  'くぉ':'qo',
    'しゃ':'sha', 'しゅ':'shu', 'しょ':'sho', 'しぇ':'she',
    'じゃ':'ja',  'じゅ':'ju',  'じょ':'jo',  'じぇ':'je',
    'ちゃ':'cha', 'ちゅ':'chu', 'ちょ':'cho', 'ちぇ':'che',
    'ぢゃ':'dya', 'ぢゅ':'dyu', 'ぢょ':'dyo', 'ぢぇ':'dye',
    'つぁ':'tsa', 'つぃ':'tsi', 'つぇ':'tse', 'つぉ':'tso',
    'てゃ':'tha', 'てゅ':'thu', 'てょ':'tho', 'てぇ':'the',
    'でゃ':'dha', 'でゅ':'dhu', 'でょ':'dho', 'でぇ':'dhe',
    'てぃ':'thi', 'とぅ':'twu', 'でぃ':'dhi', 'どぅ':'dwu',
    'にゃ':'nya', 'にゅ':'nyu', 'にょ':'nyo', 'にぇ':'nye',
    'ひゃ':'hya', 'ひゅ':'hyu', 'ひょ':'hyo', 'ひぇ':'hye',
    'びゃ':'bya', 'びゅ':'byu', 'びょ':'byo', 'びぇ':'bye',
    'ぴゃ':'pya', 'ぴゅ':'pyu', 'ぴょ':'pyo', 'ぴぇ':'pye',
    'ふぁ':'fa',  'ふぃ':'fi',  'ふぇ':'fe',  'ふぉ':'fo',
    'みゃ':'mya', 'みゅ':'myu', 'みょ':'myo', 'みぇ':'mye',
    'りゃ':'rya', 'りゅ':'ryu', 'りょ':'ryo', 'りぇ':'rye',
    'うぁ':'wha', 'うぃ':'wi',  'うぇ':'we',  'うぉ':'who',
    'ゔぁ':'va',  'ゔぃ':'vi',  'ゔぇ':'ve',  'ゔぉ':'vo',
    'あ':'a', 'い':'i', 'う':'u', 'え':'e', 'お':'o',
    'ぁ':'la', 'ぃ':'li', 'ぅ':'lu', 'ぇ':'le', 'ぉ':'lo',
    'か':'ka', 'き':'ki', 'く':'ku', 'け':'ke', 'こ':'ko',
    'が':'ga', 'ぎ':'gi', 'ぐ':'gu', 'げ':'ge', 'ご':'go',
    'さ':'sa', 'し':'shi', 'す':'su', 'せ':'se', 'そ':'so',
    'ざ':'za', 'じ':'ji', 'ず':'zu', 'ぜ':'ze', 'ぞ':'zo',
    'た':'ta', 'ち':'chi', 'つ':'tsu', 'て':'te', 'と':'to',
    'だ':'da', 'ぢ':'di', 'づ':'du', 'で':'de', 'ど':'do',
    'な':'na', 'に':'ni', 'ぬ':'nu', 'ね':'ne', 'の':'no',
    'は':'ha', 'ひ':'hi', 'ふ':'fu', 'へ':'he', 'ほ':'ho',
    'ば':'ba', 'び':'bi', 'ぶ':'bu', 'べ':'be', 'ぼ':'bo',
    'ぱ':'pa', 'ぴ':'pi', 'ぷ':'pu', 'ぺ':'pe', 'ぽ':'po',
    'ま':'ma', 'み':'mi', 'む':'mu', 'め':'me', 'も':'mo',
    'や':'ya', 'ゆ':'yu', 'よ':'yo',
    'ゃ':'lya', 'ゅ':'lyu', 'ょ':'lyo',
    'ら':'ra', 'り':'ri', 'る':'ru', 'れ':'re', 'ろ':'ro',
    'わ':'wa', 'を':'wo', 'ん':'N', 'っ':'Q', 'ゔ':'vu',
    '-':'-', ',':',', '.':'.',
    'ー':'-', '、':',', '。':'.'
}
JIS_KANA_MAP = { # JIS配列用
    'あ':'3', 'い':'e', 'う':'4', 'え':'5', 'お':'6',
    'ぁ':'#', 'ぃ':'E', 'ぅ':'$', 'ぇ':'%', 'ぉ':'&',
    'か':'t', 'き':'g', 'く':'h', 'け':':', 'こ':'b',
    'が':'t@', 'ぎ':'g@', 'ぐ':'h@', 'げ':':@', 'ご':'b@',
    'さ':'x', 'し':'d', 'す':'r', 'せ':'p', 'そ':'c',
    'ざ':'x@', 'じ':'d@', 'ず':'r@', 'ぜ':'p@', 'ぞ':'c@',
    'た':'q', 'ち':'a', 'つ':'z', 'て':'w', 'と':'s',
    'だ':'q@', 'ぢ':'a@', 'づ':'z@', 'で':'w@', 'ど':'s@',
    'な':'u', 'に':'i', 'ぬ':'1', 'ね':',', 'の':'k',
    'は':'f', 'ひ':'v', 'ふ':'2', 'へ':'^', 'ほ':'-',
    'ば':'f@', 'び':'v@', 'ぶ':'2@', 'べ':'^@', 'ぼ':'-@',
    'ぱ':'f[', 'ぴ':'v[', 'ぷ':'2[', 'ぺ':'^[', 'ぽ':'-[',
    'ま':'j', 'み':'n', 'む':']', 'め':'/', 'も':'m',
    'や':'7', 'ゆ':'8', 'よ':'9',
    'ゃ':'\'', 'ゅ':'(', 'ょ':')',
    'ら':'o', 'り':'l', 'る':'.', 'れ':';', 'ろ':'\\',
    'わ':'0', 'を':'}{#Shift(0)}{', 'ん':'y', 'っ':'Z', 'ゔ':'4@',
    '-':'|', ',':'<', '.':'>',
    'ー':'|', '、':'<', '。':'>'
}
def hiragana_to_romaji(text: str) -> str:
    """
    ひらがなをローマ字に変換。
    2文字キー（拗音）を優先してチェック。
    """
    result = []
    i = 0
    while i < len(text):
        # 1. 2文字のキー（拗音）をチェック
        found = False
        if i + 1 < len(text):
            two_chars = text[i:i+2]
            if two_chars in HEPBURN_ROMA_MAP:
                result.append(HEPBURN_ROMA_MAP[two_chars])
                i += 2  # 2文字進める
                found = True

        # 2. 2文字で見つからなかった場合、1文字のキーをチェック
        if not found:
            one_char = text[i]
            if one_char in HEPBURN_ROMA_MAP:
                result.append(HEPBURN_ROMA_MAP[one_char])
            else:
                # マップにない文字（カタカナや記号など）はそのまま残す
                result.append(one_char)
            i += 1  # 1文字進める
            
    return "".join(result)

def kana_to_typing_output(kana_string: str, typing_mode: int) -> str:
    if typing_mode == 0:
        raw_roma = hiragana_to_romaji(kana_string)
        # 小文字の「っ」処理（促音）：Q(子音) -> 子音を重ねる
        # (例: niQpoN -> nippoN)
        output = re.sub(r'Q([bcdfghjklmnpqrstvwxyz])', r'\1\1', raw_roma)
        # 撥音「ん」の処理：N(子音/Q) -> n(子音/Q)
        # 後に母音('a','i','u','e','o')や'y'が続かない場合
        # (例: shiNkyaku -> shinkyaku)
        output = re.sub(r'N([bcdfghjklmnpqrstvwxzQ])', r'n\1', output)
        # 残った撥音「N」の最終処理
        # (例: shiNan -> shinnan)
        output = output.replace('N', 'nn')
        # 残った促音「Q」の最終処理 (ltsuに)
        # (例: aQ -> altsu)
        output = output.replace('Q', 'ltsu') 
        return output
    else:
        return kana_string.translate(str.maketrans(JIS_KANA_MAP))