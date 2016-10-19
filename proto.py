import struct

import asyncio
import socket

from messages_pb2 import *

_id_by_class = {
    InitMessage: 0,
    InitResultMessage: 1
}


def id_by_class(message_class):
    return _id_by_class[message_class]

_class_by_id = {}
for k, v in _id_by_class.items():
    _class_by_id[v] = k


def class_by_id(message_id):
    return _class_by_id[message_id]


def parse_header(bytes):
    size, type = struct.unpack('!2i', bytes)
    return size, class_by_id(type)


def serialize(object):
    serialized = object.SerializeToString()
    header = struct.pack('!2i', len(serialized), id_by_class(object.__class__))
    return header + serialized


async def read_message_async(reader: asyncio.streams.StreamReader):
    size, message_type = parse_header(await reader.read(8))
    a = message_type()
    a.ParseFromString(await reader.read(size))
    return a


def read_message_socket(reader: socket.socket):
    size, message_type = parse_header(reader.recv(8))
    a = message_type()
    a.ParseFromString(reader.recv(size))
    return a

