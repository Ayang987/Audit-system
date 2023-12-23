from MerkleTree import merkletree
import os
import pickle
def open_file(file_path):
    files = os.listdir(file_path)
    files = [os.path.join(file_path, file) for file in files]
    files_list = []
    for file in files:
        if 'pkl' in file:
            continue
        with open(file, 'r', encoding='utf-8') as f:
            files_list.append(f.read())
    return files_list

def save_merkle_tree(save_path,root_node):
    with open(f"./{save_path}/merkle_tree.pkl", 'wb') as f:
        pickle.dump(root_node, f)

def save_root(dir,root_hash):
    with open('./dir/root_hash','w')as f:
        f.write(root_hash)


def generate_root(dir):
    data_list=open_file(dir)
    merkle_tree = merkletree(data_list)
    merkle_tree.build_tree()
    root_hash=merkle_tree.get_root()
    save_merkle_tree(dir,root_hash)

if __name__=="__main__":
    dir = 'pack'
    generate_root(dir)

    with open('pack/merkle_tree.pkl','rb')as f:
        print(pickle.load(f))
