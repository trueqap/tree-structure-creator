import os


def parse_tree_line(line):
    """
    Parse a single line from the tree structure.

    Args:
    line (str): A line from the tree output.

    Returns:
    tuple: (depth, name) where depth is an integer and name is a string.
    """
    depth = 0
    for char in line:
        if char in "│└├":
            depth += 1
        elif char != " ":
            break
    name = line.split("─")[-1].strip()
    return depth, name


def create_directory_structure(tree_file):
    """
    Create directory structure based on the tree file.

    Args:
    tree_file (str): Path to the file containing the tree structure.
    """
    with open(tree_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    root = lines[0].strip()
    os.makedirs(root, exist_ok=True)
    current_path = [root]

    for line in lines[1:]:
        depth, name = parse_tree_line(line)

        # Adjust the current path based on depth
        current_path = current_path[: depth + 1]

        if name.endswith("/"):
            # This is a directory
            current_path.append(name[:-1])
            full_path = os.path.join(*current_path)
            os.makedirs(full_path, exist_ok=True)
        else:
            # This is a file
            full_path = os.path.join(*current_path, name)
            open(full_path, "a").close()


if __name__ == "__main__":
    tree_file = "tree.txt"
    create_directory_structure(tree_file)
    print("Directory structure successfully created!")
