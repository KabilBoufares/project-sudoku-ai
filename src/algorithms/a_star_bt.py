# ==== ALGORITHME : A* + Backtracking (Recherche informée) ====

import heapq
import random
from copy import deepcopy
from typing import Dict
from src.core.grid import SudokuGrid
from src.core.validator import is_valid, is_complete

class AStarBT_Solver:
    def __init__(self, grid):
        self.original_grid = deepcopy(grid)
        self.iterations = 0
        self.solution = None
        self.max_heap_size = 1
        self.visited_count = 0

    def heuristic(self, grid):
        conflicts = 0
        for i in range(9):
            row_counts = [0] * 10
            col_counts = [0] * 10
            for j in range(9):
                row_counts[grid[i][j]] += 1
                col_counts[grid[j][i]] += 1
            conflicts += sum(c - 1 for c in row_counts if c > 1)
            conflicts += sum(c - 1 for c in col_counts if c > 1)
        return conflicts

    def get_next_states(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in random.sample(range(1, 10), 9):
                        if is_valid(grid, i, j, num):
                            new_grid = deepcopy(grid)
                            new_grid[i][j] = num
                            yield new_grid
                    return

    def solve(self):
        heap = []
        h = self.heuristic(self.original_grid)
        heapq.heappush(heap, (h, 0, self.original_grid))
        visited = set()

        while heap:
            self.max_heap_size = max(self.max_heap_size, len(heap))
            f_score, steps, current = heapq.heappop(heap)
            self.iterations += 1

            grid_tuple = tuple(tuple(row) for row in current)
            if grid_tuple in visited:
                continue
            visited.add(grid_tuple)
            self.visited_count = len(visited)

            if is_complete(current):
                self.solution = current
                return True

            # À chaque étape, on backtrack sur tous les voisins "valides"
            for neighbor in self.get_next_states(current):
                hn = self.heuristic(neighbor)
                heapq.heappush(heap, (steps + 1 + hn, steps + 1, neighbor))

        return False

    @property
    def grid(self):
        return self.solution if self.solution else self.original_grid

def solve(sudoku_grid: SudokuGrid) -> Dict:
    solver = AStarBT_Solver(sudoku_grid.grid)
    solver.solve()
    taux_succes = is_complete(solver.grid)
    return {
        "grille_resolue": solver.grid,
        "iterations": solver.iterations,
        "taux_succes": taux_succes,
        "conflits_heuristique": solver.heuristic(solver.grid),
        "etats_explores": solver.visited_count,
        "memoire_max_file": solver.max_heap_size,
        "categorie": "recherche_informee"
    }
