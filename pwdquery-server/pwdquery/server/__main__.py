import signal
import sys
import psycopg2
import argparse
import logging

from .passwordserver import Server
from . import config


def create_logger(path: str) -> None:
    logging.basicConfig(filename=path, level=logging.INFO)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Start pwdquery server')
    parser.add_argument(
        '--log-path',
        dest='log_path',
        type=str,
        default='',
        help='Path to write logs')
    parser.add_argument(
        '-c', '--config', type=str, default='', help='Configuration path')
    return parser


def create_server(configpath: str) -> Server:
    try:
        cfg = config.get(configpath)
    except config.NoConfigurationError:
        logging.critical('No configuration file found')
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
        logging.critical(f'Configuration value {invalid} is nonexistant')

    return Server(lhost, lport, dbhost, dbport, dbname, dbuser, dbpassword)


def main():
    args = create_parser().parse_args()
    try:
        create_logger(args.log_path)
        p = create_server(args.config)
    except psycopg2.OperationalError as e:
        logging.critical('Cannot connect to DB')
        sys.exit(1)

    logging.info('Starting server')

    def sigint_handler(sig, frame):
        logging.info('Stopping server')
        p.close()
        sys.exit()

    signal.signal(signal.SIGINT, sigint_handler)

    p.start()


if __name__ == '__main__':
    main()
