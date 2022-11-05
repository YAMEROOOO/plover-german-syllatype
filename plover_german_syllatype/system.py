from typing import Dict, Tuple, Union


KEYS = tuple(
    "# < ^ S- K- F- P- T- N- R- *- A- E- -I -U "
    "-R -N -T -P -S -K -F -* ->".split()
)

IMPLICIT_HYPHEN_KEYS = ("A-", "E-", "-I", "-U")

SUFFIX_KEYS = tuple()

NUMBER_KEY = None

NUMBERS = {}

FERAL_NUMBER_KEY = False

UNDO_STROKE_STENO = ""

ORTHOGRAPHY_RULES = []

ORTHOGRAPHY_RULES_ALIASES = {}

ORTHOGRAPHY_WORDLIST = None

DICTIONARIES_ROOT = "asset:plover_german_syllatype:dictionaries"

DEFAULT_DICTIONARIES = (
    "syllatype_main.syl", 
    "syllatype_commands.syl", 
    "syllatype_characters.syl"
)


def build_map(
    system_keys: str, 
    machine_keys: str
) -> Dict[str, Union[str, Tuple[str, ...]]]:
    system_keys_list = system_keys.split()
    machine_map = {s: [] for s in system_keys_list}
    for m, s in zip(machine_keys.split(), system_keys_list):
        machine_map[s].append(m)
    
    return dict(
        (m, l[0]) if len(l) == 1 else (m, tuple(l))
        for m, l in machine_map.items()
    )

KEYMAP_LAYOUTS = {
    "Gemini PR": ((
        "S1- T- P- H- *1  *3 -F -P -L -T -D "
        "S2- K- W- R- *2  *4 -R -B -G -S -Z "
                  "A- O-  -E -U"
    ), (
        "#1", "#2", "#3", "#4", "#5", "#6", "#7", 
        "#8", "#9", "#A", "#B", "#C"
    ), (
        "Fn", "pwr", "res1", "res2"
    ), None),

    "Keyboard": ((
        "q  w  e  r  t   u  i  o  p  [ ] "
        "a  s  d  f  g   j  k  l  ;  ' \\ "
                 "c  v   m  ,"
    ), (
        "1", "2", "3", "4", "5", "6", "7", "8", 
        "9", "0", "-", "=", 
    ), (
        ".", "/", "z", "x", "y", "h", "b"
    ), "space"),

    "Treal": ((
        "X1- S1- T- P- H-  *1 -F -P -L -T -D "
        "X2- S2- K- W- R-  *2 -R -B -G -S -Z "
                   "A- O-  -E -U"
    ), (
        "#1", "#2", "#3", "#4", "#5", "#6", "#7", 
        "#8", "#9", "#A", "#B"
    ), (
        "X3",
    ), None),
}

LAYOUT = (
    "F- T- N- *- ^   -> -* -N -T -F < "
    "K- S- P- R- ^   -> -R -P -S -K < "
             "A- E-  -I -U"
)

KEYMAPS = {
    map_name: {
        **build_map(LAYOUT, map_layout),
        "#": num_keys,
        "no-op": noop_keys,
        **({"arpeggiate": arp_key} if arp_key else {})
    }
    for map_name, (map_layout, num_keys, noop_keys, arp_key)
    in KEYMAP_LAYOUTS.items()
}
