from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass
class LotEntry:
    raw_lot_number: str
    option: str
    scene_base_name: str
    row_number: int


def _clean(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() == "nan":
        return ""
    return text


def _normalize_option(option_value: str) -> str:
    option = _clean(option_value).upper()
    if not option:
        return ""
    # Keep a single leading alpha/number token if someone typed extra text.
    if len(option) == 1:
        return option
    return option.split()[0]


def build_scene_base_name(lot_number: str, option: str) -> str:
    lot = _clean(lot_number).upper().replace(" ", "")
    opt = _normalize_option(option)

    if not lot:
        raise ValueError("Lot number is empty.")

    if not opt:
        return lot

    # If the lot number already ends with the option letter, convert 401A -> 401-A.
    if lot.endswith(opt) and len(lot) > len(opt):
        core = lot[: -len(opt)]
        if core.endswith("-"):
            return f"{core}{opt}"
        return f"{core}-{opt}"

    # If the lot number already has the hyphenated option, keep it.
    if lot.endswith(f"-{opt}"):
        return lot

    return f"{lot}-{opt}"


def load_lots_from_csv(csv_path: str | Path) -> List[LotEntry]:
    csv_path = Path(csv_path)
    entries: List[LotEntry] = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []

        lot_field = _find_field(fieldnames, ["Lot Number", "Lot", "LotNumber"])
        option_field = _find_field(fieldnames, ["Option", "Opt"])

        if lot_field is None:
            raise ValueError(
                "Could not find a lot number column. Expected a column like 'Lot Number'."
            )

        for row_index, row in enumerate(reader, start=2):
            raw_lot = _clean(row.get(lot_field))
            raw_option = _clean(row.get(option_field)) if option_field else ""

            if not raw_lot:
                continue

            scene_base = build_scene_base_name(raw_lot, raw_option)
            entries.append(
                LotEntry(
                    raw_lot_number=raw_lot,
                    option=raw_option,
                    scene_base_name=scene_base,
                    row_number=row_index,
                )
            )

    if not entries:
        raise ValueError("No usable lot rows were found in the CSV.")

    return entries


def _find_field(fieldnames: Iterable[str], candidates: Iterable[str]) -> Optional[str]:
    normalized = {name.strip().lower(): name for name in fieldnames if name}
    for candidate in candidates:
        key = candidate.strip().lower()
        if key in normalized:
            return normalized[key]
    return None
