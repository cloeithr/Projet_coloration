from collections import defaultdict
from typing import Dict, Set, Iterable
from models import Operation

Graph = Dict[str, Set[str]]

def build_graph_immediate(
    operations: Iterable[Operation],
    criterion: str = "of"
) -> Graph:
    """
    Construit un graphe où deux sommets sont voisins si leurs blocs
    apparaissent consécutivement sur une même machine.
    """
    graph: Graph = defaultdict(set)

    # regrouper les opérations par machine
    by_machine = defaultdict(list)
    for op in operations:
        by_machine[op.centre].append(op)

    # trier par date par machine
    for machine, ops in by_machine.items():
        ops.sort(key=lambda x: x.start)

        # voisins immédiats
        for i in range(len(ops) - 1):
            a = getattr(ops[i], criterion)
            b = getattr(ops[i+1], criterion)

            if a != b:
                graph[a].add(b)
                graph[b].add(a)

    return graph
