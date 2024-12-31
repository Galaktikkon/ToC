import sys
import subprocess
import os
import re


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>|<n>")
        sys.exit(1)

    arg = sys.argv[1]

    if arg.isnumeric():
        examples_dir = "examples"
        highest_x = -1
        highest_file = None

        for filename in os.listdir(examples_dir):
            match = re.match(r"input(\d+)\.txt", filename)
            if match:
                x = int(match.group(1))
                if x > highest_x:
                    highest_x = x
                    highest_file = filename

        if highest_file:
            new_file_name = f"input{highest_x + 1}.txt"
        else:
            new_file_name = f"input1.txt"

        input_file = new_file_name
        subprocess.run(["python", "generator.py", arg, input_file])
    else:
        input_file: str = sys.argv[1]

    subprocess.run(["python", "vis.py", input_file])
    subprocess.run(["python", "gauss.py", input_file])
    subprocess.run(["python", "checker.py", input_file, input_file])
