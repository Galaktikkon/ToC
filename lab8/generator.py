import os
import numpy as np
import sys

EPSILON = 1e-5


def compare(a, b, epsilon) -> bool:
    return abs(a - b) < epsilon


def requires_pivot(m, size) -> bool:
    matrix = m.copy()

    for i in range(size):
        if compare(0.0, matrix[i, i], EPSILON):
            return True

        for j in range(i + 1, size):
            n = matrix[j, i] / matrix[i, i]
            matrix[j, :] -= n * matrix[i, :]

    return False


def generate(file_name: str, n: int) -> None:

    A = np.random.rand(n, n)
    B = np.random.rand(n, 1)

    lu = np.linalg.matrix_rank(A) == n
    while not lu or requires_pivot(A, n):
        A = np.random.rand(n, n)
        B = np.random.rand(n, 1)
        lu = np.linalg.matrix_rank(A) == n

    with open(os.path.join("examples", file_name), "w") as f:
        f.write(f"{n}\n")
        for row in A:
            f.write(" ".join(map(str, row)) + "\n")
        f.write(" ".join(map(str, B.flatten())))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generator.py <matrix_size> <file_name>")
        sys.exit(1)

    n = int(sys.argv[1])
    file_name = sys.argv[2]

    generate(file_name, n)
