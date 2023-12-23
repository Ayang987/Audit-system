from MerkleTree import merkletree
import os
from Socket import Sock
import time


def open_file(file_path):
    files = os.listdir(file_path)
    files = [os.path.join(file_path, file) for file in files]
    files_list = []
    for file in files:
        if "pkl" in file:
            continue
        with open(file, 'r', encoding='utf-8') as f:
            files_list.append(f.read())
    return files_list


def chuli(dir, data_list):
    merkle_tree = merkletree(data_list)
    merkle_tree.build_tree()
    print(f"生成的merkle树：{merkle_tree.tree}")
    # 获取根哈希
    root_hash = merkle_tree.get_root()
    print("Root Hash:", root_hash)
    return merkle_tree, root_hash


def send_files(dir):
    """
    每次发送一个文件的相关信息，该信息包括：文件内容、该文件的审计路径、merkletree根节点
    :param file:
    :return:
    """
    data_list = open_file(dir)
    merkle_tree, root_hash = chuli(dir, data_list)

    # 获取文件名
    file_name = os.listdir("pack")

    # #发送根节点
    sed.send(root_hash)
    time.sleep(1)

    for index_to_audit in range(len(data_list)):
        # 发送文件名
        sed.send(file_name[index_to_audit])
        time.sleep(1)

        # #发送数据
        sed.send(data_list[index_to_audit])
        time.sleep(1)

        # # 发送审计证明
        audit_proof = merkle_tree.audit_proof(index_to_audit)
        sed.send(str(audit_proof))
        time.sleep(1)

    sed.send('ok')
    print(f"文件 {file_name} 已发送到 {host}:{port}")


if __name__ == "__main__":
    # 目标主机
    host = '192.168.45.62'
    # 连接的端口
    port = 9995
    # 建立连接
    sed = Sock(host, port)
    send_files('pack')
