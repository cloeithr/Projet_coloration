from datetime import datetime
from models import Operation
from graph_builder import build_graph_immediate
from coloring import greedy_coloring

def dt(s: str) -> datetime:
    # format "2025-11-24 08:00"
    return datetime.fromisoformat(s.replace(" ", "T"))

def main():
    # Une seule machine MAC101, deux OF : OF1 et OF2
    ops = [
        Operation("MAC101", "PROD1", "OF1", "0000", "0010",
                  dt("2025-11-24 08:00"), dt("2025-11-24 10:00")),
        Operation("MAC101", "PROD1", "OF2", "0000", "0010",
                  dt("2025-11-24 10:00"), dt("2025-11-24 12:00")),
        Operation("MAC101", "PROD2", "OF1", "0000", "0010",
                  dt("2025-11-24 13:00"), dt("2025-11-24 15:00")),
    ]

    # Graphe de voisinage par OF
    graph = build_graph_immediate(ops, criterion="of")
    print("Graphe (voisins par OF) :", graph)

    # Coloration
    colors_idx = greedy_coloring(graph)
    print("Couleurs (index) :", colors_idx)

if __name__ == "__main__":
    main()
