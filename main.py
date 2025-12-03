from pathlib import Path
from parse_data import load_operations, load_machines
from graph_builder import build_graph_immediate
from coloring import greedy_coloring
from palette import generate_palette
from visualization import plot_gantt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "output"


def main():
    # 1) Chargement des données
    operations = load_operations(DATA / "DataPlanification.txt")
    machines = load_machines(DATA / "DataMachine.txt")

    # Sécurité : vérifier qu'on a bien des données
    if not operations:
        print("Aucune opération chargée. Vérifie DataPlanification.txt.")
        return

    if not machines:
        print("Aucune machine chargée. Vérifie DataMachine.txt.")
        return

    # 2) Construction du graphe de voisinage par OF (Objectif 1)
    graph = build_graph_immediate(operations, criterion="of")

    # 3) Coloration gloutonne du graphe
    if not graph:
        print("Graphe vide (aucun OF trouvé).")
        return

    colors_idx = greedy_coloring(graph)

    nb_colors = max(colors_idx.values()) + 1
    palette = generate_palette(nb_colors)

    # Association OF -> couleur hex
    color_by_of = {of: palette[idx] for of, idx in colors_idx.items()}

    # 4) Création du dossier output si besoin
    OUTPUT.mkdir(exist_ok=True)

    # 5) Écriture d'un fichier texte de résultat (Objectif 1)
    out_file = OUTPUT / "coloration_of.txt"
    with out_file.open("w", encoding="utf-8") as f:
        # en-tête
        f.write(
            "centre;product;of;sequence;op;start;end;color\n"
        )
        # lignes
        for op in operations:
            color = color_by_of.get(op.of, "#000000")
            f.write(
                f"{op.centre};"
                f"{op.product};"
                f"{op.of};"
                f"{op.sequence};"
                f"{op.op};"
                f"{op.start.isoformat(sep=' ')};"
                f"{op.end.isoformat(sep=' ')};"
                f"{color}\n"
            )

    # 6) Affichage de quelques statistiques utiles
    distinct_of = {op.of for op in operations}
    print("=== Statistiques (Objectif 1) ===")
    print(f"Nombre d'opérations      : {len(operations)}")
    print(f"Nombre de machines       : {len(machines)}")
    print(f"Nombre d'OF distincts    : {len(distinct_of)}")
    print(f"Nombre de sommets graphe : {len(graph)}")
    print(f"Nombre de couleurs utilisé : {nb_colors}")
    print(f"Fichier résultat écrit dans : {out_file}")

    # 7) (Optionnel pour semaine 2) Tentative de Gantt simple
    #    La fonction plot_gantt est encore un squelette, on le complétera plus tard.
    try:
        plot_gantt(
            operations=operations,
            machines=machines,
            color_by_key=color_by_of,
            criterion="of",
            title="Coloration par OF",
            output_path=str(OUTPUT / "gantt_of.png"),
        )
        print(f"Image Gantt écrite dans : {OUTPUT / 'gantt_of.png'}")
    except Exception as e:
        # Si visualization.py n'est pas encore implémenté, on ne bloque pas le projet.
        print("plot_gantt non fonctionnel pour le moment (ce n'est pas grave pour la semaine 2).")
        print(f"Erreur : {e}")


if __name__ == "__main__":
    main()
