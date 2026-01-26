import sys
from pathlib import Path

FILE_PATH = Path(__file__).resolve()
SRC_PATH = FILE_PATH.parent
ROOT = SRC_PATH.parent
DATA = ROOT / "data"
OUT = ROOT / "output"

if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

from parse_data import load_operations
from graph_builder import build_graph_immediate, expand_graph_k_hops
from coloring import greedy_coloring, verify_coloring, get_graph_stats
from palette import build_color_map, build_hex_color_map
from visualization import plot_gantt

def run_scenario(operations, criterion, level, days=None):
    suffix = "global" if days is None else f"{days}d"
    print(f"\n--- Calcul : {criterion.upper()} (Voisinage L{level}) | Vue: {suffix} ---")
    
    # 1) Graphe
    g1 = build_graph_immediate(operations, criterion=criterion)
    graph = g1 if level == 1 else expand_graph_k_hops(g1, k=level)

    # 2) Stats et Coloration
    nb_n, nb_e, dens = get_graph_stats(graph)
    print(f"📊 Graphe : {nb_n} nœuds, {nb_e} arêtes, densité: {dens:.4f}")

    coloring_idx = greedy_coloring(graph, order="largest_first")
    nb_colors = max(coloring_idx.values()) + 1 if coloring_idx else 0
    
    is_valid = verify_coloring(graph, coloring_idx)
    status = "✅ VALIDE" if is_valid else "❌ CONFLIT"
    print(f"🎨 Coloration : {nb_colors} couleurs | {status}")

    # 3) Couleurs
    node_to_rgb = build_color_map(coloring_idx)
    node_to_hex = build_hex_color_map(coloring_idx)

    # 4) Export TXT
    out_txt = OUT / f"coloration_{criterion}_L{level}.txt"
    with out_txt.open("w", encoding="utf-8") as f:
        f.write("centre;product;of;sequence;op;start;end;color\n")
        for op in operations:
            key = getattr(op, criterion)
            f.write(f"{op.centre};{op.product};{op.of};{op.sequence};{op.op};{op.start};{op.end};{node_to_hex.get(key, '#FFFFFF')}\n")

    # 5) Image
    gantt_path = OUT / f"gantt_{criterion}_L{level}_{suffix}.png"
    plot_gantt(
        operations=operations,
        node_to_color=node_to_rgb,
        criterion=criterion,
        title=f"Gantt {criterion.upper()} L{level} ({nb_colors} coul.)",
        save_path=str(gantt_path),
        days_to_plot=days
    )
    print(f"🖼️  Image générée : {gantt_path.name}")

def main():
    OUT.mkdir(exist_ok=True)
    data_file = DATA / "DataPlanification.txt"
    if not data_file.exists():
        print(f"❌ Fichier manquant : {data_file}")
        return

    operations = load_operations(data_file)
    print(f"✔ {len(operations)} opérations chargées.")

    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Scénarios OF (L1 & L2) - Vue Globale")
        print("2. Scénarios OF (L1 & L2) - Vue 7 jours (Lisible)")
        print("3. Scénarios PRODUIT (L1 & L2) - Vue Globale")
        print("4. Scénarios PRODUIT (L1 & L2) - Vue 7 jours")
        print("5. TOUT LANCER (8 rendus)")
        print("q. Quitter")
        
        choice = input("\nVotre choix : ").strip().lower()
        if choice == 'q': break
        
        if choice == '1':
            run_scenario(operations, "of", 1, days=None)
            run_scenario(operations, "of", 2, days=None)
        elif choice == '2':
            run_scenario(operations, "of", 1, days=7)
            run_scenario(operations, "of", 2, days=7)
        elif choice == '3':
            run_scenario(operations, "product", 1, days=None)
            run_scenario(operations, "product", 2, days=None)
        elif choice == '4':
            run_scenario(operations, "product", 1, days=7)
            run_scenario(operations, "product", 2, days=7)
        elif choice == '5':
            for c in ["of", "product"]:
                for l in [1, 2]:
                    for d in [None, 7]:
                        run_scenario(operations, c, l, days=d)

if __name__ == "__main__":
    main()