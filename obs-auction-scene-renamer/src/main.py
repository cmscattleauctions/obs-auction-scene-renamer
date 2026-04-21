from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.parse_csv import load_lots_from_csv
from src.parse_obs import load_obs_collection, save_obs_collection
from src.rename_slots import apply_scene_renames


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rename OBS auction lot scenes from a monthly CSV."
    )
    parser.add_argument("--obs", required=True, help="Path to the exported OBS scene collection JSON file.")
    parser.add_argument("--csv", required=True, help="Path to the monthly auction CSV file.")
    parser.add_argument("--out", required=True, help="Path where the updated OBS JSON should be saved.")
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    obs_path = Path(args.obs)
    csv_path = Path(args.csv)
    out_path = Path(args.out)

    collection = load_obs_collection(obs_path)
    lots = load_lots_from_csv(csv_path)
    report = apply_scene_renames(collection.data, collection.slot_pairs, lots)
    save_obs_collection(collection.data, out_path)

    print("Done.")
    print(f"OBS lot slots found: {report.total_slots}")
    print(f"Lots read from CSV: {report.lots_in_csv}")
    print(f"Slots filled with current lots: {report.used_slots}")
    print(f"Overflow slots renamed to UNUSED: {report.unused_slots}")
    print(f"Output written to: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
