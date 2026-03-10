# Actibot Evaluation UI

A local web dashboard built with vanilla JavaScript and FastAPI to record success rate (SR) and duration for robot evaluation episodes.

## Features

- **Task Creation**: Creates a local `<task_name>/results.json` log automatically.
- **Stopwatch Timer**: Records episode execution duration inside your browser.
- **Score Logging**: Choose between `1 - Success` and `0 - Fail` after each episode (Default fallback: 0).
- **Session Summaries**: Generates a `summary.json` (Total episodes, Average Success rate) when finishing a task.

---

## 🚀 Environment Setup

The application relies on a python environment to run the backend server. It is recommended to run this inside a virtual environment.

### Option 1: Conda (Recommended)

1. **Create and activate a new Conda environment:**

```bash
conda create -n eval_ui python=3.10 -y
conda activate eval_ui
```

1. **Install requirements:**

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Option 2: Python venv

1. **Create a virtual environment:**

```bash
python3 -m venv venv
```

1. **Activate it:**

```bash
source venv/bin/activate
```

1. **Install requirements:**

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 💻 Running the UI

Once the dependencies are installed and the environment is **activated**, you can launch the UI by running the helper script:

```bash
chmod +x run.sh
./run.sh
```

You will see output indicating the server has started.
Open **<http://127.0.0.1:{port}/static/index.html>** in your preferred browser to use the dashboard!
