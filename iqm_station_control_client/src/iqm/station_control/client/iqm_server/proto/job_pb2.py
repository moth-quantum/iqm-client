# Copyright 2025 IQM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: job.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import common_pb2 as common__pb2
from . import uuid_pb2 as uuid__pb2
from . import qc_pb2 as qc__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tjob.proto\x12\niqm.server\x1a\x0c\x63ommon.proto\x1a\nuuid.proto\x1a\x08qc.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xcf\x03\n\x05JobV1\x12\x1c\n\x02id\x18\x01 \x02(\x0b\x32\x10.iqm.server.Uuid\x12!\n\x04type\x18\x02 \x02(\x0e\x32\x13.iqm.server.JobType\x12\x37\n\x10quantum_computer\x18\x03 \x02(\x0b\x32\x1d.iqm.server.QuantumComputerV1\x12,\n\x05input\x18\x05 \x02(\x0b\x32\x1d.iqm.server.JobInputSummaryV1\x12%\n\x06status\x18\x06 \x02(\x0e\x32\x15.iqm.server.JobStatus\x12\x16\n\x0equeue_position\x18\x07 \x01(\r\x12\r\n\x05\x65rror\x18\x08 \x01(\t\x12.\n\ncreated_at\x18\t \x02(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\n \x02(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x38\n\x14\x65xecution_started_at\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x36\n\x12\x65xecution_ended_at\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"[\n\x11JobInputSummaryV1\x12%\n\x08job_type\x18\x01 \x02(\x0e\x32\x13.iqm.server.JobType\x12\r\n\x05shots\x18\x02 \x02(\x05\x12\x10\n\x08\x63ircuits\x18\x03 \x02(\x05\"f\n\nJobEventV1\x12*\n\tkeepalive\x18\x01 \x01(\x0b\x32\x15.iqm.server.KeepaliveH\x00\x12#\n\x06update\x18\x02 \x01(\x0b\x32\x11.iqm.server.JobV1H\x00\x42\x07\n\x05value\"+\n\x0bJobLookupV1\x12\x1c\n\x02id\x18\x01 \x02(\x0b\x32\x10.iqm.server.Uuid\"\x7f\n\x12SubmitJobRequestV1\x12\x1f\n\x05qc_id\x18\x01 \x02(\x0b\x32\x10.iqm.server.Uuid\x12!\n\x04type\x18\x02 \x02(\x0e\x32\x13.iqm.server.JobType\x12\x0f\n\x07payload\x18\x03 \x02(\x0c\x12\x14\n\x0cuse_timeslot\x18\x04 \x01(\x08*!\n\x07JobType\x12\x0b\n\x07\x43IRCUIT\x10\x00\x12\t\n\x05PULSE\x10\x01*c\n\tJobStatus\x12\x0c\n\x08IN_QUEUE\x10\x00\x12\r\n\tEXECUTING\x10\x01\x12\r\n\tCOMPLETED\x10\x02\x12\r\n\tCANCELLED\x10\x03\x12\n\n\x06\x46\x41ILED\x10\x04\x12\x0f\n\x0bINTERRUPTED\x10\x05\x32\x8c\x03\n\x04Jobs\x12@\n\x0bSubmitJobV1\x12\x1e.iqm.server.SubmitJobRequestV1\x1a\x11.iqm.server.JobV1\x12\x36\n\x08GetJobV1\x12\x17.iqm.server.JobLookupV1\x1a\x11.iqm.server.JobV1\x12\x45\n\x10SubscribeToJobV1\x12\x17.iqm.server.JobLookupV1\x1a\x16.iqm.server.JobEventV10\x01\x12\x43\n\x0fGetJobPayloadV1\x12\x17.iqm.server.JobLookupV1\x1a\x15.iqm.server.DataChunk0\x01\x12\x43\n\x0fGetJobResultsV1\x12\x17.iqm.server.JobLookupV1\x1a\x15.iqm.server.DataChunk0\x01\x12\x39\n\x0b\x43\x61ncelJobV1\x12\x17.iqm.server.JobLookupV1\x1a\x11.iqm.server.JobV1')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'job_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_JOBTYPE']._serialized_start=931
  _globals['_JOBTYPE']._serialized_end=964
  _globals['_JOBSTATUS']._serialized_start=966
  _globals['_JOBSTATUS']._serialized_end=1065
  _globals['_JOBV1']._serialized_start=95
  _globals['_JOBV1']._serialized_end=558
  _globals['_JOBINPUTSUMMARYV1']._serialized_start=560
  _globals['_JOBINPUTSUMMARYV1']._serialized_end=651
  _globals['_JOBEVENTV1']._serialized_start=653
  _globals['_JOBEVENTV1']._serialized_end=755
  _globals['_JOBLOOKUPV1']._serialized_start=757
  _globals['_JOBLOOKUPV1']._serialized_end=800
  _globals['_SUBMITJOBREQUESTV1']._serialized_start=802
  _globals['_SUBMITJOBREQUESTV1']._serialized_end=929
  _globals['_JOBS']._serialized_start=1068
  _globals['_JOBS']._serialized_end=1464
# @@protoc_insertion_point(module_scope)
