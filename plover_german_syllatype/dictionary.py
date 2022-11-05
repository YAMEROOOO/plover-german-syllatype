import json
from typing import Tuple

from plover.steno_dictionary import StenoDictionary
from plover_stroke import BaseStroke

from plover_german_syllatype.system import KEYS, IMPLICIT_HYPHEN_KEYS


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
        for char in stroke:
            if in_init and (char == "-" or char in cls.medial_keys):
                order = cls.post_key_order
                in_init = False
            
            if not in_init and not in_final:
                if char not in cls.medial_keys:
                    in_final = True
            elif in_final and char in cls.medial_keys:
                raise ValueError(
                    f"Invalid stroke: Medial in wrong position in {stroke}"
                )

            if char != "-":
                to_add = 1 << order[char]
                if to_add & as_bin:
                    raise ValueError(
                        f"Invalid stroke: Duplicate key in {stroke}"
                    )

                as_bin += to_add
        
        return Stroke(as_bin)


Stroke.setup(KEYS, IMPLICIT_HYPHEN_KEYS)


class JSONSyllatypeDictionary(StenoDictionary):
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
            self.add_entry(ordered, output)
    
    def _save(self, filename: str) -> None:
        mappings = []
        for strokes, translation in self.items():
            ordered = "/".join(strokes)
            mappings.append((
                self._reorder_map.get(
                    ordered, 
                    ordered
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
    
    def add_entry(self, key: Tuple[str], output: str) -> str:
        # We have to use this instead of __setitem__ because
        # reverse dictionary checks will tell you that the
        # dictionary contains entries that aren't in _dict
        # due to the ^ and < keys.

        self._longest_key = max(self._longest_key, len(key))
        self._dict[key] = output
        self.reverse[output].append(key)
        self.casereverse[output.lower()].append(output)

    def get(self, key: Tuple[str], fallback=None) -> str:
        if len(key) > self._longest_key:
            return fallback

        capitalized = "^" in key[0]
        attach = "<" in key[0]
        
        candidate = None
        new_cap = False
        new_att = False
        for rep_cap, rep_att in [
            (False, False),
            (False, True),
            (True, False),
            (True, True)
        ]:
            key_head = key[0]
            key_tail = key[1:]

            if rep_cap: key_head = key_head.replace("^", "")
            if rep_att: key_head = key_head.replace("<", "")
            new_key = (key_head, *key_tail)

            if new_key in self._dict:
                candidate = self._dict[new_key]
                new_cap = rep_cap
                new_att = rep_att
                break
        
        if not candidate:
            return fallback

        return (
            "{^}" * (attach and new_att) +
            "{-|}" * (capitalized and new_cap) +
            candidate
        )

    def __contains__(self, key):
        return bool(self.get(key))


def split_entry(line: str) -> Tuple[str, str]:
    word = ""
    last = ""
    for i, c in enumerate(line):
        if c == ":" and last != "\\":
            return (
                word.replace(r"\:", ":").strip(), 
                line[i+1:].strip()
            )

        word += c
        last = c
    
    # Fallback
    word, outline = line.strip().split(":", 1)
    return word.strip(), outline.strip()


class SyllatypeDictionary(JSONSyllatypeDictionary):
    def _load(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as fp:
            for line in fp.readlines():
                if ":" not in line:
                    continue

                word, unordered = split_entry(line)
                ordered = tuple(
                    str(Stroke.from_stroke(stroke))
                    for stroke in
                    unordered.split("/")
                )

                self._reorder_map[ordered] = unordered
                self.add_entry(ordered, word.strip())

    def _save(self, filename: str) -> None:
        mappings = []
        for strokes, translation in self.items():
            ordered = "/".join(strokes)
            mappings.append((
                translation.replace(":", r"\:"),
                self._reorder_map.get(
                    ordered, 
                    ordered
                )
            ))
        
        mappings.sort()

        with open(filename, "w", encoding="utf-8", newline="\n") as fp:
            for (translation, outline) in mappings:
                fp.write(f"{translation}, {outline}\n")
