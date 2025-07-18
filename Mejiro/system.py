KEYS = (
'Y-', 'T-', 'K-', 'N-', 'S-', 'A-', 'I-', 'O-', 'U-', 't-', 'k-', 'n-',
'#','*',
'-Y', '-T', '-K', '-N', '-S', '-A', '-I', '-O', '-U', '-t', '-k', '-n',
)

IMPLICIT_HYPHEN_KEYS = ('#','*')

SUFFIX_KEYS = ()

NUMBER_KEY = None

NUMBERS = {}

UNDO_STROKE_STENO = ('-O')

ORTHOGRAPHY_RULES = []

ORTHOGRAPHY_RULES_ALIASES = {}

ORTHOGRAPHY_WORDLIST = None

KEYMAPS = {
        'Keyboard': {
        'Y-' : ('a','q'),
        'T-' : 's',
        'K-' : 'w',
        'N-' : 'd',
        'S-' : 'e',
        'A-' : 'f',
        'I-' : 'r',
        'O-' : 'g',
        'U-' : 't',
        't-' : ('v'),
        'k-' : ('b'),
        'n-' : 'space',
        '#'  : ('z'),
        '*' : ('\'','['),
        '-Y' : (';','p'),
        '-T' : 'l',
        '-K' : 'o',
        '-N' : 'k',
        '-S' : 'i',
        '-A' : 'j',
        '-I' : 'u',
        '-O' : 'h',
        '-U' : 'y',
        '-t' : ('m'),
        '-k' : ('n'),
        '-n' : 'Return',
        'arpeggiate' : ']'
        }
}

DICTIONARIES_ROOT = 'asset:Mejiro:dictionaries'
DEFAULT_DICTIONARIES = ('Mejiro_Commands.json','Mejiro_Users.json','Mejiro_Kana.py','Mejiro_Romaji.py')
