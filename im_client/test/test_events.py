import asyncio
from copy import deepcopy

import pytest
import utils
from test_main import INIT_MESSAGE

from im_client import proto, main

subscribe_message = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "subscribe",
    "params": {
        "name": "ExampleEvent"
    }
}


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_subscriber_list_exists(event_loop):
    async def setup(server, r, w):
        server.subscriptions = utils.MockDict()

    async def check_the_reply(server, r, w):
        message = await proto.read_message(w)
        assert message["result"] == "success"

        proto.write_message(r, subscribe_message)
        message = await proto.read_message(w)
        assert message["result"] == "success"

        added_subscriber_list = False
        for call in server.subscriptions.__setitem__.call_args_list:
            # call[0] contains the positional args and we want the first one
            if call[0][0] == "ExampleEvent":
                added_subscriber_list = True

        r.close()
        assert added_subscriber_list

    await utils.create_server(
        event_loop,
        messages=INIT_MESSAGE,
        setup=setup,
        check=check_the_reply
    )


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_subscription_is_added(event_loop):
    sub_list = utils.MockDict()

    async def setup(server, r, w):
        server.subscriptions = {
            "ExampleEvent": sub_list
        }

    async def check_the_reply(server, r, w):
        message = await proto.read_message(w)
        assert message["result"] == "success"

        proto.write_message(r, subscribe_message)
        message = await proto.read_message(w)
        assert message["result"] == "success"

        added_plugin = False
        for call in sub_list.__setitem__.call_args_list:
            if call[0][0] == "TestName":
                added_plugin = True

        r.close()
        assert added_plugin

    await utils.create_server(
        event_loop,
        messages=INIT_MESSAGE,
        setup=setup,
        check=check_the_reply
    )


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_subscription_is_removed(event_loop):
    sub_list = utils.MockDict()

    async def setup(server, r, w):
        server.subscriptions = {
            "ExampleEvent": sub_list
        }

    async def check_the_reply(server, r, w):
        message = await proto.read_message(w)
        assert message["result"] == "success"

        proto.write_message(r, subscribe_message)
        message = await proto.read_message(w)
        assert message["result"] == "success"

        added_plugin = False
        for call in sub_list.__setitem__.call_args_list:
            if call[0][0] == "TestName":
                added_plugin = True

        msg = deepcopy(subscribe_message)
        msg["method"] = "unsubscribe"
        msg["id"] = 2
        proto.write_message(r, msg)

        message = await proto.read_message(w)
        assert message["result"] == "success"

        removed_plugin = False
        for call in sub_list.pop.call_args_list:
            if call[0][0] == "TestName":
                removed_plugin = True

        r.close()
        assert added_plugin and removed_plugin

    await utils.create_server(
        event_loop,
        messages=INIT_MESSAGE,
        setup=setup,
        check=check_the_reply
    )


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_emit_receive_event(event_loop):
    # Create the event emitter plugin
    r1 = utils.MockStream()
    w1 = utils.MockStream()
    m1 = INIT_MESSAGE

    # Create the event listener plugin
    r2 = utils.MockStream()
    w2 = utils.MockStream()
    m2 = deepcopy(INIT_MESSAGE)
    m2['params']['name'] = "TestReceiver"

    # Register the plugins
    proto.write_message(r1, m1)
    proto.write_message(r2, m2)

    async def check_the_reply():
        # Make sure that the plugins were registered correctly
        assert (await proto.read_message(w1))['result'] == 'success'
        assert (await proto.read_message(w2))['result'] == 'success'

        # Register the listener
        proto.write_message(r2, subscribe_message)
        assert (await proto.read_message(w2))['result'] == 'success'

        # Emit the event
        proto.write_message(r1, {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "emit",
            "params": {
                "name": "ExampleEvent"
            }
        })
        assert (await proto.read_message(w1))['result'] == 'success'
        assert (await proto.read_message(w2)) == {
            'method': 'event',
            'params': {'name': 'ExampleEvent', 'sender': INIT_MESSAGE['params']['name']},
            'jsonrpc': '2.0'
        }

        r1.close()
        r2.close()

    # create the server
    server = main.IMClient(event_loop)

    # run the server and the client asynchronously
    try:
        await asyncio.gather(
            check_the_reply(),
            server.accept(r1, w1),
            server.accept(r2, w2)
        )
    except asyncio.streams.IncompleteReadError:  # the connection's closed
        pass


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_emit_invalid_event(event_loop):
    async def check_the_reply(server, r, w):
        # Make sure that the plugin was registered correctly
        assert (await proto.read_message(w))['result'] == 'success'

        # Emit the event
        proto.write_message(r, {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "emit",
            "params": {
                "name": "MESSAGE"
            }
        })

        assert (await proto.read_message(w))['error'] == {
            'code': 110,
            'message': 'Event invalid.'
        }

        r.close()

    await utils.create_server(
        event_loop,
        messages=INIT_MESSAGE,
        check=check_the_reply
    )


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_emit_valid_message_event(event_loop):
    async def check_the_reply(server, r, w):
        # Make sure that the plugin was registered correctly
        assert (await proto.read_message(w))['result'] == 'success'

        # Emit the event
        proto.write_message(r, {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "emit",
            "params": {
                "name": "MESSAGE",
                "from": "whoever",
                "to": "wherever",
                "text": "whatever"
            }
        })

        assert (await proto.read_message(w))['result'] == 'success'

        r.close()

    await utils.create_server(
        event_loop,
        messages=INIT_MESSAGE,
        check=check_the_reply
    )