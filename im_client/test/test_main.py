import asyncio

from im_client import proto
import utils


@utils.with_server
async def test_server(loop):
    message = proto.InitMessage()
    message.name = "TestName"
    message.secret = "hardcoded_secret"

    r, w = await asyncio.streams.open_connection('127.0.0.1', 9123, loop=loop)
    w.write(proto.serialize(message))
    reply = (await proto.read_message_async(r))

    assert reply.result == proto.InitResultMessage.Success
