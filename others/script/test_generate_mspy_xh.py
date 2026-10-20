"""Behavioral regression checks for Microsoft phonetics + Xiaohe shapes."""

from pathlib import Path
import unittest

from generate_mspy_xh import (
    Converter, apply_algebra, build_basic_pinyin_rows, build_phonetic_map,
    microsoft_code,
)


ROOT = Path(__file__).resolve().parents[2]


class MicrosoftXiaoheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping, cls.readings, cls.rules = build_phonetic_map(ROOT)

    def setUp(self):
        self.converter = Converter(self.mapping)

    def test_canonical_zero_initial_and_umlaut(self):
        for pinyin, code in [("a", "oa"), ("an", "oj"), ("ai", "ol"),
                             ("ang", "oh"), ("er", "or"), ("lv", "ly"),
                             ("lve", "lt"), ("jue", "jt")]:
            with self.subTest(pinyin=pinyin):
                self.assertEqual(microsoft_code(pinyin), code)

    def test_shared_source_vowel_key_is_resolved_by_syllable(self):
        self.assertEqual(self.mapping["qk"], "q;")
        self.assertEqual(self.mapping["gk"], "gy")
        self.assertEqual(self.converter.convert("青", "qkfo", "primary"), "q;fo")
        self.assertEqual(self.converter.convert("好", "hcnz", "primary"), "hknz")
        self.assertEqual(self.converter.convert("按", "anfn", "primary"), "ojfn")

    def test_shape_keys_are_not_phonetic_keys(self):
        # k changes as an ing vowel, but the two shape keys remain k/x.
        self.assertEqual(self.converter.convert("哎", "aikx", "primary"), "olkx")
        self.assertEqual(self.converter.convert("按", "anf", "primary"), "ojf")

    def test_phrase_length_rules_and_punctuation(self):
        cases = [("你好", "nihc", "nihk"), ("按时", "anui", "ojui"),
                 ("二进制", "ejvi", "ojvi"),
                 ("阿尔巴尼亚", "aeby", "ooby"),
                 ("阿尔，巴尼亚", "aeby", "ooby")]
        for text, source, target in cases:
            with self.subTest(text=text):
                self.assertEqual(self.converter.convert(text, source, "primary"), target)

    def test_short_codes_and_whimsical_shape_suffix(self):
        self.assertEqual(self.converter.convert("安静", "aj", "primary"), "oj")
        self.assertEqual(self.converter.convert("爱好者", "ahv", "primary"), "ohv")
        self.assertEqual(self.converter.convert("安装", "a", "single.code"), "a")
        self.assertEqual(self.converter.convert("单元", "dye", "whimsicality"), "dye")
        self.assertEqual(self.converter.convert("音形", "yxk", "whimsicality"), "yxk")

    def test_official_special_syllables_and_mnemonics(self):
        self.assertEqual(self.converter.convert("呒", "omkw", "primary"), "omkw")
        self.assertEqual(self.converter.convert("鹤", "eh", "primary"), "eh")
        self.assertEqual(self.converter.convert("为什么", "wsme", "primary"), "wsme")
        self.assertEqual(self.converter.convert("𬇙", "pwdr", "primary"), "pzdr")
        self.assertEqual(self.converter.convert("https://flypy.cc", "xhg", "primary"), "xhg")

    def test_unknown_phonetic_code_is_not_silently_preserved(self):
        with self.assertRaisesRegex(ValueError, "unknown two-key source syllable"):
            self.converter.convert("甲", "qaab", "primary")

    def test_all_reading_aliases_keep_one_canonical_target(self):
        # Both source zero-initial spellings must yield the same MS syllable.
        for code in apply_algebra("an", self.rules):
            self.assertEqual(self.mapping[code], "oj")
        for code in apply_algebra("ju", self.rules):
            self.assertEqual(self.mapping[code], "ju")


class BasicCjkPinyinTests(unittest.TestCase):
    def test_only_basic_cjk_including_both_endpoints_is_emitted(self):
        rows, missing = build_basic_pinyin_rows(
            [[char, "yi", "10"] for char in
             ("\u3400", "\u4e00", "\u9fff", "\ua000", "一丁")],
            [],
        )
        self.assertEqual(rows, [["\u4e00", "yi", "10"], ["\u9fff", "yi", "10"]])
        self.assertNotIn("\u4e00", missing)
        self.assertNotIn("\u9fff", missing)
        self.assertTrue(all(0x4E00 <= ord(char) <= 0x9FFF for char in missing))

    def test_candidates_use_complete_canonical_microsoft_codes(self):
        rows, _ = build_basic_pinyin_rows(
            [["清", "qing", "5"], ["绿", "lv", "4"], ["雪", "xue", "3"],
             ["中", "zhong", "2"], ["安", "an", "1"]],
            [],
        )
        self.assertEqual([(text, code) for text, code, _ in rows],
                         [("清", "q;"), ("绿", "ly"), ("雪", "xt"),
                          ("中", "vs"), ("安", "oj")])
        for _, code, _ in rows:
            self.assertRegex(code, r"^[a-z][a-z;]$")

    def test_homophones_polyphones_and_colliding_readings_are_deduplicated(self):
        rows, _ = build_basic_pinyin_rows(
            [["重", "zhong", "100"], ["重", "zhong", "50"],
             ["种", "zhong", "30"], ["重", "chong", "20"],
             ["虐", "nve", "10"]],
            [["重", "zhong"], ["种", "zhong"], ["重", "chong"],
             ["虐", "nue"]],
        )
        self.assertEqual(rows, [["重", "vs", "100"], ["种", "vs", "30"],
                                ["重", "is", "20"], ["虐", "nt", "10"]])

    def test_primary_frequency_wins_and_equal_weights_keep_source_order(self):
        rows, _ = build_basic_pinyin_rows(
            [["时", "shi", "50"], ["是", "shi", "100"],
             ["实", "shi", "50"], ["诗", "shi", "0"]],
            [["狮", "shi", "999"], ["是", "shi", "999999"],
             ["诗", "shi", "999"]],
        )
        self.assertEqual(rows, [["是", "ui", "100"], ["时", "ui", "50"],
                                ["实", "ui", "50"], ["狮", "ui", "1"],
                                ["诗", "ui", "0"]])

    def test_absent_or_unparseable_readings_are_reported_not_invented(self):
        rows, missing = build_basic_pinyin_rows(
            [["一", "yi", "7"]],
            [["丁", "?"], ["丂", "yi ding"]],
        )
        self.assertEqual(rows, [["一", "yi", "7"]])
        self.assertNotIn("一", missing)
        self.assertIn("丁", missing)
        self.assertIn("丂", missing)
        self.assertIn("七", missing)
        self.assertEqual(len(missing), 0xA000 - 0x4E00 - 1)


if __name__ == "__main__":
    unittest.main()
