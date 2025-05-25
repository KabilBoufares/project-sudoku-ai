# ==== ALGORITHME : DFS (Recherche Aveugle) ====

from copy import deepcopy
from typing import Dict
from src.core.grid import SudokuGrid
from src.core.validator import is_valid, is_complete

def find_empty(grid):
    """Retourne la première case vide (ou None si complète)."""
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def solve_dfs(grid):
    """
    DFS récursif pour résoudre une grille Sudoku.
    Explore en profondeur en remplissant les cases une par une.
    Mesure : nombre d'itérations, profondeur max atteinte.
    """
    iterations = [0]
    max_depth = [0]
    current_depth = [0]

    def backtrack(grid):
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
                if backtrack(grid):
                    current_depth[0] -= 1
                    return True
                grid[i][j] = 0  # Annule si échec
        current_depth[0] -= 1
        return False

    working_grid = deepcopy(grid)
    backtrack(working_grid)
    return working_grid, iterations[0], max_depth[0]

def solve(sudoku_grid: SudokuGrid) -> Dict:
    grid, iterations, max_depth = solve_dfs(sudoku_grid.grid)
    taux_succes = is_complete(grid)
    return {
        "grille_resolue": grid,
        "iterations": iterations,
        "taux_succes": taux_succes,
        "profondeur_max": max_depth,
        "categorie": "recherche_aveugle"
    }
