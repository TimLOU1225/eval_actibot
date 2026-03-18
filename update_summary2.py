import json
import os

folders = ["eval_actibot/orin_0311_test", "eval_actibot/good data"]

for folder in folders:
    results_file = os.path.join(folder, "results.json")
    if not os.path.exists(results_file):
        print(f"Results file not found for {folder}")
        continue
        
    try:
        with open(results_file, "r") as f:
            results = json.load(f)
    except Exception as e:
        print(e)
        results = []
        
    total_num = len(results)
    
    success_count = sum(1 for ep in results if ep.get("success_score") == 1)
    
    total_dur = sum(ep.get("duration", 0) for ep in results)
    success_dur = sum(ep.get("duration", 0) for ep in results if ep.get("success_score") == 1)
    fail_dur = sum(ep.get("duration", 0) for ep in results if ep.get("success_score") != 1)

    max_consecutive_successes = 0
    current_consecutive_successes = 0

    for ep in results:
        score = ep.get("success_score", 0)
        
        if score == 1:
            current_consecutive_successes += 1
            if current_consecutive_successes > max_consecutive_successes:
                max_consecutive_successes = current_consecutive_successes
        else:
            current_consecutive_successes = 0

    success_rate = success_count / total_num if total_num > 0 else 0.0
    avg_duration = total_dur / total_num if total_num > 0 else 0.0
    avg_success_duration = success_dur / success_count if success_count > 0 else 0.0
    fail_count = total_num - success_count
    avg_fail_duration = fail_dur / fail_count if fail_count > 0 else 0.0
    
    summary = {
        "total_episodes": total_num,
        "success_rate": round(success_rate, 4),
        "avg_duration": round(avg_duration, 2),
        "avg_success_duration": round(avg_success_duration, 2),
        "avg_fail_duration": round(avg_fail_duration, 2),
        "max_consecutive_successes": max_consecutive_successes
    }
    
    summary_file = os.path.join(folder, "summary.json")
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=4)
        
    print(f"Updated summary for {folder}")
