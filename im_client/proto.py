import json

import asyncio


def write_message(writer: asyncio.streams.StreamWriter, message):
    data = json.dumps(message)
    writer.write(netstring_encode(data))


async def read_message(reader: asyncio.streams.StreamReader):
    data = (await netstring_decode(reader))
    a = json.loads(data)
    return a


event_required_fields = {
    "MESSAGE": ["from", "to", "text"]
}


def validate_event(event):
    """
    Validates event's data.
    Returns True if the event's correct, false if it isn't.
    """
    if "name" not in event:
        return False
    for event_name in event_required_fields:
        if event_name == event['name']:
            for field in event_required_fields[event_name]:
                if field not in event:
                    return False
            return True
    return True


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
