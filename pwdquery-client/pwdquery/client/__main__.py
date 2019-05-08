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
        help='Only display hash')
    parser.add_argument(
        '-p',
        '--password',
        dest='password',
        action='store_true',
        default=False,
        help='Search based on password')
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
        client = PasswordClient(host)
    except config.NoConfigurationError:
        print('Error: Unable to find configuration')
        sys.exit(1)
    except ConnectionRefusedError:
        print('Error: Failed to connect to server')
        sys.exit(1)
    except KeyError as e:
        print('Error: Key {e.args[0]} cannot be found')
        sys.exit(1)

    if not args.identifier:
        parser.print_usage()
        sys.exit(1)

    if not args.password:
        passwords = '\n'.join(client.get_passwords(args.identifier))
        if not args.quiet and not args.hash:
            print(f'Cracked passwords for {args.identifier}:')
        if not args.hash:
            print(passwords)

        hashes = '\n'.join(client.get_hashes(args.identifier))
        if not args.quiet:
            print(f'Uncracked hashes for {args.identifier}:')
        if not args.quiet or (args.quiet and args.hash):
            print(hashes)
    else:
        if not args.quiet:
            print(f'Identifiers related to password {args.identifier}:')
        identifers = '\n'.join(client.get_identifiers(args.identifier))
        print(identifers)


if __name__ == '__main__':
    main()
