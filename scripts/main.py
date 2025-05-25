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

from src.algorithms import ALGORITHMS  # Import centralisé
from src.utils.loader import load_grid_from_dataset


def run_all_algorithms(difficulty: str):
    data_path = PROJECT_ROOT / "data" / f"{difficulty.lower()}.csv"

    if not data_path.exists():
        raise FileNotFoundError(f"❌ Fichier introuvable : {data_path}")

    grid_initial = SudokuGrid(load_grid_from_dataset(data_path))
    results = []

    for name, solver in ALGORITHMS.items():
        print(f"▶️ Exécution de l'algorithme : {name}")
        try:
            grid_copy = SudokuGrid(grid_initial.to_list())
            start = time.time()
            # --- Attendu : chaque solveur retourne un DICO de mesures ---
            res = solver(grid_copy)
            end = time.time()
            # Ajoute les infos de temps, nom algo, grille initiale, etc.
            res["algorithme"] = name
            res["temps"] = round(end - start, 4)
            res["grille_initiale"] = grid_initial.to_list()

            # Optionnel : vérification manuelle de succès (si non déjà dans res)
            if "taux_succes" not in res:
                res["taux_succes"] = is_valid_sudoku(SudokuGrid(res["grille_resolue"]))

            # Optionnel : nombre de cases fausses (utile pour visualisation)
            if "cases_fausses" not in res and not res.get("taux_succes", False):
                res["cases_fausses"] = count_false_cells(SudokuGrid(res["grille_resolue"]))
            else:
                res["cases_fausses"] = 0

            results.append(res)

            if not res.get("taux_succes", False):
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
