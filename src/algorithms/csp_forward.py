# ==== ALGORITHME : CSP + Forward Checking (Recherche CSP / Contraintes) ====

from copy import deepcopy
from typing import Dict, List, Tuple, Optional
from src.core.validator import is_valid, is_complete
from src.core.grid import SudokuGrid
import random

class CSPForwardSolver:
    def __init__(self, grid: List[List[int]]):
        self.original_grid = deepcopy(grid)
        self._grid = deepcopy(grid)
        self.iterations = 0
        self.nb_assignations = 0
        self.nb_backtracks = 0
        self.max_domain_size = 0

    def get_domains(self, grid: List[List[int]]) -> Dict[Tuple[int, int], List[int]]:
        domains = {}
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    d = [n for n in range(1, 10) if is_valid(grid, i, j, n)]
                    domains[(i, j)] = d
                    self.max_domain_size = max(self.max_domain_size, len(d))
        return domains

    def select_unassigned_variable(self, domains: Dict[Tuple[int, int], List[int]]) -> Tuple[int, int]:
        # MRV
        return min(domains, key=lambda var: len(domains[var]))

    def forward_check(self, grid, domains, row, col, value):
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

    def solve_recursive(self, grid, domains):
        self.iterations += 1
        if not domains:
            return True
        row, col = self.select_unassigned_variable(domains)
        for value in random.sample(domains[(row, col)], len(domains[(row, col)])):
            if is_valid(grid, row, col, value):
                grid[row][col] = value
                self.nb_assignations += 1
                new_domains = self.forward_check(grid, domains, row, col, value)
                if new_domains is not None and self.solve_recursive(grid, new_domains):
                    return True
                grid[row][col] = 0  # Backtrack
                self.nb_backtracks += 1
        return False

    def solve(self) -> bool:
        domains = self.get_domains(self._grid)
        return self.solve_recursive(self._grid, domains)

    @property
    def grid(self):
        return self._grid

def solve(sudoku_grid: SudokuGrid) -> Dict:
    solver = CSPForwardSolver(sudoku_grid.grid)
    success = solver.solve()
    return {
        "grille_resolue": solver.grid,
        "iterations": solver.iterations,
        "taux_succes": is_complete(solver.grid),
        "nb_assignations": solver.nb_assignations,
        "nb_backtracks": solver.nb_backtracks,
        "taille_max_domaine": solver.max_domain_size,
        "categorie": "recherche_csp"
    }
