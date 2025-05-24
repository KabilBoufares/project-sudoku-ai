import heapq
from copy import deepcopy
from typing import List, Tuple
from src.core.grid import SudokuGrid
from src.core.validator import is_valid, is_complete

def find_empty(grid: List[List[int]]) -> Tuple[int, int] | None:
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def heuristic_conflicts(grid: List[List[int]]) -> int:
    """
    Heuristique simple : nombre de conflits (lignes + colonnes).
    """
    conflicts = 0
    for i in range(9):
        row_count = [0] * 10
        col_count = [0] * 10
        for j in range(9):
            row_count[grid[i][j]] += 1
            col_count[grid[j][i]] += 1
        conflicts += sum(c - 1 for c in row_count if c > 1)
        conflicts += sum(c - 1 for c in col_count if c > 1)
    return conflicts

def solve_beam(grid: List[List[int]], beam_width: int = 5) -> Tuple[List[List[int]], int]:
    """
    Beam Search limité : explore les 'beam_width' meilleures grilles à chaque étape.
    """
    beam = [(heuristic_conflicts(grid), grid)]
    iterations = 0

    while beam:
        new_candidates = []
        for _, g in beam:
            iterations += 1
            if is_complete(g):
                return g, iterations

            empty = find_empty(g)
            if not empty:
                continue

            i, j = empty
            for num in range(1, 10):
                if is_valid(g, i, j, num):
                    new_grid = deepcopy(g)
                    new_grid[i][j] = num
                    score = heuristic_conflicts(new_grid)
                    new_candidates.append((score, new_grid))

        # Garde les meilleurs selon l'heuristique
        beam = heapq.nsmallest(beam_width, new_candidates, key=lambda x: x[0])

    return grid, iterations

#  Interface standard pour main.py
def solve(sudoku_grid: SudokuGrid) -> Tuple[SudokuGrid, int]:
    grid, iterations = solve_beam(sudoku_grid.grid)
    return SudokuGrid(grid), iterations
