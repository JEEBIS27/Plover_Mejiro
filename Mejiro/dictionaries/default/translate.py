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
def kana_to_typing_output(kana_string):
    if typing_mode == 0:
        output = kana_string.translate(str.maketrans(HEPBURN_ROMA_MAP))
        output = output.replace("teli", "thi").replace("deli", "dhi").replace("ful", "f").replace("vul", "v")
        output = output.replace("shily", "sh").replace("shil", "sh").replace("jily", "j").replace("jil", "j").replace("chily", "ch").replace("chil", "ch").replace("ily", "y")
        output = output.replace("nnk", "nk").replace("nng", "ng").replace("nnc", "nc").replace("nnq", "nq").replace("nns", "ns").replace("nnz", "nz").replace("nnj", "nj").replace("nnt", "nt").replace("nnd", "nd").replace("nnh", "nh").replace("nnb", "nb").replace("nnp", "np").replace("nnf", "nf").replace("nnv", "nv").replace("nnm", "nm").replace("nnr", "nr").replace("nnw", "nw").replace("nnl", "nl")
        output = output.replace("ltsuk", "kk").replace("ltsug", "gg").replace("ltsuc", "cc").replace("ltsuq", "qq").replace("ltsus", "ss").replace("ltsuz", "zz").replace("ltsuj", "jj").replace("ltsut", "tt").replace("ltsud", "dd").replace("ltsuh", "hh").replace("ltsub", "bb").replace("ltsup", "pp").replace("ltsuf", "ff").replace("ltsuv", "vv").replace("ltsum", "mm").replace("ltsuy", "yy").replace("ltsur", "rr").replace("ltsuw", "ww").replace("ltsul", "ll")
        return output
    else:
        return kana_string.translate(str.maketrans(JIS_KANA_MAP))