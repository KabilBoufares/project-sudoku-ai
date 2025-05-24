from .backtracking import solve as backtracking
from .dfs import solve as dfs
from .bfs import solve as bfs
from .a_star import solve as a_star
from .hill_climbing import solve as hill_climbing
from .hill_climbing_restart import solve as hill_climbing_restart
from .simulated_annealing import solve as simulated_annealing
from .csp_forward import solve as csp_forward
from .beam import solve as beam

# Ce dictionnaire est utilisé dans main.py pour exécuter tous les solveurs
ALGORITHMS = {
    "Backtracking": backtracking,
    "DFS": dfs,
    "BFS": bfs,
    "A*": a_star,
    "Hill Climbing": hill_climbing,
    "Hill Climbing + Restart": hill_climbing_restart,
    "Simulated Annealing": simulated_annealing,
    "CSP + Forward Checking": csp_forward,
    "Beam Search": beam,
}
