import psycopg2

# DB: passwords:abc123!!!@127.0.0.1/passwords

class Passwords:
    def __init__(self):
        self.conn = psycopg2.connect(
            host='192.168.99.100',
            user='passwords',
            password='abc123!!!',
            dbname='passwords')

    def close(self):
        self.conn.close()
        
    def create_db(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS dump (
            id INT GENERATED ALWAYS AS IDENTITY,
            identifier TEXT,
            email TEXT,
            hash TEXT,
            password TEXT
            )''')
        cur.close()
        self.conn.commit()

    def from_identifier(self,identifier: str):
        cur = self.conn.cursor()
        cur.execute('SELECT password,hash FROM dump WHERE identifier = %s', (identifier,))
        items = cur.fetchall()
        passwords = [i[0] for i in items]
        hashes = [i[1] for i in items]

        cur.close()
        self.conn.commit()
        return passwords, hashes

if __name__ == '__main__':
    store = Passwords()
    store.create_db()
    print(store.from_identifier('maxh'))
    store.close()
