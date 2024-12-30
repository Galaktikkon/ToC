import sys
import subprocess


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file: str = sys.argv[1]

    subprocess.run(["python", "vis.py", input_file])
    subprocess.run(["python", "gauss.py", input_file])
    subprocess.run(["python", "checker.py", input_file, input_file])
