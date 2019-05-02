import sys
import argparse

from .client import PasswordClient


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
    return parser.parse_args()


def dir_input(title: str) -> str:
    import readline, glob

    def complete(text, state):
        return (glob.glob(text + '*') + [None])[state]

    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    return input(title)


def main():
    args = create_parser()
    client = PasswordClient()

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

    passwords = client.get_passwords(args.identifier)
    if not args.quiet:
        print(f'Cracked passwords for {args.identifier}:')
    print(f'{passwords}')

    if not args.quiet:
        hashes = client.get_hashes(args.identifier)
        print(f'Uncracked hashes for {args.identifier}:')
        print(f'{hashes}')
    client.close()


if __name__ == '__main__':
    main()