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



import os
import importlib
import argparse

import lib.person
reload(lib.person)


DIR = os.path.dirname(os.path.abspath(__file__))

class PersonSerializer(object):

    def __init__(self, person=None):

        self._person = person

    # import format library according to given file path' extension
    def _getSerializerObject(self, filePath):

        # assuming all given files will have extension for this project
        formatName = os.path.splitext(filePath)[1][1:].lower()
        libNameToCheck = '{}Lib'.format(formatName)

        try:
            module = importlib.import_module('formatLib.{}'.format(libNameToCheck))
        except ImportError as error:
            if isinstance(error, ImportError):
                raise Exception('This format is not supported: {}\nError: {}'.format(formatName, error))

        if not hasattr(module, 'Serializer'):
            raise NotImplementedError('You must implement Serializer class in your module.')

        return getattr(module, 'Serializer')

    # invoke serialize function
    def serialize(self, filePath):

        serializerInstance = self._getSerializerObject(filePath)(self._person)
        serializerInstance.serialize(filePath)

    # invoke deserialize function
    def deserialize(self, filePath):

        serializerInstance = self._getSerializerObject(filePath)()
        return serializerInstance.deserialize(filePath)

    # get supported formats as list
    @classmethod
    def getFormats(cls):

        try:
            module = importlib.import_module('formatLib')
        except (ImportError, Exception) as error:
            if isinstance(error, ImportError):
                raise error

        moduleDir = os.path.dirname(module.__file__)
        # get format library files by filtering out .pyc and __init__ files
        formatLibFileList = (f for f in os.listdir(moduleDir) if f.endswith('.py') and not f in ['__init__.py', 'serializerLib.py'])

        # strip "Lib.py" part from file name to get format name
        # consistency in code will provide this workflow to work
        formatList = []
        for formatItem in formatLibFileList:
            formatList.append(formatItem[:-6])
        return formatList


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', required=True, help='give absolute path of input')
    args = vars(ap.parse_args())

    deserializer = PersonSerializer()
    peopleList = deserializer.deserialize(args['input'])
    # peopleList = deserializer.deserialize(os.path.join(DIR, 'testFiles', 'person.json'))
    # peopleList = deserializer.deserialize(os.path.join(DIR, 'testFiles', 'person.xml'))

    print 'Deserialized Data'
    print '-' * 100
    for person in peopleList:
        print person


    print 'Serialization in Progress'
    print '-' * 100
    for person in peopleList:
        serializer = PersonSerializer(person)
        serializer.serialize(args['input'])
        # serializer.serialize(os.path.join(DIR, 'testFiles', 'person.json'))
        # serializer.serialize(os.path.join(DIR, 'testFiles', 'person.xml'))
        print person

    print PersonSerializer.getFormats()