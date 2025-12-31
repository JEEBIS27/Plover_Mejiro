USERS_MAP = { # ユーザー略語の定義
  "SKNIA-SAUtk": "めじろしきそっき",
  "SKNIA-SInk": "めじろしき",
  "SKNIA-SNI": "めじろ",
  "SN-S": "えすえぬえす",
  "A-I": "えーあい",
  "KNUntk-KNU": "ぐーぐる",
  "TKA-STA": "はらすめんと",
  "KAUn-TAntk": "こんぴゅーたー",
  "TNIA-SNI": "でじたる",
  "In-STA": "いんふら",
  "KAUn-TKNIn": "こんびに",
  "SU-STKNAU": "すまーとふぉん",
  "SU-TKAU": "すまほ",
  "SY-IAn": "さいえんす",
  "STKU-STA": "ぷらすちっく",
  "KI-TKNAU": "きーぼーど",
  "In-NIAtk": "いんたーねっと",
  "In-TKU": "いんふるえん",
  "In-STKNAU": "いんふぉめーしょん",
  "KAU-SKNYU": "こみゅにけーしょん",
  "IU-STU": "ういるす",
  "KAU-IU": "ころなういるす",
  "A-SKNIA": "あめりか",
  "TNAU-STIA": "どれだけ",
  "SIn-KNA": "しんがた",
  "TKI-TAU": "ひとびと",
  "AU-NIA": "おねがい",
  "YAU-STAU": "よろしく",
  "TA-TAU": "たとえば",
  "KNU-TY": "ぐたいてきには",
  "TA-SI": "たしかに",
  "KIA-STIA": "けれども",
}
ABSTRACT_MAP = { # 一般略語の定義
  "YAU-STIA": "あれ",
  "KAU-STIA": "これ",
  "SAU-STIA": "それ",
  "TNAU-STIA": "どれ",
  "TNA-STIA": "だれ",
  "TAU-KAU": "ところ",
  "KAU-TAU": "こと",
  "TKI-TAU": "ひと",
  "TAU-KI": "とき",
  "SKNAU-NAU": "もの",
  "TKNIA-TIA": "すべて",
  "NA-KNA": "ながら",
  "AU-KA": "おかげ",
  "SI-KNAU": "しごと"
}

ABSTRACT_MAP_LEFT = { # 一般略語の左側ストローク定義
  "STN": "",
  "YIAU": "あの",
  "KIAU": "この",
  "SIAU": "その",
  "TIAU": "との",
  "TNIAU": "どの",
  "NIAU": "なんの",
  "IU": "いう",
  "YIU": "ああいう",
  "KIU": "こういう",
  "SIU": "そういう",
  "TNIU": "どういう",
  "NIU": "なんていう"
}

ABSTRACT_MAP_RIGHT = { # 一般略語の右側ストローク定義
  "STN": "",
  "KAU": "こと",
  "STAU": "ころ",
  "KI": "とき",
  "TAU": "ところ",
  "TKI": "ひと",
  "TKA": "はなし",
  "TKIAU": "ほう",
  "SKNAU": "もの",
  "KNAU": "ものごと",
  "SI": "しごと",
}

VERB_GODAN_MAP = { # ストローク: [語幹, 行]
    "A-STU": ["ある", 'k'],# 歩く
    "TA-TNA": ["いただ", 'k'],# 頂く
    "KI-TU": ["きがつ", 'k'],# 気が付く
    "KI-TNU": ["きづ", 'k'],# 気付く
    "TA-TA": ["たた", 'k'],# 叩く
    "NAU-SNAU": ["のぞ", 'k'],# 除く
    "TKA-TA": ["はたら", 'k'],# 働く
    "I-SAU": ["いそ", 'g'],# 急ぐ
    "I-KA": ["いか", 's'],# 活かす
    "AU-TAU": ["おと", 's'],# 落とす
    "KA-KA": ["かか", 's'],# 欠かす
    "KA-KU": ["かく", 's'],# 隠す
    "SI-SU": ["しめ", 's'],# 示す
    "TIA-STA": ["てら", 's'],# 照らす
    "TKA-NA": ["はな", 's'],# 話す
    "SKNI-NA": ["みな", 's'],# 見なす
    "SKNA-NA": ["まな", 'b'],# 学ぶ
    "TU-TU": ["つつ", 'm'],# 包む
    "TKA-SA": ["はさ", 'm'],# 挟む
    "TKI-KAU": ["ひっこ", 'm'],# 引っ込む
    "TKU-KU": ["ふく", 'm'],# 吹く
    "KNA-TKNA": ["がんば", 'r'],# 頑張る
    "KIA-": ["け", 'r'],# 蹴る
    "SYA-TKNIA": ["しゃべ", 'r'],# しゃべる
    "NA-": ["な", 'r'],# なる
    "TKA-TKNA": ["はばか", 'r'],# 憚る
    "YA-": ["や", 'r'],# やる
    "-YA": ["や", 'r'],# やる
    "-A": ["あ", 'w'],# 会う
    "I-": ["い", 'r'],# 要る
    "IU-": ["い", 'w'],# 言う
    "U-SI": ["うしな", 'w'],# 失う
    "AU-SKNAU": ["おも", 'w'],# 思う
    "SI-TIAU": ["した", 'w'],# 慕う
    "SI-KNIAU": ["したが", 'w'],# 従う
    "SI-SKNIAU": ["しま", 'w'],# 仕舞う
    "TU-KA": ["つか", 'w'],# 使う
    "TAU-SKNAU": ["ともな", 'w'],# 伴う
    "SKNA-TAU": ["まと", 'w'],# 纏う
    "SKNAU-STA": ["もら", 'w'],# 貰う
    "SKNAU-STIAU": ["もら", 'w'],# 貰う
    "TKA-STA": ["はら", 'w'],# 払う
    "SKA-STA": ["わら", 'w'],# 笑う
}
VERB_KAMI_MAP = { # ストローク: [語幹, 行]
    "TN-KI": ["で", 'k'],# 出来る
    "SI-SNI": ["しん", 'z'],# 信じる
    "KA-SNI": ["かん", 'z'],# 感じる
    "KI-SNI": ["きん", 'z'],# 禁じる
    "TNA-SNI": ["だん", 'z'],# 断じる
    "KA-SKNI": ["かんが", 'm'],# 鑑みる
}
VERB_SIMO_MAP = { # ストローク: [語幹, 行]
    "TU-TN": ["つづ", 'k'],# 続ける
    "TN-": ["", 'd'],# 出る
    "TKA-SNI": ["はじ", 'm'],# 始める
    "SKNAU-TAU": ["もと", 'm'],# 求める
    "SKA-SU": ["わす", 'r'],# 忘れる
    "KA-KNA": ["かんが", 'w'],# 考える
    "SA-SA": ["ささ", 'w'],# 支える
    "SKNA-KNA": ["まちが", 'w'],# 間違える
}