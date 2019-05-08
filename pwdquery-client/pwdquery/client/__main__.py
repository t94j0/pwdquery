import sys
import argparse

from .client import PasswordClient
from . import config


def create_parser():
    parser = argparse.ArgumentParser(
        description='Get passwords and hashes from store')
    parser.add_argument(
        'identifier',
        nargs='?',
        type=str,
        help='Identifier to get passwords from')
    parser.add_argument(
        '--csv-dump',
        dest='csvdump',
        action='store_true',
        help='Identifier to get passwords from')
    parser.add_argument(
        '-q',
        '--quiet',
        dest='quiet',
        action='store_true',
        default=False,
        help='Output quietly')
    parser.add_argument(
        '--hash',
        dest='hash',
        action='store_true',
        default=False,
        help='Get hash')
    parser.add_argument(
        '-c', '--config', default='', help='Location for configuration')
    return parser


def dir_input(title: str) -> str:
    import readline, glob

    def complete(text, state):
        return (glob.glob(text + '*') + [None])[state]

    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    return input(title)


def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        cfg = config.get(args.config)
        host = cfg['host']
        port = cfg['port']
        client = PasswordClient(host, port)
    except config.NoConfigurationError:
        print('Error: Unable to find configuration')
        sys.exit(1)
    except ConnectionRefusedError:
        print('Error: Failed to connect to server')
        sys.exit(1)
    except KeyError as e:
        print('Error: Key {e.args[0]} cannot be found')
        sys.exit(1)

    if args.csvdump:
        location = dir_input('CSV Dump: ')
        name = input('Site name [kebab-case]: ')
        year = input('Leak Year: ')
        decimal_delimit = bytes(
            [int(input('Delimiter [decimal] (,): ') or '44')])
        skip_first = input('Skip first entry? (y/N)') in ['Y', 'y']
        print(
            '\nColumn selection\nFormat: \'column_name index\'. Double enter when complete'
        )
        indicies = {}
        while True:
            inp = input()
            if inp == '':
                break
            column_name, index = inp.split(' ')
            indicies[column_name] = int(index)
        name = f'{name}.{year}'

        print('Starting transfer')
        client.dump(name, decimal_delimit, skip_first, indicies, location)
        client.close()

        sys.exit(0)

    if not args.identifier:
        parser.print_usage()
        sys.exit(1)

    passwords = client.get_passwords(args.identifier)
    if not args.quiet:
        print(f'Cracked passwords for {args.identifier}:')
    if not args.hash:
        print(passwords)

    hashes = client.get_hashes(args.identifier)
    if not args.quiet:
        print(f'Uncracked hashes for {args.identifier}:')
    if not args.quiet or (args.quiet and args.hash):
        print(hashes)
    client.close()


if __name__ == '__main__':
    main()
