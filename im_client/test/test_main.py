import asyncio

from im_client import proto
import utils

VALID_SECRET = "hardcoded_secret"

@utils.with_server
async def test_connect_with_valid_secret(loop, server):
    message = proto.InitMessage()
    message.name = "TestName"
    message.secret = VALID_SECRET

    r, w = await asyncio.streams.open_connection('127.0.0.1', 9123, loop=loop)
    w.write(proto.serialize(message))
    reply = (await proto.read_message_async(r))

    assert reply.result == proto.InitResultMessage.Success


@utils.with_server
async def test_connect_with_invalid_secret(loop, server):
    message = proto.InitMessage()
    message.name = "TestName"
    message.secret = VALID_SECRET + "1"  # make it invalid

    r, w = await asyncio.streams.open_connection('127.0.0.1', 9123, loop=loop)
    w.write(proto.serialize(message))
    reply = (await proto.read_message_async(r))

    assert reply.result == proto.InitResultMessage.Error
    assert reply.error == proto.InitResultMessage.IncorrectSecret


@utils.with_server
async def test_register_plugin(loop, server):
    message = proto.InitMessage()
    message.name = "PluginName"
    message.secret = VALID_SECRET

    r, w = await asyncio.streams.open_connection('127.0.0.1', 9123, loop=loop)
    w.write(proto.serialize(message))
    reply = (await proto.read_message_async(r))

    assert reply.result == proto.InitResultMessage.Success
    assert message.name in server.plugins.keys()
