from pathlib import Path
from parse_data import load_operations, load_machines
from graph_builder import build_graph_immediate, expand_graph_k_hops
from coloring import greedy_coloring
from palette import build_color_map, build_hex_color_map
from visualization import plot_gantt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "output"

def run_scenario(operations, machines, criterion, level):
    """Exécute, colorie et sauvegarde un scénario précis."""
    print(f"\n--- Exécution : {criterion.upper()} - Voisinage L{level} ---")
    
    # 1) Construction du graphe
    g1 = build_graph_immediate(operations, criterion=criterion)
    graph = g1 if level == 1 else expand_graph_k_hops(g1, k=level)

    # 2) Coloration (Algorithme Welsh-Powell par défaut)
    coloring_idx = greedy_coloring(graph, order="largest_first")
    nb_colors = max(coloring_idx.values()) + 1 if coloring_idx else 0

    # 3) Préparation des couleurs
    node_to_rgb = build_color_map(coloring_idx)
    node_to_hex = build_hex_color_map(coloring_idx)

    # 4) Export TXT
    file_name = f"coloration_{criterion}_L{level}.txt"
    out_file = OUT / file_name
    with out_file.open("w", encoding="utf-8") as f:
        f.write("centre;product;of;sequence;op;start;end;color\n")
        for op in operations:
            key = getattr(op, criterion)
            color = node_to_hex.get(key, "#FFFFFF")
            f.write(f"{op.centre};{op.product};{op.of};{op.sequence};{op.op};"
                    f"{op.start};{op.end};{color}\n")

    # 5) Génération du Gantt
    gantt_path = OUT / f"gantt_{criterion}_L{level}.png"
    plot_gantt(
        operations=operations,
        node_to_color=node_to_rgb,
        criterion=criterion,
        title=f"Gantt - Coloration par {criterion.upper()} (Voisinage L{level}) - {nb_colors} couleurs",
        save_path=str(gantt_path),
        min_label_hours=12.0 # Ajuste pour voir plus ou moins de texte
    )
    
    print(f"Terminé : {nb_colors} couleurs utilisées. Image : {gantt_path.name}")

def main():
    OUT.mkdir(exist_ok=True)
    operations = load_operations(DATA / "DataPlanification.txt")
    machines = load_machines(DATA / "DataMachine.txt")

    if not operations:
        print("Erreur : Aucune donnée chargée.")
        return

    # On lance les 4 combinaisons pour le rapport final
    scenarios = [
        ("of", 1),
        ("of", 2),
        ("product", 1),
        ("product", 2)
    ]

    for crit, lvl in scenarios:
        run_scenario(operations, machines, crit, lvl)

    print("\n✅ Tous les scénarios ont été générés dans le dossier /output !")

if __name__ == "__main__":
    main()
