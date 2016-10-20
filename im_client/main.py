import asyncio
import asyncio.streams

import struct

from . import proto

class IMClient:
    def __init__(self, loop: asyncio.BaseEventLoop):
        self.server = None
        self.loop = loop
        self.plugins = {}

    def start(self):
        self.server = self.loop.run_until_complete(
            asyncio.streams.start_server(self.accept, '127.0.0.1', 9123, loop=self.loop))

    def stop(self):
        if self.server is not None:
            self.server.close()

    async def accept(self, r, w: asyncio.streams.StreamWriter):
        message = await proto.read_message_async(r)
        if message.__class__ == proto.InitMessage:
            successmsg = proto.InitResultMessage()
            successmsg.result = proto.InitResultMessage.Success
            w.write(proto.serialize(successmsg))
        else:
            errmsg = proto.InitResultMessage()
            errmsg.result = proto.InitResultMessage.Error
            errmsg.error = proto.InitResultMessage.ExpectedInitMessage
            w.write(proto.serialize(errmsg))
