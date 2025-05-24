import time
import json
import argparse
from pathlib import Path
import sys

# FORCE le chemin racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.core.grid import SudokuGrid
from src.core.validator import is_valid_sudoku
from src.utils.loader import load_grid
from src.algorithms import ALGORITHMS  # ← Import centralisé

def run_all_algorithms(difficulty: str):
    data_path = PROJECT_ROOT / "data" / f"{difficulty.lower()}.csv"

    if not data_path.exists():
        raise FileNotFoundError(f"❌ Fichier introuvable : {data_path}")

    grid_initial = SudokuGrid(load_grid(str(data_path)))
    results = []

    for name, solver in ALGORITHMS.items():
        print(f"▶️ Exécution de l'algorithme : {name}")
        try:
            grid_copy = SudokuGrid(grid_initial.to_list())
            start = time.time()
            solution, iterations = solver(grid_copy)
            end = time.time()

            is_valid = is_valid_sudoku(solution)
            conflicts = getattr(solution, 'count_conflicts', lambda: 0)()
            false_cells = count_false_cells(solution) if not is_valid else 0

            results.append({
                "algorithme": name,
                "temps": round(end - start, 4),
                "iterations": iterations,
                "succes": is_valid,
                "conflicts": conflicts,
                "cases_fausses": false_cells,
                "grille_initiale": grid_initial.to_list(),
                "grille_resolue": solution.to_list()
            })

            if not is_valid:
                print(f"⚠️ {name} a généré une solution invalide.")

        except Exception as e:
            print(f"❌ Erreur avec {name} : {e}")

    # Sauvegarde des résultats DANS le bon dossier à la racine du projet
    output_dir = PROJECT_ROOT / "web_interface" / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"results_{difficulty.lower()}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Résultats sauvegardés dans : {output_file}")

def count_false_cells(grid: SudokuGrid) -> int:
    errors = 0
    for i in range(9):
        for j in range(9):
            val = grid.grid[i][j]
            grid.grid[i][j] = 0
            if not grid.is_valid_value(i, j, val):
                errors += 1
            grid.grid[i][j] = val
    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", default="Expert", help="Niveau : Easy | Medium | Hard | Expert")
    args = parser.parse_args()

    print(f"\n🚀 Lancement de la génération des résultats pour niveau : {args.level}")
    run_all_algorithms(args.level)
    print("🏁 Fin de l'exécution.\n")
