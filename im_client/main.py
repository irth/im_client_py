import asyncio
import asyncio.streams

import struct

from .plugin import Plugin
from . import proto


class IMClient:
    def __init__(self, loop: asyncio.BaseEventLoop, addr='127.0.0.1',
                 port=9123):
        self.addr = addr
        self.port = port
        self.server = None
        self.loop = loop
        self.plugins = {}
        self.subscriptions = {}

    def start(self):
        self.server = self.loop.run_until_complete(
            asyncio.streams.start_server(self.accept, self.addr, self.port,
                                         loop=self.loop))

    def stop(self):
        if self.server is not None:
            self.server.close()
            self.loop.run_until_complete(self.server.wait_closed())
            self.server = None

    def subscribe(self, plugin, event):
        try:
            self.subscriptions[event.name]
        except KeyError:
            self.subscriptions[event.name] = []

        if plugin not in self.subscriptions[event.name]:
            self.subscriptions[event.name].append((
                plugin,
                event.data if event.data is not None else b''
            ))

        def deferred():
            self.unsubscribe(plugin, event)
        plugin.defer(deferred)

    def unsubscribe(self, plugin, event):
        try:
            if plugin in self.subscriptions[event.name]:
                self.subscriptions[event.name].remove(plugin)
                if len(self.subscriptions[event.name]) == 0:
                    self.subscriptions.pop(event.name)
        except KeyError:
            pass

    def handle_message(self, plugin, message):
        if isinstance(message, proto.SubscribeMessage):
            self.subscribe(plugin, message)

    async def accept(self, r, w: asyncio.streams.StreamWriter):
        message = await proto.read_message_async(r)
        if message.__class__ == proto.InitMessage:
            if message.secret == "hardcoded_secret":
                plugin = Plugin(message.name, r, w)
                self.plugins[message.name] = plugin

                def pop():
                    self.plugins.pop(plugin.name)
                plugin.defer(pop)  # pop plugin after the connection ends

                successmsg = proto.InitResultMessage()
                successmsg.result = proto.InitResultMessage.Success
                w.write(proto.serialize(successmsg))

                # This loop is not actually infinite, as we break out of it
                # when the connection gets closed.
                while True:
                    try:
                        message = await proto.read_message_async(r)
                        self.handle_message(plugin, message)
                    except asyncio.streams.IncompleteReadError:
                        # This exception gets thrown when the connection is
                        # closed. There's no reason to keep waiting for
                        # messages when the client closes the connection.
                        break

                for i in plugin.deffered_tasks:
                    i()

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
