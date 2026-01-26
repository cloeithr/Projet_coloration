from typing import Dict, Set, List

Graph = Dict[str, Set[str]]

def greedy_coloring(graph: Graph, order: str = "largest_first") -> Dict[str, int]:
    if order == "largest_first":
        nodes: List[str] = sorted(graph.keys(), key=lambda n: len(graph[n]), reverse=True)
    else:
        nodes = list(graph.keys())

    color: Dict[str, int] = {}
    for node in nodes:
        neighbor_colors = {color[n] for n in graph[node] if n in color}
        c = 0
        while c in neighbor_colors:
            c += 1
        color[node] = c
    return color

def verify_coloring(graph: Graph, coloring: Dict[str, int]) -> bool:
    """Vérifie qu'aucun voisin n'a la même couleur."""
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if coloring[node] == coloring[neighbor]:
                return False
    return True

def get_graph_stats(graph: Graph):
    """Calcule les stats pour le rapport."""
    nb_nodes = len(graph)
    nb_edges = sum(len(v) for v in graph.values()) // 2
    density = (2 * nb_edges) / (nb_nodes * (nb_nodes - 1)) if nb_nodes > 1 else 0
    return nb_nodes, nb_edges, density