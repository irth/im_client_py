import asyncio
import asyncio.streams

import struct

from . import proto


class IMClient:
    def __init__(self, loop: asyncio.BaseEventLoop, addr='127.0.0.1',
                 port=9123):
        self.addr = addr
        self.port = port
        self.server = None
        self.loop = loop
        self.plugins = {}

    def start(self):
        self.server = self.loop.run_until_complete(
            asyncio.streams.start_server(self.accept, self.addr, self.port,
                                         loop=self.loop))

    def stop(self):
        if self.server is not None:
            self.server.close()
            self.loop.run_until_complete(self.server.wait_closed())
            self.server = None

    async def accept(self, r, w: asyncio.streams.StreamWriter):
        message = await proto.read_message_async(r)
        if message.__class__ == proto.InitMessage:
            if message.secret == "hardcoded_secret":
                successmsg = proto.InitResultMessage()
                successmsg.result = proto.InitResultMessage.Success
                w.write(proto.serialize(successmsg))
            else:
                errmsg = proto.InitResultMessage()
                errmsg.result = proto.InitResultMessage.Error
                errmsg.error = proto.InitResultMessage.IncorrectSecret
                w.write(proto.serialize(errmsg))
        else:
            errmsg = proto.InitResultMessage()
            errmsg.result = proto.InitResultMessage.Error
            errmsg.error = proto.InitResultMessage.ExpectedInitMessage
            w.write(proto.serialize(errmsg))
