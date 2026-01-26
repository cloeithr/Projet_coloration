from __future__ import annotations
from typing import Dict, Tuple, List

# Palette de couleurs contrastées pour le Gantt
DEFAULT_PALETTE: List[Tuple[float, float, float]] = [
    (0.55, 0.80, 0.35),  # vert
    (0.90, 0.40, 0.40),  # rouge doux
    (0.35, 0.65, 0.90),  # bleu
    (0.75, 0.55, 0.90),  # violet
    (0.95, 0.75, 0.35),  # orange
    (0.45, 0.85, 0.80),  # cyan
    (0.85, 0.85, 0.45),  # jaune
    (0.70, 0.70, 0.70),  # gris
    (0.55, 0.55, 0.95),  # indigo
    (0.95, 0.55, 0.75),  # rose



    (0.60, 0.40, 0.20),  # marron
    (0.20, 0.60, 0.50),  # vert-bleuté
    (0.90, 0.60, 0.20),  # ambre
    (0.45, 0.45, 0.20),  # olive
    (0.20, 0.30, 0.60),  # bleu nuit
]


def rgb_to_hex(rgb: Tuple[float, float, float]) -> str:
    """Convertit un tuple (R, G, B) en format #RRGGBB."""
    return '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def build_color_map(coloring: Dict[str, int]) -> Dict[str, Tuple[float, float, float]]:
    """Map entre l'identifiant (OF/Produit) et son tuple RGB."""
    return {node: DEFAULT_PALETTE[idx % len(DEFAULT_PALETTE)] for node, idx in coloring.items()}

def build_hex_color_map(coloring: Dict[str, int]) -> Dict[str, str]:
    """Map entre l'identifiant (OF/Produit) et son code Hexadécimal."""
    return {node: rgb_to_hex(DEFAULT_PALETTE[idx % len(DEFAULT_PALETTE)]) for node, idx in coloring.items()}