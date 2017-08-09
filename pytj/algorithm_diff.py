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


class Hunk(object):
    """A Hunk stores all information about a contiguous change of the
    destination list. It stores the inserted and deleted values as well as
    their positions in the A and B list.

    :param a_idx: _a_idx_ is the index in the A list.
    :param b_idx: _b_idx_ is the index in the B list.
    """

    def __init__(self, a_idx, b_idx):
        self.a_idx = a_idx

        # A list of values to be deleted from the A list starting at a_idx.
        self.delete_values = []

        self.b_idx = b_idx
        # A list of values to be inserted into the B list at b_idx.
        self.insert_values = []

    @property
    def insert(self):
        """Has the Hunk any values to insert?
        """
        return len(self.insert_values) > 0

    @property
    def delete(self):
        """Has the Hunk any values to be deleted?
        """
        return len(self.delete_values) > 0

    def to_s(self):
        """I guess it is the string repr which should be __str__
        """
        show_separator = False
        if self.insert and self.delete:
            s = "%sc#%s\n" % (self.a_range, self.b_range)
            show_separator = True
        elif self.insert:
            s = "%sa%s\n" % (self.a_idx, self.b_range)
        else:
            s = "%sd%s\n" % (self.a_range, self.b_idx)

        for value in self.delete_values:
            s = "%s< %s\n" % (s, value)

        if show_separator:
            s = "%s---\n" % s

        for value in self.insert_values:
            s = "%s> %s\n" % (s, value)

        return s

    @property
    def a_range(self):
        """No docstring at the origin
        """
        return self.range(
            self.a_idx + 1,
            self.a_idx + len(self.delete_values)
        )

    @property
    def b_range(self):
        """No docstring at the origin
        """
        return self.range(
            self.b_idx + 1,
            self.b_idx + len(self.insert_values)
        )

    @classmethod
    def range(cls, start_idx, end_idx):
        """No docstring at the origin

        :param start_idx:
        :param end_idx:
        :return:
        """
        if start_idx == end_idx:
            return "%s" % start_idx
        else:
            return "%s,%s" % (start_idx, end_idx)


class Diff(object):
    """This class is an implementation of the classic UNIX diff functionality.
    It's based on an original implementation by Lars Christensen, which based
    his version on the Perl Algorithm::Diff implementation. This is largely a
    from-scratch implementation that tries to have a less intrusive and more
    user-friendly interface. But some code fragments are very similar to the
    original and are copyright (C) 2001 Lars Christensen.

    :param a:
    :param b:
    """

    def __init__(self, a, b):
        # Create a new Diff between the _a_ list and _b_ list.
        self.hunks = []
        self.diff(a, b)

    def patch(self, values):
        """Modify the _values_ list according to the stored diff information.

        :param list values:
        :return:
        """
        import copy
        res = copy.copy(values)

        for hunk in self.hunks:
            if hunk.delete:
                res = res[0: hunk.b_idx] + \
                      res[hunk.b_idx + len(hunk.delete_values):]

            if hunk.insert:
                res = res[0:hunk.b_idx] + \
                      hunk.insert_values + \
                      res[hunk.b_idx:]
        return res

    def edit_script(self):
        """
        """
        script = []
        for hunk in self.hunks:
            if hunk.delete:
                script.append(
                    "%sd%s" % (
                        hunk.a_idx + 1,
                        len(hunk.delete_values)
                    )
                )

            if hunk.insert:
                script.append(
                    "%si%s" % (
                        hunk.b_idx + 1,
                        ','.join(map(str, hunk.insert_values))
                    )
                )

        return script

    def to_s(self):
        """Return the diff list as standard UNIX diff output.
        """
        value = ''.join(map(Hunk.to_s, self.hunks))
        return value

    def diff(self, a, b):
        """no docstring on the origin

        :param a:
        :param b:
        :return:
        """
        index_translation_table = self.compute_index_translations(a, b)

        ai = bi = 0
        table_length = len(index_translation_table)

        while ai < table_length:
            # Check if value from index ai should be included in B.
            dest_index = index_translation_table[ai]
            if dest_index is not None:
                # Yes, it needs to go to position dest_index. All values from
                # bi to new_index - 1 are new values in B, not in A.
                while bi < dest_index:
                    self.insert_element(ai, bi, b[bi])
                    bi += 1
                bi += 1
            else:
                # No, it's not in B. Put it onto the deletion list.
                self.delete_element(ai, bi, a[ai])
            ai += 1

        # The remainder of the A list has to be deleted.
        while ai < len(a):
            self.delete_element(ai, bi, a[ai])
            ai += 1

        # The remainder of the B list are new values.
        while bi < len(b):
            self.insert_element(ai, bi, b[bi])
            bi += 1

    def compute_index_translations(self, a, b):
        """Computes the index translation LUT which show what item of the a is
        where on the b.

        :param list a:
        :param list b:
        :return:
        """
        import copy
        index_translation_table = [None] * len(a)
        b_copy = copy.copy(b)
        last_index = -1
        for i in range(len(a)):
            try:
                index = b_copy.index(a[i])
                while index < last_index:
                    b_copy[index] = None
                    index = b_copy.index(a[i])

                last_index = index
                index_translation_table[i] = index
                b_copy[index] = None
            except ValueError:
                continue

        return index_translation_table

    def delete_element(self, a_idx, b_idx, value):
        """no docstring at the origin

        :param a_idx:
        :param b_idx:
        :param value:
        :return:
        """
        if len(self.hunks) == 0 or \
                                self.hunks[-1].a_idx + len(
                            self.hunks[-1].delete_values) != a_idx:
            hunk = Hunk(a_idx, b_idx)
            self.hunks.append(hunk)
        else:
            hunk = self.hunks[-1]
        hunk.delete_values.append(value)

    def insert_element(self, a_idx, b_idx, value):
        """no docstring at the origin
        
        :param a_idx:
        :param b_idx:
        :param value:
        :return:
        """
        if len(self.hunks) == 0 or \
                        (self.hunks[-1].b_idx + len(
                            self.hunks[-1].insert_values)) != b_idx:
            hunk = Hunk(a_idx, b_idx)
            self.hunks.append(hunk)
        else:
            hunk = self.hunks[-1]
        hunk.insert_values.append(value)


class Diffable(list):
    """no docstring at the origin
    """

    def diff(self, b):
        """no docstring at origin

        :param list b:
        :return:
        """
        return Diff(self, b)

    def patch(self, diff):
        return diff.patch(self)


class DiffableString(str):
    """no docstring at the origin
    """

    def diff(self, b):
        """no docstring at the origin

        :param str b:
        :return:
        """
        return Diffable(self.split("\n")).diff(b.split("\n"))

    def patch(self, hunks):
        """no docstring at the origin
        
        :param hunks:
        :return:
        """
        return '%s' % '\n'.join(Diffable(self.split('\n')).patch(hunks))
