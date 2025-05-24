from copy import deepcopy
from typing import Dict, List, Tuple, Optional
from src.core.validator import is_valid
from src.core.grid import SudokuGrid
import random

class CSPForwardSolver:
    def __init__(self, grid: List[List[int]]):
        self.original_grid = deepcopy(grid)
        self._grid = deepcopy(grid)
        self.iterations = 0

    def get_domains(self, grid: List[List[int]]) -> Dict[Tuple[int, int], List[int]]:
        """Construit les domaines valides pour chaque case vide."""
        domains = {}
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    domains[(i, j)] = [n for n in range(1, 10) if is_valid(grid, i, j, n)]
        return domains

    def select_unassigned_variable(self, domains: Dict[Tuple[int, int], List[int]]) -> Tuple[int, int]:
        """Heuristique MRV : retourne la variable avec le plus petit domaine."""
        return min(domains, key=lambda var: len(domains[var]))

    def forward_check(
        self, grid: List[List[int]], domains: Dict[Tuple[int, int], List[int]], row: int, col: int, value: int
    ) -> Optional[Dict[Tuple[int, int], List[int]]]:
        """Met à jour les domaines voisins. Retourne None si un domaine devient vide."""
        new_domains = deepcopy(domains)
        del new_domains[(row, col)]

        for i in range(9):
            for j in range(9):
                if (i, j) in new_domains and (
                    i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3)
                ):
                    if value in new_domains[(i, j)]:
                        new_domains[(i, j)].remove(value)
                        if not new_domains[(i, j)]:
                            return None
        return new_domains

    def solve_recursive(self, grid: List[List[int]], domains: Dict[Tuple[int, int], List[int]]) -> bool:
        self.iterations += 1
        if not domains:
            return True

        row, col = self.select_unassigned_variable(domains)
        for value in random.sample(domains[(row, col)], len(domains[(row, col)])):
            if is_valid(grid, row, col, value):
                grid[row][col] = value
                new_domains = self.forward_check(grid, domains, row, col, value)
                if new_domains is not None and self.solve_recursive(grid, new_domains):
                    return True
                grid[row][col] = 0  # Backtrack

        return False

    def solve(self) -> bool:
        domains = self.get_domains(self._grid)
        return self.solve_recursive(self._grid, domains)

    @property
    def grid(self) -> List[List[int]]:
        return self._grid

#  Interface standard pour main.py
def solve(sudoku_grid: SudokuGrid) -> Tuple[SudokuGrid, int]:
    solver = CSPForwardSolver(sudoku_grid.grid)
    solver.solve()
    return SudokuGrid(solver.grid), solver.iterations
