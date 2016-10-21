import asyncio
import threading

from im_client import main


def with_server(f):
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        server = main.IMClient(loop)
        server.start()
        loop.run_until_complete(f(loop))
        server.stop()

    return wrapped
