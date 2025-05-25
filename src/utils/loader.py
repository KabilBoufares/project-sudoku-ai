import random
import csv
from pathlib import Path

# Base du projet (2 niveaux au-dessus de ce fichier)
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

def list_grids(data_dir=DATA_DIR):
    """
    Liste les fichiers .csv disponibles dans le dossier data/.
    Args:
        data_dir (Path): Dossier à lister.
    Returns:
        List[str]: Noms des fichiers .csv
    """
    return [f.name for f in data_dir.glob("*.csv")]

def load_grid_from_dataset(filename, data_dir=DATA_DIR):
    """
    Charge une grille aléatoire depuis un fichier CSV formaté avec les colonnes : puzzle_id, puzzle, solution, difficulty.
    :param filename: nom du fichier (ex: 'expert.csv')
    :param data_dir: dossier data/
    :return: grille sous forme 9x9 (List[List[int]])
    """
    path = Path(filename)
    if not path.exists():
        path = data_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"❌ Fichier introuvable : {path}")

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        if not reader:
            raise ValueError("❌ Fichier vide ou format invalide.")

        # Choisir une ligne aléatoire
        row = random.choice(reader)
        puzzle_str = row['puzzle']

        if len(puzzle_str) != 81 or not puzzle_str.isdigit():
            raise ValueError("❌ Format de grille invalide (81 chiffres requis).")

        # Convertir en matrice 9x9
        grid = [[int(puzzle_str[i * 9 + j]) for j in range(9)] for i in range(9)]
        return grid

# Fonction interactive (facultative)
def choose_grid(data_dir=DATA_DIR):
    """
    Permet à l'utilisateur de choisir un fichier dans /data et charger une grille (non utilisée dans l'interface web).
    """
    files = list_grids(data_dir)
    if not files:
        print("❌ Aucun fichier .csv trouvé dans le dossier /data/")
        return None

    print("\n📋 Sélectionnez une grille à charger :")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    while True:
        choice = input("Entrez le numéro : ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return load_grid_from_dataset(files[int(choice) - 1], data_dir)
        print("⛔ Choix invalide, veuillez réessayer.")
