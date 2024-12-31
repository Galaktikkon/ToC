import numpy as np
import sys

from utils.read import read_input

EPSILON = 1e-5


def destruct_matrix(M: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return M[:, :-1], M[:, -1]


def compare(a, b, epsilon):
    return abs(a - b) < epsilon


def check(input_file, output_file):

    I = read_input(input_file)
    lhs, rhs = destruct_matrix(I)

    x = np.linalg.solve(lhs, rhs)

    O = read_input(output_file, "results")
    processed_lhs, processed_rhs = destruct_matrix(O)

    for i in range(processed_lhs.shape[0]):
        for j in range(processed_lhs.shape[1]):
            if i == j:
                if not compare(1.0, processed_lhs[i][j], EPSILON):
                    print(f"Error 1 {i} {j}")
                    return
            else:
                if not compare(0.0, processed_lhs[i][j], EPSILON):
                    print(f"Error 2 {i} {j}")
                    return

    print(f"Ground truth (numpy):\n{" ".join(map(str, x))}")
    print()
    print(f"User solution:\n{" ".join(map(str, processed_rhs))}")

    for i in range(len(processed_rhs)):
        if not compare(x[i], processed_rhs[i], EPSILON):
            print(f"Error 3 {len(processed_rhs) + 1} {i}")
            print(f"{x[i]} {processed_rhs[i]}")
            return


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python checker.py <input_file> <output_file>")
        sys.exit(1)

    input_file: str = sys.argv[1]
    output_file: str = sys.argv[2]

    check(input_file, output_file)
