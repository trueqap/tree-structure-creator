import os
import re


def parse_tree_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    structure = []
    current_path = []

    # Add root directory
    root_dir = lines[0].strip()
    structure.append((root_dir, True))

    for line in lines[1:]:
        depth = len(re.findall(r"│   |\s{4}", line))
        name = line.strip().split("─ ")[-1]

        while len(current_path) > depth:
            current_path.pop()

        if "└─" in line or "├─" in line:
            current_path = current_path[:depth]
            current_path.append(name)
            full_path = os.path.join(root_dir, *current_path)
            is_dir = "/" in name
            if full_path:  # Only add if not empty
                structure.append((full_path, is_dir))

    return structure


def create_structure(structure):
    for path, is_dir in structure:
        try:
            if is_dir:
                os.makedirs(path, exist_ok=True)
            else:
                dir_path = os.path.dirname(path)
                if dir_path:  # Check if the directory path is not empty
                    os.makedirs(dir_path, exist_ok=True)
                open(path, "a").close()
        except OSError as e:
            print(f"Error occurred while creating '{path}': {e}")


def main():
    tree_file = "tree.txt"
    if not os.path.exists(tree_file):
        print(
            f"The file '{tree_file}' does not exist. Please make sure the file is in the correct location."
        )
        return

    structure = parse_tree_file(tree_file)
    if not structure:
        print("The file structure is empty or not in the correct format.")
        return

    create_structure(structure)
    print("File and folder structure successfully created.")


if __name__ == "__main__":
    main()
