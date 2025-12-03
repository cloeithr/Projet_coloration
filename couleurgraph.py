def color_graph(graph):
    colors = {}
    available_colors = ["red", "green", "blue", "yellow", "orange", "purple"]

    for node in graph:
        used = {colors[n] for n in graph[node] if n in colors}
        for color in available_colors:
            if color not in used:
                colors[node] = color
                break

    return colors
