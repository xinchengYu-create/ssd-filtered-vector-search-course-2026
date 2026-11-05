# Search-budget calibration for the SSD filtered-vector-search course

This repository implements an **offline workload-specific GateANN budget policy**, together with the commands needed to reproduce calibration. It complements the course baseline and does not modify either system's search implementation.

## Reproduce

Use the course repository and its exact commits, prepare its dataset/indexes and run all 30 official measurements first. Then run GateANN on Low with L=640,1280,2560,5120 and on Medium with L=640,1280, repeating each setting three times. Save a `run_id` for each repetition in the supplementary CSV.

```sh
python3 calibrate_budget.py official_results.csv supplement.csv --target 90 --output budget_policy.json
python3 run_policy.py --help
```

The calibration selects the lowest-median-latency tested configuration whose **minimum measured Recall across three repeats** reaches the target. An unmet target returns null, and execution refuses that workload. This is offline calibration on the measured queries. Generalization to unseen queries and labels requires a separate held-out experiment. The policy is not a new graph-search algorithm.

The course source, data, indexes and machine-specific credentials are not included.

Course repository: https://gitee.com/wei-fangyu/fvs-course-lab
