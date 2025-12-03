import matplotlib.pyplot as plt

def export_txt(operations, colors, path):
    with open(path, "w") as f:
        for op in operations:
            f.write(f"{op.id} - {colors[op.id]} - type={op.criterion}\n")

def plot_gantt(operations, colors):
    fig, ax = plt.subplots()

    for i, op in enumerate(operations):
        ax.barh(op.machine, op.end - op.start, left=op.start, color=colors[op.id])
        ax.text(op.start, i, op.id)

    plt.show()
