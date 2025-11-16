KEYS = (
'S-', 'T-', 'K-', 'N-', 'Y-', 'I-', 'A-', 'U-', 'n-', 't-', 'k-',
'#',
'-S', '-T', '-K', '-N', '-Y', '-I', '-A', '-U', '-n', '-t', '-k',
'*',
)

IMPLICIT_HYPHEN_KEYS = ('#')

SUFFIX_KEYS = ()

NUMBER_KEY = None

NUMBERS = {}

UNDO_STROKE_STENO = ('-U')

ORTHOGRAPHY_RULES = []

ORTHOGRAPHY_RULES_ALIASES = {}

ORTHOGRAPHY_WORDLIST = None

KEYMAPS = {
        'Gemini PR': {
        'S-' : ('S1-','S2-'),
        'T-' : 'T-',
        'K-' : 'K-',
        'N-' : 'W-',
        'Y-' : 'P-',
        'I-' : 'H-',
        'A-' : 'R-',
        'U-' : ('*1','*2'),
        'n-' : '#3',
        't-' : ('A-'),
        'k-' : ('O-'),
        '#'  : ('#1','#2'),
        '-S' : ('-T','-S'),
        '-T' : '-L',
        '-K' : '-G',
        '-N' : '-B',
        '-Y' : '-P',
        '-I' : '-F',
        '-A' : '-R',
        '-U' : ('*3','*4'),
        '-n' : '#4',
        '-t' : ('-U'),
        '-k' : ('-E'),
        '*' : ('-D','-Z')
        },
        'Keyboard': {
        'S-' : ('a','q'),
        'T-' : 'w',
        'K-' : 's',
        'N-' : 'd',
        'Y-' : 'e',
        'I-' : 'r',
        'A-' : 'f',
        'U-' : ('t','g'),
        'n-' : 'space',
        't-' : ('v'),
        'k-' : ('b'),
        '#'  : ('['),
        '-S' : (';','p'),
        '-T' : 'o',
        '-K' : 'l',
        '-N' : 'k',
        '-Y' : 'i',
        '-I' : 'u',
        '-A' : 'j',
        '-U' : ('y','h'),
        '-n' : 'Return',
        '-t' : ('m'),
        '-k' : ('n'),
        '*' : ('\''),
        'arpeggiate' : ']'
        }
}

DICTIONARIES_ROOT = 'asset:Mejiro:dictionaries/default'
DEFAULT_DICTIONARIES = ('mejiro_commands.json','mejiro_base.py')



