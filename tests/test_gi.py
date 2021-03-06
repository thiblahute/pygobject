# -*- Mode: Python; py-indent-offset: 4 -*-
# coding=utf-8
# vim: tabstop=4 shiftwidth=4 expandtab

import sys

import unittest
import tempfile
import shutil
import os
import locale
import subprocess
from io import StringIO, BytesIO

import gi
from gi.repository import GObject, GLib

from gi.repository import GIMarshallingTests

from compathelper import _bytes

if sys.version_info < (3, 0):
    CONSTANT_UTF8 = "const \xe2\x99\xa5 utf8"
    PY2_UNICODE_UTF8 = unicode(CONSTANT_UTF8, 'UTF-8')
    CHAR_255 = '\xff'
else:
    CONSTANT_UTF8 = "const ♥ utf8"
    CHAR_255 = bytes([255])

CONSTANT_NUMBER = 42


class Number(object):

    def __init__(self, value):
        self.value = value

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)


class Sequence(object):

    def __init__(self, sequence):
        self.sequence = sequence

    def __len__(self):
        return len(self.sequence)

    def __getitem__(self, key):
        return self.sequence[key]


class TestConstant(unittest.TestCase):

# Blocked by https://bugzilla.gnome.org/show_bug.cgi?id=595773
#    def test_constant_utf8(self):
#        self.assertEqual(CONSTANT_UTF8, GIMarshallingTests.CONSTANT_UTF8)

    def test_constant_number(self):
        self.assertEqual(CONSTANT_NUMBER, GIMarshallingTests.CONSTANT_NUMBER)


class TestBoolean(unittest.TestCase):

    def test_boolean_return(self):
        self.assertEqual(True, GIMarshallingTests.boolean_return_true())
        self.assertEqual(False, GIMarshallingTests.boolean_return_false())

    def test_boolean_in(self):
        GIMarshallingTests.boolean_in_true(True)
        GIMarshallingTests.boolean_in_false(False)

        GIMarshallingTests.boolean_in_true(1)
        GIMarshallingTests.boolean_in_false(0)

    def test_boolean_out(self):
        self.assertEqual(True, GIMarshallingTests.boolean_out_true())
        self.assertEqual(False, GIMarshallingTests.boolean_out_false())

    def test_boolean_inout(self):
        self.assertEqual(False, GIMarshallingTests.boolean_inout_true_false(True))
        self.assertEqual(True, GIMarshallingTests.boolean_inout_false_true(False))


class TestInt8(unittest.TestCase):

    MAX = GObject.G_MAXINT8
    MIN = GObject.G_MININT8

    def test_int8_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int8_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int8_return_min())

    def test_int8_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.int8_in_max(max)
        GIMarshallingTests.int8_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.int8_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.int8_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int8_in_max, "self.MAX")

    def test_int8_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int8_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int8_out_min())

    def test_int8_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int8_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int8_inout_min_max(Number(self.MIN)))


class TestUInt8(unittest.TestCase):

    MAX = GObject.G_MAXUINT8

    def test_uint8_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint8_return())

    def test_uint8_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint8_in(number)
        GIMarshallingTests.uint8_in(CHAR_255)

        number.value += 1
        self.assertRaises(ValueError, GIMarshallingTests.uint8_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.uint8_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint8_in, "self.MAX")

    def test_uint8_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint8_out())

    def test_uint8_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint8_inout(Number(self.MAX)))


class TestInt16(unittest.TestCase):

    MAX = GObject.G_MAXINT16
    MIN = GObject.G_MININT16

    def test_int16_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int16_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int16_return_min())

    def test_int16_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.int16_in_max(max)
        GIMarshallingTests.int16_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.int16_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.int16_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int16_in_max, "self.MAX")

    def test_int16_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int16_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int16_out_min())

    def test_int16_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int16_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int16_inout_min_max(Number(self.MIN)))


class TestUInt16(unittest.TestCase):

    MAX = GObject.G_MAXUINT16

    def test_uint16_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint16_return())

    def test_uint16_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint16_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.uint16_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.uint16_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint16_in, "self.MAX")

    def test_uint16_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint16_out())

    def test_uint16_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint16_inout(Number(self.MAX)))


class TestInt32(unittest.TestCase):

    MAX = GObject.G_MAXINT32
    MIN = GObject.G_MININT32

    def test_int32_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int32_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int32_return_min())

    def test_int32_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.int32_in_max(max)
        GIMarshallingTests.int32_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.int32_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.int32_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int32_in_max, "self.MAX")

    def test_int32_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int32_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int32_out_min())

    def test_int32_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int32_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int32_inout_min_max(Number(self.MIN)))


class TestUInt32(unittest.TestCase):

    MAX = GObject.G_MAXUINT32

    def test_uint32_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint32_return())

    def test_uint32_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint32_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.uint32_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.uint32_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint32_in, "self.MAX")

    def test_uint32_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint32_out())

    def test_uint32_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint32_inout(Number(self.MAX)))


class TestInt64(unittest.TestCase):

    MAX = 2 ** 63 - 1
    MIN = - (2 ** 63)

    def test_int64_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int64_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int64_return_min())

    def test_int64_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.int64_in_max(max)
        GIMarshallingTests.int64_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.int64_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.int64_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int64_in_max, "self.MAX")

    def test_int64_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int64_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int64_out_min())

    def test_int64_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int64_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int64_inout_min_max(Number(self.MIN)))


class TestUInt64(unittest.TestCase):

    MAX = 2 ** 64 - 1

    def test_uint64_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint64_return())

    def test_uint64_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint64_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.uint64_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.uint64_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint64_in, "self.MAX")

    def test_uint64_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint64_out())

    def test_uint64_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint64_inout(Number(self.MAX)))


class TestShort(unittest.TestCase):

    MAX = GObject.constants.G_MAXSHORT
    MIN = GObject.constants.G_MINSHORT

    def test_short_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.short_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.short_return_min())

    def test_short_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.short_in_max(max)
        GIMarshallingTests.short_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.short_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.short_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.short_in_max, "self.MAX")

    def test_short_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.short_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.short_out_min())

    def test_short_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.short_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.short_inout_min_max(Number(self.MIN)))


class TestUShort(unittest.TestCase):

    MAX = GObject.constants.G_MAXUSHORT

    def test_ushort_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ushort_return())

    def test_ushort_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.ushort_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.ushort_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.ushort_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.ushort_in, "self.MAX")

    def test_ushort_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ushort_out())

    def test_ushort_inout(self):
        self.assertEqual(0, GIMarshallingTests.ushort_inout(Number(self.MAX)))


class TestInt(unittest.TestCase):

    MAX = GObject.constants.G_MAXINT
    MIN = GObject.constants.G_MININT

    def test_int_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int_return_min())

    def test_int_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.int_in_max(max)
        GIMarshallingTests.int_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.int_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.int_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.int_in_max, "self.MAX")

    def test_int_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.int_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.int_out_min())

    def test_int_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.int_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.int_inout_min_max(Number(self.MIN)))
        self.assertRaises(TypeError, GIMarshallingTests.int_inout_min_max, Number(self.MIN), CONSTANT_NUMBER)


class TestUInt(unittest.TestCase):

    MAX = GObject.constants.G_MAXUINT

    def test_uint_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint_return())

    def test_uint_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.uint_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.uint_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.uint_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.uint_in, "self.MAX")

    def test_uint_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.uint_out())

    def test_uint_inout(self):
        self.assertEqual(0, GIMarshallingTests.uint_inout(Number(self.MAX)))


class TestLong(unittest.TestCase):

    MAX = GObject.constants.G_MAXLONG
    MIN = GObject.constants.G_MINLONG

    def test_long_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.long_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.long_return_min())

    def test_long_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.long_in_max(max)
        GIMarshallingTests.long_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.long_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.long_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.long_in_max, "self.MAX")

    def test_long_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.long_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.long_out_min())

    def test_long_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.long_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.long_inout_min_max(Number(self.MIN)))


class TestULong(unittest.TestCase):

    MAX = GObject.constants.G_MAXULONG

    def test_ulong_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ulong_return())

    def test_ulong_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.ulong_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.ulong_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.ulong_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.ulong_in, "self.MAX")

    def test_ulong_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ulong_out())

    def test_ulong_inout(self):
        self.assertEqual(0, GIMarshallingTests.ulong_inout(Number(self.MAX)))


class TestSSize(unittest.TestCase):

    MAX = GObject.constants.G_MAXLONG
    MIN = GObject.constants.G_MINLONG

    def test_ssize_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ssize_return_max())
        self.assertEqual(self.MIN, GIMarshallingTests.ssize_return_min())

    def test_ssize_in(self):
        max = Number(self.MAX)
        min = Number(self.MIN)

        GIMarshallingTests.ssize_in_max(max)
        GIMarshallingTests.ssize_in_min(min)

        max.value += 1
        min.value -= 1

        self.assertRaises(ValueError, GIMarshallingTests.ssize_in_max, max)
        self.assertRaises(ValueError, GIMarshallingTests.ssize_in_min, min)

        self.assertRaises(TypeError, GIMarshallingTests.ssize_in_max, "self.MAX")

    def test_ssize_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.ssize_out_max())
        self.assertEqual(self.MIN, GIMarshallingTests.ssize_out_min())

    def test_ssize_inout(self):
        self.assertEqual(self.MIN, GIMarshallingTests.ssize_inout_max_min(Number(self.MAX)))
        self.assertEqual(self.MAX, GIMarshallingTests.ssize_inout_min_max(Number(self.MIN)))


class TestSize(unittest.TestCase):

    MAX = GObject.constants.G_MAXULONG

    def test_size_return(self):
        self.assertEqual(self.MAX, GIMarshallingTests.size_return())

    def test_size_in(self):
        number = Number(self.MAX)

        GIMarshallingTests.size_in(number)

        number.value += 1

        self.assertRaises(ValueError, GIMarshallingTests.size_in, number)
        self.assertRaises(ValueError, GIMarshallingTests.size_in, Number(-1))

        self.assertRaises(TypeError, GIMarshallingTests.size_in, "self.MAX")

    def test_size_out(self):
        self.assertEqual(self.MAX, GIMarshallingTests.size_out())

    def test_size_inout(self):
        self.assertEqual(0, GIMarshallingTests.size_inout(Number(self.MAX)))


class TestFloat(unittest.TestCase):

    MAX = GObject.constants.G_MAXFLOAT
    MIN = GObject.constants.G_MINFLOAT

    def test_float_return(self):
        self.assertAlmostEqual(self.MAX, GIMarshallingTests.float_return())

    def test_float_in(self):
        GIMarshallingTests.float_in(Number(self.MAX))

        self.assertRaises(TypeError, GIMarshallingTests.float_in, "self.MAX")

    def test_float_out(self):
        self.assertAlmostEqual(self.MAX, GIMarshallingTests.float_out())

    def test_float_inout(self):
        self.assertAlmostEqual(self.MIN, GIMarshallingTests.float_inout(Number(self.MAX)))


class TestDouble(unittest.TestCase):

    MAX = GObject.constants.G_MAXDOUBLE
    MIN = GObject.constants.G_MINDOUBLE

    def test_double_return(self):
        self.assertAlmostEqual(self.MAX, GIMarshallingTests.double_return())

    def test_double_in(self):
        GIMarshallingTests.double_in(Number(self.MAX))

        self.assertRaises(TypeError, GIMarshallingTests.double_in, "self.MAX")

    def test_double_out(self):
        self.assertAlmostEqual(self.MAX, GIMarshallingTests.double_out())

    def test_double_inout(self):
        self.assertAlmostEqual(self.MIN, GIMarshallingTests.double_inout(Number(self.MAX)))


class TestGType(unittest.TestCase):

    def test_gtype_name(self):
        self.assertEqual("void", GObject.TYPE_NONE.name)
        self.assertEqual("gchararray", GObject.TYPE_STRING.name)

        def check_readonly(gtype):
            gtype.name = "foo"

        self.assertRaises(AttributeError, check_readonly, GObject.TYPE_NONE)
        self.assertRaises(AttributeError, check_readonly, GObject.TYPE_STRING)

    def test_gtype_return(self):
        self.assertEqual(GObject.TYPE_NONE, GIMarshallingTests.gtype_return())
        self.assertEqual(GObject.TYPE_STRING, GIMarshallingTests.gtype_string_return())

    def test_gtype_in(self):
        GIMarshallingTests.gtype_in(GObject.TYPE_NONE)
        GIMarshallingTests.gtype_string_in(GObject.TYPE_STRING)
        self.assertRaises(TypeError, GIMarshallingTests.gtype_in, "foo")
        self.assertRaises(TypeError, GIMarshallingTests.gtype_string_in, "foo")

    def test_gtype_out(self):
        self.assertEqual(GObject.TYPE_NONE, GIMarshallingTests.gtype_out())
        self.assertEqual(GObject.TYPE_STRING, GIMarshallingTests.gtype_string_out())

    def test_gtype_inout(self):
        self.assertEqual(GObject.TYPE_INT, GIMarshallingTests.gtype_inout(GObject.TYPE_NONE))


class TestUtf8(unittest.TestCase):

    def test_utf8_none_return(self):
        self.assertEqual(CONSTANT_UTF8, GIMarshallingTests.utf8_none_return())

    def test_utf8_full_return(self):
        self.assertEqual(CONSTANT_UTF8, GIMarshallingTests.utf8_full_return())

    def test_utf8_none_in(self):
        GIMarshallingTests.utf8_none_in(CONSTANT_UTF8)
        if sys.version_info < (3, 0):
            GIMarshallingTests.utf8_none_in(PY2_UNICODE_UTF8)

        self.assertRaises(TypeError, GIMarshallingTests.utf8_none_in, CONSTANT_NUMBER)
        self.assertRaises(TypeError, GIMarshallingTests.utf8_none_in, None)

    def test_utf8_none_out(self):
        self.assertEqual(CONSTANT_UTF8, GIMarshallingTests.utf8_none_out())

    def test_utf8_full_out(self):
        self.assertEqual(CONSTANT_UTF8, GIMarshallingTests.utf8_full_out())

    def test_utf8_dangling_out(self):
        GIMarshallingTests.utf8_dangling_out()

    def test_utf8_none_inout(self):
        self.assertEqual("", GIMarshallingTests.utf8_none_inout(CONSTANT_UTF8))

    def test_utf8_full_inout(self):
        self.assertEqual("", GIMarshallingTests.utf8_full_inout(CONSTANT_UTF8))


class TestArray(unittest.TestCase):

    def test_array_fixed_int_return(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_fixed_int_return())

    def test_array_fixed_short_return(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_fixed_short_return())

    def test_array_fixed_int_in(self):
        GIMarshallingTests.array_fixed_int_in(Sequence([-1, 0, 1, 2]))

        self.assertRaises(TypeError, GIMarshallingTests.array_fixed_int_in, Sequence([-1, '0', 1, 2]))

        self.assertRaises(TypeError, GIMarshallingTests.array_fixed_int_in, 42)
        self.assertRaises(TypeError, GIMarshallingTests.array_fixed_int_in, None)

    def test_array_fixed_short_in(self):
        GIMarshallingTests.array_fixed_short_in(Sequence([-1, 0, 1, 2]))

    def test_array_fixed_out(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_fixed_out())

    def test_array_fixed_inout(self):
        self.assertEqual([2, 1, 0, -1], GIMarshallingTests.array_fixed_inout([-1, 0, 1, 2]))

    def test_array_return(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_return())

    def test_array_in(self):
        GIMarshallingTests.array_in(Sequence([-1, 0, 1, 2]))

    def test_array_in_len_zero_terminated(self):
        GIMarshallingTests.array_in_len_zero_terminated(Sequence([-1, 0, 1, 2]))

    def test_array_uint8_in(self):
        GIMarshallingTests.array_uint8_in(Sequence([97, 98, 99, 100]))
        GIMarshallingTests.array_uint8_in(_bytes("abcd"))

    def test_array_out(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.array_out())

    def test_array_inout(self):
        self.assertEqual([-2, -1, 0, 1, 2], GIMarshallingTests.array_inout(Sequence([-1, 0, 1, 2])))

    def test_method_array_in(self):
        object_ = GIMarshallingTests.Object()
        object_.method_array_in(Sequence([-1, 0, 1, 2]))

    def test_method_array_out(self):
        object_ = GIMarshallingTests.Object()
        self.assertEqual([-1, 0, 1, 2], object_.method_array_out())

    def test_method_array_inout(self):
        object_ = GIMarshallingTests.Object()
        self.assertEqual([-2, -1, 0, 1, 2], object_.method_array_inout(Sequence([-1, 0, 1, 2])))

    def test_method_array_return(self):
        object_ = GIMarshallingTests.Object()
        self.assertEqual([-1, 0, 1, 2], object_.method_array_return())

    def test_array_enum_in(self):
        GIMarshallingTests.array_enum_in([GIMarshallingTests.Enum.VALUE1,
                                          GIMarshallingTests.Enum.VALUE2,
                                          GIMarshallingTests.Enum.VALUE3])

    def test_array_boxed_struct_in(self):
        struct1 = GIMarshallingTests.BoxedStruct()
        struct1.long_ = 1
        struct2 = GIMarshallingTests.BoxedStruct()
        struct2.long_ = 2
        struct3 = GIMarshallingTests.BoxedStruct()
        struct3.long_ = 3

        GIMarshallingTests.array_struct_in([struct1, struct2, struct3])

    def test_array_simple_struct_in(self):
        struct1 = GIMarshallingTests.SimpleStruct()
        struct1.long_ = 1
        struct2 = GIMarshallingTests.SimpleStruct()
        struct2.long_ = 2
        struct3 = GIMarshallingTests.SimpleStruct()
        struct3.long_ = 3

        GIMarshallingTests.array_simple_struct_in([struct1, struct2, struct3])

    def test_array_multi_array_key_value_in(self):
        GIMarshallingTests.multi_array_key_value_in(["one", "two", "three"],
                                                    [1, 2, 3])

    def test_array_in_nonzero_nonlen(self):
        GIMarshallingTests.array_in_nonzero_nonlen(1, b'abcd')

    def test_array_fixed_out_struct(self):
        struct1, struct2 = GIMarshallingTests.array_fixed_out_struct()

        self.assertEqual(7, struct1.long_)
        self.assertEqual(6, struct1.int8)
        self.assertEqual(6, struct2.long_)
        self.assertEqual(7, struct2.int8)

    def test_array_zero_terminated_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.array_zero_terminated_return())

    def test_array_zero_terminated_return_null(self):
        self.assertEqual([], GIMarshallingTests.array_zero_terminated_return_null())

    def test_array_zero_terminated_in(self):
        GIMarshallingTests.array_zero_terminated_in(Sequence(['0', '1', '2']))

    def test_array_zero_terminated_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.array_zero_terminated_out())

    def test_array_zero_terminated_inout(self):
        self.assertEqual(['-1', '0', '1', '2'], GIMarshallingTests.array_zero_terminated_inout(['0', '1', '2']))


class TestGStrv(unittest.TestCase):

    def test_gstrv_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gstrv_return())

    def test_gstrv_in(self):
        GIMarshallingTests.gstrv_in(Sequence(['0', '1', '2']))

    def test_gstrv_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gstrv_out())

    def test_gstrv_inout(self):
        self.assertEqual(['-1', '0', '1', '2'], GIMarshallingTests.gstrv_inout(['0', '1', '2']))


class TestArrayGVariant(unittest.TestCase):

    def test_array_gvariant_none_in(self):
        v = [GLib.Variant("i", 27), GLib.Variant("s", "Hello")]
        returned = [GLib.Variant.unpack(r) for r in GIMarshallingTests.array_gvariant_none_in(v)]
        self.assertEqual([27, "Hello"], returned)

    def test_array_gvariant_container_in(self):
        v = [GLib.Variant("i", 27), GLib.Variant("s", "Hello")]
        returned = [GLib.Variant.unpack(r) for r in GIMarshallingTests.array_gvariant_container_in(v)]
        self.assertEqual([27, "Hello"], returned)

    def test_array_gvariant_full_in(self):
        v = [GLib.Variant("i", 27), GLib.Variant("s", "Hello")]
        returned = [GLib.Variant.unpack(r) for r in GIMarshallingTests.array_gvariant_full_in(v)]
        self.assertEqual([27, "Hello"], returned)

    def test_bytearray_gvariant(self):
        v = GLib.Variant.new_bytestring(b"foo")
        self.assertEqual(v.get_bytestring(), b"foo")


class TestGArray(unittest.TestCase):

    def test_garray_int_none_return(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.garray_int_none_return())

    def test_garray_utf8_none_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.garray_utf8_none_return())

    def test_garray_utf8_container_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.garray_utf8_container_return())

    def test_garray_utf8_full_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.garray_utf8_full_return())

    def test_garray_int_none_in(self):
        GIMarshallingTests.garray_int_none_in(Sequence([-1, 0, 1, 2]))

        self.assertRaises(TypeError, GIMarshallingTests.garray_int_none_in, Sequence([-1, '0', 1, 2]))

        self.assertRaises(TypeError, GIMarshallingTests.garray_int_none_in, 42)
        self.assertRaises(TypeError, GIMarshallingTests.garray_int_none_in, None)

    def test_garray_utf8_none_in(self):
        GIMarshallingTests.garray_utf8_none_in(Sequence(['0', '1', '2']))

    def test_garray_utf8_none_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.garray_utf8_none_out())

    def test_garray_utf8_container_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.garray_utf8_container_out())

    def test_garray_utf8_full_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.garray_utf8_full_out())

    def test_garray_utf8_none_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.garray_utf8_none_inout(Sequence(('0', '1', '2'))))

    def test_garray_utf8_container_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.garray_utf8_container_inout(['0', '1', '2']))

    def test_garray_utf8_full_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.garray_utf8_full_inout(['0', '1', '2']))


class TestGPtrArray(unittest.TestCase):

    def test_gptrarray_utf8_none_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gptrarray_utf8_none_return())

    def test_gptrarray_utf8_container_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gptrarray_utf8_container_return())

    def test_gptrarray_utf8_full_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gptrarray_utf8_full_return())

    def test_gptrarray_utf8_none_in(self):
        GIMarshallingTests.gptrarray_utf8_none_in(Sequence(['0', '1', '2']))

    def test_gptrarray_utf8_none_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gptrarray_utf8_none_out())

    def test_gptrarray_utf8_container_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gptrarray_utf8_container_out())

    def test_gptrarray_utf8_full_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gptrarray_utf8_full_out())

    def test_gptrarray_utf8_none_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.gptrarray_utf8_none_inout(Sequence(('0', '1', '2'))))

    def test_gptrarray_utf8_container_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.gptrarray_utf8_container_inout(['0', '1', '2']))

    def test_gptrarray_utf8_full_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.gptrarray_utf8_full_inout(['0', '1', '2']))


class TestGList(unittest.TestCase):

    def test_glist_int_none_return(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.glist_int_none_return())

    def test_glist_utf8_none_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.glist_utf8_none_return())

    def test_glist_utf8_container_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.glist_utf8_container_return())

    def test_glist_utf8_full_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.glist_utf8_full_return())

    def test_glist_int_none_in(self):
        GIMarshallingTests.glist_int_none_in(Sequence((-1, 0, 1, 2)))

        self.assertRaises(TypeError, GIMarshallingTests.glist_int_none_in, Sequence((-1, '0', 1, 2)))

        self.assertRaises(TypeError, GIMarshallingTests.glist_int_none_in, 42)
        self.assertRaises(TypeError, GIMarshallingTests.glist_int_none_in, None)

    def test_glist_utf8_none_in(self):
        GIMarshallingTests.glist_utf8_none_in(Sequence(('0', '1', '2')))

    def test_glist_utf8_none_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.glist_utf8_none_out())

    def test_glist_utf8_container_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.glist_utf8_container_out())

    def test_glist_utf8_full_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.glist_utf8_full_out())

    def test_glist_utf8_none_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.glist_utf8_none_inout(Sequence(('0', '1', '2'))))

    def test_glist_utf8_container_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.glist_utf8_container_inout(('0', '1', '2')))

    def test_glist_utf8_full_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.glist_utf8_full_inout(('0', '1', '2')))


class TestGSList(unittest.TestCase):

    def test_gslist_int_none_return(self):
        self.assertEqual([-1, 0, 1, 2], GIMarshallingTests.gslist_int_none_return())

    def test_gslist_utf8_none_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gslist_utf8_none_return())

    def test_gslist_utf8_container_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gslist_utf8_container_return())

    def test_gslist_utf8_full_return(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gslist_utf8_full_return())

    def test_gslist_int_none_in(self):
        GIMarshallingTests.gslist_int_none_in(Sequence((-1, 0, 1, 2)))

        self.assertRaises(TypeError, GIMarshallingTests.gslist_int_none_in, Sequence((-1, '0', 1, 2)))

        self.assertRaises(TypeError, GIMarshallingTests.gslist_int_none_in, 42)
        self.assertRaises(TypeError, GIMarshallingTests.gslist_int_none_in, None)

    def test_gslist_utf8_none_in(self):
        GIMarshallingTests.gslist_utf8_none_in(Sequence(('0', '1', '2')))

    def test_gslist_utf8_none_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gslist_utf8_none_out())

    def test_gslist_utf8_container_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gslist_utf8_container_out())

    def test_gslist_utf8_full_out(self):
        self.assertEqual(['0', '1', '2'], GIMarshallingTests.gslist_utf8_full_out())

    def test_gslist_utf8_none_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.gslist_utf8_none_inout(Sequence(('0', '1', '2'))))

    def test_gslist_utf8_container_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.gslist_utf8_container_inout(('0', '1', '2')))

    def test_gslist_utf8_full_inout(self):
        self.assertEqual(['-2', '-1', '0', '1'], GIMarshallingTests.gslist_utf8_full_inout(('0', '1', '2')))


class TestGHashTable(unittest.TestCase):

    def test_ghashtable_int_none_return(self):
        self.assertEqual({-1: 1, 0: 0, 1: -1, 2: -2}, GIMarshallingTests.ghashtable_int_none_return())

    def test_ghashtable_int_none_return2(self):
        self.assertEqual({'-1': '1', '0': '0', '1': '-1', '2': '-2'}, GIMarshallingTests.ghashtable_utf8_none_return())

    def test_ghashtable_int_container_return(self):
        self.assertEqual({'-1': '1', '0': '0', '1': '-1', '2': '-2'}, GIMarshallingTests.ghashtable_utf8_container_return())

    def test_ghashtable_int_full_return(self):
        self.assertEqual({'-1': '1', '0': '0', '1': '-1', '2': '-2'}, GIMarshallingTests.ghashtable_utf8_full_return())

    def test_ghashtable_int_none_in(self):
        GIMarshallingTests.ghashtable_int_none_in({-1: 1, 0: 0, 1: -1, 2: -2})

        self.assertRaises(TypeError, GIMarshallingTests.ghashtable_int_none_in, {-1: 1, '0': 0, 1: -1, 2: -2})
        self.assertRaises(TypeError, GIMarshallingTests.ghashtable_int_none_in, {-1: 1, 0: '0', 1: -1, 2: -2})

        self.assertRaises(TypeError, GIMarshallingTests.ghashtable_int_none_in, '{-1: 1, 0: 0, 1: -1, 2: -2}')
        self.assertRaises(TypeError, GIMarshallingTests.ghashtable_int_none_in, None)

    def test_ghashtable_utf8_none_in(self):
        GIMarshallingTests.ghashtable_utf8_none_in({'-1': '1', '0': '0', '1': '-1', '2': '-2'})

    def test_ghashtable_utf8_none_out(self):
        self.assertEqual({'-1': '1', '0': '0', '1': '-1', '2': '-2'}, GIMarshallingTests.ghashtable_utf8_none_out())

    def test_ghashtable_utf8_container_out(self):
        self.assertEqual({'-1': '1', '0': '0', '1': '-1', '2': '-2'}, GIMarshallingTests.ghashtable_utf8_container_out())

    def test_ghashtable_utf8_full_out(self):
        self.assertEqual({'-1': '1', '0': '0', '1': '-1', '2': '-2'}, GIMarshallingTests.ghashtable_utf8_full_out())

    def test_ghashtable_utf8_none_inout(self):
        i = {'-1': '1', '0': '0', '1': '-1', '2': '-2'}
        self.assertEqual({'-1': '1', '0': '0', '1': '1'},
                         GIMarshallingTests.ghashtable_utf8_none_inout(i))

    def test_ghashtable_utf8_container_inout(self):
        i = {'-1': '1', '0': '0', '1': '-1', '2': '-2'}
        self.assertEqual({'-1': '1', '0': '0', '1': '1'},
                         GIMarshallingTests.ghashtable_utf8_container_inout(i))

    def test_ghashtable_utf8_full_inout(self):
        i = {'-1': '1', '0': '0', '1': '-1', '2': '-2'}
        self.assertEqual({'-1': '1', '0': '0', '1': '1'},
                         GIMarshallingTests.ghashtable_utf8_full_inout(i))


class TestGValue(unittest.TestCase):

    def test_gvalue_return(self):
        self.assertEqual(42, GIMarshallingTests.gvalue_return())

    def test_gvalue_in(self):
        GIMarshallingTests.gvalue_in(42)
        value = GObject.Value()
        value.init(GObject.TYPE_INT)
        value.set_int(42)
        GIMarshallingTests.gvalue_in(value)

    def test_gvalue_out(self):
        self.assertEqual(42, GIMarshallingTests.gvalue_out())

    def test_gvalue_out_caller_allocates(self):
        self.assertEqual(42, GIMarshallingTests.gvalue_out_caller_allocates())

    def test_gvalue_inout(self):
        self.assertEqual('42', GIMarshallingTests.gvalue_inout(42))
        value = GObject.Value()
        value.init(GObject.TYPE_INT)
        value.set_int(42)
        self.assertEqual('42', GIMarshallingTests.gvalue_inout(value))

    def test_gvalue_flat_array_in(self):
        # the function already asserts the correct values
        GIMarshallingTests.gvalue_flat_array([42, "42", True])

    def test_gvalue_flat_array_out(self):
        values = GIMarshallingTests.return_gvalue_flat_array()
        self.assertEqual(values, [42, '42', True])


class TestGClosure(unittest.TestCase):

    def test_gclosure_in(self):
        GIMarshallingTests.gclosure_in(lambda: 42)

        # test passing a closure between two C calls
        closure = GIMarshallingTests.gclosure_return()
        GIMarshallingTests.gclosure_in(closure)

        self.assertRaises(TypeError, GIMarshallingTests.gclosure_in, 42)
        self.assertRaises(TypeError, GIMarshallingTests.gclosure_in, None)


class TestPointer(unittest.TestCase):
    def test_pointer_in_return(self):
        self.assertEqual(GIMarshallingTests.pointer_in_return(42), 42)


class TestEnum(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''Run tests under a test locale.

        Upper case conversion of member names should not be locale specific
        e.  g. in Turkish, "i".upper() == "i", which gives results like "iNVALiD"

        Run test under a locale which defines toupper('a') == 'a'
        '''
        cls.locale_dir = tempfile.mkdtemp()
        src = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'te_ST@nouppera')
        dest = os.path.join(cls.locale_dir, 'te_ST.UTF-8@nouppera')
        subprocess.check_call(['localedef', '-i', src, '-c', '-f', 'UTF-8', dest])
        os.environ['LOCPATH'] = cls.locale_dir
        locale.setlocale(locale.LC_ALL, 'te_ST.UTF-8@nouppera')

    @classmethod
    def tearDownClass(cls):
        locale.setlocale(locale.LC_ALL, 'C')
        shutil.rmtree(cls.locale_dir)
        try:
            del os.environ['LOCPATH']
        except KeyError:
            pass

    def test_enum(self):
        self.assertTrue(issubclass(GIMarshallingTests.Enum, int))
        self.assertTrue(isinstance(GIMarshallingTests.Enum.VALUE1, GIMarshallingTests.Enum))
        self.assertTrue(isinstance(GIMarshallingTests.Enum.VALUE2, GIMarshallingTests.Enum))
        self.assertTrue(isinstance(GIMarshallingTests.Enum.VALUE3, GIMarshallingTests.Enum))
        self.assertEqual(42, GIMarshallingTests.Enum.VALUE3)

    def test_value_nick_and_name(self):
        self.assertEqual(GIMarshallingTests.Enum.VALUE1.value_nick, 'value1')
        self.assertEqual(GIMarshallingTests.Enum.VALUE2.value_nick, 'value2')
        self.assertEqual(GIMarshallingTests.Enum.VALUE3.value_nick, 'value3')

        self.assertEqual(GIMarshallingTests.Enum.VALUE1.value_name, 'GI_MARSHALLING_TESTS_ENUM_VALUE1')
        self.assertEqual(GIMarshallingTests.Enum.VALUE2.value_name, 'GI_MARSHALLING_TESTS_ENUM_VALUE2')
        self.assertEqual(GIMarshallingTests.Enum.VALUE3.value_name, 'GI_MARSHALLING_TESTS_ENUM_VALUE3')

    def test_enum_in(self):
        GIMarshallingTests.enum_in(GIMarshallingTests.Enum.VALUE3)
        GIMarshallingTests.enum_in(42)

        self.assertRaises(TypeError, GIMarshallingTests.enum_in, 43)
        self.assertRaises(TypeError, GIMarshallingTests.enum_in, 'GIMarshallingTests.Enum.VALUE3')

    def test_enum_out(self):
        enum = GIMarshallingTests.enum_out()
        self.assertTrue(isinstance(enum, GIMarshallingTests.Enum))
        self.assertEqual(enum, GIMarshallingTests.Enum.VALUE3)

    def test_enum_inout(self):
        enum = GIMarshallingTests.enum_inout(GIMarshallingTests.Enum.VALUE3)
        self.assertTrue(isinstance(enum, GIMarshallingTests.Enum))
        self.assertEqual(enum, GIMarshallingTests.Enum.VALUE1)

    def test_enum_second(self):
        # check for the bug where different non-gtype enums share the same class
        self.assertNotEqual(GIMarshallingTests.Enum, GIMarshallingTests.SecondEnum)

        # check that values are not being shared between different enums
        self.assertTrue(hasattr(GIMarshallingTests.SecondEnum, "SECONDVALUE1"))
        self.assertRaises(AttributeError, getattr, GIMarshallingTests.Enum, "SECONDVALUE1")
        self.assertTrue(hasattr(GIMarshallingTests.Enum, "VALUE1"))
        self.assertRaises(AttributeError, getattr, GIMarshallingTests.SecondEnum, "VALUE1")


class TestGEnum(unittest.TestCase):

    def test_genum(self):
        self.assertTrue(issubclass(GIMarshallingTests.GEnum, GObject.GEnum))
        self.assertTrue(isinstance(GIMarshallingTests.GEnum.VALUE1, GIMarshallingTests.GEnum))
        self.assertTrue(isinstance(GIMarshallingTests.GEnum.VALUE2, GIMarshallingTests.GEnum))
        self.assertTrue(isinstance(GIMarshallingTests.GEnum.VALUE3, GIMarshallingTests.GEnum))
        self.assertEqual(42, GIMarshallingTests.GEnum.VALUE3)

    def test_value_nick_and_name(self):
        self.assertEqual(GIMarshallingTests.GEnum.VALUE1.value_nick, 'value1')
        self.assertEqual(GIMarshallingTests.GEnum.VALUE2.value_nick, 'value2')
        self.assertEqual(GIMarshallingTests.GEnum.VALUE3.value_nick, 'value3')

        self.assertEqual(GIMarshallingTests.GEnum.VALUE1.value_name, 'GI_MARSHALLING_TESTS_GENUM_VALUE1')
        self.assertEqual(GIMarshallingTests.GEnum.VALUE2.value_name, 'GI_MARSHALLING_TESTS_GENUM_VALUE2')
        self.assertEqual(GIMarshallingTests.GEnum.VALUE3.value_name, 'GI_MARSHALLING_TESTS_GENUM_VALUE3')

    def test_genum_in(self):
        GIMarshallingTests.genum_in(GIMarshallingTests.GEnum.VALUE3)
        GIMarshallingTests.genum_in(42)

        self.assertRaises(TypeError, GIMarshallingTests.genum_in, 43)
        self.assertRaises(TypeError, GIMarshallingTests.genum_in, 'GIMarshallingTests.GEnum.VALUE3')

    def test_genum_out(self):
        genum = GIMarshallingTests.genum_out()
        self.assertTrue(isinstance(genum, GIMarshallingTests.GEnum))
        self.assertEqual(genum, GIMarshallingTests.GEnum.VALUE3)

    def test_genum_inout(self):
        genum = GIMarshallingTests.genum_inout(GIMarshallingTests.GEnum.VALUE3)
        self.assertTrue(isinstance(genum, GIMarshallingTests.GEnum))
        self.assertEqual(genum, GIMarshallingTests.GEnum.VALUE1)


class TestGFlags(unittest.TestCase):

    def test_flags(self):
        self.assertTrue(issubclass(GIMarshallingTests.Flags, GObject.GFlags))
        self.assertTrue(isinstance(GIMarshallingTests.Flags.VALUE1, GIMarshallingTests.Flags))
        self.assertTrue(isinstance(GIMarshallingTests.Flags.VALUE2, GIMarshallingTests.Flags))
        self.assertTrue(isinstance(GIMarshallingTests.Flags.VALUE3, GIMarshallingTests.Flags))
        # __or__() operation should still return an instance, not an int.
        self.assertTrue(isinstance(GIMarshallingTests.Flags.VALUE1 | GIMarshallingTests.Flags.VALUE2,
                                   GIMarshallingTests.Flags))
        self.assertEqual(1 << 1, GIMarshallingTests.Flags.VALUE2)

    def test_value_nick_and_name(self):
        self.assertEqual(GIMarshallingTests.Flags.VALUE1.first_value_nick, 'value1')
        self.assertEqual(GIMarshallingTests.Flags.VALUE2.first_value_nick, 'value2')
        self.assertEqual(GIMarshallingTests.Flags.VALUE3.first_value_nick, 'value3')

        self.assertEqual(GIMarshallingTests.Flags.VALUE1.first_value_name, 'GI_MARSHALLING_TESTS_FLAGS_VALUE1')
        self.assertEqual(GIMarshallingTests.Flags.VALUE2.first_value_name, 'GI_MARSHALLING_TESTS_FLAGS_VALUE2')
        self.assertEqual(GIMarshallingTests.Flags.VALUE3.first_value_name, 'GI_MARSHALLING_TESTS_FLAGS_VALUE3')

    def test_flags_in(self):
        GIMarshallingTests.flags_in(GIMarshallingTests.Flags.VALUE2)
        # result of __or__() operation should still be valid instance, not an int.
        GIMarshallingTests.flags_in(GIMarshallingTests.Flags.VALUE2 | GIMarshallingTests.Flags.VALUE2)
        GIMarshallingTests.flags_in_zero(Number(0))

        self.assertRaises(TypeError, GIMarshallingTests.flags_in, 1 << 1)
        self.assertRaises(TypeError, GIMarshallingTests.flags_in, 'GIMarshallingTests.Flags.VALUE2')

    def test_flags_out(self):
        flags = GIMarshallingTests.flags_out()
        self.assertTrue(isinstance(flags, GIMarshallingTests.Flags))
        self.assertEqual(flags, GIMarshallingTests.Flags.VALUE2)

    def test_flags_inout(self):
        flags = GIMarshallingTests.flags_inout(GIMarshallingTests.Flags.VALUE2)
        self.assertTrue(isinstance(flags, GIMarshallingTests.Flags))
        self.assertEqual(flags, GIMarshallingTests.Flags.VALUE1)


class TestNoTypeFlags(unittest.TestCase):

    def test_flags(self):
        self.assertTrue(issubclass(GIMarshallingTests.NoTypeFlags, GObject.GFlags))
        self.assertTrue(isinstance(GIMarshallingTests.NoTypeFlags.VALUE1, GIMarshallingTests.NoTypeFlags))
        self.assertTrue(isinstance(GIMarshallingTests.NoTypeFlags.VALUE2, GIMarshallingTests.NoTypeFlags))
        self.assertTrue(isinstance(GIMarshallingTests.NoTypeFlags.VALUE3, GIMarshallingTests.NoTypeFlags))
        # __or__() operation should still return an instance, not an int.
        self.assertTrue(isinstance(GIMarshallingTests.NoTypeFlags.VALUE1 | GIMarshallingTests.NoTypeFlags.VALUE2,
                                   GIMarshallingTests.NoTypeFlags))
        self.assertEqual(1 << 1, GIMarshallingTests.NoTypeFlags.VALUE2)

    def test_value_nick_and_name(self):
        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE1.first_value_nick, 'value1')
        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE2.first_value_nick, 'value2')
        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE3.first_value_nick, 'value3')

        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE1.first_value_name, 'GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE1')
        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE2.first_value_name, 'GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE2')
        self.assertEqual(GIMarshallingTests.NoTypeFlags.VALUE3.first_value_name, 'GI_MARSHALLING_TESTS_NO_TYPE_FLAGS_VALUE3')

    def test_flags_in(self):
        GIMarshallingTests.no_type_flags_in(GIMarshallingTests.NoTypeFlags.VALUE2)
        GIMarshallingTests.no_type_flags_in(GIMarshallingTests.NoTypeFlags.VALUE2 | GIMarshallingTests.NoTypeFlags.VALUE2)
        GIMarshallingTests.no_type_flags_in_zero(Number(0))

        self.assertRaises(TypeError, GIMarshallingTests.no_type_flags_in, 1 << 1)
        self.assertRaises(TypeError, GIMarshallingTests.no_type_flags_in, 'GIMarshallingTests.NoTypeFlags.VALUE2')

    def test_flags_out(self):
        flags = GIMarshallingTests.no_type_flags_out()
        self.assertTrue(isinstance(flags, GIMarshallingTests.NoTypeFlags))
        self.assertEqual(flags, GIMarshallingTests.NoTypeFlags.VALUE2)

    def test_flags_inout(self):
        flags = GIMarshallingTests.no_type_flags_inout(GIMarshallingTests.NoTypeFlags.VALUE2)
        self.assertTrue(isinstance(flags, GIMarshallingTests.NoTypeFlags))
        self.assertEqual(flags, GIMarshallingTests.NoTypeFlags.VALUE1)


class TestStructure(unittest.TestCase):

    def test_simple_struct(self):
        self.assertTrue(issubclass(GIMarshallingTests.SimpleStruct, GObject.GPointer))

        struct = GIMarshallingTests.SimpleStruct()
        self.assertTrue(isinstance(struct, GIMarshallingTests.SimpleStruct))

        self.assertEqual(0, struct.long_)
        self.assertEqual(0, struct.int8)

        struct.long_ = 6
        struct.int8 = 7

        self.assertEqual(6, struct.long_)
        self.assertEqual(7, struct.int8)

        del struct

    def test_nested_struct(self):
        struct = GIMarshallingTests.NestedStruct()

        self.assertTrue(isinstance(struct.simple_struct, GIMarshallingTests.SimpleStruct))

        struct.simple_struct.long_ = 42
        self.assertEqual(42, struct.simple_struct.long_)

        del struct

    def test_not_simple_struct(self):
        struct = GIMarshallingTests.NotSimpleStruct()
        self.assertEqual(None, struct.pointer)

    def test_simple_struct_return(self):
        struct = GIMarshallingTests.simple_struct_returnv()

        self.assertTrue(isinstance(struct, GIMarshallingTests.SimpleStruct))
        self.assertEqual(6, struct.long_)
        self.assertEqual(7, struct.int8)

        del struct

    def test_simple_struct_in(self):
        struct = GIMarshallingTests.SimpleStruct()
        struct.long_ = 6
        struct.int8 = 7

        GIMarshallingTests.SimpleStruct.inv(struct)

        del struct

        struct = GIMarshallingTests.NestedStruct()

        self.assertRaises(TypeError, GIMarshallingTests.SimpleStruct.inv, struct)

        del struct

        self.assertRaises(TypeError, GIMarshallingTests.SimpleStruct.inv, None)

    def test_simple_struct_method(self):
        struct = GIMarshallingTests.SimpleStruct()
        struct.long_ = 6
        struct.int8 = 7

        struct.method()

        del struct

        self.assertRaises(TypeError, GIMarshallingTests.SimpleStruct.method)

    def test_pointer_struct(self):
        self.assertTrue(issubclass(GIMarshallingTests.PointerStruct, GObject.GPointer))

        struct = GIMarshallingTests.PointerStruct()
        self.assertTrue(isinstance(struct, GIMarshallingTests.PointerStruct))

        del struct

    def test_pointer_struct_return(self):
        struct = GIMarshallingTests.pointer_struct_returnv()

        self.assertTrue(isinstance(struct, GIMarshallingTests.PointerStruct))
        self.assertEqual(42, struct.long_)

        del struct

    def test_pointer_struct_in(self):
        struct = GIMarshallingTests.PointerStruct()
        struct.long_ = 42

        struct.inv()

        del struct

    def test_boxed_struct(self):
        self.assertTrue(issubclass(GIMarshallingTests.BoxedStruct, GObject.GBoxed))

        struct = GIMarshallingTests.BoxedStruct()
        self.assertTrue(isinstance(struct, GIMarshallingTests.BoxedStruct))

        self.assertEqual(0, struct.long_)
        self.assertEqual([], struct.g_strv)

        del struct

    def test_boxed_struct_new(self):
        struct = GIMarshallingTests.BoxedStruct.new()
        self.assertTrue(isinstance(struct, GIMarshallingTests.BoxedStruct))

        del struct

    def test_boxed_struct_copy(self):
        struct = GIMarshallingTests.BoxedStruct()

        new_struct = struct.copy()
        self.assertTrue(isinstance(new_struct, GIMarshallingTests.BoxedStruct))

        del new_struct
        del struct

    def test_boxed_struct_return(self):
        struct = GIMarshallingTests.boxed_struct_returnv()

        self.assertTrue(isinstance(struct, GIMarshallingTests.BoxedStruct))
        self.assertEqual(42, struct.long_)
        self.assertEqual(['0', '1', '2'], struct.g_strv)

        del struct

    def test_boxed_struct_in(self):
        struct = GIMarshallingTests.BoxedStruct()
        struct.long_ = 42

        struct.inv()

        del struct

    def test_boxed_struct_out(self):
        struct = GIMarshallingTests.boxed_struct_out()

        self.assertTrue(isinstance(struct, GIMarshallingTests.BoxedStruct))
        self.assertEqual(42, struct.long_)

        del struct

    def test_boxed_struct_inout(self):
        in_struct = GIMarshallingTests.BoxedStruct()
        in_struct.long_ = 42

        out_struct = GIMarshallingTests.boxed_struct_inout(in_struct)

        self.assertTrue(isinstance(out_struct, GIMarshallingTests.BoxedStruct))
        self.assertEqual(0, out_struct.long_)

        del in_struct
        del out_struct

    def test_union(self):
        union = GIMarshallingTests.Union()

        self.assertTrue(isinstance(union, GIMarshallingTests.Union))

        new_union = union.copy()
        self.assertTrue(isinstance(new_union, GIMarshallingTests.Union))

        del union
        del new_union

    def test_union_return(self):
        union = GIMarshallingTests.union_returnv()

        self.assertTrue(isinstance(union, GIMarshallingTests.Union))
        self.assertEqual(42, union.long_)

        del union

    def test_union_in(self):
        union = GIMarshallingTests.Union()
        union.long_ = 42

        union.inv()

        del union

    def test_union_method(self):
        union = GIMarshallingTests.Union()
        union.long_ = 42

        union.method()

        del union

        self.assertRaises(TypeError, GIMarshallingTests.Union.method)


class TestGObject(unittest.TestCase):

    def test_object(self):
        self.assertTrue(issubclass(GIMarshallingTests.Object, GObject.GObject))

        object_ = GIMarshallingTests.Object()
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 1)

    def test_object_new(self):
        object_ = GIMarshallingTests.Object.new(42)
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 1)

    def test_object_int(self):
        object_ = GIMarshallingTests.Object(int=42)
        self.assertEqual(object_.int_, 42)
# FIXME: Don't work yet.
#        object_.int_ = 0
#        self.assertEqual(object_.int_, 0)

    def test_object_static_method(self):
        GIMarshallingTests.Object.static_method()

    def test_object_method(self):
        GIMarshallingTests.Object(int=42).method()
        self.assertRaises(TypeError, GIMarshallingTests.Object.method, GObject.GObject())
        self.assertRaises(TypeError, GIMarshallingTests.Object.method)

    def test_sub_object(self):
        self.assertTrue(issubclass(GIMarshallingTests.SubObject, GIMarshallingTests.Object))

        object_ = GIMarshallingTests.SubObject()
        self.assertTrue(isinstance(object_, GIMarshallingTests.SubObject))

    def test_sub_object_new(self):
        self.assertRaises(TypeError, GIMarshallingTests.SubObject.new, 42)

    def test_sub_object_static_method(self):
        object_ = GIMarshallingTests.SubObject()
        object_.static_method()

    def test_sub_object_method(self):
        object_ = GIMarshallingTests.SubObject(int=42)
        object_.method()

    def test_sub_object_sub_method(self):
        object_ = GIMarshallingTests.SubObject()
        object_.sub_method()

    def test_sub_object_overwritten_method(self):
        object_ = GIMarshallingTests.SubObject()
        object_.overwritten_method()

        self.assertRaises(TypeError, GIMarshallingTests.SubObject.overwritten_method, GIMarshallingTests.Object())

    def test_sub_object_int(self):
        object_ = GIMarshallingTests.SubObject()
        self.assertEqual(object_.int_, 0)
# FIXME: Don't work yet.
#        object_.int_ = 42
#        self.assertEqual(object_.int_, 42)

    def test_object_none_return(self):
        object_ = GIMarshallingTests.Object.none_return()
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 2)

    def test_object_full_return(self):
        object_ = GIMarshallingTests.Object.full_return()
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 1)

    def test_object_none_in(self):
        object_ = GIMarshallingTests.Object(int=42)
        GIMarshallingTests.Object.none_in(object_)
        self.assertEqual(object_.__grefcount__, 1)

        object_ = GIMarshallingTests.SubObject(int=42)
        GIMarshallingTests.Object.none_in(object_)

        object_ = GObject.GObject()
        self.assertRaises(TypeError, GIMarshallingTests.Object.none_in, object_)

        self.assertRaises(TypeError, GIMarshallingTests.Object.none_in, None)

    def test_object_none_out(self):
        object_ = GIMarshallingTests.Object.none_out()
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 2)

        new_object = GIMarshallingTests.Object.none_out()
        self.assertTrue(new_object is object_)

    def test_object_full_out(self):
        object_ = GIMarshallingTests.Object.full_out()
        self.assertTrue(isinstance(object_, GIMarshallingTests.Object))
        self.assertEqual(object_.__grefcount__, 1)

    def test_object_none_inout(self):
        object_ = GIMarshallingTests.Object(int=42)
        new_object = GIMarshallingTests.Object.none_inout(object_)

        self.assertTrue(isinstance(new_object, GIMarshallingTests.Object))

        self.assertFalse(object_ is new_object)

        self.assertEqual(object_.__grefcount__, 1)
        self.assertEqual(new_object.__grefcount__, 2)

        new_new_object = GIMarshallingTests.Object.none_inout(object_)
        self.assertTrue(new_new_object is new_object)

        GIMarshallingTests.Object.none_inout(GIMarshallingTests.SubObject(int=42))

    def test_object_full_inout(self):
        object_ = GIMarshallingTests.Object(int=42)
        new_object = GIMarshallingTests.Object.full_inout(object_)

        self.assertTrue(isinstance(new_object, GIMarshallingTests.Object))

        self.assertFalse(object_ is new_object)

        self.assertEqual(object_.__grefcount__, 2)
        self.assertEqual(new_object.__grefcount__, 1)

# FIXME: Doesn't actually return the same object.
#    def test_object_inout_same(self):
#        object_ = GIMarshallingTests.Object()
#        new_object = GIMarshallingTests.object_full_inout(object_)
#        self.assertTrue(object_ is new_object)
#        self.assertEqual(object_.__grefcount__, 1)


class TestPythonGObject(unittest.TestCase):

    class Object(GIMarshallingTests.Object):
        def __init__(self, int):
            GIMarshallingTests.Object.__init__(self)
            self.val = None

        def method(self):
            # Don't call super, which asserts that self.int == 42.
            pass

        def do_method_int8_in(self, int8):
            self.val = int8

        def do_method_int8_out(self):
            return 42

        def do_method_with_default_implementation(self, int8):
            GIMarshallingTests.Object.do_method_with_default_implementation(self, int8)
            self.props.int += int8

        def do_vfunc_return_value_only(self):
            return 4242

        def do_vfunc_one_out_parameter(self):
            return 42.42

        def do_vfunc_multiple_out_parameters(self):
            return (42.42, 3.14)

        def do_vfunc_return_value_and_one_out_parameter(self):
            return (5, 42)

        def do_vfunc_return_value_and_multiple_out_parameters(self):
            return (5, 42, 99)

        def do_vfunc_caller_allocated_out_parameter(self):
            return 'hello'

    class SubObject(GIMarshallingTests.SubObject):
        def __init__(self, int):
            GIMarshallingTests.SubObject.__init__(self)
            self.val = None

        def do_method_with_default_implementation(self, int8):
            self.val = int8

    class Interface3Impl(GObject.Object, GIMarshallingTests.Interface3):
        def __init__(self):
            GObject.Object.__init__(self)
            self.variants = None
            self.n_variants = None

        def do_test_variant_array_in(self, variants, n_variants):
            self.variants = variants
            self.n_variants = n_variants

    def test_object(self):
        self.assertTrue(issubclass(self.Object, GIMarshallingTests.Object))

        object_ = self.Object(int=42)
        self.assertTrue(isinstance(object_, self.Object))

    def test_object_method(self):
        self.Object(int=0).method()

    def test_object_vfuncs(self):
        object_ = self.Object(int=42)
        object_.method_int8_in(84)
        self.assertEqual(object_.val, 84)
        self.assertEqual(object_.method_int8_out(), 42)

        object_.method_with_default_implementation(42)
        self.assertEqual(object_.props.int, 84)

        self.assertEqual(object_.vfunc_return_value_only(), 4242)
        self.assertAlmostEqual(object_.vfunc_one_out_parameter(), 42.42, places=5)

        (a, b) = object_.vfunc_multiple_out_parameters()
        self.assertAlmostEqual(a, 42.42, places=5)
        self.assertAlmostEqual(b, 3.14, places=5)

        self.assertEqual(object_.vfunc_return_value_and_one_out_parameter(), (5, 42))
        self.assertEqual(object_.vfunc_return_value_and_multiple_out_parameters(), (5, 42, 99))

        self.assertEqual(object_.vfunc_caller_allocated_out_parameter(), 'hello')

        class ObjectWithoutVFunc(GIMarshallingTests.Object):
            def __init__(self, int):
                GIMarshallingTests.Object.__init__(self)

        object_ = ObjectWithoutVFunc(int=42)
        object_.method_with_default_implementation(84)
        self.assertEqual(object_.props.int, 84)

    def test_subobject_parent_vfunc(self):
        object_ = self.SubObject(int=81)
        object_.method_with_default_implementation(87)
        self.assertEqual(object_.val, 87)

    def test_dynamic_module(self):
        from gi.module import DynamicGObjectModule
        self.assertTrue(isinstance(GObject, DynamicGObjectModule))
        # compare the same enum from both the pygobject attrs and gi GObject attrs
        self.assertEqual(GObject.SIGNAL_ACTION, GObject.SignalFlags.ACTION)
        # compare a static gobject attr with a dynamic GObject attr
        import gi._gobject
        self.assertEqual(GObject.GObject, gi._gobject.GObject)

    def test_subobject_non_vfunc_do_method(self):
        class PythonObjectWithNonVFuncDoMethod:
            def do_not_a_vfunc(self):
                return 5

        class ObjectOverrideNonVFuncDoMethod(GIMarshallingTests.Object, PythonObjectWithNonVFuncDoMethod):
            def do_not_a_vfunc(self):
                value = super(ObjectOverrideNonVFuncDoMethod, self).do_not_a_vfunc()
                return 13 + value

        object_ = ObjectOverrideNonVFuncDoMethod()
        self.assertEqual(18, object_.do_not_a_vfunc())

    def test_native_function_not_set_in_subclass_dict(self):
        # Previously, GI was setting virtual functions on the class as well
        # as any *native* class that subclasses it. Here we check that it is only
        # set on the class that the method is originally from.
        self.assertTrue('do_method_with_default_implementation' in GIMarshallingTests.Object.__dict__)
        self.assertTrue('do_method_with_default_implementation' not in GIMarshallingTests.SubObject.__dict__)

    def test_subobject_with_interface_and_non_vfunc_do_method(self):
        # There was a bug for searching for vfuncs in interfaces. It was
        # triggered by having a do_* method that wasn't overriding
        # a native vfunc, as well as inheriting from an interface.
        class GObjectSubclassWithInterface(GObject.GObject, GIMarshallingTests.Interface):
            def do_method_not_a_vfunc(self):
                pass

    def test_subsubobject(self):
        class SubSubSubObject(GIMarshallingTests.SubSubObject):
            def do_method_deep_hierarchy(self, num):
                self.props.int = num * 2

        sub_sub_sub_object = SubSubSubObject()
        GIMarshallingTests.SubSubObject.do_method_deep_hierarchy(sub_sub_sub_object, 5)
        self.assertEqual(sub_sub_sub_object.props.int, 5)

    def test_interface3impl(self):
        iface3 = self.Interface3Impl()
        variants = [GLib.Variant('i', 27), GLib.Variant('s', 'Hello')]
        iface3.test_variant_array_in(variants)
        self.assertEqual(iface3.n_variants, 2)
        self.assertEqual(iface3.variants[0].unpack(), 27)
        self.assertEqual(iface3.variants[1].unpack(), 'Hello')

    def test_python_subsubobject_vfunc(self):
        class PySubObject(GIMarshallingTests.Object):
            def __init__(self):
                GIMarshallingTests.Object.__init__(self)
                self.sub_method_int8_called = 0

            def do_method_int8_in(self, int8):
                self.sub_method_int8_called += 1

        class PySubSubObject(PySubObject):
            def __init__(self):
                PySubObject.__init__(self)
                self.subsub_method_int8_called = 0

            def do_method_int8_in(self, int8):
                self.subsub_method_int8_called += 1

        so = PySubObject()
        so.method_int8_in(1)
        self.assertEqual(so.sub_method_int8_called, 1)

        # it should call the method on the SubSub object only
        sso = PySubSubObject()
        sso.method_int8_in(1)
        self.assertEqual(sso.subsub_method_int8_called, 1)
        self.assertEqual(sso.sub_method_int8_called, 0)

    def test_callback_in_vfunc(self):
        class SubObject(GIMarshallingTests.Object):
            def __init__(self):
                GObject.GObject.__init__(self)
                self.worked = False

            def do_vfunc_with_callback(self, callback):
                self.worked = callback(42) == 42

        _object = SubObject()
        _object.call_vfunc_with_callback()
        self.assertTrue(_object.worked)
        _object.worked = False
        _object.call_vfunc_with_callback()
        self.assertTrue(_object.worked)


class TestMultiOutputArgs(unittest.TestCase):

    def test_int_out_out(self):
        self.assertEqual((6, 7), GIMarshallingTests.int_out_out())

    def test_int_return_out(self):
        self.assertEqual((6, 7), GIMarshallingTests.int_return_out())


class TestGErrorException(unittest.TestCase):
    def test_gerror_exception(self):
        self.assertRaises(GObject.GError, GIMarshallingTests.gerror)
        try:
            GIMarshallingTests.gerror()
        except Exception:
            etype, e = sys.exc_info()[:2]
            self.assertEqual(e.domain, GIMarshallingTests.CONSTANT_GERROR_DOMAIN)
            self.assertEqual(e.code, GIMarshallingTests.CONSTANT_GERROR_CODE)
            self.assertEqual(e.message, GIMarshallingTests.CONSTANT_GERROR_MESSAGE)


# Interface


class TestInterfaces(unittest.TestCase):

    class TestInterfaceImpl(GObject.GObject, GIMarshallingTests.Interface):
        def __init__(self):
            GObject.GObject.__init__(self)
            self.val = None

        def do_test_int8_in(self, int8):
            self.val = int8

    def setUp(self):
        self.instance = self.TestInterfaceImpl()

    def test_wrapper(self):
        self.assertTrue(issubclass(GIMarshallingTests.Interface, GObject.GInterface))
        self.assertEqual(GIMarshallingTests.Interface.__gtype__.name, 'GIMarshallingTestsInterface')
        self.assertRaises(NotImplementedError, GIMarshallingTests.Interface)

    def test_implementation(self):
        self.assertTrue(issubclass(self.TestInterfaceImpl, GIMarshallingTests.Interface))
        self.assertTrue(isinstance(self.instance, GIMarshallingTests.Interface))

    def test_int8_int(self):
        GIMarshallingTests.test_interface_test_int8_in(self.instance, 42)
        self.assertEqual(self.instance.val, 42)

    def test_subclass(self):
        class TestInterfaceImplA(self.TestInterfaceImpl):
            pass

        class TestInterfaceImplB(TestInterfaceImplA):
            pass

        instance = TestInterfaceImplA()
        GIMarshallingTests.test_interface_test_int8_in(instance, 42)
        self.assertEqual(instance.val, 42)

    def test_mro(self):
        # there was a problem with Python bailing out because of
        # http://en.wikipedia.org/wiki/Diamond_problem with interfaces,
        # which shouldn't really be a problem.

        class TestInterfaceImpl(GObject.GObject, GIMarshallingTests.Interface):
            pass

        class TestInterfaceImpl2(GIMarshallingTests.Interface,
                                 TestInterfaceImpl):
            pass

        class TestInterfaceImpl3(self.TestInterfaceImpl,
                                 GIMarshallingTests.Interface2):
            pass


class TestInterfaceClash(unittest.TestCase):

    def test_clash(self):
        def create_clash():
            class TestClash(GObject.GObject, GIMarshallingTests.Interface, GIMarshallingTests.Interface2):
                def do_test_int8_in(self, int8):
                    pass
            TestClash()

        self.assertRaises(TypeError, create_clash)


class TestOverrides(unittest.TestCase):

    def test_constant(self):
        self.assertEqual(GIMarshallingTests.OVERRIDES_CONSTANT, 7)

    def test_struct(self):
        # Test that the constructor has been overridden.
        struct = GIMarshallingTests.OverridesStruct(42)

        self.assertTrue(isinstance(struct, GIMarshallingTests.OverridesStruct))

        # Test that the method has been overridden.
        self.assertEqual(6, struct.method())

        del struct

        # Test that the overrides wrapper has been registered.
        struct = GIMarshallingTests.overrides_struct_returnv()

        self.assertTrue(isinstance(struct, GIMarshallingTests.OverridesStruct))

        del struct

    def test_object(self):
        # Test that the constructor has been overridden.
        object_ = GIMarshallingTests.OverridesObject(42)

        self.assertTrue(isinstance(object_, GIMarshallingTests.OverridesObject))

        # Test that the alternate constructor has been overridden.
        object_ = GIMarshallingTests.OverridesObject.new(42)

        self.assertTrue(isinstance(object_, GIMarshallingTests.OverridesObject))

        # Test that the method has been overridden.
        self.assertEqual(6, object_.method())

        # Test that the overrides wrapper has been registered.
        object_ = GIMarshallingTests.OverridesObject.returnv()

        self.assertTrue(isinstance(object_, GIMarshallingTests.OverridesObject))

    def test_module_name(self):
        self.assertEqual(GIMarshallingTests.OverridesStruct.__module__, 'gi.overrides.GIMarshallingTests')
        self.assertEqual(GObject.InitiallyUnowned.__module__, 'gi.repository.GObject')


class TestDir(unittest.TestCase):
    def test_members_list(self):
        list = dir(GIMarshallingTests)
        self.assertTrue('OverridesStruct' in list)
        self.assertTrue('BoxedStruct' in list)
        self.assertTrue('OVERRIDES_CONSTANT' in list)
        self.assertTrue('GEnum' in list)
        self.assertTrue('int32_return_max' in list)

    def test_modules_list(self):
        import gi.repository
        list = dir(gi.repository)
        self.assertTrue('GIMarshallingTests' in list)

        # FIXME: test to see if a module which was not imported is in the list
        #        we should be listing every typelib we find, not just the ones
        #        which are imported
        #
        #        to test this I recommend we compile a fake module which
        #        our tests would never import and check to see if it is
        #        in the list:
        #
        # self.assertTrue('DoNotImportDummyTests' in list)


class TestGErrorArrayInCrash(unittest.TestCase):
    # Previously there was a bug in invoke, in which C arrays were unwrapped
    # from inside GArrays to be passed to the C function. But when a GError was
    # set, invoke would attempt to free the C array as if it were a GArray.
    # This crash is only for C arrays. It does not happen for C functions which
    # take in GArrays. See https://bugzilla.gnome.org/show_bug.cgi?id=642708
    def test_gerror_array_in_crash(self):
        self.assertRaises(GObject.GError, GIMarshallingTests.gerror_array_in, [1, 2, 3])


class TestGErrorOut(unittest.TestCase):
    # See https://bugzilla.gnome.org/show_bug.cgi?id=666098
    def test_gerror_out(self):
        error, debug = GIMarshallingTests.gerror_out()

        self.assertIsInstance(error, GObject.GError)
        self.assertEqual(error.domain, GIMarshallingTests.CONSTANT_GERROR_DOMAIN)
        self.assertEqual(error.code, GIMarshallingTests.CONSTANT_GERROR_CODE)
        self.assertEqual(error.message, GIMarshallingTests.CONSTANT_GERROR_MESSAGE)
        self.assertEqual(debug, GIMarshallingTests.CONSTANT_GERROR_DEBUG_MESSAGE)


class TestGErrorOutTransferNone(unittest.TestCase):
    # See https://bugzilla.gnome.org/show_bug.cgi?id=666098
    def test_gerror_out_transfer_none(self):
        error, debug = GIMarshallingTests.gerror_out_transfer_none()

        self.assertIsInstance(error, GObject.GError)
        self.assertEqual(error.domain, GIMarshallingTests.CONSTANT_GERROR_DOMAIN)
        self.assertEqual(error.code, GIMarshallingTests.CONSTANT_GERROR_CODE)
        self.assertEqual(error.message, GIMarshallingTests.CONSTANT_GERROR_MESSAGE)
        self.assertEqual(GIMarshallingTests.CONSTANT_GERROR_DEBUG_MESSAGE, debug)


class TestGErrorReturn(unittest.TestCase):
    # See https://bugzilla.gnome.org/show_bug.cgi?id=666098
    def test_return_gerror(self):
        error = GIMarshallingTests.gerror_return()

        self.assertIsInstance(error, GObject.GError)
        self.assertEqual(error.domain, GIMarshallingTests.CONSTANT_GERROR_DOMAIN)
        self.assertEqual(error.code, GIMarshallingTests.CONSTANT_GERROR_CODE)
        self.assertEqual(error.message, GIMarshallingTests.CONSTANT_GERROR_MESSAGE)


class TestKeywordArgs(unittest.TestCase):

    def test_calling(self):
        kw_func = GIMarshallingTests.int_three_in_three_out

        self.assertEqual(kw_func(1, 2, 3), (1, 2, 3))
        self.assertEqual(kw_func(**{'a': 4, 'b': 5, 'c': 6}), (4, 5, 6))
        self.assertEqual(kw_func(1, **{'b': 7, 'c': 8}), (1, 7, 8))
        self.assertEqual(kw_func(1, 7, **{'c': 8}), (1, 7, 8))
        self.assertEqual(kw_func(1, c=8, **{'b': 7}), (1, 7, 8))
        self.assertEqual(kw_func(2, c=4, b=3), (2, 3, 4))
        self.assertEqual(kw_func(a=2, c=4, b=3), (2, 3, 4))

    def assertRaisesMessage(self, exception, message, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except exception:
            (e_type, e) = sys.exc_info()[:2]
            if message is not None:
                self.assertEqual(str(e), message)
        except:
            raise
        else:
            msg = "%s() did not raise %s" % (func.__name__, exception.__name__)
            raise AssertionError(msg)

    def test_type_errors(self):
        # test too few args
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (0 given)",
                                 GIMarshallingTests.int_three_in_three_out)
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (1 given)",
                                 GIMarshallingTests.int_three_in_three_out, 1)
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (0 given)",
                                 GIMarshallingTests.int_three_in_three_out, *())
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (0 given)",
                                 GIMarshallingTests.int_three_in_three_out, *(), **{})
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 non-keyword arguments (0 given)",
                                 GIMarshallingTests.int_three_in_three_out, *(), **{'c': 4})

        # test too many args
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 arguments (4 given)",
                                 GIMarshallingTests.int_three_in_three_out, *(1, 2, 3, 4))
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() takes exactly 3 non-keyword arguments (4 given)",
                                 GIMarshallingTests.int_three_in_three_out, *(1, 2, 3, 4), c=6)

        # test too many keyword args
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() got multiple values for keyword argument 'a'",
                                 GIMarshallingTests.int_three_in_three_out, 1, 2, 3, **{'a': 4, 'b': 5})
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() got an unexpected keyword argument 'd'",
                                 GIMarshallingTests.int_three_in_three_out, d=4)
        self.assertRaisesMessage(TypeError, "int_three_in_three_out() got an unexpected keyword argument 'e'",
                                 GIMarshallingTests.int_three_in_three_out, **{'e': 2})

    def test_kwargs_are_not_modified(self):
        d = {'b': 2}
        d2 = d.copy()
        GIMarshallingTests.int_three_in_three_out(1, c=4, **d)
        self.assertEqual(d, d2)


class TestPropertiesObject(unittest.TestCase):

    def setUp(self):
        self.obj = GIMarshallingTests.PropertiesObject()

    def test_boolean(self):
        self.assertEqual(self.obj.props.some_boolean, False)
        self.obj.props.some_boolean = True
        self.assertEqual(self.obj.props.some_boolean, True)

        obj = GIMarshallingTests.PropertiesObject(some_boolean=True)
        self.assertEqual(obj.props.some_boolean, True)

    @unittest.expectedFailure
    def test_char(self):
        # gobject-introspection thinks it has a guint8 type tag, which is
        # wrong; this will raise an assertion critical which we need to ignore
        old_mask = GLib.log_set_always_fatal(
            GLib.LogLevelFlags.LEVEL_WARNING | GLib.LogLevelFlags.LEVEL_ERROR)
        self.assertEqual(self.obj.props.some_char, 0)
        self.obj.props.some_char = GObject.G_MAXINT8
        self.assertEqual(self.obj.props.some_char, GObject.G_MAXINT8)

        GLib.log_set_always_fatal(old_mask)

        obj = GIMarshallingTests.PropertiesObject(some_char=-42)
        self.assertEqual(obj.props.some_char, -42)

    def test_uchar(self):
        self.assertEqual(self.obj.props.some_uchar, 0)
        self.obj.props.some_uchar = GObject.G_MAXUINT8
        self.assertEqual(self.obj.props.some_uchar, GObject.G_MAXUINT8)

        obj = GIMarshallingTests.PropertiesObject(some_uchar=42)
        self.assertEqual(obj.props.some_uchar, 42)

    def test_int(self):
        self.assertEqual(self.obj.props.some_int, 0)
        self.obj.props.some_int = GObject.G_MAXINT
        self.assertEqual(self.obj.props.some_int, GObject.G_MAXINT)

        obj = GIMarshallingTests.PropertiesObject(some_int=-42)
        self.assertEqual(obj.props.some_int, -42)

        self.assertRaises(TypeError, setattr, self.obj.props, 'some_int', 'foo')
        self.assertRaises(TypeError, setattr, self.obj.props, 'some_int', None)

        self.assertEqual(obj.props.some_int, -42)

    def test_uint(self):
        self.assertEqual(self.obj.props.some_uint, 0)
        self.obj.props.some_uint = GObject.G_MAXUINT
        self.assertEqual(self.obj.props.some_uint, GObject.G_MAXUINT)

        obj = GIMarshallingTests.PropertiesObject(some_uint=42)
        self.assertEqual(obj.props.some_uint, 42)

        self.assertRaises(TypeError, setattr, self.obj.props, 'some_uint', 'foo')
        self.assertRaises(TypeError, setattr, self.obj.props, 'some_uint', None)

        self.assertEqual(obj.props.some_uint, 42)

    def test_long(self):
        self.assertEqual(self.obj.props.some_long, 0)
        self.obj.props.some_long = GObject.G_MAXLONG
        self.assertEqual(self.obj.props.some_long, GObject.G_MAXLONG)

        obj = GIMarshallingTests.PropertiesObject(some_long=-42)
        self.assertEqual(obj.props.some_long, -42)

        self.assertRaises(TypeError, setattr, self.obj.props, 'some_long', 'foo')
        self.assertRaises(TypeError, setattr, self.obj.props, 'some_long', None)

        self.assertEqual(obj.props.some_long, -42)

    def test_ulong(self):
        self.assertEqual(self.obj.props.some_ulong, 0)
        self.obj.props.some_ulong = GObject.G_MAXULONG
        self.assertEqual(self.obj.props.some_ulong, GObject.G_MAXULONG)

        obj = GIMarshallingTests.PropertiesObject(some_ulong=42)
        self.assertEqual(obj.props.some_ulong, 42)

        self.assertRaises(TypeError, setattr, self.obj.props, 'some_ulong', 'foo')
        self.assertRaises(TypeError, setattr, self.obj.props, 'some_ulong', None)

        self.assertEqual(obj.props.some_ulong, 42)

    def test_int64(self):
        self.assertEqual(self.obj.props.some_int64, 0)
        self.obj.props.some_int64 = GObject.G_MAXINT64
        self.assertEqual(self.obj.props.some_int64, GObject.G_MAXINT64)

        obj = GIMarshallingTests.PropertiesObject(some_int64=-4200000000000000)
        self.assertEqual(obj.props.some_int64, -4200000000000000)

    def test_uint64(self):
        self.assertEqual(self.obj.props.some_uint64, 0)
        self.obj.props.some_uint64 = GObject.G_MAXUINT64
        self.assertEqual(self.obj.props.some_uint64, GObject.G_MAXUINT64)

        obj = GIMarshallingTests.PropertiesObject(some_uint64=4200000000000000)
        self.assertEqual(obj.props.some_uint64, 4200000000000000)

    def test_float(self):
        self.assertEqual(self.obj.props.some_float, 0)
        self.obj.props.some_float = GObject.G_MAXFLOAT
        self.assertEqual(self.obj.props.some_float, GObject.G_MAXFLOAT)

        obj = GIMarshallingTests.PropertiesObject(some_float=42.42)
        self.assertAlmostEqual(obj.props.some_float, 42.42, 4)

        obj = GIMarshallingTests.PropertiesObject(some_float=42)
        self.assertAlmostEqual(obj.props.some_float, 42.0, 4)

        self.assertRaises(TypeError, setattr, self.obj.props, 'some_float', 'foo')
        self.assertRaises(TypeError, setattr, self.obj.props, 'some_float', None)

        self.assertAlmostEqual(obj.props.some_float, 42.0, 4)

    def test_double(self):
        self.assertEqual(self.obj.props.some_double, 0)
        self.obj.props.some_double = GObject.G_MAXDOUBLE
        self.assertEqual(self.obj.props.some_double, GObject.G_MAXDOUBLE)

        obj = GIMarshallingTests.PropertiesObject(some_double=42.42)
        self.assertAlmostEqual(obj.props.some_double, 42.42)

        obj = GIMarshallingTests.PropertiesObject(some_double=42)
        self.assertAlmostEqual(obj.props.some_double, 42.0)

        self.assertRaises(TypeError, setattr, self.obj.props, 'some_double', 'foo')
        self.assertRaises(TypeError, setattr, self.obj.props, 'some_double', None)

        self.assertAlmostEqual(obj.props.some_double, 42.0)

    def test_strv(self):
        self.assertEqual(self.obj.props.some_strv, [])
        self.obj.props.some_strv = ['hello', 'world']
        self.assertEqual(self.obj.props.some_strv, ['hello', 'world'])

        self.assertRaises(TypeError, setattr, self.obj.props, 'some_strv', 1)
        self.assertRaises(TypeError, setattr, self.obj.props, 'some_strv', 'foo')
        self.assertRaises(TypeError, setattr, self.obj.props, 'some_strv', [1, 2])
        self.assertRaises(TypeError, setattr, self.obj.props, 'some_strv', ['foo', 1])

        self.assertEqual(self.obj.props.some_strv, ['hello', 'world'])

        obj = GIMarshallingTests.PropertiesObject(some_strv=['hello', 'world'])
        self.assertEqual(obj.props.some_strv, ['hello', 'world'])

    def test_boxed_struct(self):
        self.assertEqual(self.obj.props.some_boxed_struct, None)

        class GStrv(list):
            __gtype__ = GObject.TYPE_STRV

        struct1 = GIMarshallingTests.BoxedStruct()
        struct1.long_ = 1

        self.obj.props.some_boxed_struct = struct1
        self.assertEqual(self.obj.props.some_boxed_struct.long_, 1)
        self.assertEqual(self.obj.some_boxed_struct.long_, 1)

        self.assertRaises(TypeError, setattr, self.obj.props, 'some_boxed_struct', 1)
        self.assertRaises(TypeError, setattr, self.obj.props, 'some_boxed_struct', 'foo')

        obj = GIMarshallingTests.PropertiesObject(some_boxed_struct=struct1)
        self.assertEqual(obj.props.some_boxed_struct.long_, 1)


class TestKeywords(unittest.TestCase):
    def test_method(self):
        # g_variant_print()
        v = GLib.Variant('i', 1)
        self.assertEqual(v.print_(False), '1')

    def test_function(self):
        # g_thread_yield()
        self.assertEqual(GLib.Thread.yield_(), None)

    def test_struct_method(self):
        # g_timer_continue()
        # we cannot currently instantiate GLib.Timer objects, so just ensure
        # the method exists
        self.assertTrue(callable(GLib.Timer.continue_))

    def test_uppercase(self):
        self.assertEqual(GLib.IOCondition.IN.value_nicks, ['in'])


class TestModule(unittest.TestCase):
    def test_path(self):
        self.assertTrue(GIMarshallingTests.__path__.endswith('GIMarshallingTests-1.0.typelib'),
                        GIMarshallingTests.__path__)

    def test_str(self):
        self.assertTrue("'GIMarshallingTests' from '" in str(GIMarshallingTests),
                        str(GIMarshallingTests))

    def test_dir(self):
        _dir = dir(GIMarshallingTests)
        self.assertGreater(len(_dir), 10)

        self.assertTrue('SimpleStruct' in _dir)
        self.assertTrue('Interface2' in _dir)
        self.assertTrue('CONSTANT_GERROR_CODE' in _dir)
        self.assertTrue('array_zero_terminated_inout' in _dir)

        # assert that dir() does not contain garbage
        for item_name in _dir:
            item = getattr(GIMarshallingTests, item_name)
            self.assertTrue(hasattr(item, '__class__'))

    def test_help(self):
        orig_stdout = sys.stdout
        try:
            if sys.version_info.major < 3:
                sys.stdout = BytesIO()
            else:
                sys.stdout = StringIO()
            help(GIMarshallingTests)
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = orig_stdout

        self.assertTrue('SimpleStruct' in output, output)
        self.assertTrue('Interface2' in output, output)
        self.assertTrue('method_array_inout' in output, output)


class TestProjectVersion(unittest.TestCase):
    def test_version_str(self):
        self.assertGreaterEqual(gi.__version__, "3.3.5")

    def test_version_info(self):
        self.assertEqual(len(gi.version_info), 3)
        self.assertGreaterEqual(gi.version_info, (3, 3, 5))

    def test_check_version(self):
        self.assertRaises(ValueError, gi.check_version, (99, 0, 0))
        self.assertRaises(ValueError, gi.check_version, "99.0.0")
        gi.check_version((3, 3, 5))
        gi.check_version("3.3.5")
