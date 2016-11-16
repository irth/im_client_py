import asyncio.queues
import unittest.mock

from im_client import proto, IMClient


# TODO: figure out how to make nice docs and describe why it implements only these two functions
class MockStream:
    class EndOfStream:
        pass

    def __init__(self):
        self._queue = asyncio.queues.Queue()
        self._data = b''

    def close(self):
        eos = self.EndOfStream()
        self._queue.put_nowait(eos)

    def write(self, data: bytes):
        for byte in data:
            self._queue.put_nowait(byte)
        self._data += data

    def get_bytes(self):
        return self._data

    async def readexactly(self, n=-1):
        ret = b''
        if n == 0:
            return ret

        while len(ret) < n:
            data = await self._queue.get()
            if isinstance(data, self.EndOfStream):
                break  # the mocked socket was closed
            b = list(self._data)
            b.pop()
            self._data = bytes(b)
            ret += bytes([data])

        if len(ret) < n != -1:
            raise asyncio.streams.IncompleteReadError(ret, n)
        return ret


def MockList(base=None):
    base_list = [] if base is None else base

    def setitem(key, value):
        base_list[key] = value

    def append(value):
        base_list.append(value)

    def getitem(key):
        return base_list[key]

    def remove(key):
        base_list.remove(key)

    def get_all():
        return base_list

    mock = unittest.mock.MagicMock()
    mock.__setitem__.side_effect = setitem
    mock.append.side_effect = append
    mock.__getitem__.side_effect = getitem
    mock.remove.side_effect = remove
    mock.get_all.side_effect = get_all

    return mock


def MockDict(base=None):
    base_dict = {} if base is None else base

    def setitem(key, value):
        base_dict[key] = value

    def getitem(key):
        return base_dict[key]

    def pop(key, default=None):
        return base_dict.pop(key, default)

    mock = unittest.mock.MagicMock()
    mock.__setitem__.side_effect = setitem
    mock.__getitem__.side_effect = getitem
    mock.pop.sideeffect = pop

    return mock


async def create_server(event_loop, messages=None, setup=None, check=None):
    r = MockStream()
    w = MockStream()
    if messages is not None:
        if isinstance(messages, dict):
            messages = [messages]
        if isinstance(messages, list):
            for message in messages:
                proto.write_message(r, message)

    server = IMClient(event_loop)
    if setup is not None:
        await setup(server, r, w)

    if check is not None:
        try:
            await asyncio.gather(
                check(server, r, w),
                server.accept(r, w)
            )
        except asyncio.streams.IncompleteReadError:
            pass  # the connection's closed

    return server, r, w

