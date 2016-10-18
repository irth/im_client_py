import struct

import proto
import socket

a = proto.InitErrorMessage()
a.error = proto.InitErrorMessage.AlreadyRegistered
s = socket.socket()
s.connect(("127.0.0.1", 9123))

s.send(proto.serialize(a))
print(proto.read_message_socket(s))
