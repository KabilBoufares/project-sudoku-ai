import random
from copy import deepcopy
from typing import List, Tuple, Optional
from src.core.grid import SudokuGrid

class HillClimbingSolver:
    """
    Algorithme de résolution de Sudoku par Hill Climbing local :
    échange des cellules non fixes au sein des blocs 3x3 pour minimiser les conflits.
    """

    def __init__(self, grid: List[List[int]]):
        self.original_grid = deepcopy(grid)
        self.grid = self._generate_initial_grid(grid)
        self.fixed_cells = [[cell != 0 for cell in row] for row in grid]
        self.iterations = 0
        self.conflicts = self._calculate_conflicts()

    def _generate_initial_grid(self, grid: List[List[int]]) -> List[List[int]]:
        """Remplit chaque bloc 3x3 avec des chiffres aléatoires sans doublons."""
        new_grid = deepcopy(grid)
        for block_row in range(3):
            for block_col in range(3):
                nums = list(range(1, 10))
                # Supprimer les valeurs déjà fixées
                for i in range(3):
                    for j in range(3):
                        val = grid[block_row * 3 + i][block_col * 3 + j]
                        if val in nums:
                            nums.remove(val)
                # Remplir les cases restantes
                random.shuffle(nums)
                idx = 0
                for i in range(3):
                    for j in range(3):
                        r, c = block_row * 3 + i, block_col * 3 + j
                        if new_grid[r][c] == 0:
                            new_grid[r][c] = nums[idx]
                            idx += 1
        return new_grid

    def _calculate_conflicts(self) -> int:
        """Retourne le nombre de conflits (uniquement lignes et colonnes)."""
        conflicts = 0
        for i in range(9):
            row_count = [0] * 10
            col_count = [0] * 10
            for j in range(9):
                row_count[self.grid[i][j]] += 1
                col_count[self.grid[j][i]] += 1
            conflicts += sum(c - 1 for c in row_count if c > 1)
            conflicts += sum(c - 1 for c in col_count if c > 1)
        return conflicts

    def solve(self, max_iterations: int = 10000) -> bool:
        """
        Applique l’algorithme de Hill Climbing avec recherche de swap optimal local.
        """
        for _ in range(max_iterations):
            self.iterations += 1
            best_swap: Optional[Tuple[int, int, int, int]] = None
            best_score = self.conflicts

            for block_row in range(3):
                for block_col in range(3):
                    # Identifier les cellules modifiables dans ce bloc
                    cells = [
                        (i, j)
                        for i in range(block_row * 3, block_row * 3 + 3)
                        for j in range(block_col * 3, block_col * 3 + 3)
                        if not self.fixed_cells[i][j]
                    ]

                    for idx1 in range(len(cells)):
                        for idx2 in range(idx1 + 1, len(cells)):
                            i1, j1 = cells[idx1]
                            i2, j2 = cells[idx2]

                            # Swap temporaire
                            self.grid[i1][j1], self.grid[i2][j2] = self.grid[i2][j2], self.grid[i1][j1]
                            score = self._calculate_conflicts()

                            if score < best_score:
                                best_score = score
                                best_swap = (i1, j1, i2, j2)

                            # Défaire le swap
                            self.grid[i1][j1], self.grid[i2][j2] = self.grid[i2][j2], self.grid[i1][j1]

            if best_swap:
                i1, j1, i2, j2 = best_swap
                self.grid[i1][j1], self.grid[i2][j2] = self.grid[i2][j2], self.grid[i1][j1]
                self.conflicts = best_score
                if self.conflicts == 0:
                    return True
            else:
                break  # Aucun progrès possible

        return self.conflicts == 0

# Interface attendue par main.py
def solve(sudoku_grid: SudokuGrid) -> Tuple[SudokuGrid, int]:
    solver = HillClimbingSolver(sudoku_grid.grid)
    solver.solve()
    return SudokuGrid(solver.grid), solver.iterations
