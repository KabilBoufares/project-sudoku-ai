# Sudoku AI Comparator

##  Project Objective

This project is a **Sudoku AI Comparator**: a web-based dashboard to compare the performance of various AI algorithms for solving Sudoku puzzles. It provides visualizations, metrics, and automated analysis for each algorithm and difficulty level.

---

##  Application Architecture

```
project-sudoku-ai/
│
├── data/                # Datasets (CSV) for each difficulty (generated with sudoku generator)
│
├── docs/                # Documentation (optional)
│
├── scripts/
│   ├── main.py          # Runs all algorithms for a given difficulty, saves results as JSON
│   ├── run_solver.py    # CLI: generates results and launches the web server
│   └── server.py        # Flask web server serving the dashboard and triggering computation
│
├── src/
│   ├── algorithms/      # All AI algorithms (Backtracking, DFS, BFS, A*, Beam, Hill Climbing, etc.)
│   ├── core/            # Core logic (SudokuGrid class, validator)
│   ├── results/         # (Optional) Logs or extra results
│   └── utils/           # Utilities (dataset loader, sudoku generator)
│
├── web_interface/
│   ├── index.html       # Main dashboard UI
│   ├── styles.css       # Styling
│   ├── js/              # Frontend logic (charts, grid rendering, analysis, etc.)
│   └── data/            # Results JSON files for each difficulty (used by the dashboard)
│
└── README.md            # This file
```

---

##  How to Run

### 1. **Install dependencies**

- Python 3.8+
- Flask (`pip install flask`)

### 2. **Generate Results & Launch Server**

From the project root, run:

```sh
python scripts/run_solver.py --level Expert
```

- This will generate results for the selected difficulty (`Easy`, `Medium`, `Hard`, `Expert`) and launch the web dashboard at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

- You can also run the server directly:

```sh
python scripts/server.py
```

And trigger new runs from the web interface.

---

##  Web Dashboard

- **Select Difficulty:** Choose a level and view algorithm performance.
- **Run Level:** Regenerate results for the selected difficulty.
- **Run All:** (Future) Run all levels in batch.
- **Visualizations:** Charts for time, conflicts, memory, and success rate.
- **Comparison Table:** Detailed metrics per algorithm.
- **Automated Analysis:** Insights and highlights.

---

##  Dataset

- Datasets (`easy.csv`, `medium.csv`, `hard.csv`, `expert.csv`) are generated using the Sudoku generator in [`src/utils/generator.py`](src/utils/generator.py).
- Each CSV contains puzzles, solutions, and difficulty scores.

---

##  Algorithms

Implemented in [`src/algorithms/`](src/algorithms/):

- Backtracking, DFS, BFS (Blind Search)
- A*, Beam Search, A* + Backtracking (Informed Search)
- Hill Climbing, Hill Climbing + Restart (Local Search)
- (Extendable for CSP and other methods)

---

##  Extending

- Add new algorithms in `src/algorithms/` and register them in [`src/algorithms/__init__.py`](src/algorithms/__init__.py).
- Add new metrics or visualizations in the frontend (`web_interface/js/`).

---

##  References

- Sudoku generator: [`src/utils/generator.py`](src/utils/generator.py)
- Dataset loader: [`src/utils/loader.py`](src/utils/loader.py)
- Core grid logic: [`src/core/grid.py`](src/core/grid.py)
