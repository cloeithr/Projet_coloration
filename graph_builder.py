from __future__ import annotations
from collections import defaultdict
from typing import Dict, Set, List
from models import Operation


Graph = Dict[str, Set[str]]  # node -> set(neighbors)


def build_graph_immediate(operations: List[Operation], criterion: str = "of") -> Graph:
    """
    Construit un graphe de conflits à partir des opérations triées par machine/temps.
    Noeuds = valeurs du critère (OF ou produit).
    Arêtes = deux noeuds apparaissent consécutivement sur une même machine (voisinage L1).
    """
    if criterion not in {"of", "product"}:
        raise ValueError("criterion must be 'of' or 'product'")

    graph: Graph = defaultdict(set)

    # Regroupe par machine
    by_machine: Dict[str, List[Operation]] = defaultdict(list)
    for op in operations:
        by_machine[op.centre].append(op)

    for centre, ops in by_machine.items():
        ops_sorted = sorted(ops, key=lambda x: (x.start, x.end))

        # on ajoute aussi les noeuds isolés au graphe
        for op in ops_sorted:
            node = getattr(op, criterion)
            graph[node]  # assure la clé

        # Arêtes entre consécutifs (L1)
        for i in range(len(ops_sorted) - 1):
            a = getattr(ops_sorted[i], criterion)
            b = getattr(ops_sorted[i + 1], criterion)
            if a != b:
                graph[a].add(b)
                graph[b].add(a)

    return graph


def expand_graph_k_hops(g1: Graph, k: int = 2) -> Graph:
    """
    Construit un graphe où on connecte deux noeuds si leur distance <= k dans g1.
    (k=2 correspond à un "voisinage L2" : voisins + voisins des voisins).
    """
    if k < 1:
        raise ValueError("k must be >= 1")

    nodes = list(g1.keys())
    gk: Graph = defaultdict(set)

    # BFS limitée à k niveaux depuis chaque noeud
    for src in nodes:
        gk[src]  # assure clé
        visited = {src}
        frontier = {src}

        for _ in range(k):
            nxt = set()
            for u in frontier:
                for v in g1.get(u, set()):
                    if v not in visited:
                        visited.add(v)
                        nxt.add(v)
            frontier = nxt

        # visited contient src + tout ce qui est à distance <= k
        for dst in visited:
            if dst != src:
                gk[src].add(dst)
                gk[dst].add(src)

    return gk
