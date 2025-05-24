import random
import math
from copy import deepcopy
from typing import Tuple
from src.core.grid import SudokuGrid

class SimulatedAnnealingSolver:
    def __init__(self, grid, max_iterations=10000, initial_temp=1.0, cooling_rate=0.003):
        self.original_grid = grid
        self.grid = self._generate_initial_grid(grid)
        self.fixed_cells = [[cell != 0 for cell in row] for row in grid]
        self.iterations = 0
        self.conflicts = self._calculate_conflicts()
        self.max_iterations = max_iterations
        self.temperature = initial_temp
        self.cooling_rate = cooling_rate

    def _generate_initial_grid(self, grid):
        new_grid = deepcopy(grid)
        for block_row in range(3):
            for block_col in range(3):
                nums = list(range(1, 10))
                for i in range(3):
                    for j in range(3):
                        val = grid[block_row*3 + i][block_col*3 + j]
                        if val in nums:
                            nums.remove(val)
                random.shuffle(nums)
                idx = 0
                for i in range(3):
                    for j in range(3):
                        if new_grid[block_row*3 + i][block_col*3 + j] == 0:
                            new_grid[block_row*3 + i][block_col*3 + j] = nums[idx]
                            idx += 1
        return new_grid

    def _calculate_conflicts(self):
        conflicts = 0
        for i in range(9):
            row_counts = [0] * 10
            col_counts = [0] * 10
            for j in range(9):
                row_counts[self.grid[i][j]] += 1
                col_counts[self.grid[j][i]] += 1
            conflicts += sum(c - 1 for c in row_counts if c > 1)
            conflicts += sum(c - 1 for c in col_counts if c > 1)
        return conflicts

    def _random_swap(self):
        block_row, block_col = random.randint(0, 2), random.randint(0, 2)
        cells = [
            (i, j)
            for i in range(block_row*3, block_row*3 + 3)
            for j in range(block_col*3, block_col*3 + 3)
            if not self.fixed_cells[i][j]
        ]
        if len(cells) < 2:
            return

        (i1, j1), (i2, j2) = random.sample(cells, 2)
        self.grid[i1][j1], self.grid[i2][j2] = self.grid[i2][j2], self.grid[i1][j1]

    def solve(self):
        for _ in range(self.max_iterations):
            self.iterations += 1
            prev_grid = deepcopy(self.grid)
            prev_conflicts = self.conflicts

            self._random_swap()
            new_conflicts = self._calculate_conflicts()

            delta = new_conflicts - prev_conflicts
            if delta < 0:
                self.conflicts = new_conflicts
            else:
                prob = math.exp(-delta / self.temperature) if self.temperature > 0 else 0
                if random.random() < prob:
                    self.conflicts = new_conflicts
                else:
                    self.grid = prev_grid  # revert

            self.temperature *= (1 - self.cooling_rate)

            if self.conflicts == 0:
                return True

        return False

def solve(sudoku_grid: SudokuGrid) -> Tuple[SudokuGrid, int]:
    solver = SimulatedAnnealingSolver(sudoku_grid.grid)
    solver.solve()
    return SudokuGrid(solver.grid), solver.iterations
