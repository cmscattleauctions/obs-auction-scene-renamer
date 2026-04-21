from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SCENE_SLOT_PATTERN = re.compile(r"^(\d{3,4}(?:-[A-Z])?)\s+(Transition|Video)$", re.IGNORECASE)


@dataclass
class SceneSlotPair:
    index: int
    transition_name: str
    video_name: str


@dataclass
class ObsCollection:
    data: dict
    slot_pairs: List[SceneSlotPair]


def load_obs_collection(json_path: str | Path) -> ObsCollection:
    json_path = Path(json_path)
    with json_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    scene_order = data.get("scene_order", [])
    names = [entry.get("name", "") for entry in scene_order if isinstance(entry, dict)]
    slot_pairs = find_lot_scene_pairs(names)

    if not slot_pairs:
        raise ValueError(
            "No lot scene pairs were detected in the OBS export. "
            "Expected scene names like '401-A Transition' and '401-A Video'."
        )

    return ObsCollection(data=data, slot_pairs=slot_pairs)


def save_obs_collection(data: dict, json_path: str | Path) -> None:
    json_path = Path(json_path)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=4)


def find_lot_scene_pairs(scene_names: Iterable[str]) -> List[SceneSlotPair]:
    slots: List[SceneSlotPair] = []
    scene_names = list(scene_names)

    i = 0
    slot_index = 1
    while i < len(scene_names) - 1:
        current = _normalize_spaces(scene_names[i])
        nxt = _normalize_spaces(scene_names[i + 1])
        cur_match = SCENE_SLOT_PATTERN.match(current)
        nxt_match = SCENE_SLOT_PATTERN.match(nxt)

        if cur_match and nxt_match:
            cur_base, cur_kind = cur_match.groups()
            nxt_base, nxt_kind = nxt_match.groups()
            if cur_kind.lower() == "transition" and nxt_kind.lower() == "video" and cur_base == nxt_base:
                slots.append(
                    SceneSlotPair(
                        index=slot_index,
                        transition_name=scene_names[i],
                        video_name=scene_names[i + 1],
                    )
                )
                slot_index += 1
                i += 2
                continue

        i += 1

    return slots


def _normalize_spaces(text: str) -> str:
    return " ".join(str(text).split())
