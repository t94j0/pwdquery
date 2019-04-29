import socket
import struct
import binascii


class Socket:
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    def send_keep_going(self, keep_going=True):
        header = struct.pack('>?', keep_going)
        self.s.sendall(header)

    def send_int(self, tid: int):
        header = struct.pack('>I', tid)
        self.s.sendall(header)

    def command(self, tid, data):
        self.send_keep_going()
        self.send_int(tid)
        self.send_int(len(data))
        self.s.sendall(data.encode('utf-8'))
        return self.recv()

    def send(self, data):
        len_s = struct.pack('>I', len(data))
        self.s.sendall(len_s)
        self.s.sendall(data.encode('utf-8'))

    def send_hex(self, data):
        data = binascii.hexlify(data.encode('utf-8'))
        len_s = struct.pack('>I', len(data))
        self.s.sendall(len_s)
        self.s.sendall(data)

    def unsafe_send(self, data):
        self.s.sendall(data)

    def recv(self):
        len_s = struct.unpack('>I', self.s.recv(4))[0]
        msg = self.s.recv(len_s).decode('utf-8')
        return msg

    def close(self):
        self.send_keep_going(False)
        self.s.close()

    def __exit__(self):
        self.close()
