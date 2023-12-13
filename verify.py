import hashlib
import os
import pickle
import main


class MerkleNode:
    def __init__(self, hash_value, raw_file=None,left=None, right=None):
        self.hash_value = hash_value
        self.left = left
        self.right = right
        self.raw_file=raw_file

def calculate_file_hash(file_path):
    sha512 = hashlib.sha512()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha512.update(chunk)
    return sha512.hexdigest()


def build_merkle_tree(file_path):
    # Read the file and build a list of leaf nodes
    leaf_nodes = [MerkleNode(calculate_file_hash(file_path[0])),
                  MerkleNode(hash_value=calculate_file_hash(file_path[1])),
                  MerkleNode(hash_value=calculate_file_hash(file_path[2])),
                  MerkleNode(hash_value=calculate_file_hash(file_path[3]))]

    # Build the Merkle Tree bottom-up
    while len(leaf_nodes) > 1:
        new_level = []
        for i in range(0, len(leaf_nodes), 2):
            left = leaf_nodes[i]
            right = leaf_nodes[i + 1] if i + 1 < len(leaf_nodes) else None
            combined_hash = hashlib.sha512((left.hash_value + (right.hash_value if right else '')).encode()).hexdigest()

            new_node = MerkleNode(hash_value=combined_hash, left=left, right=right)
            new_level.append(new_node)
        leaf_nodes = new_level

    return leaf_nodes[0]  # Return the root of the Merkle Tree


def load_merkle_tree(load_path):
    with open(load_path, 'rb') as f:
        return pickle.load(f)


def verify_file_integrity(file_path, merkle_tree_root):
    current_hash = build_merkle_tree(file_path)
    result1=verify_merkle_tree(merkle_tree_root, current_hash)
    result2=verify_file(merkle_tree_root,current_hash)
    return result1,result2


def verify_file(node, re_node):
    if node.left == None:

        return node.raw_files
    a=None
    b=None
    if node.left.hash_value != re_node.left.hash_value:
        a = verify_file(node.left, re_node.left)
    if node.right.hash_value != re_node.right.hash_value:
        b = verify_file(node.right, re_node.right)
    return (a if a else [])+(b if b else [])

def verify_merkle_tree(node, re_node):
    if node is None:
        return True
    try:
        # combined_hash = hashlib.sha512(
        #     (node.left.hash_value + (node.right.hash_value if node.right else '')).encode()).hexdigest()
        # print(f"combined_hash={combined_hash}")
        # re_combined_hash = hashlib.sha512(
        #     (re_node.left.hash_value + (re_node.right.hash_value if re_node.right else '')).encode()).hexdigest()
        # print(f"re_combined_hash={re_combined_hash}")

        if node.hash_value != re_node.hash_value:
            return False
    except:
        pass
    return verify_merkle_tree(node.left, re_node.left) and verify_merkle_tree(node.right, re_node.right)


def main():
    # Step 2: Verify file integrity
    file_path = ["111.txt", "222.txt", "新建文本文档.txt", "example.txt"]
    loaded_merkle_tree = load_merkle_tree('merkle_tree.pkl')

    result1,result2 = verify_file_integrity(file_path, loaded_merkle_tree)

    if result1:
        print("File integrity verified successfully.")
    else:
        print("File integrity verification failed.")
        for file in result2:
            print(f"{file} is erro")


if __name__ == "__main__":
    main()
