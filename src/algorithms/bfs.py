# ==== ALGORITHME : BFS (Recherche Aveugle) ====

from collections import deque
from copy import deepcopy
from typing import Dict
from src.core.grid import SudokuGrid
from src.core.validator import is_valid, is_complete

def find_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def solve_bfs(grid):
    queue = deque()
    queue.append((deepcopy(grid), 0))
    iterations = 0
    max_queue_size = 1  # Pour évaluer le pic de mémoire utilisée

    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        current_grid, depth = queue.popleft()
        iterations += 1

        if is_complete(current_grid):
            return current_grid, iterations, max_queue_size

        empty = find_empty(current_grid)
        if not empty:
            continue

        i, j = empty
        for num in range(1, 10):
            if is_valid(current_grid, i, j, num):
                new_grid = deepcopy(current_grid)
                new_grid[i][j] = num
                queue.append((new_grid, depth + 1))

    return None, iterations, max_queue_size

def solve(sudoku_grid: SudokuGrid) -> Dict:
    grid, iterations, max_queue_size = solve_bfs(sudoku_grid.grid)
    taux_succes = is_complete(grid) if grid else False
    return {
        "grille_resolue": grid if grid is not None else [],
        "iterations": iterations,
        "taux_succes": taux_succes,
        "memoire_max_file": max_queue_size,
        "categorie": "recherche_aveugle"
    }
