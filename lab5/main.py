from copy import copy
from collections import deque
import os
import sys
import pydot
import matplotlib.pyplot as plt


def read_input(file_name: str) -> tuple[dict[str, tuple[str, set[str]]], set[str], str]:

    with open("examples\\" + file_name, "r") as f:

        lines: list[str] = f.read().split(sep="\n")

        transactions, alphabet, word = lines[:-4], lines[-3], lines[-1]

    w: str = word[4:]
    A: set[str] = set(alphabet[5:-1].split(sep=", "))

    T: dict[str, tuple[str, set[str]]] = {}

    for t in transactions:
        key: str = t[1]
        left: str = t[4]
        right: set[str] = set(filter(lambda x: 97 <= ord(x) <= 122, t[8:]))
        T[key] = (left, right)

    return T, A, w


def get_sets(
    T: dict[str, tuple[str, set[str]]], A: list[str]
) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:

    D: set[tuple[str, str]] = set()
    I: set[tuple[str, str]] = set()

    for x in A:
        for y in A:
            if (T[x][0] in T[y][0]) or (T[x][0] in T[y][1]) or (T[y][0] in T[x][1]):
                D.add((x, y))
            else:
                I.add((x, y))

    return D, I


def get_indexed_word(w: str) -> list[str]:

    C: dict[str, int] = {}

    indexed_word: list[str] = []

    for letter in w:

        if letter in C:
            C[letter] += 1
        else:
            C[letter] = 1

        indexed_word.append(letter + str(C[letter]))

    return indexed_word


def get_diekert(D: set[tuple[str, str]], w: str) -> dict[str, set[str]]:

    G: dict[str, set[str]] = {}

    indexed_word: list[str] = get_indexed_word(w)

    for index in indexed_word:
        G[index] = set()

    for i, letter in enumerate(w):
        for j, next_letter in enumerate(w[i:]):
            for x, y in D:
                if (
                    x == letter
                    and y == next_letter
                    and indexed_word[i] != indexed_word[j + i]
                ):
                    G[indexed_word[i]].add(indexed_word[j + i])

    return G


def find_longest_paths(G: dict[str, set[str]]) -> dict[(str, str), list[str]]:

    all_paths: list[list[str]] = []

    def dfs(node: str, visited: set[str], path: list[str]):

        nonlocal G, all_paths
        visited.add(node)
        path.append(node)

        if len(path) > 1:
            all_paths.append(copy(path))

        for v in G[node]:
            if v not in visited:
                dfs(v, visited, path)

        visited.remove(node)
        path.pop()

    for root in G:
        dfs(root, set(), [])

    C: dict[(str, str), int] = {}
    P: dict[(str, str), list[str]] = {}

    for path in all_paths:
        a = path[0]
        b = path[-1]

        path_length = len(path) - 1

        if a != b:
            if (a, b) in C:
                if C[(a, b)] < path_length:
                    C[(a, b)] = path_length
                    P[(a, b)] = path
                elif C[(a, b)] == path_length:
                    del C[(a, b)]
                    del P[(a, b)]
            else:
                C[(a, b)] = path_length
                P[(a, b)] = path

    return P


def get_hesse(G: dict[str, set[str]], w: str) -> dict[str, set[str]]:

    P = find_longest_paths(G)

    H: dict[str, set[str]] = {}

    for index in get_indexed_word(w):
        H[index] = set()

    for path in P.values():
        for i in range(len(path) - 1):
            H[path[i]].add(path[i + 1])

    return H


def find_roots(H: dict[str, set[str]]) -> set[str]:

    is_root: dict[str, bool] = {}

    for v in H:
        is_root[v] = True

    for v in H:
        for u in H[v]:
            is_root[u] = False

    return set(filter(lambda v: is_root[v], is_root.keys()))


def get_foata(H: dict[str, set[str]]) -> str:

    start: str = "start"

    H[start] = find_roots(H)

    D: dict[str, int] = {}

    for v in H.keys():
        D[v] = 0

    Q = deque()

    Q.append(start)

    bundler: dict[int, list[str]] = {}

    while Q:
        v = Q.popleft()

        for u in H[v]:
            D[u] = max(D[u], D[v] + 1)
            Q.append(u)

    del D["start"]
    del H["start"]

    for key in D:
        if D[key] in bundler:
            bundler[D[key]].append(key[0])
        else:
            bundler[D[key]] = [key[0]]

    bundler = {i: bundler[i] for i in sorted(bundler.keys())}

    return "".join(list(map(lambda l: f'({"".join(sorted(l))})', bundler.values())))


def visualize_graph(graph: pydot.Dot) -> None:
    graph_path = "graph.png"
    graph.write_png(graph_path)

    img = plt.imread(graph_path)
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.axis("off")
    plt.show()

    os.remove("graph.png")


def save_to_file(
    D: set[tuple[str, str]],
    I: set[tuple[str, str]],
    F: dict[str, set[str]],
    filename: str,
    graph: pydot.Dot,
) -> None:

    save_file = f"results\\{filename}_result.txt"
    temp = f"results\\{filename}.dot"

    graph.write_raw(temp)

    with open(save_file, "w+") as f:
        f.write(f"D = {D}\n")
        f.write(f"I = {I}\n")
        f.write(f"FNF([w]) = {F}\n")

        with open(temp, "r") as g:
            f.write(g.read())

    os.remove(temp)


def create_vis_graph(H: dict[str, set[str]], w: str) -> pydot.Dot:

    indexed_word = get_indexed_word(w)

    translator = {}

    for i, index in enumerate(indexed_word, start=1):
        translator[index] = i

    graph = pydot.Dot(graph_type="digraph")

    for v in H:
        for u in H[v]:
            graph.add_edge(pydot.Edge(translator[v], translator[u]))

    for i, letter in enumerate(w, start=1):
        node_obj = pydot.Node(i)
        node_obj.set_label(letter)
        graph.add_node(node_obj)

    return graph


if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else "example_1.txt"

    T, A, w = read_input(filename)

    D, I = get_sets(T, A)

    G = get_diekert(D, w)
    H = get_hesse(G, w)
    F = get_foata(H)

    vis_graph = create_vis_graph(H, w)

    visualize_graph(vis_graph)

    save_file = os.path.basename(filename).split(".")[0]

    save_to_file(D, I, F, save_file, vis_graph)
