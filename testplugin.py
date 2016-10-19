import struct

import proto
import socket

a = proto.InitResultMessage()
a.result = proto.InitResultMessage.Success
s = socket.socket()
s.connect(("127.0.0.1", 9123))

s.send(proto.serialize(a))
print(proto.read_message_socket(s))
