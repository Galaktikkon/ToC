import os
import sys
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import pydot
from utils.read import *
from utils.trace import *


def create_vis_graph(
    H: dict[str, set[str]], word: str, FD: dict[str, int]
) -> pydot.Dot:

    translator = {}

    colors = list(mcolors.TABLEAU_COLORS.values())

    for i, index in enumerate(word, start=1):
        translator[index] = i

    graph = pydot.Dot(graph_type="digraph")

    for v in H:
        for u in H[v]:
            graph.add_edge(pydot.Edge(translator[v], translator[u]))

    for i, letter in enumerate(word, start=1):
        node = pydot.Node(i)
        node.set_style("filled")
        node.set_fillcolor(f"{colors[FD[letter] - 1]}")
        node.set_label(f"<{letter[0]}<SUB>{letter[1:]}</SUB>>")
        graph.add_node(node)

    return graph


def visualize_graph(graph: pydot.Dot) -> None:
    graph_path = "graph.png"
    graph.write_png(graph_path)

    img = plt.imread(graph_path)
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.axis("off")
    plt.show()

    os.remove("graph.png")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python vis.py <input_file>")
        sys.exit(1)

    file_name: str = sys.argv[1]

    M = read_input(file_name=file_name)
    n = M.shape[0]

    T = get_transactions(n)
    S = get_alphabet(T)
    D = get_dependency_set(S)

    G = get_diekert(D, S)
    H = get_hesse(G, S)
    FF, FD, FP = get_foata(H)

    vis_graph = create_vis_graph(H, S, FD)

    visualize_graph(vis_graph)
