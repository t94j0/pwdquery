import socket
import struct
import binascii

from pwdquery.socket import Connection


def create_connection(host, port) -> Connection:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s
