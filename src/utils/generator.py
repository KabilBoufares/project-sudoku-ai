import random
import copy

GRID_SIZE = 9
BLOCK_SIZE = 3

def is_valid(grid, row, col, num):
    """
    Vérifie si un chiffre peut être placé à la position (row, col)
    sans violer les règles du Sudoku.
    """
    for i in range(GRID_SIZE):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    start_row = (row // BLOCK_SIZE) * BLOCK_SIZE
    start_col = (col // BLOCK_SIZE) * BLOCK_SIZE

    for i in range(BLOCK_SIZE):
        for j in range(BLOCK_SIZE):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

def solve_grid(grid):
    """
    Remplit la grille avec des chiffres valides (résolution complète via backtracking).
    """
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_grid(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def generate_full_grid():
    """
    Génère une grille complète et valide de Sudoku.
    Returns:
        List[List[int]]: Grille complète
    """
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    solve_grid(grid)
    return grid

def remove_cells(grid, difficulty="medium"):
    """
    Supprime des cases selon le niveau de difficulté.
    
    Args:
        grid: grille complète
        difficulty: niveau ('easy', 'medium', 'hard', 'expert')

    Returns:
        List[List[int]]: Grille partiellement remplie
    """
    grid_copy = copy.deepcopy(grid)
    levels = {
        "easy": 30,
        "medium": 40,
        "hard": 50,
        "expert": 60,
    }
    to_remove = levels.get(difficulty.lower(), 40)
    removed = 0
    while removed < to_remove:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if grid_copy[i][j] != 0:
            grid_copy[i][j] = 0
            removed += 1
    return grid_copy

def generate_sudoku(difficulty="medium"):
    """
    Génère une grille jouable selon une difficulté choisie.
    
    Args:
        difficulty: Niveau de difficulté à appliquer.

    Returns:
        List[List[int]]: Grille à jouer
    """
    full_grid = generate_full_grid()
    puzzle = remove_cells(full_grid, difficulty)
    return puzzle
