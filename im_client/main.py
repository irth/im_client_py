import asyncio
import asyncio.streams

from .netstringrpc import NetstringRPC
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
            self.subscriptions[event['name']]
        except KeyError:
            self.subscriptions[event['name']] = {}

        if plugin not in self.subscriptions[event['name']]:
            self.subscriptions[event['name']][plugin.name] = (
                plugin,
                event['data'] if 'data' in event else None
            )

        def deferred():
            self.unsubscribe(plugin, event)

        plugin.defer(deferred)

    def unsubscribe(self, plugin, event):
        try:
            if plugin.name in self.subscriptions[event['name']]:
                self.subscriptions[event['name']].pop(plugin.name)
                if len(self.subscriptions[event['name']]) == 0:
                    self.subscriptions.pop(event['name'])
        except KeyError:
            pass

    def register_handlers(self, plugin):
        async def subscribe_handler(params):
            self.subscribe(plugin, params)
            return {
                "result": "success"
            }

        plugin.rpc.register_handler("subscribe", subscribe_handler)

        async def unsubscribe_handler(params):
            self.unsubscribe(plugin, params)
            return {
                "result": "success"
            }

        plugin.rpc.register_handler("unsubscribe", unsubscribe_handler)

    async def accept(self, r, w: asyncio.streams.StreamWriter):
        # TODO: document the RPC API
        rpc = NetstringRPC(r, w, self.loop)
        plugin = Plugin(rpc)

        async def init_handler(params=None):
            if (params is None
                    or "secret" not in params
                    or "name" not in params):
                return {
                    "error": {
                        "code": -32602,
                        "message": "Invalid method parameter(s)."
                    }
                }
            elif params['secret'] != "hardcoded_secret":
                return {
                    "error": {
                        "code": 100,
                        "message": "Incorrect secret."
                    }
                }

            # If we're here it means that the init message is correct
            plugin.name = params['name']
            self.plugins[params['name']] = plugin

            def pop():
                self.plugins.pop(plugin.name)

            plugin.defer(pop)  # pop plugin after the connection ends

            self.register_handlers(plugin)

            return {
                "result": "success"
            }

        rpc.register_handler("init", init_handler)

        try:
            await rpc.loop()
        except asyncio.streams.IncompleteReadError:
            for i in plugin.deffered_tasks:
                i()
