import signal
import sys
import psycopg2
import argparse

from .passwordserver import Server
from . import config


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Start pwdquery server')
    parser.add_argument(
        '-c', '--config', type=str, default='', help='Configuration path')
    return parser


def create_server(configpath: str) -> Server:
    try:
        cfg = config.get(configpath)
    except config.NoConfigurationError:
        print('Error: No configuration file found')
        sys.exit(1)

    try:
        lhost = cfg['host']
        lport = cfg['port']
        dbhost = cfg['db']['host']
        dbport = cfg['db']['port']
        dbname = cfg['db']['name']
        dbuser = cfg['db']['user']
        dbpassword = cfg['db']['password']
    except KeyError as e:
        invalid = e.args[0]
        print(f'Configuration value {invalid} is nonexistant')

    return Server(lhost, lport, dbhost, dbport, dbname, dbuser, dbpassword)


def sigint_handler(sig, frame):
    print('Stopping server')
    p.close()
    sys.exit()


def main():
    signal.signal(signal.SIGINT, sigint_handler)

    args = create_parser().parse_args()
    try:
        p = create_server(args.config)
    except psycopg2.OperationalError as e:
        print('Error: Cannot connect to DB')
        sys.exit(1)

    print('Starting server')
    p.start()


if __name__ == '__main__':
    main()
