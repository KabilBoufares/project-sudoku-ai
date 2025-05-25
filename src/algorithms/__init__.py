# ==== Imports des algorithmes (par catégorie) ====

# --- Recherche aveugle ---
from .backtracking import solve as backtracking
from .dfs import solve as dfs
from .bfs import solve as bfs

# --- Recherche informée ---
from .a_star import solve as a_star
from .beam import solve as beam
from .a_star_bt import solve as a_star_bt  # Assure-toi que ce fichier existe !

# --- Recherche locale (métaheuristique) ---
from .hill_climbing import solve as hill_climbing
from .hill_climbing_restart import solve as hill_climbing_restart

# --- CSP (contraintes) ---


# --- Dictionnaire centralisé des solveurs ---
ALGORITHMS = {
    "Backtracking": backtracking,
    "DFS": dfs,
    "BFS": bfs,
    "A*": a_star,
    "A* + Backtracking": a_star_bt,
    "Hill Climbing": hill_climbing,
    "Hill Climbing + Restart": hill_climbing_restart,
    "Beam Search": beam,
}
