import numpy as np
import sys
from concurrent.futures import ThreadPoolExecutor
from vis import *
from trace import *
from utils.read import *


def A(M: np.ndarray[float], i: int, k: int) -> float:
    return M[k, i] / M[i, i]


def B(M: np.ndarray[float], i: int, j: int, m: float) -> None:
    M[i, j] *= m


def C(M: np.ndarray[float], i: int, j: int, k: int) -> None:
    M[k, j] -= M[i, j]


def asynchronous_gauss(I: np.ndarray[float]) -> np.ndarray[float]:

    n, _ = I.shape

    coefficents = {}

    M = I.copy()

    def callback(t: str):
        nonlocal coefficents, M
        match t[0]:
            case "A":
                i, k = np.array(list(t[1:]), dtype=int) - 1
                coefficents[f"A{i}{k}"] = A(M, i, k)
            case "B":
                i, j, k = np.array(list(t[1:]), dtype=int) - 1
                B(M, i, j, coefficents[f"A{i}{k}"])
            case "C":
                i, j, k = np.array(list(t[1:]), dtype=int) - 1
                C(M, i, j, k)

    pools: list[dict[int, np.ndarray[str]]] = []

    T = get_transactions(n)
    FNF = ""
    for t in T:
        D = get_dependency_set(t)
        G = get_diekert(D, t)
        H = get_hesse(G, t)
        F, _, FP = get_foata(H)
        pools.append(FP)
        FNF += F

    print(f"Foata normal form: \n{FNF}\n")

    for pool in pools:
        for i in pool.keys():
            with ThreadPoolExecutor() as executor:
                for action in pool[i]:
                    executor.submit(callback, action)

    return M


def get_singular(T: np.ndarray) -> np.ndarray:

    M = T.copy()
    n = M.shape[0]

    for i in range(n - 1, -1, -1):

        sum_b = M[i, -1]

        for j in range(i + 1, n):
            sum_b -= M[i, j] * M[j, -1]

        M[i, -1] = sum_b / M[i, i]

        for j in range(i + 1, n):
            M[i, j] = 0

        M[i, i] = 1

    return np.array(M)


def save_matrix(M: np.ndarray, file_name: str):
    with open(os.path.join("results", file_name), "w+") as f:
        n, _ = M.shape
        f.write(f"{n}\n")
        for row in M:
            f.write(" ".join(map(str, row[:-1])) + "\n")
        f.write(" ".join(map(str, M[:, -1])))


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python gauss.py <input_file>")
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
    print(f"Input matrix: \n {M}")
    print()
    Q = asynchronous_gauss(M)
    J = get_singular(Q)
    print(f"Triangular matrix form: \n{Q}")
    print()
    print(f"Singular matrix form: \n {J}")
    print()
    save_matrix(J, file_name)
