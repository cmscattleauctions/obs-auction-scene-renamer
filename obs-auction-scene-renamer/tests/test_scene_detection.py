import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.parse_obs import find_lot_scene_pairs


class TestSceneDetection(unittest.TestCase):
    def test_find_scene_pairs(self):
        scene_names = [
            "CMS Logo",
            "401-A Transition",
            "401-A Video",
            "Option Lot Interlude 1",
            "402 Transition",
            "402 Video",
        ]
        slots = find_lot_scene_pairs(scene_names)
        self.assertEqual(len(slots), 2)
        self.assertEqual(slots[0].transition_name, "401-A Transition")
        self.assertEqual(slots[1].video_name, "402 Video")


if __name__ == "__main__":
    unittest.main()
