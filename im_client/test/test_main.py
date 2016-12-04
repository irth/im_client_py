from copy import deepcopy

import pytest
import utils

from im_client import proto

VALID_SECRET = "hardcoded_secret"
INIT_MESSAGE = {
    "jsonrpc": "2.0",
    "id": 0,
    "method": "init",
    "params": {
        "name": "TestName",
        "secret": VALID_SECRET
    }
}


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_connect_with_valid_secret(event_loop):
    async def check_the_reply(server, r, w):
        message = await proto.read_message(w)
        r.close()
        assert message == {
            "id": 0,
            "jsonrpc": "2.0",
            "result": "success"
        }

    await utils.create_server(
        event_loop,
        messages=INIT_MESSAGE,
        check=check_the_reply
    )


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_connect_with_invalid_secret(event_loop):
    async def check_the_reply(server, r, w):
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

    msg = deepcopy(INIT_MESSAGE)
    msg['params']['secret'] = VALID_SECRET + "1"

    await utils.create_server(
        event_loop,
        messages=msg,
        check=check_the_reply
    )


