import socket
from pwdquery.socket import Connection, ConnectionError


class SocketServer:
    def __init__(self, host, port):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(10)

    def start(self):
        while True:
            conn = Connection(*self.socket.accept())
            address = conn.format_address()
            print(f'Client {address} connected')
            try:
                self._connection(conn)
                print('Client {address} closed session')
                conn.close()
            except ConnectionError:
                print(f'Client {address} force closed the connection')

    def _connection(self, conn):
        while True:
            keep_going = conn.read_bool()
            if not keep_going:
                break

            req_type = conn.read_int()
            self.router(self, req_type, conn)

    def close(self):
        self.socket.close()

    def __exit__(self):
        self.close()
