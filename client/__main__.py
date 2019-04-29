import argparse

from .client import PasswordClient

parser = argparse.ArgumentParser(
    description='Get passwords and hashes from store')
parser.add_argument(
    'identifier', type=str, help='Identifier to get passwords from')
parser.add_argument(
    '-q',
    '--quiet',
    dest='quiet',
    action='store_true',
    default=False,
    help='Output quietly')
args = parser.parse_args()

client = PasswordClient()
passwords = client.get_passwords(args.identifier)

if not args.quiet:
    print(f'Cracked passwords for {args.identifier}:')
print(f'{passwords}')

if not args.quiet:
    hashes = client.get_hashes(args.identifier)
    print(f'Uncracked hashes for {args.identifier}:')
    print(f'{hashes}')
client.close()
