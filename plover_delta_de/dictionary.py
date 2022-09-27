import json
from typing import Tuple

from plover.steno_dictionary import StenoDictionary
from plover_stroke import BaseStroke

from plover_delta_de.system import KEYS, IMPLICIT_HYPHEN_KEYS


class Stroke(BaseStroke):
    @classmethod
    def setup(cls, keys: tuple, implicit_hyphen_keys: tuple):
        cls.keys = keys
        cls.ihks = implicit_hyphen_keys

        medial_pos_list = [list(cls.keys).index(k) for k in cls.ihks]
        cls.medial_pos = min(medial_pos_list)
        cls.final_pos = max(medial_pos_list)

        cls.init_key_order = {
            k.replace("-", ""): n
            for n, k in enumerate(list(cls.keys)[:cls.medial_pos])
        }
        cls.post_key_order = {
            k.replace("-", ""): n + cls.medial_pos
            for n, k in enumerate(list(cls.keys)[cls.medial_pos:])
        }
        cls.medial_keys = set(k.replace("-", "") for k in cls.ihks)

        super().setup(keys, implicit_hyphen_keys)

    @classmethod
    def from_stroke(cls, stroke: str) -> str:
        as_bin = 0
        order = cls.init_key_order
        in_init = True
        in_final = False
        first_e = False
        for char in stroke:
            if in_init and (char == "-" or char in cls.medial_keys):
                order = cls.post_key_order
                in_init = False
            
            if not in_init and not in_final:
                if char not in cls.medial_keys:
                    in_final = True
                elif char == "E" and first_e:
                    char = "e"
            elif in_final and char in cls.medial_keys:
                if char == "E":
                    char = "e"
                else:
                    raise ValueError(
                        "Invalid stroke: Medial in wrong position"
                    )
            
            if char == "E":
                first_e = True

            if char != "-":
                to_add = 1 << order[char]
                if to_add & as_bin:
                    raise ValueError("Invalid stroke: Duplicate key")

                as_bin += to_add
        
        return Stroke(as_bin)


Stroke.setup(KEYS, IMPLICIT_HYPHEN_KEYS)


class DeltaDictionary(StenoDictionary):
    readonly = False

    def __init__(self) -> None:
        super().__init__()
        self._reorder_map = {}
    
    def _load(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as fp:
            json_data = json.load(fp)
        
        for unordered, output in json_data.items():
            ordered = tuple(
                str(Stroke.from_stroke(stroke))
                for stroke in
                unordered.split("/")
            )

            self._reorder_map[ordered] = unordered
            self[ordered] = output
    
    def _save(self, filename: str) -> None:
        mappings = []
        for strokes, translation in self.items():
            ordered = "/".join(strokes)
            mappings.append((
                self._reorder_map.get(
                    ordered, 
                    ordered.replace("e", "E")
                ),
                translation
            ))
        
        mappings.sort()

        with open(filename, "w", encoding="utf-8", newline="\n") as fp:
            json.dump(
                dict(mappings),
                fp,
                ensure_ascii=False,
                indent=0,
                separators=(",", ": ")
            )

            fp.write("\n")
    
    def __contains__(self, key: Tuple[str]) -> bool:
        return False
    
    def get(self, key: Tuple[str], fallback=None) -> str:
        if len(key) > self._longest_key:
            return fallback
        
        if key in self._dict:
            return self[key]

        capitalized = "^" in key[0]
        attach = "<" in key[0]
        if not (capitalized or attach):
            return fallback
        
        new_key = (
            key[0].replace("^", "").replace("<", ""),
            *key[1:]
        )

        if new_key not in self._dict:
            return fallback
        
        return (
            "{^}" * attach +
            "{-|}" * capitalized +
            self[new_key]
        )


def split_entry(line: str) -> Tuple[str, str]:
    word = ""
    last = ""
    for i, c in enumerate(line):
        if c == "," and last != "\\":
            return (
                word.replace("\,", ",").strip(), 
                line[i+1:].strip()
            )

        word += c
        last = c
    
    # Fallback
    word, outline = line.strip().split(",", 1)
    return word.strip(), outline.strip()


class DeltaWordDictionary(DeltaDictionary):
    def _load(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                if "," not in line:
                    continue

                word, unordered = split_entry(line)
                ordered = tuple(
                    str(Stroke.from_stroke(stroke))
                    for stroke in
                    unordered.split(".")
                )

                self._reorder_map[ordered] = unordered
                self[ordered] = word.strip()
    
    def _save(self, filename: str) -> None:
        mappings = []
        for strokes, translation in self.items():
            ordered = "/".join(strokes)
            mappings.append((
                translation.replace(",", "\,"),
                self._reorder_map.get(
                    ordered, 
                    ordered.replace("/", ".").replace("e", "E")
                )
            ))
        
        mappings.sort()

        with open(filename, "w", encoding="utf-8", newline="\n") as fp:
            for (translation, outline) in mappings:
                fp.write(f"{translation}, {outline}\n")
