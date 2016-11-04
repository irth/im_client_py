# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages.proto',
  package='im_client',
  serialized_pb=_b('\n\x0emessages.proto\x12\tim_client\"+\n\x0bInitMessage\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0e\n\x06secret\x18\x02 \x02(\t\"\x83\x02\n\x11InitResultMessage\x12\x37\n\x06result\x18\x01 \x02(\x0e\x32\'.im_client.InitResultMessage.InitResult\x12\x39\n\x05\x65rror\x18\x02 \x01(\x0e\x32*.im_client.InitResultMessage.InitErrorCode\"T\n\rInitErrorCode\x12\x13\n\x0fIncorrectSecret\x10\x00\x12\x15\n\x11\x41lreadyRegistered\x10\x01\x12\x17\n\x13\x45xpectedInitMessage\x10\x02\"$\n\nInitResult\x12\x0b\n\x07Success\x10\x00\x12\t\n\x05\x45rror\x10\x01\".\n\x10SubscribeMessage\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_INITRESULTMESSAGE_INITERRORCODE = _descriptor.EnumDescriptor(
  name='InitErrorCode',
  full_name='im_client.InitResultMessage.InitErrorCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='IncorrectSecret', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlreadyRegistered', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ExpectedInitMessage', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=212,
  serialized_end=296,
)
_sym_db.RegisterEnumDescriptor(_INITRESULTMESSAGE_INITERRORCODE)

_INITRESULTMESSAGE_INITRESULT = _descriptor.EnumDescriptor(
  name='InitResult',
  full_name='im_client.InitResultMessage.InitResult',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Success', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Error', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=298,
  serialized_end=334,
)
_sym_db.RegisterEnumDescriptor(_INITRESULTMESSAGE_INITRESULT)


_INITMESSAGE = _descriptor.Descriptor(
  name='InitMessage',
  full_name='im_client.InitMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='im_client.InitMessage.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='secret', full_name='im_client.InitMessage.secret', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=72,
)


_INITRESULTMESSAGE = _descriptor.Descriptor(
  name='InitResultMessage',
  full_name='im_client.InitResultMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='im_client.InitResultMessage.result', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error', full_name='im_client.InitResultMessage.error', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _INITRESULTMESSAGE_INITERRORCODE,
    _INITRESULTMESSAGE_INITRESULT,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=75,
  serialized_end=334,
)


_SUBSCRIBEMESSAGE = _descriptor.Descriptor(
  name='SubscribeMessage',
  full_name='im_client.SubscribeMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='im_client.SubscribeMessage.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='im_client.SubscribeMessage.data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=336,
  serialized_end=382,
)

_INITRESULTMESSAGE.fields_by_name['result'].enum_type = _INITRESULTMESSAGE_INITRESULT
_INITRESULTMESSAGE.fields_by_name['error'].enum_type = _INITRESULTMESSAGE_INITERRORCODE
_INITRESULTMESSAGE_INITERRORCODE.containing_type = _INITRESULTMESSAGE
_INITRESULTMESSAGE_INITRESULT.containing_type = _INITRESULTMESSAGE
DESCRIPTOR.message_types_by_name['InitMessage'] = _INITMESSAGE
DESCRIPTOR.message_types_by_name['InitResultMessage'] = _INITRESULTMESSAGE
DESCRIPTOR.message_types_by_name['SubscribeMessage'] = _SUBSCRIBEMESSAGE

InitMessage = _reflection.GeneratedProtocolMessageType('InitMessage', (_message.Message,), dict(
  DESCRIPTOR = _INITMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:im_client.InitMessage)
  ))
_sym_db.RegisterMessage(InitMessage)

InitResultMessage = _reflection.GeneratedProtocolMessageType('InitResultMessage', (_message.Message,), dict(
  DESCRIPTOR = _INITRESULTMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:im_client.InitResultMessage)
  ))
_sym_db.RegisterMessage(InitResultMessage)

SubscribeMessage = _reflection.GeneratedProtocolMessageType('SubscribeMessage', (_message.Message,), dict(
  DESCRIPTOR = _SUBSCRIBEMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:im_client.SubscribeMessage)
  ))
_sym_db.RegisterMessage(SubscribeMessage)


# @@protoc_insertion_point(module_scope)
