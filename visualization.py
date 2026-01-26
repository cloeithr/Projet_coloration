from __future__ import annotations
from typing import Dict, Tuple, List, Optional
from datetime import datetime, timedelta
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
    min_label_hours: float = 24.0,
    days_to_plot: Optional[int] = None  # None = Tout l'horizon
):
    if criterion not in {"of", "product"}:
        raise ValueError("criterion must be 'of' or 'product'")

    machines = sorted({op.centre for op in operations})
    y_positions = {m: i for i, m in enumerate(machines)}

    fig_h = max(6, 0.35 * len(machines))
    fig_w = 18
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    def dt2num(dt: datetime) -> float:
        return mdates.date2num(dt)

    for op in operations:
        node = getattr(op, criterion)
        rgb = node_to_color.get(node, (0.8, 0.8, 0.8))
        
        start = dt2num(op.start)
        end = dt2num(op.end)
        width = max(1e-6, end - start)

        ax.barh(
            y=y_positions[op.centre],
            width=width,
            left=start,
            height=0.8,
            align="center",
            edgecolor="black",
            linewidth=0.3,
            color=rgb,
        )

        if show_labels:
            hours = (op.end - op.start).total_seconds() / 3600.0
            if hours >= min_label_hours:
                ax.text(
                    start + width / 2,
                    y_positions[op.centre],
                    f"{node}",
                    va="center", ha="center", fontsize=7, color="black", clip_on=True,
                )

    # Gestion de la fenêtre de temps
    if days_to_plot is not None and operations:
        min_start = min(op.start for op in operations)
        ax.set_xlim(dt2num(min_start), dt2num(min_start + timedelta(days=days_to_plot)))
        title += f" (Vue {days_to_plot} jours)"

    ax.set_yticks(range(len(machines)))
    ax.set_yticklabels(machines)
    ax.set_xlabel("Temps")
    ax.set_ylabel("Machines")
    ax.set_title(title)

    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()