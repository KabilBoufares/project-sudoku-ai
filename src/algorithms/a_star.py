import heapq
import random
from copy import deepcopy
from src.core.validator import is_valid, is_complete
from src.core.grid import SudokuGrid

class AStarSolver:
    def __init__(self, grid: list[list[int]]):
        self.original_grid = deepcopy(grid)
        self.iterations = 0
        self.solution = None

    def heuristic(self, grid: list[list[int]]) -> int:
        """
        Heuristique : nombre total de conflits visibles (lignes + colonnes).
        """
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

    def get_next_states(self, grid: list[list[int]]):
        """
        Génère les voisins en remplissant une case vide
        avec une valeur valide (ordre aléatoire).
        """
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in random.sample(range(1, 10), 9):
                        if is_valid(grid, i, j, num):
                            new_grid = deepcopy(grid)
                            new_grid[i][j] = num
                            yield new_grid
                    return  # On ne remplit qu'une seule case à la fois

    def solve(self) -> bool:
        """
        Applique l'algorithme A* pour résoudre la grille Sudoku.
        """
        heap = []
        h = self.heuristic(self.original_grid)
        heapq.heappush(heap, (h, 0, self.original_grid))

        visited = set()

        while heap:
            f_score, steps, current = heapq.heappop(heap)
            self.iterations += 1

            grid_tuple = tuple(tuple(row) for row in current)
            if grid_tuple in visited:
                continue
            visited.add(grid_tuple)

            if is_complete(current):
                self.solution = current
                return True

            for neighbor in self.get_next_states(current):
                hn = self.heuristic(neighbor)
                heapq.heappush(heap, (steps + 1 + hn, steps + 1, neighbor))

        return False

    @property
    def grid(self) -> list[list[int]]:
        return self.solution if self.solution else self.original_grid

# Interface utilisée dans main.py
def solve(sudoku_grid: SudokuGrid) -> tuple[SudokuGrid, int]:
    """
    Point d'entrée appelé par main.py
    Args:
        sudoku_grid: SudokuGrid
    Returns:
        Tuple de (grille résolue, nombre d'itérations)
    """
    solver = AStarSolver(sudoku_grid.grid)
    solver.solve()
    return SudokuGrid(solver.grid), solver.iterations
