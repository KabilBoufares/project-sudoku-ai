# ==== ALGORITHME : Backtracking (Recherche Aveugle) ====

from copy import deepcopy
from typing import Dict
from src.core.grid import SudokuGrid
from src.core.validator import is_valid, is_complete

def find_empty(grid):
    """Retourne la première case vide ou None si la grille est complète."""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def solve_backtracking(grid):
    """
    Résout une grille de Sudoku avec backtracking simple.
    Retourne la solution, le nombre d'itérations, le nombre de backtracks, la profondeur max.
    """
    iterations = [0]
    backtracks = [0]
    max_depth = [0]
    current_depth = [0]

    def backtrack():
        iterations[0] += 1
        current_depth[0] += 1
        max_depth[0] = max(max_depth[0], current_depth[0])

        empty = find_empty(grid)
        if not empty:
            current_depth[0] -= 1
            return True

        i, j = empty
        for num in range(1, 10):
            if is_valid(grid, i, j, num):
                grid[i][j] = num
                if backtrack():
                    current_depth[0] -= 1
                    return True
                grid[i][j] = 0
                backtracks[0] += 1
        current_depth[0] -= 1
        return False

    backtrack()
    return grid, iterations[0], backtracks[0], max_depth[0]

# ==== Interface "moderne" pour main.py ====
def solve(sudoku_grid: SudokuGrid) -> Dict:
    working_grid = deepcopy(sudoku_grid.grid)
    grid, iterations, backtracks, max_depth = solve_backtracking(working_grid)
    taux_succes = is_complete(grid)
    return {
        "grille_resolue": grid,
        "iterations": iterations,
        "taux_succes": taux_succes,
        "nb_backtracks": backtracks,
        "profondeur_max": max_depth,
        "categorie": "recherche_aveugle"
    }
