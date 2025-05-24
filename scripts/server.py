from flask import Flask, request, jsonify, send_from_directory
import subprocess
from pathlib import Path

# Correction : base projet = racine
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "web_interface"

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/run", methods=["GET"])
def run_main():
    difficulty = request.args.get("difficulty", "Expert").capitalize()
    print(f" Requête de génération de grille pour niveau : {difficulty}")
    
    scripts_dir = BASE_DIR / "scripts"
    main_script = scripts_dir / "main.py"

    if not main_script.exists():
        error_msg = f" main.py introuvable à l’emplacement : {main_script}"
        print(error_msg)
        return jsonify({"success": False, "error": error_msg}), 500

    try:
        subprocess.run(["python", str(main_script), "--level", difficulty], check=True)
        return jsonify({"success": True})
    except subprocess.CalledProcessError as e:
        print(f" Erreur d’exécution : {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    print(" Serveur Flask en cours de démarrage : http://127.0.0.1:5000/")
    app.run(debug=True)
