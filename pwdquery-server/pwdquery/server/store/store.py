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
            priority   INT DEFAULT 0,

            UNIQUE (identifier, hash, password)
            )''')
        cur.close()
        self.conn.commit()

    def _increase_priority(self, ids):
        cur = self.conn.cursor()
        execute_values(
            cur,
            'UPDATE dump SET priority = priority + 1 WHERE id = %s AND priority > 0',
            ids)
        cur.close()
        self.conn.commit()

    def top_priority(self, limit=1):
        cur = self.conn.cursor()
        cur.execute(
            'SELECT id,hash FROM dump WHERE identifier = %s ORDER BY priority DESC LIMIT %s',
            (identifier, limit))
        data = cur.fetchall()
        cur.close()
        return data

    def add_password(self, _id, password):
        cur = self.conn.cursor()
        cur.execute(
            'UPDATE dump SET priority = -1, password = %s WHERE id = %s',
            password, _id)
        cur.close()
        self.conn.commit()

    def get_passwords(self, identifier: str):
        cur = self.conn.cursor()
        cur.execute('SELECT id,password FROM dump WHERE identifier = %s',
                    (identifier, ))
        data = cur.fetchall()
        ids = [str(i[0]) for i in data]
        passwords = [i[1] for i in data if i[1] != '']
        self._increase_priority(ids)

        cur.close()
        return passwords

    def get_hashes(self, identifier: str):
        cur = self.conn.cursor()
        cur.execute('SELECT id,hash FROM dump WHERE identifier = %s',
                    (identifier, ))

        data = cur.fetchall()
        ids = [str(i[0]) for i in data]
        hashes = [i[1] for i in data if i[1] != '']
        self._increase_priority(ids)

        cur.close()
        return hashes

    def get_identifiers(self, password: str):
        cur = self.conn.cursor()
        cur.execute('SELECT identifier FROM dump WHERE password = %s',
                    (password, ))
        identifiers = [i[0] for i in cur.fetchall() if i[0] != '']
        cur.close()
        return identifiers

    def insert(self, password: 'Password'):
        self.insert_store.append(password.tuple())
        if len(self.insert_store) >= self.buffer:
            self.flush()

    def flush(self):
        cur = self.conn.cursor()
        execute_values(
            cur,
            'INSERT INTO dump(identifier, email, hash, password, dump, priority) VALUES %s ON CONFLICT DO NOTHING',
            self.insert_store)
        self.insert_store = []
        cur.close()
        self.conn.commit()
