from .router import Socket, Router, route
from .store import PasswordStore, Password


class Server(Socket):
    router = Router()

    def __init__(self, host='localhost', port=1234):
        super().__init__(host, port)
        self.store = PasswordStore()

    @route(router, 0)
    def get_hashes(self, conn):
        identifier = conn.read_string()
        data = '\n'.join(self.store.get_hashes(identifier))
        conn.send_string(data)

    @route(router, 1)
    def get_passwords(self, conn):
        identifier = conn.read_string()
        data = '\n'.join(self.store.get_passwords(identifier))
        conn.send_string(data)

    @route(router, 3)
    def dump(self, conn):
        # Get parameters
        dump_name, delimiter, skip_first = conn.get_struct('>50sc?')
        dump_name = dump_name.decode('utf-8').replace('\0', '')
        delimiter = delimiter.decode('utf-8')

        # Get columns
        col_desc = conn.read_string().split('\n')
        columns = {c.split('=')[0]: int(c.split('=')[1]) for c in col_desc}

        csvfile = (x.replace('\0', '') for x in getcsv(sc))
        reader = csv.reader(csvfile, delimiter=delimiter)
        if skip_first:
            next(reader)
        for row in reader:
            pwd_args = {k: row[v] for k, v in columns.items() if v < len(row)}
            p = Password(dump=dump_name, **pwd_args)
            self.store.insert(p)
        self.store.flush()
