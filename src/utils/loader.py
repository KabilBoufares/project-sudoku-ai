from pathlib import Path
import csv

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

def load_grid(filename, data_dir=DATA_DIR):
    """
    Charge une grille Sudoku à partir d’un fichier CSV (9x9).
    Args:
        filename (str or Path): nom du fichier ou chemin absolu.
        data_dir (Path): dossier de base.
    Returns:
        List[List[int]]: Grille Sudoku 9x9
    """
    path = Path(filename)
    if not path.exists():
        path = data_dir / filename
    if not path.exists():
        raise FileNotFoundError(f" Fichier introuvable : {path}")

    grid = []
    with path.open(encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            grid.append([int(cell) for cell in row])

    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError(" La grille doit être de dimension 9x9.")

    return grid

def choose_grid(data_dir=DATA_DIR):
    """
    Affiche les grilles disponibles et permet à l'utilisateur d'en choisir une.
    Args:
        data_dir (Path): Dossier contenant les grilles.
    Returns:
        List[List[int]]: Grille Sudoku choisie.
    """
    files = list_grids(data_dir)
    if not files:
        print(" Aucun fichier .csv trouvé dans le dossier /data/")
        return None

    print("\n📋 Sélectionnez une grille à charger :")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    while True:
        choice = input("Entrez le numéro : ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return load_grid(files[int(choice) - 1], data_dir)
        print(" Choix invalide, veuillez réessayer.")
