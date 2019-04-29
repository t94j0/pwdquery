from .socket import Socket


class PasswordClient:
    def __init__(self, host='localhost', port=1234):
        self.socket = Socket(host, port)

    def get_hashes(self, identifier: str):
        return self.socket.command(f'get_hashes {identifier}')

    def get_passwords(self, identifier: str):
        return self.socket.command(f'get_passwords {identifier}')

    def get_identifier(self, password: str):
        self.socket.send(f'get_identifier {password}')

    def close(self):
        self.socket.close()

    def __exit__(self):
        self.close()
