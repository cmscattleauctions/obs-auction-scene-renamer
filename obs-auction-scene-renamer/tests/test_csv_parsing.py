import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.parse_csv import build_scene_base_name


class TestCsvParsing(unittest.TestCase):
    def test_build_scene_base_name_with_option_appended(self):
        self.assertEqual(build_scene_base_name("401A", "A"), "401-A")

    def test_build_scene_base_name_with_blank_option(self):
        self.assertEqual(build_scene_base_name("402", ""), "402")

    def test_build_scene_base_name_with_hyphenated_option(self):
        self.assertEqual(build_scene_base_name("401-A", "A"), "401-A")


if __name__ == "__main__":
    unittest.main()
