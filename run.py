import hashlib
import os
import pickle


class MerkleNode:
    def __init__(self, hash_value, raw_files=None, left=None, right=None):
        self.hash_value = hash_value
        self.left = left
        self.right = right
        self.raw_files = raw_files


def calculate_file_hash(file_path):
    sha512 = hashlib.sha512()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha512.update(chunk)
    return sha512.hexdigest()


# def determine_file_type(file_path):
#     if


def build_big_tree(file_path):
    list = []
    for file in file_path:
        if os.path.isfile(file):
            list.append(MerkleNode(hash_value=calculate_file_hash(file), raw_files=[file]))
        elif os.path.isdir(file):
            list_dir = open_file(file)
            small_root = build_big_tree(list_dir)
            small_root.raw_files = [file]
            list.append(small_root)
    return build_merkle_tree(list)


def build_merkle_tree(file_path):
    leaf_nodes = file_path
    print(leaf_nodes)
    # Build the Merkle Tree bottom-up
    while len(leaf_nodes) > 1:
        new_level = []
        for i in range(0, len(leaf_nodes), 2):
            left = leaf_nodes[i]
            right = leaf_nodes[i + 1] if i + 1 < len(leaf_nodes) else None
            combined_hash = hashlib.sha512((left.hash_value + (right.hash_value if right else '')).encode()).hexdigest()

            new_node = MerkleNode(hash_value=combined_hash,
                                  raw_files=((left.raw_files + right.raw_files) if right else left.raw_files),
                                  left=left,
                                  right=right)
            new_level.append(new_node)
        leaf_nodes = new_level

    return leaf_nodes[0]  # Return the root of the Merkle Tree


def save_merkle_tree(root_node, save_path):
    with open(save_path, 'wb') as f:
        print(root_node)
        pickle.dump(root_node, f)


def open_file(main_file):
    file_list = os.listdir(main_file)
    full_path = [os.path.join(main_file, i) for i in file_list]
    return full_path


# Example usage:
def main():
    # Step 1: Build Merkle Tree and save it
    file_path = open_file("pack")
    print(file_path)
    merkle_tree_root = build_big_tree(file_path)

    save_merkle_tree(merkle_tree_root, 'merkle_tree.pkl')


if __name__ == "__main__":
    main()
