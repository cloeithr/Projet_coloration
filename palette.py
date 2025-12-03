from colorsys import hsv_to_rgb

def generate_palette(n: int) -> list[str]:
    """
    Génère n couleurs pastel **très distinctes** en format HEX (#RRGGBB)
    en utilisant un espacement régulier dans le cercle HSV.
    """
    colors = []
    for i in range(n):
        # 1. Teinte espacée régulièrement
        h = i / n  

        # 2. Saturation réduite -> pastel
        s = 0.45  

        # 3. Luminosité élevée -> lisible sur Gantt
        v = 0.95  

        # Conversion HSV -> RGB
        r, g, b = hsv_to_rgb(h, s, v)

        # Conversion RGB -> HEX
        hex_color = '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
        colors.append(hex_color)

    return colors
def hsv_distance(h1: float, h2: float) -> float:
    """
    Distance circulaire entre deux teintes (0 à 1).
    """
    d = abs(h1 - h2)
    return min(d, 1 - d)
