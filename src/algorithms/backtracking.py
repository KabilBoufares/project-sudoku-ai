from copy import deepcopy
from typing import Tuple
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
    Retourne True si solution trouvée, False sinon.
    """
    iterations = [0]

    def backtrack():
        iterations[0] += 1
        empty = find_empty(grid)
        if not empty:
            return True

        i, j = empty
        for num in range(1, 10):
            if is_valid(grid, i, j, num):
                grid[i][j] = num
                if backtrack():
                    return True
                grid[i][j] = 0  # backtrack
        return False

    backtrack()
    return grid, iterations[0]

#  Interface standard pour main.py
def solve(sudoku_grid: SudokuGrid) -> Tuple[SudokuGrid, int]:
    working_grid = deepcopy(sudoku_grid.grid)
    grid, iterations = solve_backtracking(working_grid)
    return SudokuGrid(grid), iterations
