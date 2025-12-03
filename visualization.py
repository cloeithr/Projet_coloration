import matplotlib.pyplot as plt
from typing import Dict, Iterable
from models import Operation, Machine

def plot_gantt(
    operations: Iterable[Operation],
    machines: list[Machine],
    color_by_key: Dict[str, str],
    criterion: str,
    title: str,
    output_path: str | None = None,
):
    """
    Affiche un Gantt coloré. (code complet viendra plus tard)
    """
    plt.figure(figsize=(14, 6))
    plt.title(title)
    plt.xlabel("Temps")
    plt.ylabel("Machines")

    # TODO: implémenter le tracé

    if output_path:
        plt.savefig(output_path, bbox_inches="tight")
    else:
        plt.show()
