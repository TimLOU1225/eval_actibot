from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import json
from typing import Optional

app = FastAPI()

# Mount the static directory for index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class TaskCreate(BaseModel):
    task_name: str

class EpisodeData(BaseModel):
    task_name: str
    index: int
    success_score: int
    duration: float
    ps: Optional[float] = None

@app.post("/create_task")
async def create_task(task_data: TaskCreate):
    task_name = task_data.task_name
    if not task_name:
        raise HTTPException(status_code=400, detail="Task name cannot be empty")
    
    task_dir = os.path.join(BASE_DIR, task_name)
    if not os.path.exists(task_dir):
        os.makedirs(task_dir)
    
    results_file = os.path.join(task_dir, "results.json")
    if not os.path.exists(results_file):
        with open(results_file, "w") as f:
            json.dump([], f)
            
    return {"message": "Task created successfully", "task_name": task_name}

@app.post("/save_episode")
async def save_episode(data: EpisodeData):
    task_dir = os.path.join(BASE_DIR, data.task_name)
    if not os.path.exists(task_dir):
        raise HTTPException(status_code=404, detail="Task folder not found. Create task first.")
        
    results_file = os.path.join(task_dir, "results.json")
    
    # Read existing results
    try:
        with open(results_file, "r") as f:
            results = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        results = []
        
    # Append new episode
    new_episode = {
        "index": data.index,
        "success_score": data.success_score,
        "duration": data.duration,
        "ps": data.ps
    }
    results.append(new_episode)
    
    # Save back to file
    with open(results_file, "w") as f:
        json.dump(results, f, indent=4)
        
    return {"message": "Episode saved successfully", "episode": new_episode}

@app.get("/stats/{task_name}")
async def get_stats(task_name: str):
    task_dir = os.path.join(BASE_DIR, task_name)
    results_file = os.path.join(task_dir, "results.json")
    
    if not os.path.exists(results_file):
        return {"total_num": 0, "success_rate": 0.0, "next_index": 1}
        
    try:
        with open(results_file, "r") as f:
            results = json.load(f)
    except json.JSONDecodeError:
        results = []
        
    total_num = len(results)
    if total_num == 0:
        return {"total_num": 0, "success_rate": 0.0, "next_index": 1}
        
    success_count = sum(1 for ep in results if ep.get("success_score") == 1)
    success_rate = success_count / total_num
    
    next_index = max((ep.get("index", 0) for ep in results), default=0) + 1
    
    return {
        "total_num": total_num,
        "success_rate": success_rate,
        "next_index": next_index
    }

class TaskFinish(BaseModel):
    task_name: str

@app.post("/finish_task")
async def finish_task(data: TaskFinish):
    task_dir = os.path.join(BASE_DIR, data.task_name)
    results_file = os.path.join(task_dir, "results.json")
    
    if not os.path.exists(results_file):
        raise HTTPException(status_code=404, detail="No results found for task")
        
    try:
        with open(results_file, "r") as f:
            results = json.load(f)
    except json.JSONDecodeError:
        results = []
        
    total_num = len(results)
    
    success_count = 0
    total_duration = 0.0
    success_duration = 0.0
    fail_duration = 0.0
    
    max_consecutive_successes = 0
    current_consecutive_successes = 0

    for ep in results:
        score = ep.get("success_score", 0)
        dur = ep.get("duration", 0.0)
        
        total_duration += dur
        if score == 1:
            success_count += 1
            success_duration += dur
            current_consecutive_successes += 1
            if current_consecutive_successes > max_consecutive_successes:
                max_consecutive_successes = current_consecutive_successes
        else:
            fail_duration += dur
            current_consecutive_successes = 0

    success_rate = success_count / total_num if total_num > 0 else 0.0
    avg_duration = total_duration / total_num if total_num > 0 else 0.0
    avg_success_duration = success_duration / success_count if success_count > 0 else 0.0
    fail_count = total_num - success_count
    avg_fail_duration = fail_duration / fail_count if fail_count > 0 else 0.0
    
    summary = {
        "total_episodes": total_num,
        "success_rate": round(success_rate, 4),
        "avg_duration": round(avg_duration, 2),
        "avg_success_duration": round(avg_success_duration, 2),
        "avg_fail_duration": round(avg_fail_duration, 2),
        "max_consecutive_successes": max_consecutive_successes
    }
    
    summary_file = os.path.join(task_dir, "summary.json")
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=4)
        
    return {"message": "Task finished. Summary saved.", "summary": summary}
