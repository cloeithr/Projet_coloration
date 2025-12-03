from typing import Dict, Set

Graph = Dict[str, Set[str]]

def greedy_coloring(graph: Graph) -> Dict[str, int]:
    """
    Algorithme glouton de coloration.
    Retourne un dict: sommet -> index de couleur.
    """
    color = {}
    for node in graph:
        neighbor_colors = {color[n] for n in graph[node] if n in color}
        c = 0
        while c in neighbor_colors:
            c += 1
        color[node] = c
    return color
