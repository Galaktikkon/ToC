from collections import deque
from copy import copy
import numpy as np


def get_alphabet(T: np.ndarray[str]) -> set[str]:
    return np.concatenate(T)


def get_transactions(n: int) -> np.ndarray[str]:

    T = []

    for i in range(1, n + 1):

        for j in range(i + 1, n + 1):
            transaction = []
            transaction.append(f"A{i}{j}")
            for k in range(1, n + 2):
                if k >= i:
                    transaction.append(f"B{i}{k}{j}")
                    transaction.append(f"C{i}{k}{j}")

            T.append(transaction)

    return np.array(T, dtype=object)


def get_dependency_set(
    S: set[str],
) -> set[tuple[str, str]]:

    D: set[tuple[str, str]] = set()

    for x in S:
        for y in S:
            match x[0], y[0]:
                case "A", "C":
                    if x[1:] == y[2:]:
                        D.add((x, y))
                        D.add((y, x))
                    if x[1] == y[2] == y[3]:
                        D.add((x, y))
                        D.add((y, x))
                case "A", "B":
                    if x[1] == y[1] and x[2] == y[3]:
                        D.add((x, y))
                        D.add((y, x))
                case "B", "C":
                    if x[1] == y[3] and x[2] == y[2]:
                        D.add((x, y))
                        D.add((y, x))
                    if x[1:] == y[1:]:
                        D.add((x, y))
                        D.add((y, x))
                case "C", "C":
                    if x[2:] == y[2:]:
                        D.add((x, y))
                        D.add((y, x))
    return D


def get_diekert(D: set[tuple[str, str]], word: list[str]) -> dict[str, set[str]]:

    G: dict[str, set[str]] = {}

    for letter in word:
        G[letter] = set()

    for i, letter in enumerate(word):
        for j, next_letter in enumerate(word[i:]):
            for x, y in D:
                if x == letter and y == next_letter and word[i] != word[j + i]:
                    G[word[i]].add(word[j + i])

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


def get_hesse(G: dict[str, set[str]], word: list[str]) -> dict[str, set[str]]:

    P = find_longest_paths(G)

    H: dict[str, set[str]] = {}

    for letter in word:
        H[letter] = set()

    for path in P.values():
        for i in range(len(path) - 1):
            H[path[i]].add(path[i + 1])

    return H


def find_roots(T: set[str]) -> set[str]:
    min_t = min(filter(lambda t: "A" in t, T), key=lambda t: t[1])

    return set(filter(lambda t: t == min_t, T))


def get_foata(
    H: dict[str, set[str]]
) -> tuple[str, dict[str, int], dict[int, np.ndarray[str]]]:

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
            bundler[D[key]].append(key)
        else:
            bundler[D[key]] = [key]

    bundler = {i: bundler[i] for i in sorted(bundler.keys())}

    foata_form = "".join(
        list(map(lambda l: f'({",".join(sorted(l))})', bundler.values()))
    )

    foata_dict = {}

    for key in bundler:
        for letter in bundler[key]:
            foata_dict[letter] = key

    foata_pools = bundler

    return foata_form, foata_dict, foata_pools


if __name__ == "__main__":
    pass
