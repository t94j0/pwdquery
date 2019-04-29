import struct

from .socket import Socket


class PasswordClient:
    def __init__(self, host='localhost', port=1234):
        self.socket = Socket(host, port)

    def get_hashes(self, identifier: str):
        return self.socket.command(0, identifier)

    def get_passwords(self, identifier: str):
        return self.socket.command(1, identifier)

    def get_identifier(self, password: str):
        self.socket.send(3, identifier)

    def dump(self, name: str, delimiter: str, skip_first: bool, columns,
             filename: str):
        self.socket.send_keep_going()
        self.socket.send_int(2)
        data = struct.pack('>50sc?', name.encode('utf-8'), delimiter,
                           skip_first)
        self.socket.unsafe_send(data)
        cols = '\n'.join([f'{k}={v}' for k, v in columns.items()])
        self.socket.send(cols)
        for line in open(filename):
            print(line)
            self.socket.send_hex(line)
        self.socket.send_keep_going(False)

    def close(self):
        self.socket.close()

    def __exit__(self):
        self.close()
