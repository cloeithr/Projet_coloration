from __future__ import annotations
from typing import Dict, Tuple, List, Optional
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from models import Operation


def plot_gantt(
    operations: List[Operation],
    node_to_color: Dict[str, Tuple[float, float, float]],
    criterion: str,
    title: str,
    save_path: str,
    show_labels: bool = True,
    min_label_hours: float = 24.0,   # n’affiche le texte que si barre >= 24h (réglable)
):
    if criterion not in {"of", "product"}:
        raise ValueError("criterion must be 'of' or 'product'")

    # machines triées “humainement”
    machines = sorted({op.centre for op in operations})
    y_positions = {m: i for i, m in enumerate(machines)}

    # figure plus grande si beaucoup de machines
    fig_h = max(6, 0.35 * len(machines))
    fig_w = 18
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    # Prépare la conversion dates->matplotlib
    def dt2num(dt: datetime) -> float:
        return mdates.date2num(dt)

    for op in operations:
        node = getattr(op, criterion)
        rgb = node_to_color.get(node, (0.8, 0.8, 0.8))

        y = y_positions[op.centre]
        start = dt2num(op.start)
        end = dt2num(op.end)
        width = max(1e-6, end - start)

        ax.barh(
            y=y,
            width=width,
            left=start,
            height=0.8,
            align="center",
            edgecolor="black",
            linewidth=0.3,
            color=rgb,
        )

        # label seulement si barre assez longue
        if show_labels:
            hours = (op.end - op.start).total_seconds() / 3600.0
            if hours >= min_label_hours:
                ax.text(
                    start + width / 2,
                    y,
                    f"{node}",
                    va="center",
                    ha="center",
                    fontsize=7,
                    color="black",
                    clip_on=True,
                )

    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(machines)
    ax.set_xlabel("Temps")
    ax.set_ylabel("Machines")
    ax.set_title(title)

    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    from datetime import timedelta

# Limiter l'affichage à 7 jours (une semaine)
    min_start = min(op.start for op in operations)
    max_end = min_start + timedelta(days=7)
    ax.set_xlim(min_start, max_end)


    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close(fig)
