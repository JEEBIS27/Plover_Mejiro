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
        'Gemini PR': {
        'Y-' : ('S1-','S2-'),
        'T-' : 'K-',
        'K-' : 'T-',
        'N-' : 'W-',
        'S-' : 'P-',
        'A-' : 'R-',
        'I-' : 'H-',
        'O-' : '*2',
        'U-' : '*1',
        't-' : ('A-'),
        'k-' : ('O-'),
        'n-' : '#3',
        '#'  : ('#1','#2'),
        '*' : ('-D','-Z'),
        '-Y' : ('-T','-S'),
        '-T' : '-G',
        '-K' : '-L',
        '-N' : '-B',
        '-S' : '-P',
        '-A' : '-R',
        '-I' : '-F',
        '-O' : '*4',
        '-U' : '*3',
        '-t' : ('-U'),
        '-k' : ('-E'),
        '-n' : '#4',
        'arpeggiate' : '#5'
        },
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
        '#'  : ('Tab'),
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

