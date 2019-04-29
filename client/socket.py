import socket
import struct


class Socket:
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    def command(self, cmd: str) -> str:
        self.send(cmd)
        return self.recv()

    def send(self, data):
        len_s = struct.pack('>I', len(data))
        self.s.sendall(len_s)
        self.s.sendall(data.encode('utf-8'))

    def recv(self):
        len_s = struct.unpack('>I', self.s.recv(4))[0]
        msg = self.s.recv(len_s).decode('utf-8')
        return msg

    def close(self):
        len_s = struct.pack('>I', 0)
        self.s.sendall(len_s)
        self.s.close()

    def __exit__(self):
        self.close()
