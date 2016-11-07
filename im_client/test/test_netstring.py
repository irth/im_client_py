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
