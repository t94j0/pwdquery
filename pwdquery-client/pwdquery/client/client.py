import requests
from typing import List


class PasswordClient:
    def __init__(self, host: str = 'http://localhost:1234'):
        self.host = host

    def get_hashes(self, identifier: str) -> List[str]:
        return requests.get(f'{self.host}/hashes/{identifier}').json()

    def get_passwords(self, identifier: str):
        return requests.get(f'{self.host}/passwords/{identifier}').json()

    def get_identifiers(self, password: str):
        return requests.get(f'{self.host}/identifiers/{password}').json()
