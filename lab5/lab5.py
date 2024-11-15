from itertools import product

transaction = tuple[str, set[str]]


def read_input(file_name: str) -> tuple[dict[str, transaction], set[str], str]:

    with open("examples\\" + file_name, "r") as f:

        lines: list[str] = f.read().split(sep="\n")

        transactions, alphabet, word = lines[:-4], lines[-3], lines[-1]

    w: str = word[4:]
    A: set[str] = set(alphabet[5:-1].split(sep=", "))

    T: dict[str, transaction] = {}

    for t in transactions:
        key: str = t[1]
        left: str = t[4]
        right: set[str] = set(filter(lambda x: 97 <= ord(x) <= 122, t[8:]))
        T[key] = (left, right)

    return T, A, w


def get_dependent(T: dict[str, transaction], A: list[str]) -> set[tuple[str, str]]:

    D: set[tuple[str, str]] = set()

    for x in A:
        for y in A:

            if (T[x][0] in T[y][0]) or (T[x][0] in T[y][1]) or (T[y][0] in T[x][1]):
                D.add((x, y))

    return D


def get_independent(D: set[tuple[str, str]], A: list[str]) -> set[tuple[str, str]]:

    P = set(product(A, A))

    I = P - D

    return I


if __name__ == "__main__":

    T, A, w = read_input("example_1.txt")

    D = get_dependent(T, A)
    I = get_independent(D, A)
