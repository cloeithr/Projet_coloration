from chargement import load_from_csv
from graph import build_graph
from couleurgraph import color_graph
from visualisation import export_txt, plot_gantt

def main():
    operations = load_from_csv("../data/operations.csv")
    graph = build_graph(operations)
    colors = color_graph(graph)

    export_txt(operations, colors, "../result.txt")
    plot_gantt(operations, colors)

if __name__ == "__main__":
    main()
