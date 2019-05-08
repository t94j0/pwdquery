import csv
import binascii

from .socketserver import SocketServer
from .router import Router, route
from .store import PasswordStore, Password


class Server(SocketServer):
    router = Router()

    def __init__(self, lhost: str, lport: int, dbhost: str, dbport: int,
                 dbname: str, dbuser: str, dbpassword: str):
        super().__init__(lhost, lport)
        self.store = PasswordStore(dbhost, dbport, dbname, dbuser, dbpassword)

    @route(router, 0)
    def get_hashes(self, conn):
        identifier = conn.read_string()
        hashes = self.store.get_hashes(identifier)
        data = '\n'.join(hashes)
        conn.send_string(data)

    @route(router, 1)
    def get_passwords(self, conn):
        identifier = conn.read_string()
        passwords = self.store.get_passwords(identifier)
        data = '\n'.join(passwords)
        conn.send_string(data)

    @route(router, 2)
    def get_identifers(self, conn):
        password = conn.read_string()
        identifers = self.store.get_identifiers(password)
        data = '\n'.join(identifers)
        conn.send_string(data)

    def getcsv(self, conn):
        while True:
            length = conn.read_int()
            if length == 0:
                break
            print(f'len: {length}')
            yield conn.read_hex(size=length)
