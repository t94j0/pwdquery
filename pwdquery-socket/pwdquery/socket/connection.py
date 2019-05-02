import struct
import binascii
from typing import Tuple


class ConnectionError(Exception):
    pass


class Connection:
    def __init__(self, conn: 'socket.connection', address='0.0.0.0'):
        self._conn = conn
        self.address = address

    def read_int(self) -> int:
        return struct.unpack('>I', self._conn.recv(4))[0]

    def read_bool(self) -> bool:
        return struct.unpack('>?', self._conn.recv(1))[0]

    def read_string(self, decode_method: str = 'utf-8', size: int = 0) -> str:
        length = self.read_int() if size == 0 else size
        return self._conn.recv(length).decode(decode_method)

    def read_struct(self, pattern: str) -> Tuple:
        length = struct.calcsize(pattern)
        data = self._conn.recv(length)
        return struct.unpack(pattern, data)

    def send_bool(self, data: bool) -> None:
        header = struct.pack('>?', data)

    def send_int(self, data: int) -> None:
        header = struct.pack('>I', data)
        self.s.sendall(header)

    def send_string(self, data: str, encode_method: str = 'utf-8') -> None:
        len_s = struct.pack('>I', len(data))
        self._conn.sendall(len_s)
        self._conn.sendall(data.encode(encode_method))

    def send_struct(self, pattern: str, *args) -> None:
        for a in args:
            if type(a) == str:
                raise ConnectionError(
                    'Data passed to send_struct should be a byte object')
        data = struct.pack(pattern, data.encode(encode_method))
        self._conn.sendall(data)

    def send_hex(self, data: str, encode_method: str = 'utf-8') -> None:
        hexed_data = binascii.hexlify(data.encode(encode_method))
        self.send_int(len(hexed_data))
        self._conn.sendall(hexed_data)

    def close(self) -> None:
        self._conn.close()
