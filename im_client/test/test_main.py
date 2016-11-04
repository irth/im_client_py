import pytest

from im_client import main, proto
import utils

VALID_SECRET = "hardcoded_secret"


@pytest.mark.asyncio
async def test_connect_with_valid_secret():
    message = proto.InitMessage()
    message.name = "TestName"
    message.secret = VALID_SECRET

    server = main.IMClient(None)
    r = utils.MockStream()
    w = utils.MockStream()
    r.write(proto.serialize(message))
    r.close()

    await server.accept(r, w)
    reply = (await proto.read_message_async(w))

    assert reply.result == proto.InitResultMessage.Success


@pytest.mark.asyncio
async def test_connect_with_invalid_secret():
    message = proto.InitMessage()
    message.name = "TestName"
    message.secret = VALID_SECRET + "1"  # make it invalid

    server = main.IMClient(None)
    r = utils.MockStream()
    w = utils.MockStream()
    r.write(proto.serialize(message))
    r.close()

    await server.accept(r, w)
    reply = (await proto.read_message_async(w))

    # TODO: maybe get rid of _async and _socket as it was only needed for the synchronous tests...

    assert reply.result == proto.InitResultMessage.Error
    assert reply.error == proto.InitResultMessage.IncorrectSecret


@pytest.mark.asyncio
async def test_register_plugin():
    message = proto.InitMessage()
    message.name = "PluginName"
    message.secret = VALID_SECRET

    server = main.IMClient(None)
    server.plugins = utils.MockDict()
    r = utils.MockStream()
    w = utils.MockStream()
    r.write(proto.serialize(message))
    r.close()

    await server.accept(r, w)
    reply = (await proto.read_message_async(w))

    assert reply.result == proto.InitResultMessage.Success
    added = False
    for call in server.plugins.__setitem__.call_args_list:
        # call[0] contains the positional args and we want the first one
        if call[0][0] == message.name:
            added = True
            break
    assert added


@pytest.mark.asyncio
async def test_unregister_plugin():
    message = proto.InitMessage()
    message.name = "PluginName"
    message.secret = VALID_SECRET

    server = main.IMClient(None)
    r = utils.MockStream()
    w = utils.MockStream()
    r.write(proto.serialize(message))
    r.close()

    await server.accept(r, w)
    reply = (await proto.read_message_async(w))

    assert reply.result == proto.InitResultMessage.Success
    assert message.name not in server.plugins.keys()


@pytest.mark.asyncio
async def test_subscribe_event():
    init_message = proto.InitMessage()
    init_message.name = "PluginName"
    init_message.secret = VALID_SECRET
    subscribe_message = proto.SubscribeMessage()
    subscribe_message.name = "ExampleEvent"

    async def subscriber_list_exists():
        r = utils.MockStream()
        w = utils.MockStream()
        r.write(proto.serialize(init_message))
        r.write(proto.serialize(subscribe_message))
        r.close()
        server = main.IMClient(None)

        sub_list = utils.MockList()
        server.subscriptions = utils.MockDict()

        await server.accept(r, w)
        reply = (await proto.read_message_async(w))

        assert reply.result == proto.InitResultMessage.Success

        added_subscriber_list = False
        print("subs", server.subscriptions.__setitem__.__call_args_list[0])
        for call in server.subscriptions.__setitem__.call_args_list:
            # call[0] contains the positional args and we want the first one
            print("call", call)
            if call[0][0] == subscribe_message.name:
                added_subscriber_list = True

        return added_subscriber_list

    async def plugin_is_added():
        r = utils.MockStream()
        w = utils.MockStream()
        r.write(proto.serialize(init_message))
        r.write(proto.serialize(subscribe_message))
        r.close()
        server = main.IMClient(None)

        sub_list = utils.MockList()
        server.subscriptions = {
            subscribe_message.name: sub_list
        }

        await server.accept(r, w)
        reply = (await proto.read_message_async(w))

        assert reply.result == proto.InitResultMessage.Success

        added_plugin = False
        for call in sub_list.append.call_args_list:
            print(call)
            if call[0][0][0].name == init_message.name:
                added_plugin = True

        return added_plugin

    assert (await subscriber_list_exists())
    assert (await plugin_is_added())