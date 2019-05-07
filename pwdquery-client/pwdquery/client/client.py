import struct

from .create_connection import create_connection


class PasswordClient:
    def __init__(self, host='localhost', port=1234):
        self._conn = create_connection(host, port)

    def _command(self, tid: int, data: str) -> None:
        self._conn.send_bool(True)
        self._conn.send_int(tid)
        self._conn.send_string(data)
        return self._conn.read_string()

    def get_hashes(self, identifier: str):
        return self._command(0, identifier)

    def get_passwords(self, identifier: str):
        return self._command(1, identifier)

    def get_identifier(self, password: str):
        self._command(3, password)

    def dump(self, name: str, delimiter: str, skip_first: bool, columns,
             filename: str):
        self._conn.send_bool(True)
        self._conn.send_int(2)
        self._conn.send_struct('>50sc?', name.encode('utf-8'), delimiter,
                               skip_first)
        cols = '\n'.join([f'{k}={v}' for k, v in columns.items()])
        self._conn.send_string(cols)
        for line in open(filename):
            self._conn.send_hex(line)
        self._conn.send_bool(False)

    def close(self):
        self._conn.close()

    def __exit__(self):
        self.close()
