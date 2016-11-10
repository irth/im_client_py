import json
import struct

import asyncio
import socket

from .messages_pb2 import *

_id_by_class = {
    InitMessage: 0,
    InitResultMessage: 1,
    SubscribeMessage: 2
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


def write_message(writer: asyncio.streams.StreamWriter, message):
    data = json.dumps(message)
    writer.write(netstring_encode(data))


async def read_message(reader: asyncio.streams.StreamReader):
    data = (await netstring_decode(reader))
    a = json.loads(data)
    return a


def netstring_encode(string):
    enc = string.encode('utf-8')
    return str(len(enc)).encode('utf-8') + ":".encode('utf-8') + enc


async def netstring_decode(reader: asyncio.streams.StreamReader):
    len = b''
    while True:
        char = await reader.readexactly(1)  # read one byte
        if char == ':'.encode('utf-8'):
            break
        else:
            len += char
    len = int(len)
    return (await reader.readexactly(len)).decode('utf-8')
