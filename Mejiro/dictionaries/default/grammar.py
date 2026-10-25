"""接続可能性は文字列の末尾で推測せず、確定した出力の活用から決める。"""

from Mejiro.dictionaries.default.abbreviations import (
    ABSTRACT_MAP, ABSTRACT_MAP_LEFT, ABSTRACT_MAP_RIGHT,
)

UNKNOWN = "unknown"
NOMINALIZABLE = "nominalizable"
INCOMPLETE = "incomplete"
ATTRIBUTIVE_NA = "attributive_na"
QUESTION_PREDICATE = "question_predicate"
NOUN = "noun"
PLACE = "place"
INDEFINITE_NOUN = "indefinite_noun"
QUESTION_PARTICLE = "question_particle"

# 一般略語として確定した語だけを分類する。通常入力への末尾推測には使わない。
PLACE_WORDS = {
    "あそこ", "ここ", "そこ", "どこ", "あっち", "こっち", "そっち", "どっち",
    "あちら", "こちら", "そちら", "どちら", "ところ", "とこ",
}
INDEFINITE_WORDS = {"なに", "なん", "どれ"}
ATTRIBUTIVE_NA_WORDS = {"あんな", "こんな", "そんな", "どんな"}
QUESTION_PARTICLES = {"の", "と", "も", "から", "だから", "だけ"}

# 例外活用のうち「の」で名詞化できるもの。
# 可能の各活用は通常の右手活用と同じ接続になる。
NOMINALIZABLE_EXCEPTIONS = {
    "nt-", "nt-n", "nt-t", "nt-nt",  # やすい・にくい・たい・てほしい
    "tk-", "tk-n", "tk-t", "tk-k", "tk-nt", "tk-nk", "tk-tk",
}


def verb_context(left, right, *, desu=False):
    """語幹側の活用ではなく、出力全体の最終活用を分類する。"""
    if desu:
        # 丁寧形はユーザー指定の入力方針として「のが」を選ぶ。
        if right == "k":  # でしょうか。「のが」への直接接続とは分ける。
            return QUESTION_PREDICATE
        return NOMINALIZABLE if right in ("", "t") else INCOMPLETE
    if left == "ntk" and right in ("k", "ntk"):  # ましょうか・しようか
        return QUESTION_PREDICATE
    if left in ("nt", "tk", "ntk"):
        return (NOMINALIZABLE if left + "-" + right in NOMINALIZABLE_EXCEPTIONS
                else INCOMPLETE)
    # 辞書形・否定・過去・丁寧形。ている／使役／受身等も最終形で判定。
    return NOMINALIZABLE if right != "ntk" else INCOMPLETE


def particle_context(text):
    # 「な」の直後は「なのが」にできる。他の格・係・接続助詞の後は
    # 「な」「のが」のいずれも接続を保証できない。句読点もここで切る。
    if text == "な":
        return ATTRIBUTIVE_NA
    if text in QUESTION_PARTICLES:
        return QUESTION_PARTICLE
    return INCOMPLETE


def abstract_context(left, right, asterisk):
    """一般略語の語彙／複合略語の右側の主要語に接続情報を付ける。"""
    key = left + "-" + right + asterisk
    if key in ABSTRACT_MAP:
        head = ABSTRACT_MAP[key]
    elif asterisk and left in ABSTRACT_MAP_LEFT and right in ABSTRACT_MAP_RIGHT:
        head = ABSTRACT_MAP_RIGHT[right]
        if not head:
            # 「この」「こういう」等の連体修飾語だけでは名詞句は未完成。
            prefix = ABSTRACT_MAP_LEFT[left]
            return ATTRIBUTIVE_NA if prefix in ATTRIBUTIVE_NA_WORDS else INCOMPLETE
    else:
        return UNKNOWN
    if head in PLACE_WORDS:
        return PLACE
    if head in INDEFINITE_WORDS:
        return INDEFINITE_NOUN
    if head in ATTRIBUTIVE_NA_WORDS:
        return ATTRIBUTIVE_NA
    if head in QUESTION_PARTICLES:
        return QUESTION_PARTICLE
    if head == "ただ":  # 副詞／名詞等の用法をこの略語だけでは確定できない。
        return INCOMPLETE
    return NOUN


def choose_na_particle(context):
    return "のが" if context in (NOMINALIZABLE, ATTRIBUTIVE_NA) else "な"


def choose_he_particle(context, right=""):
    # 名詞修飾は「ことへの／人への」を優先。「何かの」は不定語の別構造。
    # 述語には「しているかのよう」の接続もある。
    if right in ("k", "nk"):
        return "か" if context in (NOMINALIZABLE, INDEFINITE_NOUN) else "へ"
    if context in (NOMINALIZABLE, QUESTION_PREDICATE, NOUN,
                   INDEFINITE_NOUN, QUESTION_PARTICLE):
        return "か"
    return "へ"


def attached_context(left, right, particle, base=UNKNOWN):
    """語＋助詞を一打で出す場合も、独立入力と同じ接続情報にする。"""
    if not left and not right:
        return base
    if (left, right) in (("n", ""), ("n", "n")):  # である・だったへの置換
        return NOMINALIZABLE
    return particle_context(particle)
