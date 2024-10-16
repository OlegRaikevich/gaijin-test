import os
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        type=str,
        help="path to directory where need to search python files"
    )

    args = parser.parse_args()
    execute_commands(args.directory)


def find_python_files(directory):
    python_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return sorted(python_files)


def extract_commands_list(file):
    with open(file, "r") as file:
        content = file.read()
        local_dict = {}
        exec(content, {}, local_dict)
        return local_dict.get('CMDS', [])


def execute_commands(directory):
    python_files = find_python_files(directory)
    executed_cmds = set()

    for file in python_files:
        cmds = extract_commands_list(file)
        for cmd in cmds:
            if cmd not in executed_cmds:
                subprocess.run(cmd, shell=True)
                executed_cmds.add(cmd)
            else:
                print(f"Command {cmd} already executed.")


if __name__ == "__main__":
    main()
