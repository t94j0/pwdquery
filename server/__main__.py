import signal
import sys

from .server import Server

p = Server('localhost', 1234)


def sigint_handler(sig, frame):
    print('Stopping server')
    p.close()
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)

print('Starting server')
p.start()
