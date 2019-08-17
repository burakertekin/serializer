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


import json

import serializerLib
reload(serializerLib)
import lib.person
reload(lib.person)

# json serializer
# in order to obtain multiple line person data input, added a "root" key for person data list
# this key is needed in dict to use this serializer
class Serializer(serializerLib.Serializer):

    def __init__(self, person=None):
        serializerLib.Serializer.__dict__['__init__'](self, person)

    def serialize(self, filePath):

        # get person data
        content = {'name': self._person.name, 'address': self._person.address, 'phone': self._person.phone}

        # read existing content and append person data
        data = self.read(filePath)
        data['root'].append(content)

        # write new content to file
        self.write(filePath, data)

    def deserialize(self, filePath):

        # read people file
        data = self.read(filePath)

        # list all people from file data, remove listed ones
        peopleList = []
        for item in list(data['root']):
            peopleList.append(lib.person.Person(name=item['name'], address=item['address'], phone=item['phone']))
            data['root'].remove(item)

        # write clean list back to file
        self.write(filePath, data)

        return peopleList

    def read(self, filePath):
        with open(filePath, 'r') as inFile:
            try:
                data = json.load(inFile)
            except ValueError:
                data = {'root': []}
            return data

    def write(self, filePath, content):
        with open(filePath, 'w') as outFile:
            json.dump(content, outFile, sort_keys=True, indent=4)