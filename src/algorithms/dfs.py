from copy import deepcopy
from typing import Tuple
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
    """
    iterations = [0]  # Utilise une liste pour garder une référence mutable

    def backtrack(grid):
        iterations[0] += 1
        empty = find_empty(grid)
        if not empty:
            return True  # Grille complète

        i, j = empty
        for num in range(1, 10):
            if is_valid(grid, i, j, num):
                grid[i][j] = num
                if backtrack(grid):
                    return True
                grid[i][j] = 0  # Annule si échec

        return False

    working_grid = deepcopy(grid)
    backtrack(working_grid)
    return working_grid, iterations[0]

#  Interface standard pour main.py
def solve(sudoku_grid: SudokuGrid) -> Tuple[SudokuGrid, int]:
    grid, iterations = solve_dfs(sudoku_grid.grid)
    return SudokuGrid(grid), iterations
