import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.parse_csv import LotEntry
from src.parse_obs import SceneSlotPair
from src.rename_slots import apply_scene_renames


class TestRenaming(unittest.TestCase):
    def test_apply_scene_renames_marks_unused_slots(self):
        obs = {
            "scene_order": [
                {"name": "401-A Transition"},
                {"name": "401-A Video"},
                {"name": "402 Transition"},
                {"name": "402 Video"},
            ],
            "sources": [
                {"name": "401-A Transition"},
                {"name": "401-A Video"},
                {"name": "402 Transition"},
                {"name": "402 Video"},
            ],
        }
        slots = [
            SceneSlotPair(index=1, transition_name="401-A Transition", video_name="401-A Video"),
            SceneSlotPair(index=2, transition_name="402 Transition", video_name="402 Video"),
        ]
        lots = [LotEntry(raw_lot_number="501A", option="A", scene_base_name="501-A", row_number=2)]
        report = apply_scene_renames(obs, slots, lots)
        self.assertEqual(report.used_slots, 1)
        self.assertEqual(obs["scene_order"][0]["name"], "501-A Transition")
        self.assertEqual(obs["scene_order"][2]["name"], "UNUSED 001 Transition")


if __name__ == "__main__":
    unittest.main()
