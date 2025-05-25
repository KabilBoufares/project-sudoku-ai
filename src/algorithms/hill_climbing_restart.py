# ==== ALGORITHME : Hill Climbing + Restart (Recherche locale) ====

from typing import Dict
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
        self.nb_restart = 0
        self.success = False

    def solve(self) -> bool:
        for restart in range(self.max_restarts):
            solver = HillClimbingSolver(self.original_grid)
            success = solver.solve(max_iterations=self.max_iterations)
            self.total_iterations += solver.iterations

            if solver.conflicts < self.best_conflicts:
                self.best_conflicts = solver.conflicts
                self.best_grid = solver.grid

            if success:
                self.nb_restart = restart  # nombre de restarts nécessaires avant succès
                self.success = True
                return True  # early success

        self.nb_restart = self.max_restarts
        self.success = (self.best_conflicts == 0)
        return self.success

def solve(sudoku_grid: SudokuGrid) -> Dict:
    solver = HillClimbingWithRestart(sudoku_grid.grid, max_restarts=10, max_iterations=1000)
    solver.solve()
    return {
        "grille_resolue": solver.best_grid,
        "iterations": solver.total_iterations,
        "taux_succes": solver.success,
        "conflits_finaux": solver.best_conflicts,
        "nb_restarts": solver.nb_restart,
        "categorie": "recherche_locale"
    }
