"""Execute the fixed course GateANN adapter with a calibrated workload budget."""
import argparse
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--bucket", choices=["low", "medium", "high"], required=True)
    parser.add_argument("--course-root", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    policy = json.loads(args.policy.read_text(encoding="utf-8"))[args.bucket]
    if policy is None:
        raise SystemExit("Recall target not reached during calibration; refusing execution")
    command = ["python3", str(args.course_root / "adapters/gateann_adapter.py"), "search",
               "--repo", str(args.repo), "--dataset-root", str(args.dataset_root),
               "--run-root", str(args.run_root), "--tier", "formal", "--bucket", args.bucket,
               "--L", str(policy["L"]), "--threads", "1", "--beamwidth", "8", "--k", "10",
               "--full-adj-neighbors", "32", "--run-id", args.run_id]
    if args.dry_run:
        print(json.dumps(command))
    else:
        subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
