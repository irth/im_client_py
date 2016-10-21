import asyncio

from im_client import proto
import utils


@utils.with_server
async def test_connect_with_valid_secret(loop):
    message = proto.InitMessage()
    message.name = "TestName"
    message.secret = "hardcoded_secret"

    r, w = await asyncio.streams.open_connection('127.0.0.1', 9123, loop=loop)
    w.write(proto.serialize(message))
    reply = (await proto.read_message_async(r))

    assert reply.result == proto.InitResultMessage.Success


@utils.with_server
async def test_connect_with_invalid_secret(loop):
    message = proto.InitMessage()
    message.name = "TestName"
    message.secret = "invalid_secret"

    r, w = await asyncio.streams.open_connection('127.0.0.1', 9123, loop=loop)
    w.write(proto.serialize(message))
    reply = (await proto.read_message_async(r))

    assert reply.result == proto.InitResultMessage.Error
    assert reply.error == proto.InitResultMessage.IncorrectSecret
