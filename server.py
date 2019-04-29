import socket
import struct

from passwords import PasswordStore

store = PasswordStore()

s = socket.socket()
s.bind(('localhost', 1234))
s.listen(10)

while True:
    sc, address = s.accept()
    print(f'Connection from: {address[0]}')
    while True:
        len_s = struct.unpack('>I', sc.recv(4))[0]
        if len_s == 0:
            break

        client_message = sc.recv(len_s).decode('utf-8')

        if client_message.startswith('get_hashes'):
            identifier = client_message.split()[1]
            data = ''.join(store.get_hashes(identifier))
            len_s = struct.pack('>I', len(data))
            sc.sendall(len_s)
            sc.sendall(data.encode('utf-8'))

        elif client_message.startswith('get_password'):
            identifier = client_message.split()[1]
            data = ''.join(store.get_passwords(identifier))
            len_s = struct.pack('>I', len(data))
            sc.sendall(len_s)
            sc.sendall(data.encode('utf-8'))

    sc.close()

s.close()
