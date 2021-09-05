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


def test_edit_script_and_patch_identical_inputs():
    set_ = TestData(
        "identical inputs",
        [1, 2, 3],
        [1, 2, 3],
        [],
        []
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_edit_script_and_patch_delete_1_element_in_the_middle():
    set_ = TestData(
        "delete 1 element in the middle",
        [1, 2, 3],
        [1, 3],
        ['2d1'],
        ['2i2']
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_edit_script_and_patch_delete_2_elements_in_the_middle():
    set_ = TestData(
        "delete 2 elements in the middle",
        [1, 2, 3, 4],
        [1, 4],
        ['2d2'],
        ['2i2,3']
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_edit_script_and_patch_delete_2_elements_at_2_different_locations():
    set_ = TestData(
        "delete 2 elements at 2 different locations",
        [1, 2, 3, 4, 5],
        [1, 3, 5],
        ['2d1', '4d1'],
        ['2i2', '4i4']
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_edit_script_and_patch_delete_2_and_insert_1_elements_at_2_different_locations():
    set_ = TestData(
        "delete 2 and insert 1 elements at 2 different locations",
        [1, 2, 3, 5, 6, 7],
        [1, 3, 4, 5, 7],
        ['2d1', '3i4', '5d1'],
        ['2i2', '3d1', '5i6']
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_edit_script_and_patch_delete_at_start():
    set_ = TestData(
        "delete at start",
        [1, 2],
        [2],
        ['1d1'],
        ['1i1']
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_edit_script_and_patch_delete_at_end():
    set_ = TestData(
        "delete at end",
        [1, 2],
        [1],
        ['2d1'],
        ['2i2']
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_edit_script_and_patch_delete_all():
    set_ = TestData(
        "delete all",
        [1],
        [],
        ['1d1'],
        ['1i1']
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_edit_script_and_patch_replace_1_in_the_middle():
    set_ = TestData(
        "replace 1 in the middle",
        [1, 0, 3],
        [1, 2, 3],
        ['2d1', '2i2'],
        ['2d1', '2i0']
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_edit_script_and_patch_replace_2_in_the_middle():
    set_ = TestData(
        "replace 2 in the middle",
        [1, 0, 0, 4],
        [1, 2, 3, 4],
        ['2d2', '2i2,3'],
        ['2d2', '2i0,0']
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_edit_script_and_patch_many_similar_values_some_changes():
    set_ = TestData(
        "many similar values, some changes",
        [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
        ['3i1,1', '7d1', '11d1', '12i0'],
        ['3d2', '7i1', '12d1', '11i1']
    )

    diff = set_.a.diff(set_.b)
    res = diff.edit_script()
    assert res == set_.a_b
    assert set_.a.patch(diff) == set_.b

    diff = set_.b.diff(set_.a)
    res = diff.edit_script()
    assert res == set_.b_a
    assert set_.b.patch(diff) == set_.a


def test_string_diff_some_insertions_some_changes_some_deletions():
    """No docstring at the origin
    """
    set_ = TestData(
        "Some insertions, some changes, some deletions",
        "0\n1\n2\n4\n5\n6\n7\n",
        "0\n2\nA\nB\n6\n5\n7\n \n",
        "2d1\n< 1\n4,5c3,4\n< 4\n< 5\n---\n> A\n> B\n6a6\n> 5\n7a8\n>  \n",
        "1a2\n> 1\n3,5c4\n< A\n< B\n< 6\n---\n> 4\n6a6\n> 6\n8d7\n<  \n"
    )

    diff = set_.a.diff(set_.b)
    res = diff.to_s()
    assert res == set_.a_b, "A->B text diff %s failed" % set_.name
    assert set_.a.patch(diff) == set_.b, "A->B text patch %s failed" % set_.name

    diff = set_.b.diff(set_.a)
    res = diff.to_s()
    assert res == set_.b_a, "B->A text diff %s failed" % set_.name
    assert set_.b.patch(diff) == set_.a, "B->A text patch %s failed" % set_.name


def test_string_diff_some_insertions_some_changes_some_deletions_2():
    """No docstring at the origin
    """
    set_ = TestData(
        "Some insertions, some changes, some deletions",
        "foo\nbar\n",
        "foo\nbaz\n",
        "2c2\n< bar\n---\n> baz\n",
        "2c2\n< baz\n---\n> bar\n"
    )

    diff = set_.a.diff(set_.b)
    res = diff.to_s()
    assert res == set_.a_b, "A->B text diff %s failed" % set_.name
    assert set_.a.patch(diff) == set_.b, "A->B text patch %s failed" % set_.name

    diff = set_.b.diff(set_.a)
    res = diff.to_s()
    assert res == set_.b_a, "B->A text diff %s failed" % set_.name
    assert set_.b.patch(diff) == set_.a, "B->A text patch %s failed" % set_.name
