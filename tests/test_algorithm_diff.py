# -*- coding: utf-8 -*-
# pyTJ
# Copyright (C) 2017 Erkan Ozgur Yilmaz
#
# This file is part of pyTJ.
#
# pyTJ is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# pyTJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with pyTJ.  If not, see <http://www.gnu.org/licenses/>

import pytest
from pytj.algorithm_diff import Diffable, DiffableString


class TestData(object):
    """
    """

    def __init__(self, name, a, b, a_b, b_a):
        self.name = name

        self.a = self.b = None
        if isinstance(a, list):
            self.a = Diffable(a)
        elif isinstance(a, str):
            self.a = DiffableString(a)

        if isinstance(b, list):
            self.b = Diffable(b)
        elif isinstance(b, str):
            self.b = DiffableString(b)

        self.a_b = a_b
        self.b_a = b_a


def test_edit_script_and_patch():
    """No docstring at the origin
    """
    data = [
        TestData(
            "identical inputs",
            [1, 2, 3],
            [1, 2, 3],
            [],
            []
        ),
        TestData(
            "delete 1 element in the middle",
            [1, 2, 3],
            [1, 3],
            ['2d1'],
            ['2i2']
        ),
        TestData(
            "delete 2 elements in the middle",
            [1, 2, 3, 4],
            [1, 4],
            ['2d2'],
            ['2i2,3']
        ),
        TestData(
            "delete 2 elements at 2 different locations",
            [1, 2, 3, 4, 5],
            [1, 3, 5],
            ['2d1', '4d1'],
            ['2i2', '4i4']
        ),
        TestData(
            "delete 2 and insert 1 elements at 2 different locations",
            [1, 2, 3, 5, 6, 7],
            [1, 3, 4, 5, 7],
            ['2d1', '3i4', '5d1'],
            ['2i2', '3d1', '5i6']
        ),
        TestData(
            "delete at start",
            [1, 2],
            [2],
            ['1d1'],
            ['1i1']
        ),
        TestData(
            "delete at end",
            [1, 2],
            [1],
            ['2d1'],
            ['2i2']
        ),
        TestData(
            "delete all",
            [1],
            [],
            ['1d1'],
            ['1i1']
        ),
        TestData(
            "replace 1 in the middle",
            [1, 0, 3],
            [1, 2, 3],
            ['2d1', '2i2'],
            ['2d1', '2i0']
        ),
        TestData(
            "replace 2 in the middle",
            [1, 0, 0, 4],
            [1, 2, 3, 4],
            ['2d2', '2i2,3'],
            ['2d2', '2i0,0']
        ),
        TestData(
            "many similar values, some changes",
            [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
            # ['3i1,1', '7d1', '11d1', '12i0'],
            ['3i1,1', '9i0', '11i1', '14i0,0', '11d5'],
            # ['3d2', '7i1', '12d1', '11i1']
            ['3i0', '5i0', '7i1', '10i1,1,1', '14i0', '9d8']
        )
    ]
    for set_ in data:
        diff = set_.a.diff(set_.b)
        res = diff.edit_script()
        assert set_.a_b == res, "A->B edit script %s failed" % set_.name
        assert set_.b == set_.a.patch(diff), "A->B patch %s failed" % set_.name

        diff = set_.b.diff(set_.a)
        res = diff.edit_script()
        assert set_.b_a == res, "B->A edit script %s failed" % set_.name
        assert set_.a == set_.b.patch(diff), "B->A patch %s failed" % set_.name


def test_string_diff():
    """No docstring at the origin
    """
    data = [
        TestData(
            "Some insertions, some changes, some deletions",
            "0\n1\n2\n4\n5\n6\n7\n",
            "0\n2\nA\nB\n6\n5\n7\n \n",
            # "2d1\n< 1\n4,5c3,4\n< 4\n< 5\n---\n> A\n> B\n6a6\n> 5\n7a8\n>  \n",
            "2d1\n< 1\n4c#3,5\n< 4\n---\n> A\n> B\n> 6\n6d6\n< 6\n7a8\n>  \n",
            # "1a2\n> 1\n3,5c4\n< A\n< B\n< 6\n---\n> 4\n6a6\n> 6\n8d7\n<  \n"
            "1a2\n> 1\n3,4c#4,5\n< A\n< B\n---\n> 4\n> 5\n6d6\n< 5\n8d7\n<  \n"
        ),
        TestData(
            "Some insertions, some changes, some deletions",
            "foo\nbar\n",
            "foo\nbaz\n",
            "2c#2\n< bar\n---\n> baz\n",
            "2c#2\n< baz\n---\n> bar\n"
        )
    ]

    for set_ in data:
        diff = set_.a.diff(set_.b)
        res = diff.to_s()
        assert set_.a_b == res, "A->B text diff %s failed" % set_.name
        assert set_.b == set_.a.patch(diff), \
            "A->B text patch %s failed" % set_.name

        diff = set_.b.diff(set_.a)
        res = diff.to_s()
        assert set_.b_a == res, "B->A text diff %s failed" % set_.name
        assert set_.a == set_.b.patch(diff), \
            "B->A text patch %s failed" % set_.name
