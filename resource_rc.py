# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.15.2)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x00\x9f\
\x3c\
\x73\x76\x67\x20\x78\x6d\x6c\x6e\x73\x3d\x22\x68\x74\x74\x70\x3a\
\x2f\x2f\x77\x77\x77\x2e\x77\x33\x2e\x6f\x72\x67\x2f\x32\x30\x30\
\x30\x2f\x73\x76\x67\x22\x20\x68\x65\x69\x67\x68\x74\x3d\x22\x32\
\x34\x22\x20\x76\x69\x65\x77\x42\x6f\x78\x3d\x22\x30\x20\x2d\x39\
\x36\x30\x20\x39\x36\x30\x20\x39\x36\x30\x22\x20\x77\x69\x64\x74\
\x68\x3d\x22\x32\x34\x22\x3e\x3c\x70\x61\x74\x68\x20\x64\x3d\x22\
\x4d\x34\x38\x30\x2d\x33\x34\x35\x20\x32\x34\x30\x2d\x35\x38\x35\
\x6c\x35\x36\x2d\x35\x36\x20\x31\x38\x34\x20\x31\x38\x34\x20\x31\
\x38\x34\x2d\x31\x38\x34\x20\x35\x36\x20\x35\x36\x2d\x32\x34\x30\
\x20\x32\x34\x30\x5a\x22\x2f\x3e\x3c\x2f\x73\x76\x67\x3e\
"

qt_resource_name = b"\
\x00\x06\
\x07\xac\x02\xc3\
\x00\x73\
\x00\x74\x00\x79\x00\x6c\x00\x65\x00\x73\
\x00\x04\
\x00\x06\xfa\x5e\
\x00\x69\
\x00\x63\x00\x6f\x00\x6e\
\x00\x0c\
\x0b\xd3\x97\xa7\
\x00\x64\
\x00\x72\x00\x6f\x00\x70\x00\x64\x00\x6f\x00\x77\x00\x6e\x00\x2e\x00\x73\x00\x76\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x12\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
\x00\x00\x00\x20\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x12\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x20\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x8e\xb9\x18\x7e\xeb\
"

qt_version = [int(v) for v in QtCore.qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()