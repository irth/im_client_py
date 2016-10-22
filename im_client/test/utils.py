import asyncio
import threading

from im_client import main


def with_server(f):
    def wrapped(event_loop, *args, **kwargs):
        try:
            server = main.IMClient(event_loop)
            server.start()
            event_loop.run_until_complete(f(event_loop, server))
        finally:
            server.stop()
            event_loop.stop()

    return wrapped
