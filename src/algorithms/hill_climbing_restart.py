from typing import Tuple
from src.core.grid import SudokuGrid
from src.algorithms.hill_climbing import HillClimbingSolver

class HillClimbingWithRestart:
    def __init__(self, grid, max_restarts=10, max_iterations=10000):
        self.original_grid = grid
        self.max_restarts = max_restarts
        self.max_iterations = max_iterations
        self.best_grid = None
        self.best_conflicts = float("inf")
        self.total_iterations = 0

    def solve(self) -> bool:
        for _ in range(self.max_restarts):
            solver = HillClimbingSolver(self.original_grid)
            success = solver.solve(max_iterations=self.max_iterations)
            self.total_iterations += solver.iterations

            if solver.conflicts < self.best_conflicts:
                self.best_conflicts = solver.conflicts
                self.best_grid = solver.grid

            if success:
                return True  # early success

        return self.best_conflicts == 0

# 🔁 Interface standard pour main.py
def solve(sudoku_grid: SudokuGrid) -> Tuple[SudokuGrid, int]:
    solver = HillClimbingWithRestart(sudoku_grid.grid, max_restarts=10, max_iterations=1000)
    solver.solve()
    return SudokuGrid(solver.best_grid), solver.total_iterations
