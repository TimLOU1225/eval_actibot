#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./generate_summary.sh <path_to_results.json> [threshold]"
    exit 1
fi

RESULTS_PATH="$1"
THRESHOLD=${2:-40.0}

if [ ! -f "$RESULTS_PATH" ]; then
    echo "Error: File $RESULTS_PATH not found!"
    exit 1
fi

DIR_NAME=$(dirname "$RESULTS_PATH")
SUMMARY_PATH="$DIR_NAME/summary.json"

python3 - <<PY_SCRIPT
import json
import os

results_path = "$RESULTS_PATH"
summary_path = "$SUMMARY_PATH"
threshold = float("$THRESHOLD")

try:
    with open(results_path, "r") as f:
        results = json.load(f)
except Exception as e:
    print(f"Error reading {results_path}: {e}")
    exit(1)

total_num = len(results)

if total_num == 0:
    print("Warning: No episodes found in results.")
    exit(0)

success_count_original = sum(1 for ep in results if ep.get("success_score", 0) == 1)
success_count_threshold = 0

total_duration = 0.0
success_duration = 0.0
fail_duration = 0.0

max_consecutive_successes = 0
current_consecutive_successes = 0

for ep in results:
    base_score = ep.get("success_score", 0)
    dur = ep.get("duration", 0.0)
    
    # 超过阈值标记为失败
    score = 0 if dur > threshold else base_score
    
    total_duration += dur
    
    if score == 1:
        success_count_threshold += 1
        success_duration += dur
        current_consecutive_successes += 1
        if current_consecutive_successes > max_consecutive_successes:
            max_consecutive_successes = current_consecutive_successes
    else:
        fail_duration += dur
        current_consecutive_successes = 0

success_rate_original = success_count_original / total_num
success_rate_threshold = success_count_threshold / total_num

avg_duration = total_duration / total_num
avg_success_duration = success_duration / success_count_threshold if success_count_threshold > 0 else 0.0
fail_count = total_num - success_count_threshold
avg_fail_duration = fail_duration / fail_count if fail_count > 0 else 0.0

summary = {
    "total_episodes": total_num,
    "success_rate_original": round(success_rate_original, 4),
    "success_rate_threshold": round(success_rate_threshold, 4),
    "threshold_used": threshold,
    "avg_duration": round(avg_duration, 2),
    "avg_success_duration": round(avg_success_duration, 2),
    "avg_fail_duration": round(avg_fail_duration, 2),
    "max_consecutive_successes": max_consecutive_successes
}

with open(summary_path, "w") as f:
    json.dump(summary, f, indent=4)

print(f"Summary generated at: {summary_path}")
print(json.dumps(summary, indent=4))
PY_SCRIPT
