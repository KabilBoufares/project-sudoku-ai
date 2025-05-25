# ==== ALGORITHME : Beam Search (Recherche informée) ====

import heapq
from copy import deepcopy
from typing import Dict, List
from src.core.grid import SudokuGrid
from src.core.validator import is_valid, is_complete

def find_empty(grid: List[List[int]]):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def heuristic_conflicts(grid: List[List[int]]) -> int:
    """
    Heuristique : nombre de conflits (lignes + colonnes).
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

def solve_beam(grid: List[List[int]], beam_width: int = 5):
    """
    Beam Search limité : explore les 'beam_width' meilleures grilles à chaque étape.
    Mesure : itérations, heuristique finale, états explorés, taux succès.
    """
    beam = [(heuristic_conflicts(grid), deepcopy(grid))]
    iterations = 0
    max_beam_size = 1
    etats_explores = set()

    while beam:
        max_beam_size = max(max_beam_size, len(beam))
        new_candidates = []
        for _, g in beam:
            iterations += 1
            grid_tuple = tuple(tuple(row) for row in g)
            etats_explores.add(grid_tuple)
            if is_complete(g):
                return g, iterations, heuristic_conflicts(g), len(etats_explores), max_beam_size

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

    # Si échec, retourne la meilleure grille trouvée
    if beam:
        best_grid = beam[0][1]
    else:
        best_grid = grid
    return best_grid, iterations, heuristic_conflicts(best_grid), len(etats_explores), max_beam_size

def solve(sudoku_grid: SudokuGrid) -> Dict:
    grid, iterations, h_final, etats, max_beam = solve_beam(sudoku_grid.grid)
    taux_succes = is_complete(grid)
    return {
        "grille_resolue": grid,
        "iterations": iterations,
        "taux_succes": taux_succes,
        "conflits_heuristique": h_final,
        "etats_explores": etats,
        "memoire_max_beam": max_beam,
        "categorie": "recherche_informee"
    }
