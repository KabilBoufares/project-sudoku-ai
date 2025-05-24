from typing import List

def is_valid(grid: List[List[int]], row: int, col: int, num: int) -> bool:
    """
    Vérifie si 'num' peut être placé à la position (row, col) selon les règles du Sudoku.
    
    Args:
        grid: matrice 9x9 (liste de listes)
        row: index de ligne (0 à 8)
        col: index de colonne (0 à 8)
        num: valeur entre 1 et 9

    Returns:
        True si placement valide, sinon False
    """
    if grid[row][col] != 0:
        return False

    if num in grid[row]:
        return False

    if any(grid[i][col] == num for i in range(9)):
        return False

    row_start, col_start = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[row_start + i][col_start + j] == num:
                return False

    return True

def is_complete(grid: List[List[int]]) -> bool:
    """
    Vérifie si la grille ne contient aucune case vide.

    Args:
        grid: matrice 9x9

    Returns:
        True si complète, sinon False
    """
    return all(cell != 0 for row in grid for cell in row)

def is_valid_sudoku(grid_obj) -> bool:
    """
    Vérifie si la grille contenue dans grid_obj est une solution correcte.

    Args:
        grid_obj: instance de SudokuGrid (avec attribut .grid)

    Returns:
        True si la grille est complète et valide, sinon False
    """
    grid = grid_obj.grid

    if not is_complete(grid):
        return False

    for i in range(9):
        row_vals = set()
        col_vals = set()
        block_vals = set()

        for j in range(9):
            # Ligne
            val_row = grid[i][j]
            if val_row in row_vals or not (1 <= val_row <= 9):
                return False
            row_vals.add(val_row)

            # Colonne
            val_col = grid[j][i]
            if val_col in col_vals or not (1 <= val_col <= 9):
                return False
            col_vals.add(val_col)

            # Bloc 3x3
            r = 3 * (i // 3) + j // 3
            c = 3 * (i % 3) + j % 3
            val_block = grid[r][c]
            if val_block in block_vals or not (1 <= val_block <= 9):
                return False
            block_vals.add(val_block)

    return True
