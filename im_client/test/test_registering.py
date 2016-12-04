import asyncio

import pytest
import utils
from test_main import INIT_MESSAGE

from im_client import proto


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_register_plugin(event_loop):
    server, r, w = await utils.create_server(
        event_loop,
        messages=INIT_MESSAGE
    )

    server.plugins = utils.MockDict()

    async def check_the_reply():
        message = await proto.read_message(w)
        r.close()
        assert message["result"] == "success"

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
    server, r, w = await utils.create_server(
        event_loop,
        messages=INIT_MESSAGE
    )

    async def check_the_reply():
        message = await proto.read_message(w)
        r.close()
        assert message["result"] == "success"

    try:
        await asyncio.gather(
            check_the_reply(),
            server.accept(r, w)
        )
    except asyncio.streams.IncompleteReadError:
        pass  # the connection's closed

    assert "TestName" not in server.plugins.keys()