import numpy as np
import sys
from concurrent.futures import ThreadPoolExecutor
import threading
from utils.vis import *
from utils.trace import *


def read_input(file_name: str) -> np.ndarray[int]:

    with open("examples\\" + file_name, "r") as f:

        lines: list[str] = f.read().split(sep="\n")

    data: np.ndarray[float] = np.array(
        list(
            map(
                lambda row: np.astype(np.array(row.split(" ")), np.float64),
                lines[1:],
            )
        )
    )

    A: np.ndarray[float] = data[:-1]
    b: np.ndarray[float] = np.array([data[-1]])

    M = np.hstack((A, b.T))

    return M


def A(M: np.ndarray[float], i: int, k: int) -> float:
    return M[k, i] / M[i, i]


def B(M: np.ndarray[float], i: int, j: int, m: float) -> None:
    M[i, j] *= m


def C(M: np.ndarray[float], i: int, j: int, k: int) -> None:
    M[k, j] -= M[i, j]


def concurrent_gauss(M: np.ndarray[float], T: np.ndarray[str]) -> np.ndarray[float]:

    lock = threading.Lock()
    coefficents = {}

    def callback(t: str):
        nonlocal coefficents, M
        match t[0]:
            case "A":
                i, k = np.array(list(t[1:]), dtype=int) - 1
                with lock:
                    coefficents[f"A{i}{k}"] = A(M, i, k)
            case "B":
                i, j, k = np.array(list(t[1:]), dtype=int) - 1
                with lock:
                    B(M, i, j, coefficents[f"A{i}{k}"])
            case "C":
                i, j, k = np.array(list(t[1:]), dtype=int) - 1
                with lock:
                    C(M, i, j, k)

    pools: list[dict[int, np.ndarray[str]]] = []

    for t in T:
        D = get_dependency_set(t)
        G = get_diekert(D, t)
        H = get_hesse(G, t)
        _, _, FP = get_foata(H)
        pools.append(FP)

    for pool in pools:
        for i in pool.keys():
            with ThreadPoolExecutor() as executor:
                for action in pool[i]:
                    executor.submit(callback, action)

    return M


if __name__ == "__main__":

    file_name: str = sys.argv[1] if len(sys.argv) > 1 else "input1.txt"

    M = read_input(file_name=file_name)
    # k = 3
    # R = np.random.randint(size=(k, k), high=10, low=1)
    # b = np.random.randint(size=(1, k), high=10, low=1)
    # M = np.hstack((R, b.T))
    n = M.shape[0]

    T = get_transactions(n)
    S = get_alphabet(T)
    D = get_dependency_set(S)

    G = get_diekert(D, S)
    H = get_hesse(G, S)
    FF, FD, FP = get_foata(H)
    vis_graph = create_vis_graph(H, S, FD)

    visualize_graph(vis_graph)

    print(M)
    a = M[:, [range(n)]].reshape(n, -1)
    b = M[:, n]
    print(np.linalg.solve(a, b))
    CG = concurrent_gauss(M, T)
    print(CG)
    c = CG[:, [range(n)]].reshape(n, -1)
    d = CG[:, n]
    print(np.linalg.solve(c, d))
    # print(np.allclose(CG, U))
