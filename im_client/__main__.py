from . import IMClient
import asyncio

loop = asyncio.get_event_loop()
IMClient(loop).start()
loop.run_forever()
