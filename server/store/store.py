import psycopg2
from psycopg2.extras import execute_values
from .password import Password


class PasswordStore:
    def __init__(self, buf=10000):
        self.conn = psycopg2.connect(
            host='127.0.0.1',
            user='passwords',
            password='abc123!!!',
            dbname='passwords')
        self._create_db()
        self.buffer = buf
        self.insert_store = []

    def _create_db(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS dump (
            id         INT GENERATED ALWAYS AS IDENTITY,
            identifier TEXT,
            email      TEXT,
            hash       TEXT,
            password   TEXT,
            dump       TEXT,

            UNIQUE (identifier, hash, password)
            )''')
        cur.close()
        self.conn.commit()

    def get_passwords(self, identifier: str):
        cur = self.conn.cursor()
        cur.execute('SELECT password FROM dump WHERE identifier = %s',
                    (identifier, ))
        passwords = [i[0] for i in cur.fetchall() if i[0] != '']

        cur.close()
        self.conn.commit()
        return passwords

    def get_hashes(self, identifier: str):
        cur = self.conn.cursor()
        cur.execute('SELECT hash FROM dump WHERE identifier = %s',
                    (identifier, ))
        hashes = [i[0] for i in cur.fetchall() if i[0] != '']
        cur.close()
        self.conn.commit()
        return hashes

    def get_identifiers(self, password: str):
        cur = self.conn.cursor()
        cur.execute('SELECT identifier FROM dump WHERE password = %s',
                    (password, ))
        identifiers = [i[0] for i in cur.fetchall() if i[0] != '']
        cur.close()
        self.conn.commit()
        return identifiers

    def insert(self, password: 'Password'):
        self.insert_store.append(password.tuple())
        if len(self.insert_store) >= self.buffer:
            self.flush()

    def flush(self):
        cur = self.conn.cursor()
        execute_values(
            cur,
            'INSERT INTO dump(identifier, email, hash, password, dump) VALUES %s ON CONFLICT DO NOTHING',
            self.insert_store)
        self.insert_store = []
        cur.close()
        self.conn.commit()
