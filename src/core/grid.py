class SudokuGrid:
    def __init__(self, grid):
        """
        Initialise une grille Sudoku à partir d'une matrice 9x9.
        :param grid: liste de listes 9x9 avec des entiers (0 = case vide)
        """
        if len(grid) != 9 or any(len(row) != 9 for row in grid):
            raise ValueError("La grille doit être une matrice 9x9.")
        self._grid = [row[:] for row in grid]

    @property
    def grid(self):
        """Accès sécurisé à la grille (lecture seule)"""
        return self._grid

    def print_grid(self):
        """Affiche la grille dans un format lisible en console"""
        print(self)

    def __str__(self):
        """Retourne la grille sous forme de chaîne formatée"""
        rows = []
        for i in range(9):
            if i % 3 == 0 and i != 0:
                rows.append("-" * 21)
            row = []
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row.append("|")
                val = self._grid[i][j]
                row.append(str(val) if val != 0 else ".")
            rows.append(" ".join(row))
        return "\n".join(rows)

    def get_row(self, i):
        return self._grid[i]

    def get_column(self, j):
        return [self._grid[i][j] for i in range(9)]

    def get_block(self, row, col):
        """Retourne les 9 valeurs de la sous-grille 3x3 contenant la case (row, col)"""
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        return [
            self._grid[i][j]
            for i in range(row_start, row_start + 3)
            for j in range(col_start, col_start + 3)
        ]

    def to_list(self):
        """Retourne la grille sous forme de liste de listes"""
        return [row[:] for row in self._grid]

    def is_valid_value(self, row, col, value):
        """Vérifie si une valeur est autorisée à la position (row, col)"""
        return (
            value not in self.get_row(row)
            and value not in self.get_column(col)
            and value not in self.get_block(row, col)
        )

    def count_conflicts(self):
        """Compte le nombre total de conflits dans la grille actuelle"""
        conflicts = 0
        for i in range(9):
            for j in range(9):
                val = self._grid[i][j]
                if val != 0:
                    self._grid[i][j] = 0  # Temporarily clear
                    if not self.is_valid_value(i, j, val):
                        conflicts += 1
                    self._grid[i][j] = val
        return conflicts
