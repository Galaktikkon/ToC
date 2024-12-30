import numpy as np
import matplotlib.pyplot as plt
import time
from multiprocessing import Manager, shared_memory
from gauss import *
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def naive_gauss(M: np.ndarray) -> np.ndarray:
    n, _ = M.shape

    for i in range(n):
        M[i] = M[i] / M[i, i]
        for j in range(i + 1, n):
            M[j] = M[j] - M[j, i] * M[i]

    return M


def callback(
    t: str, shm_name: str, dtype: np.dtype, shape: tuple[int, int], coefficients: dict
) -> None:

    existing_shm = shared_memory.SharedMemory(name=shm_name)
    shared_matrix = np.ndarray(shape=shape, dtype=dtype, buffer=existing_shm.buf)

    match t[0]:
        case "A":
            i, k = np.array(list(t[1:]), dtype=int) - 1
            coefficients[f"A{i}{k}"] = A(shared_matrix, i, k)
        case "B":
            i, j, k = np.array(list(t[1:]), dtype=int) - 1
            B(shared_matrix, i, j, coefficients[f"A{i}{k}"])
        case "C":
            i, j, k = np.array(list(t[1:]), dtype=int) - 1
            C(shared_matrix, i, j, k)

    existing_shm.close()


def parallel_gauss_no_prep(
    M: np.ndarray[float], pools: list[dict[int, np.ndarray[str]]]
) -> np.ndarray[float]:

    coefficients = Manager().dict()

    shm = shared_memory.SharedMemory(create=True, size=M.nbytes)
    shm_matrix = np.ndarray(M.shape, dtype=M.dtype, buffer=shm.buf)
    shm_matrix[:] = M[:]

    futures = []
    for pool in pools:
        for i in pool.keys():
            with ProcessPoolExecutor() as executor:
                for action in pool[i]:
                    futures.append(
                        executor.submit(
                            callback,
                            action,
                            shm.name,
                            shm_matrix.dtype,
                            shm_matrix.shape,
                            coefficients,
                        )
                    )

    for future in futures:
        future.result()

    result = shm_matrix.copy()
    shm.close()
    shm.unlink()

    return result


def asynchronous_gauss_no_prep(
    M: np.ndarray[float], pools: list[dict[int, np.ndarray[str]]]
) -> np.ndarray[float]:

    coefficents = {}

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

    for pool in pools:
        for i in pool.keys():
            with ThreadPoolExecutor() as executor:
                for action in pool[i]:
                    executor.submit(callback, action)

    return M


def gauss_prep(n: int) -> list[dict[int, np.ndarray[str]]]:
    pools: list[dict[int, np.ndarray[str]]] = []

    T = get_transactions(n)

    for t in T:
        D = get_dependency_set(t)
        G = get_diekert(D, t)
        H = get_hesse(G, t)
        _, _, FP = get_foata(H)
        pools.append(FP)

    return pools


def run_tests(f, *args) -> float:

    start_time = time.time()
    f(*args)
    end_time = time.time()
    return end_time - start_time


def visualize_gauss_timing(
    ns,
    naive_times,
    parallel_total,
    asynchronous_total,
    parallel_no_prep_times,
    asynchronous_no_prep_times,
    prep_times,
):
    plt.plot(ns, naive_times, label="Naive Gauss", linestyle="-", marker="o")
    plt.plot(
        ns, parallel_total, label="parallel Gauss Total", linestyle="--", marker="x"
    )
    plt.plot(
        ns,
        asynchronous_total,
        label="Asynchronous Gauss Total",
        linestyle="--",
        marker="v",
    )
    plt.plot(
        ns,
        parallel_no_prep_times,
        label="parallel Gauss",
        linestyle="-.",
        marker="s",
    )
    plt.plot(
        ns,
        asynchronous_no_prep_times,
        label="Asynchronous Gauss",
        linestyle="-.",
        marker="^",
    )
    plt.plot(
        ns,
        prep_times,
        label="Preparation Time",
        linestyle=":",
        marker="d",
    )

    plt.xlabel("Matrix size (n)")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.title("Performance Comparison of Gauss Elimination Algorithms")
    plt.show()


def get_random_matrix(n: int) -> np.ndarray:

    A = np.random.rand(n, n)
    b = np.random.rand(n)
    M = np.hstack([A, b.reshape(-1, 1)])
    return M


if __name__ == "__main__":
    ns = range(2, 6)
    total_ns = len(ns)

    naive_times = np.zeros(total_ns)
    prep_times = np.zeros(total_ns)
    parallel_no_prep_times = np.zeros(total_ns)
    asynchronous_no_prep_times = np.zeros(total_ns)

    for i, n in enumerate(ns):

        M = get_random_matrix(n)
        naive_times[i] = run_tests(naive_gauss, M)
        prep_times[i] = run_tests(gauss_prep, n)

        pools = gauss_prep(n)
        parallel_no_prep_times[i] = run_tests(parallel_gauss_no_prep, M, pools)
        asynchronous_no_prep_times[i] = run_tests(asynchronous_gauss_no_prep, M, pools)

        print(f"Tested {((i + 1) / total_ns) * 100:.2f}% of all n", end="\r")

    parallel_total = parallel_no_prep_times + prep_times
    asynchronous_total = asynchronous_no_prep_times + prep_times

    visualize_gauss_timing(
        ns,
        naive_times,
        parallel_total,
        asynchronous_total,
        parallel_no_prep_times,
        asynchronous_no_prep_times,
        prep_times,
    )
