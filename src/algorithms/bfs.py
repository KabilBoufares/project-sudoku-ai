from collections import deque
from copy import deepcopy
from typing import Tuple
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

    while queue:
        current_grid, depth = queue.popleft()
        iterations += 1

        if is_complete(current_grid):
            return current_grid, iterations

        empty = find_empty(current_grid)
        if not empty:
            continue

        i, j = empty
        for num in range(1, 10):
            if is_valid(current_grid, i, j, num):
                new_grid = deepcopy(current_grid)
                new_grid[i][j] = num
                queue.append((new_grid, depth + 1))

    return None, iterations

def solve(sudoku_grid: SudokuGrid) -> Tuple[SudokuGrid, int]:
    grid, iterations = solve_bfs(sudoku_grid.grid)
    if grid is None:
        return sudoku_grid, iterations
    return SudokuGrid(grid), iterations
