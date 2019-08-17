#!/usr/bin/python
#
# Copyright (C) 2019 by Burak Ertekin.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation under the terms of the GNU General Public License is hereby
# granted. No representations are made about the suitability of this software
# for any purpose. It is provided "as is" without express or implied warranty.
# See the GNU General Public License for more details.
#


# generic serializer class to be inherited in all supported formats
class Serializer(object):

    def __init__(self, person=None):

        self._person = person

    def serialize(self, filePath):

        raise NotImplementedError('You must implement serialize method in your child class.')

    def deserialize(self, filePath):

        raise NotImplementedError('You must implement deserialize method in your child class.')

    def read(self, filePath):

        _file = open(filePath, 'r')
        _content = _file.read()
        _file.close()

        return _content

    def write(self, filePath, content):

        _file = open(self._file, 'w')
        _file.write(content)
        _file.close()

        return True