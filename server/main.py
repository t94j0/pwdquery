import psycopg2

# DB: passwords:abc123!!!@127.0.0.1/passwords


def create_db():
    conn = psycopg2.connect(
        host='127.0.0.1',
        user='passwords',
        password='abc123!!!',
        dbname='passwords')

    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS dump (
        id INT GENERATED ALWAYS AS IDENTITY,
        identifier TEXT,
        email TEXT,
        hash TEXT,
        password TEXT
        )''')
    cur.close()
    conn.commit()
    conn.close()


create_db()
print('Created database')
