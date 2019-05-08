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
        passwords = [l for l in self._command(1, identifier).split('\n')]
        passwords = [l for l in passwords if l != '']
        return '\n'.join(passwords)

    def get_identifiers(self, password: str):
        return self._command(2, password)

    def close(self):
        self._conn.close()

    def __exit__(self):
        self.close()
