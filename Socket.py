import socket


class Sock():
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, value):

        # 创建一个套接字对象
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # s.settimeout(1)
            # 连接到接收方的主机和端口
            s.connect((self.host, self.port))

            # 发送数据
            s.sendall(value.encode('utf-8'))
            print(f'{value} is send succfully!')

    def reciver(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 监听来自发送方的连接
            s.bind((self.host, self.port))
            s.listen()

            conn, addr = s.accept()

            with conn:
                value = ''
                while True:
                    temp = conn.recv(2048).decode('utf-8')
                    if temp != '':
                        value += temp
                    else:
                        break
                print(f"收到了{value}")

            return value
