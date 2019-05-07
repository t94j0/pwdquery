import yaml
import pathlib
from os.path import expanduser
from typing import Optional

userpath = expanduser('~')
CHECKS = [f'{userpath}/.config/pwdquery.yml', f'{userpath}/pwdquery.yml']


class NoConfigurationError(Exception):
    pass


def get_valid_config_path(p: str = '') -> Optional[str]:
    for path in [p] + CHECKS:
        config = pathlib.Path(path)
        if config.is_file():
            return path
    return None


def get(path: str):
    config_path = get_valid_config_path(path)
    if config_path == None:
        raise NoConfigurationError
    with open(config_path, 'r') as config_file:
        return yaml.load(config_file, Loader=yaml.CLoader)
