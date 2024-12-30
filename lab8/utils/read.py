import os
import numpy as np


def read_input(file_name: str, dir: str = "examples") -> np.ndarray[int]:

    with open(os.path.join(dir, file_name), "r") as f:

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


if __name__ == "__main__":
    pass
