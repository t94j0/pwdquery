import struct
import socket
from functools import wraps


def route(router: 'Router', index: int):
    def decorator(func):
        router.add(index, func)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)

        return wrapper

    return decorator


class Socket:
    def __init__(self, host, port):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(10)

    def start(self):
        while True:
            conn = Connection(self.socket.accept())
            self._connection(conn)

    def _connection(self, conn):
        while True:
            keep_going = conn.read_bool()
            if not keep_going:
                break

            req_type = conn.read_int()
            self.router(self, req_type, conn)
        conn.close()

    def close(self):
        self.socket.close()

    def __exit__(self):
        self.close()


class Router:
    commands = {}

    def add(self, index, func):
        self.commands[index] = func

    def __call__(self, _self, index, conn):
        func = self.commands[index]
        func(_self, conn)


class Connection:
    def __init__(self, accept):
        self.conn = accept[0]
        self.address = accept[1]
        self.length = 0

    def read_int(self):
        return struct.unpack('>I', self.conn.recv(4))[0]

    def read_string(self, decode_method='utf-8'):
        length = self.read_int()
        return self.conn.recv(length).decode(decode_method)

    def send_string(self, data, encode_method='utf-8'):
        len_s = struct.pack('>I', len(data))
        self.conn.sendall(len_s)
        self.conn.sendall(data.encode(encode_method))

    def read_bool(self) -> bool:
        return struct.unpack('>?', self.conn.recv(1))[0]

    def close(self):
        self.conn.close()
