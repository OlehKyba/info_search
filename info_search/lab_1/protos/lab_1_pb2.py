# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: info_search/lab_1/protos/lab_1.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n$info_search/lab_1/protos/lab_1.proto\x12\x14info_search.lab_1.v1"3\n\x04Term\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\r\x12\x11\n\tfrequency\x18\x03 \x01(\r"B\n\x07Lexicon\x12)\n\x05terms\x18\x01 \x03(\x0b\x32\x1a.info_search.lab_1.v1.Term\x12\x0c\n\x04\x64ocs\x18\x02 \x03(\tb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "info_search.lab_1.protos.lab_1_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _TERM._serialized_start = 62
    _TERM._serialized_end = 113
    _LEXICON._serialized_start = 115
    _LEXICON._serialized_end = 181
# @@protoc_insertion_point(module_scope)