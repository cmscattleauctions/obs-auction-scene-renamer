from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from src.parse_csv import LotEntry
from src.parse_obs import SceneSlotPair


@dataclass
class RenameReport:
    used_slots: int
    unused_slots: int
    total_slots: int
    lots_in_csv: int
    rename_map: Dict[str, str]


def apply_scene_renames(obs_data: dict, slots: List[SceneSlotPair], lots: List[LotEntry]) -> RenameReport:
    if len(lots) > len(slots):
        raise ValueError(
            f"The CSV contains {len(lots)} lot entries, but the OBS template only has {len(slots)} lot slots. "
            "Add more backup slot scenes to the OBS template and try again."
        )

    rename_map: Dict[str, str] = {}

    for slot, lot in zip(slots, lots):
        rename_map[slot.transition_name] = f"{lot.scene_base_name} Transition"
        rename_map[slot.video_name] = f"{lot.scene_base_name} Video"

    remaining_slots = slots[len(lots):]
    for idx, slot in enumerate(remaining_slots, start=1):
        unused_name = f"UNUSED {idx:03d}"
        rename_map[slot.transition_name] = f"{unused_name} Transition"
        rename_map[slot.video_name] = f"{unused_name} Video"

    _ensure_no_duplicates(rename_map)
    renamed_data = _deep_replace_exact_strings(obs_data, rename_map)
    obs_data.clear()
    obs_data.update(renamed_data)

    return RenameReport(
        used_slots=len(lots),
        unused_slots=len(remaining_slots),
        total_slots=len(slots),
        lots_in_csv=len(lots),
        rename_map=rename_map,
    )


def _ensure_no_duplicates(rename_map: Dict[str, str]) -> None:
    new_names = list(rename_map.values())
    if len(new_names) != len(set(new_names)):
        duplicates = sorted({name for name in new_names if new_names.count(name) > 1})
        raise ValueError(f"Duplicate target scene names were generated: {duplicates}")


def _deep_replace_exact_strings(value: Any, rename_map: Dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {key: _deep_replace_exact_strings(val, rename_map) for key, val in value.items()}
    if isinstance(value, list):
        return [_deep_replace_exact_strings(item, rename_map) for item in value]
    if isinstance(value, str):
        return rename_map.get(value, value)
    return value
