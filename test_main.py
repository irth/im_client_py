import asyncio

import pytest

import main
import socket
import proto
import threading

def test_connect():
    loop = asyncio.get_event_loop()
    server = main.IMClient(loop)
    server.start()
    server_thread = threading.Thread(target=loop.run_forever)
    server_thread.start()
    message = proto.InitMessage()
    message.name = "TestName"
    message.secret = "hardcoded_secret"

    s = socket.socket()
    s.connect(('127.0.0.1', 9123))
    s.send(proto.serialize(message))
    assert proto.read_message_socket(s).result == proto.InitResultMessage.Success
    server.stop()
    loop.stop()