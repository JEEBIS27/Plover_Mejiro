import re
from Mejiro.dictionaries.default.settings import typing_mode
HEPBURN_ROMA_MAP = {
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
    'わ':'wa', 'を':'wo', 'ん':'nn', 'っ':'ltsu', 'ゔ':'vu',
    '-':'-', ',':',', '.':'.',
    'ー':'-', '、':',', '。':'.'
}
JIS_KANA_MAP = {
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

def create_replacer_function(kana_map):

    sorted_keys = sorted(kana_map.keys(), key=len, reverse=True)

    pattern_string = '|'.join(re.escape(k) for k in sorted_keys)

    def replacer(match):
        return kana_map[match.group(0)]

    return re.compile(f"({pattern_string})"), replacer

HEPBURN_PATTERN, HEPBURN_REPLACER = create_replacer_function(HEPBURN_ROMA_MAP)
# 子音(k,g,c,z,s,x,j,d,t,b,p,f,r,v) i(またはu) l (a,e,i,o,u,y)
YOUON_PATTERN = re.compile(r"([kgczsxjdtbpfrv](?:u|i)?)([l][yaeuiou])")

def youon_replacer(match):
    # 'ki' から 'i' を削除し、'lya' から 'l' を削除して結合 -> 'k' + 'ya' = 'kya'
    base_consonant = match.group(1)[:-1] # 'ki' から 'i' を削除 -> 'k'
    youon_vowel = match.group(2)[1:]      # 'lya' から 'l' を削除 -> 'ya'
    return base_consonant + youon_vowel

HATSUON_PATTERN = re.compile(r"n(n)([kgcqstjdhbpfvmrywzl])")

HATSUON_REPLACER = r"n\2"

SOKUON_PATTERN = re.compile(r"ltsu([kgcqstjdhbpfvmrywz])")

SOKUON_REPLACER = r"\1\1"

F_V_SHORTEN_PATTERN = re.compile(r"(f|v)ul")

F_V_SHORTEN_REPLACER = r"\1"

SH_CH_J_SHORTEN_PATTERN = re.compile(r"(sh|ch|j|y)il(y?)")

SH_CH_J_SHORTEN_REPLACER = r"\1"

def kana_to_typing_output(kana_string):
    if typing_mode == 0:

        output = HEPBURN_PATTERN.sub(HEPBURN_REPLACER, kana_string)

        output = YOUON_PATTERN.sub(youon_replacer, output)

        output = HATSUON_PATTERN.sub(HATSUON_REPLACER, output)

        output = SOKUON_PATTERN.sub(SOKUON_REPLACER, output)

        output = F_V_SHORTEN_PATTERN.sub(F_V_SHORTEN_REPLACER, output)

        output = SH_CH_J_SHORTEN_PATTERN.sub(SH_CH_J_SHORTEN_REPLACER, output)

        output = output.replace("teli", "thi").replace("deli", "dhi").replace("dolu", "dwu")
        return output
    else:
        return kana_string.translate(str.maketrans(JIS_KANA_MAP))