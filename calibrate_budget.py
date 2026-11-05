"""Calibrate per-workload search budgets using observed recall and latency."""
import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path


def calibrate(rows, target=90.0, system="gateann"):
    groups = defaultdict(list)
    for row in rows:
        if row["system"] == system:
            groups[(row["bucket"], int(row["L"]))].append(row)
    candidates = defaultdict(list)
    for (bucket, budget), samples in groups.items():
        repeats = {row.get("repeat") or row.get("run_id") for row in samples}
        if len(repeats) < 3:
            raise ValueError(f"Need three independent repeats for {bucket}, L={budget}")
        candidates[bucket].append({
            "L": budget,
            "recall_median": statistics.median(float(r["recall_percent"]) for r in samples),
            "recall_min": min(float(r["recall_percent"]) for r in samples),
            "latency_us_median": statistics.median(float(r["mean_latency_us"]) for r in samples),
        })
    selected = {}
    for bucket, options in candidates.items():
        feasible = [option for option in options if option["recall_min"] >= target]
        selected[bucket] = min(feasible, key=lambda option: option["latency_us_median"]) if feasible else None
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_files", nargs="+", type=Path)
    parser.add_argument("--target", type=float, default=90.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for path in args.csv_files:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            rows.extend(csv.DictReader(stream))
    args.output.write_text(json.dumps(calibrate(rows, args.target), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
