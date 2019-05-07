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
    def dump(self, conn):
        # Get parameters
        dump_name, delimiter, skip_first = conn.read_struct('>50sc?')
        dump_name = dump_name.decode('utf-8').replace('\0', '')
        delimiter = delimiter.decode('utf-8')

        # Get columns
        col_desc = conn.read_string().split('\n')
        columns = {c.split('=')[0]: int(c.split('=')[1]) for c in col_desc}

        csvfile = (x.replace('\0', '') for x in self.getcsv(conn))
        reader = csv.reader(csvfile, delimiter=delimiter)
        if skip_first:
            next(reader)
        for row in reader:
            pwd_args = {k: row[v] for k, v in columns.items() if v < len(row)}
            p = Password(dump=dump_name, **pwd_args)
            self.store.insert(p)
        self.store.flush()

    def getcsv(self, conn):
        while True:
            length = conn.read_int()
            if length == 0:
                break
            data = conn.read_string(size=length)
            yield binascii.unhexlify(data).decode('utf-8')
