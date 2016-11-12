import asyncio

import pytest

from im_client import main, proto
import utils

VALID_SECRET = "hardcoded_secret"


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_connect_with_valid_secret(event_loop):
    r = utils.MockStream()
    w = utils.MockStream()

    server = main.IMClient(event_loop)

    proto.write_message(r, {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "init",
        "params": {
            "name": "TestName",
            "secret": VALID_SECRET
        }
    })

    async def check_the_reply():
        message = await proto.read_message(w)
        r.close()
        assert message == {
            "id": 0,
            "jsonrpc": "2.0",
            "result": "success"
        }

    try:
        await asyncio.gather(
            check_the_reply(),
            server.accept(r, w)
        )
    except asyncio.streams.IncompleteReadError:
        pass  # the connection's closed


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_connect_with_invalid_secret(event_loop):
    r = utils.MockStream()
    w = utils.MockStream()

    server = main.IMClient(event_loop)

    proto.write_message(r, {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "init",
        "params": {
            "name": "TestName",
            "secret": VALID_SECRET + "1"  # make the secret invalid
        }
    })

    async def check_the_reply():
        message = await proto.read_message(w)
        r.close()
        assert message == {
            "id": 0,
            "jsonrpc": "2.0",
            "error": {
                "code": 100,
                "message": "Incorrect secret."
            }
        }

    try:
        await asyncio.gather(
            check_the_reply(),
            server.accept(r, w)
        )
    except asyncio.streams.IncompleteReadError:
        pass  # the connection's closed


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_register_plugin(event_loop):
    r = utils.MockStream()
    w = utils.MockStream()

    server = main.IMClient(event_loop)
    server.plugins = utils.MockDict()

    proto.write_message(r, {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "init",
        "params": {
            "name": "TestName",
            "secret": VALID_SECRET
        }
    })

    async def check_the_reply():
        message = await proto.read_message(w)
        r.close()
        assert message == {
            "id": 0,
            "jsonrpc": "2.0",
            "result": "success"
        }

        added = False
        for call in server.plugins.__setitem__.call_args_list:
            # call[0] contains the positional args and we want the first one
            if call[0][0] == "TestName":
                added = True
                break
        assert added

    try:
        await asyncio.gather(
            check_the_reply(),
            server.accept(r, w)
        )
    except asyncio.streams.IncompleteReadError:
        pass  # the connection's closed


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_unregister_plugin(event_loop):
    r = utils.MockStream()
    w = utils.MockStream()

    server = main.IMClient(event_loop)

    proto.write_message(r, {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "init",
        "params": {
            "name": "TestName",
            "secret": VALID_SECRET
        }
    })

    async def check_the_reply():
        message = await proto.read_message(w)
        r.close()
        assert message == {
            "id": 0,
            "jsonrpc": "2.0",
            "result": "success"
        }

    try:
        await asyncio.gather(
            check_the_reply(),
            server.accept(r, w)
        )
    except asyncio.streams.IncompleteReadError:
        pass  # the connection's closed

    assert "TestName" not in server.plugins.keys()


init_message = {
    "jsonrpc": "2.0",
    "id": 0,
    "method": "init",
    "params": {
        "name": "TestName",
        "secret": VALID_SECRET
    }
}

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
    r = utils.MockStream()
    w = utils.MockStream()

    proto.write_message(r, init_message)

    server = main.IMClient(event_loop)

    server.subscriptions = utils.MockDict()

    async def check_the_reply():
        message = await proto.read_message(w)
        assert message == {
            "id": 0,
            "jsonrpc": "2.0",
            "result": "success"
        }

        proto.write_message(r, subscribe_message)
        message = await proto.read_message(w)
        assert message == {
            "id": 1,
            "jsonrpc": "2.0",
            "result": "success"
        }

        added_subscriber_list = False
        for call in server.subscriptions.__setitem__.call_args_list:
            # call[0] contains the positional args and we want the first one
            if call[0][0] == "ExampleEvent":
                added_subscriber_list = True

        r.close()
        assert added_subscriber_list

    try:
        await asyncio.gather(
            check_the_reply(),
            server.accept(r, w)
        )
    except asyncio.streams.IncompleteReadError:
        pass  # the connection's closed


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_subscription_is_added(event_loop):
    r = utils.MockStream()
    w = utils.MockStream()

    proto.write_message(r, init_message)

    server = main.IMClient(event_loop)

    sub_list = utils.MockList()
    server.subscriptions = {
        "ExampleEvent": sub_list
    }

    async def check_the_reply():
        message = await proto.read_message(w)
        assert message == {
            "id": 0,
            "jsonrpc": "2.0",
            "result": "success"
        }

        proto.write_message(r, subscribe_message)
        message = await proto.read_message(w)
        assert message == {
            "id": 1,
            "jsonrpc": "2.0",
            "result": "success"
        }

        added_plugin = False
        for call in sub_list.append.call_args_list:
            if call[0][0][0].name == "TestName":
                added_plugin = True

        r.close()
        assert added_plugin

    try:
        await asyncio.gather(
            check_the_reply(),
            server.accept(r, w)
        )
    except asyncio.streams.IncompleteReadError:
        pass  # the connection's closed
