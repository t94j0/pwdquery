import socket

from passwords import PasswordStore

store = PasswordStore()

s = socket.socket()
s.bind(('localhost', 1234))
s.listen(10)

while True:
    sc, address = s.accept()
    print(f'Connection from: {address[0]}')
    client_message = sc.recv(1024).decode('utf-8')

    if client_message.startswith('get_hashes'):
        identifier = client_message.split()[1]
        data = ''.join(store.get_hashes(identifier))
        sc.send(data.encode('utf-8'))
    elif client_message.startswith('get_password'):
        identifier = client_message.split()[1]
        data = ''.join(store.get_passwords(identifier))
        sc.send(data.encode('utf-8'))

    sc.close()

s.close()
