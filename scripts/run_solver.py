import subprocess
import webbrowser
import time
import os
import argparse
import sys
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lancer la génération + serveur web Sudoku")
    parser.add_argument("--level", type=str, default="Expert", choices=["Easy", "Medium", "Hard", "Expert"],
                        help="Niveau de difficulté de la grille Sudoku")
    args = parser.parse_args()

    BASE_DIR = Path(__file__).resolve().parent  # scripts/
    PROJECT_ROOT = BASE_DIR.parent

    main_path = PROJECT_ROOT / "scripts" / "main.py"
    server_path = PROJECT_ROOT / "scripts" / "server.py"

    def run_main(level):
        print(f"\n Génération des résultats pour le niveau : {level}\n")
        if not main_path.exists():
            print(f" Fichier introuvable : {main_path}")
            sys.exit(1)
        subprocess.run(["python", str(main_path), "--level", level], check=True)

    def run_server():
        print(" Lancement du serveur Flask...\n")
        if not server_path.exists():
            print(f" Fichier introuvable : {server_path}")
            sys.exit(1)
        return subprocess.Popen(["python", str(server_path)])

    try:
        run_main(args.level)
        server_process = run_server()

        time.sleep(2)  # Laisse le temps au serveur de démarrer
        url = "http://127.0.0.1:5000/"
        webbrowser.open(url)
        print(f" Interface lancée : {url}\n")

        server_process.wait()

    except KeyboardInterrupt:
        print("\n Arrêt du serveur demandé par l'utilisateur.")
        server_process.terminate()

    except subprocess.CalledProcessError as e:
        print(f" Erreur lors de l’exécution de main.py : {e}")
