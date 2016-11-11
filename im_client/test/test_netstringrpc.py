import asyncio
import pytest

from im_client import proto, netstringrpc
from utils import MockStream

@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_netstringrpc_make_request(event_loop):
    r = MockStream()
    w = MockStream()

    rpc = netstringrpc.NetstringRPC(r, w, event_loop)
    proto.write_message(r, {
        "jsonrpc": "2.0",
        "result": "ThisIsATest",
        "id": rpc.last_id
    })
    r.close()

    future = rpc.test.method()
    try:
        await rpc.loop()
    except asyncio.streams.IncompleteReadError:
        # connection closed
        response = await future
        assert response['result'] == "ThisIsATest"


@pytest.mark.asyncio
async def test_netstringrpc_handle_request(event_loop):
    r = MockStream()
    w = MockStream()

    rpc = netstringrpc.NetstringRPC(r, w, event_loop)
    async def handler():
        return {
            "result": 42,
        }
    rpc.register_handler("the_answer", handler)

    proto.write_message(r, {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "the_answer"
    })

    async def check_the_reply():
        message = await proto.read_message(w)
        r.close()
        assert message["id"] == 0
        assert message["result"] == 42
        assert message['jsonrpc'] == "2.0"

    try:
        await asyncio.gather(
            check_the_reply(),
            rpc.loop()
        )
    except asyncio.streams.IncompleteReadError:
        pass  # the connection's closed