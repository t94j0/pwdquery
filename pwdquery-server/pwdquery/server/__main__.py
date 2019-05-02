import signal
import sys

print('Here!')

from .passwordserver import Server

print('There!')

p = Server('localhost', 1234)


def sigint_handler(sig, frame):
    print('Stopping server')
    p.close()
    sys.exit()


def main():
    signal.signal(signal.SIGINT, sigint_handler)

    print('Starting server')
    p.start()


if __name__ == '__main__':
    main()