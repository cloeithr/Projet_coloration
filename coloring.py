from typing import Dict, Set, List

Graph = Dict[str, Set[str]]

def greedy_coloring(graph: Graph, order: str = "largest_first") -> Dict[str, int]:
    """
    Coloration gloutonne.
    order:
      - "as_is"         : ordre naturel du dict (moins bon)
      - "largest_first" : trie les sommets par degré décroissant (souvent meilleur)
    """
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
