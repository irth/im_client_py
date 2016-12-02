import asyncio
from . import proto


class RPCCall:
    def __init__(self, conn, name, notification=False):
        if name == "_notification":
            self.notification = True
        else:
            self.notification = notification
        self.conn = conn
        self.name = name if not name == "_notification" else None

    def __getattr__(self, name):
        if name == '_notification':
            return RPCCall(self.conn, self.name, notification=True)
        else:
            if self.name is not None:
                new_name = "%s.%s" % (self.name, name)
            else:
                new_name = name
            return RPCCall(self.conn, new_name, notification=self.notification)

    def __call__(self, params=None):
        request = {
            "jsonrpc": "2.0",
            "method": self.name
        }

        response = None
        if not self.notification:
            request["id"] = self.conn.last_id
            # the main loop will mark futures done when needed
            response = asyncio.Future()
            self.conn.response_futures[request['id']] = response

        if params is not None:
            request["params"] = params
        self.conn.last_id += 1

        proto.write_message(self.conn.writer, request)

        if response is not None:
            return response


class NetstringRPC:
    def __init__(self, reader: asyncio.streams.StreamReader,
                 writer: asyncio.streams.StreamWriter,
                 loop: asyncio.AbstractEventLoop):
        self.event_loop = loop
        self.reader = reader
        self.writer = writer
        self.last_id = 0
        self.handlers = {}
        self.response_futures = {}
        self.request_futures = {}

    def register_handler(self, method, handler):
        self.handlers[method] = handler

    def check_futures(self):
        # Check whether the method calls have finished, and if so, send the
        # result back.
        # I wrap the iterator in a list because I want to remove the keys
        # while in the loop.

        for message_id, future in list(self.request_futures.items()):
            if future.done():
                result = future.result()
                result['jsonrpc'] = "2.0"
                result['id'] = message_id
                proto.write_message(self.writer, result)
                del self.request_futures[message_id]
        self.event_loop.call_soon(self.check_futures)

    def close(self):
        self.writer.close()

    async def loop(self):
        self.event_loop.call_soon(self.check_futures)
        while True:
            message = (await proto.read_message(self.reader))
            message_type = "invalid"
            if "method" in message:
                message_type = "request" if "id" in message else "notification"
            elif "id" in message:
                if "result" in message or "error" in message:
                    message_type = "response"

            if message_type == "invalid":
                continue  # silently ignore the error because i'm too lazy
            elif message_type == "response":
                if message['id'] in self.response_futures:
                    self.response_futures[message['id']].set_result(message)
            elif message_type == "request" or message_type == "notification":
                if message['method'] in self.handlers:
                    if "params" in message:
                        coro = self.handlers[message['method']](message['params'])
                    else:
                        coro = self.handlers[message['method']]()
                    future = asyncio.ensure_future(coro)

                    if message_type != "notification":
                        # If the request is a so-called notification, we
                        # don't need to (and in fact can't) return a response.
                        # So we won't bother even checking for it.
                        self.request_futures[message['id']] = future

    def __getattr__(self, item):
        return RPCCall(self, item)
