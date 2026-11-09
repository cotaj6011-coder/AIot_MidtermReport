from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/historical/parking_birmingham/dataset.csv"
OUTPUT = ROOT / "data/uci_quality_report.json"


def analyze(path: Path = SOURCE) -> dict:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    exact_duplicates = len(rows) - len({tuple(sorted(row.items())) for row in rows})
    facilities: dict[str, list[datetime]] = defaultdict(list)
    missing_cells = 0
    for row in rows:
        missing_cells += sum(value.strip() == "" for value in row.values())
        facilities[row["SystemCodeNumber"]].append(datetime.strptime(row["LastUpdated"], "%Y-%m-%d %H:%M:%S"))
    gaps = Counter()
    facility_stats = {}
    for facility, timestamps in sorted(facilities.items()):
        ordered = sorted(set(timestamps))
        intervals = [int((b - a).total_seconds() // 60) for a, b in zip(ordered, ordered[1:])]
        gaps.update(interval for interval in intervals if interval > 30)
        facility_stats[facility] = {
            "rows": len(timestamps),
            "unique_timestamps": len(ordered),
            "start": ordered[0].isoformat(sep=" "),
            "end": ordered[-1].isoformat(sep=" "),
            "gaps_over_30_minutes": sum(interval > 30 for interval in intervals),
        }
    return {
        "source": str(path.relative_to(ROOT)),
        "rows": len(rows),
        "columns": list(rows[0]),
        "facilities": len(facilities),
        "missing_cells": missing_cells,
        "exact_duplicate_rows": exact_duplicates,
        "date_start": min(min(values) for values in facilities.values()).isoformat(sep=" "),
        "date_end": max(max(values) for values in facilities.values()).isoformat(sep=" "),
        "facility_row_range": [min(map(len, facilities.values())), max(map(len, facilities.values()))],
        "gap_minutes_over_30": dict(sorted(gaps.items())),
        "per_facility": facility_stats,
    }


if __name__ == "__main__":
    report = analyze()
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "per_facility"}, ensure_ascii=False, indent=2))

