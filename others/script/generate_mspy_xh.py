#!/usr/bin/env python3
"""Generate Microsoft double-pinyin + Xiaohe shape dictionaries (Python 3.8+).

Run from any directory: python3 others/script/generate_mspy_xh.py [--check]
Source dictionaries stay untouched. Source layer and candidate order are retained.
The independent basic-CJK pinyin table uses source frequencies and no shape codes.
Microsoft keyboard: https://github.com/rime/rime-double-pinyin
"""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
import unicodedata


LAYERS = (
    "user.top", "user", "primary", "secondary", "whimsicality", "off-table",
    "single.code", "full.code.words", "full.code.chars", "japanese",
    "rare.chars", "secondary.simple",
)
DEFAULT_LAYERS = tuple(layer for layer in LAYERS if layer != "secondary.simple")
BASIC_CJK = range(0x4E00, 0xA000)
FINALS = {
    "a": "a", "o": "o", "e": "e", "i": "i", "u": "u", "v": "y",
    "ai": "l", "ei": "z", "ao": "k", "ou": "b", "an": "j", "en": "f",
    "ang": "h", "eng": "g", "ong": "s", "er": "r", "ia": "w",
    "ie": "x", "iao": "c", "iu": "q", "ian": "m", "in": "n",
    "iang": "d", "ing": ";", "iong": "s", "ua": "w", "uo": "o",
    "uai": "y", "ui": "v", "uan": "r", "un": "p", "uang": "d",
    "ue": "t", "ve": "t", "van": "r", "vn": "p",
}
# Official mnemonic/nonstandard spellings are fixed codes, not regular pinyin.
FIXED_ENTRIES = {
    ("鹤", "eh"), ("偶尔", "eo"), ("什么", "sm"),
    ("桃李争妍", "tlzy"), ("为什么", "wsme"),
}
# Official syllabic m/n/ng/hm encodings have no standard two-key MS equivalent.
SPECIAL_SYLLABLES = {"om": "om", "on": "on", "og": "og", "hm": "hm"}


def is_han(char):
    return char == "〇" or "CJK UNIFIED IDEOGRAPH" in unicodedata.name(char, "") or "CJK COMPATIBILITY IDEOGRAPH" in unicodedata.name(char, "")


def dictionary_rows(path):
    """Yield all data fields, preserving source order and optional columns."""
    in_data = False
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if line.strip() == "...":
            in_data = True
            continue
        if not in_data or not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 2:
            raise ValueError("{}:{}: expected tab-separated text/code".format(path, number))
        yield fields


def microsoft_code(pinyin):
    """Return one canonical code: zero initial o, ue/ve t, ü y."""
    pinyin = pinyin.replace("ü", "v")
    if pinyin[0] in "aoe":
        initial, final = "o", pinyin
    elif pinyin[:2] in ("zh", "ch", "sh"):
        initial, final = {"zh": "v", "ch": "i", "sh": "u"}[pinyin[:2]], pinyin[2:]
    else:
        initial, final = pinyin[0], pinyin[1:]
    if final not in FINALS:
        raise ValueError("unsupported pinyin syllable: " + pinyin)
    return initial + FINALS[final]


def build_basic_pinyin_rows(primary_rows, supplemental_rows):
    """Return weighted basic-CJK two-key candidates and characters without readings.

    The primary dictionary's per-reading frequency wins over supplemental
    duplicates, including a frequency of zero. Other readings receive weight 1.
    Different readings that share a Microsoft code produce only one candidate.
    """
    candidates = {}
    for rows, weighted in ((primary_rows, True), (supplemental_rows, False)):
        for fields in rows:
            text, pinyin = fields[:2]
            if len(text) != 1 or ord(text) not in BASIC_CJK:
                continue
            if not re.fullmatch("[a-z]+", pinyin):
                continue
            code = microsoft_code(pinyin)
            weight = int(fields[2]) if weighted and len(fields) > 2 else 1
            key = (text, code)
            if key not in candidates or (weighted and weight > candidates[key]):
                candidates[key] = weight
    # Python's stable sort preserves source order for equal-weight candidates.
    rows = [[text, code, str(weight)] for (text, code), weight in
            sorted(candidates.items(), key=lambda item: -item[1])]
    readable = {text for text, _ in candidates}
    missing = [chr(codepoint) for codepoint in BASIC_CJK
               if chr(codepoint) not in readable]
    return rows, missing


def source_algebra(root):
    """Reuse the repository's Xiaohe spelling algebra, including vowel aliases."""
    text = (root / "double_pinyin_flypy.schema.yaml").read_text(encoding="utf-8")
    block = text.split("\nspeller:", 1)[1].split("\n  algebra:", 1)[1]
    rules = []
    for line in block.splitlines():
        value = line.strip()
        if value.startswith("- "):
            rules.append(value[2:].split("  #", 1)[0].strip())
    return rules


def apply_algebra(pinyin, rules):
    forms = {pinyin}
    for rule in rules:
        op, pattern, *rest = rule.split("/")
        if op == "xlit":
            translation = str.maketrans(pattern, rest[0])
            forms = {value.translate(translation) for value in forms}
        elif op in ("xform", "derive"):
            replacement = re.sub(r"\$(\d+)", r"\\g<\1>", rest[0])
            changed = {re.sub(pattern, replacement, value) for value in forms}
            forms = forms | changed if op == "derive" else changed
        elif op == "erase":
            forms = {value for value in forms if not re.search(pattern, value)}
        else:
            raise ValueError("unsupported source algebra: " + rule)
    return forms


def build_phonetic_map(root):
    rules = source_algebra(root)
    syllables = set()
    readings = defaultdict(set)
    for name in ("8105", "41448"):
        for fields in dictionary_rows(root / "cn_dicts" / (name + ".dict.yaml")):
            text, pinyin = fields[:2]
            if len(text) == 1 and re.fullmatch("[a-z]+", pinyin):
                syllables.add(pinyin)
                readings[text].add(pinyin)
    mapping = dict(SPECIAL_SYLLABLES)
    for syllable in sorted(syllables):
        target = microsoft_code(syllable)
        for code in apply_algebra(syllable, rules):
            if len(code) != 2:
                raise ValueError("source syllable is not two keys: " + syllable)
            if code in mapping and mapping[code] != target:
                raise ValueError("ambiguous source code: {} -> {}, {}".format(code, mapping[code], target))
            mapping[code] = target
    return mapping, readings, rules


def convert_initial(initial):
    return "o" if initial in "aeo" else initial


class Converter:
    def __init__(self, mapping):
        self.mapping = mapping
        self.stats = Counter()
        self.fixed = Counter()

    def syllable(self, code):
        if code not in self.mapping:
            raise ValueError("unknown two-key source syllable: " + code)
        if code in SPECIAL_SYLLABLES:
            self.stats["special_syllable"] += 1
        return self.mapping[code]

    def convert(self, text, code, layer):
        if (text, code) in FIXED_ENTRIES:
            self.fixed[(text, code)] += 1
            self.stats["fixed_mnemonic"] += 1
            return code
        if len(code) == 1:
            self.stats["fixed_one_key"] += 1
            return code
        # Ignore punctuation when applying the phrase's first/last Han rules.
        han_text = "".join(char for char in text if is_han(char))
        ordinary = bool(han_text) and all(is_han(char) or unicodedata.category(char).startswith("P") for char in text)
        if not ordinary or not re.fullmatch("[a-z]{2,4}", code):
            self.stats["fixed_literal"] += 1
            return code
        count = len(han_text)
        if count == 1:
            self.stats["single_character"] += 1
            return self.syllable(code[:2]) + code[2:]
        if layer == "whimsicality":
            # Two initials plus a mnemonic shape key; shape is never remapped.
            self.stats["whimsical_phrase"] += 1
            return "".join(convert_initial(c) for c in code[:2]) + code[2:]
        if len(code) == 4:
            if count == 2:
                result = self.syllable(code[:2]) + self.syllable(code[2:])
            elif count == 3:
                result = "".join(convert_initial(c) for c in code[:2]) + self.syllable(code[2:])
            else:
                result = "".join(convert_initial(c) for c in code)
            self.stats["full_phrase"] += 1
            return result
        if len(code) == 3 and count == 2:
            self.stats["three_key_two_character"] += 1
            return self.syllable(code[:2]) + convert_initial(code[2])
        self.stats["initial_abbreviation"] += 1
        return "".join(convert_initial(c) for c in code)


def header(name):
    return (
        "# Rime dictionary\n# encoding: utf-8\n"
        "# Generated by others/script/generate_mspy_xh.py; edit the Xiaohe source tables.\n"
        "# Microsoft double pinyin + original Xiaohe shapes; source candidate order retained.\n\n"
        "---\nname: {}\nversion: \"1\"\nsort: original\n"
        "use_preset_vocabulary: false\n...\n"
    ).format(name)


def generated_files(root):
    mapping, readings, rules = build_phonetic_map(root)
    converter = Converter(mapping)
    outputs = {}
    pinyin_rows, missing_basic = build_basic_pinyin_rows(
        dictionary_rows(root / "cn_dicts/8105.dict.yaml"),
        dictionary_rows(root / "cn_dicts/41448.dict.yaml"),
    )
    outputs[Path("mspy_xh_pinyin.dict.yaml")] = (
        "# Rime dictionary\n# encoding: utf-8\n"
        "# Generated by others/script/generate_mspy_xh.py.\n"
        "# Basic CJK readings from cn_dicts/8105.dict.yaml and 41448.dict.yaml;\n"
        "# Microsoft double pinyin only, without invented shape codes.\n\n"
        "---\nname: mspy_xh_pinyin\nversion: \"1\"\nsort: by_weight\n"
        "use_preset_vocabulary: false\n...\n"
    ) + "".join("\t".join(row) + "\n" for row in pinyin_rows)
    converted = {}
    missing_reading = []
    for layer in LAYERS:
        suffix = ".yaml" if layer == "full.code.chars" else ".dict.yaml"
        source = root / "xhup_dicts" / ("xhup." + layer + suffix)
        result = []
        for fields in dictionary_rows(source):
            text, code = fields[:2]
            try:
                new_code = converter.convert(text, code, layer)
            except ValueError as exc:
                raise ValueError("{}: {!r} {}: {}".format(source.name, text, code, exc)) from exc
            result.append([text, new_code] + fields[2:])
            if len(text) == 1 and is_han(text) and len(code) == 4:
                if not any(code[:2] in apply_algebra(p, rules) for p in readings[text]):
                    missing_reading.append((text, code, new_code))
        converted[layer] = result
        name = "mspy_xh." + layer
        outputs[Path("mspy_xh_dicts") / (name + ".dict.yaml")] = header(name) + "".join("\t".join(row) + "\n" for row in result)

    # Wildcards refer to the enabled default character tables only.
    reverse_rows = []
    reverse_seen = set()
    active = [row for layer in DEFAULT_LAYERS for row in converted[layer]]
    for text, code, *_ in active:
        if len(text) != 1 or not is_han(text) or not re.fullmatch("[a-z][a-z;]{3}", code):
            continue
        for mask in range(1, 16):
            wildcard = "".join("`" if mask & (1 << i) else char for i, char in enumerate(code))
            key = (text, wildcard)
            if key not in reverse_seen:
                reverse_seen.add(key)
                reverse_rows.append("{}\t{}\n".format(*key))
    outputs[Path("mspy_xh_reverse.dict.yaml")] = header("mspy_xh_reverse") + "".join(reverse_rows)

    actual_codes = defaultdict(list)
    for text, code, *_ in active:
        if len(code) < 4 and code not in actual_codes[text]:
            actual_codes[text].append(code)
    hints = []
    for fields in dictionary_rows_for_hints(root / "opencc" / "short_hints.txt"):
        text = fields[0]
        if actual_codes[text]:
            shortest = min(actual_codes[text], key=len)
            hints.append("{}\t{}\n".format(text, shortest))
    outputs[Path("opencc/mspy_xh_short_hints.txt")] = "".join(hints)
    hint_dict = {"type": "text", "file": "mspy_xh_short_hints.txt"}
    hint_config = {
        "name": "微软双拼音形简码提示",
        "segmentation": {"type": "mmseg", "dict": hint_dict},
        "conversion_chain": [{"dict": hint_dict}],
    }
    outputs[Path("opencc/mspy_xh_short_hints.json")] = json.dumps(hint_config, ensure_ascii=False, indent=2) + "\n"
    return outputs, converted, converter, missing_reading, missing_basic


def dictionary_rows_for_hints(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            yield line.split("\t")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--check", action="store_true", help="check generated files without writing")
    args = parser.parse_args()
    try:
        outputs, layers, converter, missing, missing_basic = generated_files(args.root)
    except (ValueError, OSError) as exc:
        parser.exit(1, "conversion failed: {}\n".format(exc))
    stale = []
    for relative, content in outputs.items():
        target = args.root / relative
        if args.check:
            if not target.exists() or target.read_bytes() != content.encode("utf-8"):
                stale.append(str(relative))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content.encode("utf-8"))
    for layer, entries in layers.items():
        print("{}: {} entries".format(layer, len(entries)))
    print("Conversion categories:", dict(sorted(converter.stats.items())))
    print("Fixed mnemonics:", ["{} {}".format(*entry) for entry in sorted(converter.fixed)])
    print("Character reading absent/mismatched; converted by source syllable:", sorted(set(missing)))
    print("Basic CJK U+4E00–U+9FFF: {} total, {} double-pinyin input, {} without pinyin".format(
        len(BASIC_CJK), len(BASIC_CJK) - len(missing_basic), len(missing_basic)))
    print("Basic CJK without pinyin:", " ".join("U+{:04X}".format(ord(char))
                                            for char in missing_basic))
    if stale:
        print("Stale generated files:\n" + "\n".join(stale), file=sys.stderr)
        return 1
    print("{} {} generated files".format("Verified" if args.check else "Wrote", len(outputs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
