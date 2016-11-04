import asyncio.queues
import unittest.mock


# TODO: figure out how to make nice docs and describe why it implements only these two functions
class MockStream:
    class EndOfStream:
        pass

    def __init__(self):
        self.queue = asyncio.queues.Queue()

    def close(self):
        eos = self.EndOfStream()
        self.queue.put_nowait(eos)

    def write(self, data: bytes):
        for byte in data:
            self.queue.put_nowait(byte)

    async def readexactly(self, n=-1):
        ret = b''
        if n == 0:
            return ret

        while len(ret) < n:
            data = await self.queue.get()
            if isinstance(data, self.EndOfStream):
                break  # the mocked socket was closed
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

    mock = unittest.mock.MagicMock()
    mock.__setitem__.side_effect = setitem
    mock.append.side_effect = append
    mock.__getitem__.side_effect = getitem
    mock.remove.sideeffect = remove

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
