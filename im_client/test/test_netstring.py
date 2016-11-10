import json

import pytest

from im_client import proto
import utils


def test_netstring_encode():
    enc = proto.netstring_encode('a string')
    assert enc == b'8:a string'

    pl_str = 'a string with półiśh ćhąrąćtęrś'
    enc = proto.netstring_encode(pl_str)
    assert enc == b'40:' + pl_str.encode('utf-8')


@pytest.mark.asyncio
async def test_netstring_decode():
    s = utils.MockStream()
    s.write(b'8:a string')

    assert (await proto.netstring_decode(s)) == 'a string'


@pytest.mark.asyncio
async def test_write_message():
    s = utils.MockStream()
    obj = {
        "a": 1,
        "b": 2
    }
    proto.write_message(s, obj)
    assert s.get_bytes() == proto.netstring_encode(json.dumps(obj))


@pytest.mark.asyncio
async def test_read_message():
    s = utils.MockStream()
    obj = {
        "a": 1,
        "b": 2
    }
    message = json.dumps(obj)
    s.write(proto.netstring_encode(message))

    assert (await proto.read_message(s)) == obj
