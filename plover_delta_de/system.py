from typing import Dict, Tuple, Union


KEYS = tuple(
    "# S- K- F- P- T- N- R- *- >- E- I- -A -U "
    "-+ -* -R -N -P -S -K -F -T -e".split()
)

IMPLICIT_HYPHEN_KEYS = tuple("E- I- -A -U".split())

SUFFIX_KEYS = tuple()

NUMBER_KEY = None

NUMBERS = {}

FERAL_NUMBER_KEY = False

UNDO_STROKE_STENO = ""

ORTHOGRAPHY_RULES = []

ORTHOGRAPHY_RULES_ALIASES = {}

ORTHOGRAPHY_WORDLIST = None

DICTIONARIES_ROOT = "asset:plover_delta_de:dictionaries"

DEFAULT_DICTIONARIES = tuple()


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
        "S1- T- P- H- *1    -F -P -L -T -D "
        "S2- K- W- R- *2    -R -B -G -S -Z "
                   "A- O-  -E -U"
    ), (
        "#1", "#2", "#3", "#4", "#5", "#6", "#7", 
        "#8", "#9", "#A", "#B", "#C"
    ), (
        "Fn", "pwr", "res1", "res2", "*3", "*4"
    ), None),

    "Keyboard": ((
        "q  w  e  r  t      u  i  o  p  [ "
        "a  s  d  f  g      j  k  l  ;  ' "
                  "v  b    n  m"
    ), (
        "1", "2", "3", "4", "5", "6", "7", "8", 
        "9", "0", "-", "=", 
    ), (
        ",", ".", "/", "]", "\\", "y", "h", "z", 
        "x"
    ), "space"),

    "Treal": ((
        "S1- T- P- H- *1    -F -P -L -T -D "
        "S2- K- W- R- *2    -R -B -G -S -Z "
                   "A- O-  -E -U"
    ), (
        "#1", "#2", "#3", "#4", "#5", "#6", "#7", 
        "#8", "#9", "#A", "#B"
    ), (
        "X1-", "X2-", "X3"
    ), None),
}

LAYOUT = (
    "T- R- S- *- -+    -* -N -S -F -e "
    "N- P- K- F- >-    -R -P -K -T -e "
              "E- I-  -A -U"
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
