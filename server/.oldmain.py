import sys
import socket
import struct
import signal
import csv
import binascii

from .store import PasswordStore, Password

store = PasswordStore()

HOST = 'localhost'
PORT = 1234

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)
print(f'Server started. Listening on {PORT}')


def sigint_handler(sig, frame):
    print('Stopping server')
    s.close()
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)


def getcsv(conn):
    while True:
        line_len = struct.unpack('>I', conn.recv(4))[0]
        if line_len == 0:
            break
        line = conn.recv(line_len)
        yield binascii.unhexlify(line).decode('UTF-8')


def get_int(conn: 'socket.connection'):
    return struct.unpack('>I', sc.recv(4))[0]


def get_string(conn: 'socket.connection',
               length: int,
               decode_method: str = 'utf-8'):
    return conn.recv(length).decode(decode_method)


def send_string(conn: 'socket.connection',
                data: str,
                encode_method: str = 'utf-8'):
    len_s = struct.pack('>I', len(data))
    conn.sendall(len_s)
    conn.sendall(data.encode('utf-8'))


while True:
    sc, address = s.accept()
    print(f'Connection from: {address[0]}')
    while True:
        len_s = get_int(sc)
        if len_s == 0:
            break

        type_s = get_int(sc)

        # get_hashes - len_s = size of message
        if type_s == 0:
            identifier = get_string(sc, len_s)
            data = '\n'.join(store.get_hashes(identifier))
            send_string(conn, data)

        # get_passwords - len_s = size of message
        elif type_s == 1:
            identifier = get_string(sc, len_s)
            data = '\n'.join(store.get_passwords(identifier))
            send_string(sc, data)

        # dump - len_s = 1
        elif type_s == 2:
            # name, delimiter, skip_first
            FORMAT = '>50sc?'
            dump_name, delimiter, skip_first = struct.unpack(
                FORMAT, sc.recv(struct.calcsize(FORMAT)))
            dump_name = dump_name.decode('utf-8').replace('\0', '')
            delimiter = delimiter.decode('utf-8')
            # columns: identifier=0\nemail=1\nhash=2
            # length of column id
            len_s = struct.unpack('>I', sc.recv(4))[0]
            col_desc = sc.recv(len_s).decode('utf-8').split('\n')
            columns = {c.split('=')[0]: int(c.split('=')[1]) for c in col_desc}
            # Read CSV from wire
            csvfile = (x.replace('\0', '') for x in getcsv(sc))
            reader = csv.reader(csvfile, delimiter=delimiter)
            if skip_first:
                next(reader)
            for row in reader:
                pwd_args = {
                    k: row[v]
                    for k, v in columns.items() if v < len(row)
                }
                p = Password(dump=dump_name, **pwd_args)
                store.insert(p)
            store.flush()

    sc.close()

s.close()
