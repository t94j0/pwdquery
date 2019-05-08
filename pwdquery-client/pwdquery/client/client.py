import json
import requests
from typing import List, Dict


class PasswordClient:
    def __init__(self, host: str = 'http://localhost:1234'):
        self.host = host

    def get_hashes(self, identifier: str) -> List[str]:
        return requests.get(f'{self.host}/hashes/{identifier}').json()

    def get_passwords(self, identifier: str):
        return requests.get(f'{self.host}/passwords/{identifier}').json()

    def get_identifiers(self, password: str):
        return requests.get(f'{self.host}/identifiers/{password}').json()

    def dump(self, path: str, name: str, delim: int, skip: bool,
             indicies: Dict[str, int]):
        files = {'file': open(path, 'rb')}
        values = {
            'name': name,
            'delimiter': delim,
            'skip': 'true' if skip else 'false',
            'indicies': json.dumps(indicies)
        }
        return requests.post(
            f'{self.host}/upload-csv', files=files, data=values)
