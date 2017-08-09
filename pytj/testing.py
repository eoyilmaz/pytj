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
"""Tools for tests
"""

import os
import glob


class MessageChecker(object):
    """Check that all messages that were generated during the TaskJuggler run
    match the references specified in the test file.

    mapped from: TaskJuggler/test/MessageChecker.rb
    """

    @classmethod
    def check_messages(cls, tj, file_path):
        ref_messages = cls.collect_messages(file_path)

    @classmethod
    def collect_messages(cls, file_path):
        """All files that generate messages have comments in them that specify
        the expected messages. The comments have the following form:

        MARK: <type> <lineNo> <message Id>
        We collect all these reference messages to compare them with the
        generated messages after the test has been run.

        :param file_path:
        :return:
        """
        import re
        regex = re.compile('^# MARK: ([a-z]+) ([0-9]+) ([a-z0-9_]*)')

        ref_messages = []
        with open(file_path, 'r') as f:
            for line in f.readlines():
                match = regex.match(line)
                if match:
                    groups = match.groups()
                    ref_messages.append([
                        groups[0], int(groups[1]), groups[2]
                    ])
        return ref_messages.reverse()


class ReferenceGenerator(object):
    """mapped from: TaskJuggler/test/ReferenceGenerator.rb
    """

    def __init__(self):
        AppConfig = dict()
        AppConfig['appName'] = 'taskjuggler3'
        os.environ['TASKJUGGLER_DATA_PATH'] = \
            os.path.pathsep.join(['./', '../'])
        os.environ['TZ'] = 'Europe/Istanbul'

    @classmethod
    def generate(cls):
        cls.process_directory('ReportGenerator/Correct')

    @classmethod
    def process_project(cls, tjp_file, output_dir):
        """No docstring at the origin

        :param tjp_file:
        :param output_dir:
        :return:
        """
        cls.delete_old_reports(tjp_file[0, -5])

        print("Generating references for %s" % tjp_file)

        tj = TaskJuggler()
        tj.parse([tjp_file])
        tj.schedule()
        tj.generate_reports(output_dir)

        if not tj.message_handler.messages:
            raise Exception(
                "Unexpected error in %{tjp_file}".format(tjp_file=tjp_file)
            )

    @classmethod
    def process_directory(cls, directory):
        """No docstring at the origin

        :param directory:
        :return:
        """
        print("Generating references in %s" % directory)
        path = os.path.dirname(__file__)
        project_dir = os.path.join(path, "TestSuite/%s/" % directory)
        output_dir = os.path.join(path, "TestSuite/%s/refs/" % directory)

        for f in glob.glob('%s/*.tjp' % project_dir):
            cls.process_project(f, output_dir)

    @classmethod
    def delete_old_reports(cls, basename):
        """No docstring at the origin

        :param basename:
        :return:
        """
        for ext in ['.csv', '.html']:
            for f in glob.glob('%s-[0-9]*.%s' % (basename, ext)):
                print("Removing old report %s" % f)
                os.remove(f)

    @classmethod
    def error(cls, text):
        """No docstring at the origin

        :param text:
        :return:
        """
        import sys
        sys.stderr.write(text)
        sys.exit(1)
