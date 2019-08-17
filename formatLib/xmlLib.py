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

import xml.etree.ElementTree as ET

import serializerLib
reload(serializerLib)
import lib.person
reload(lib.person)

# xml serializer
# in order to obtain multiple line person data input, added a "root" tag for person data list
# this tag is needed in root to use this serializer
class Serializer(serializerLib.Serializer):

    def __init__(self, person=None):
        serializerLib.Serializer.__dict__['__init__'](self, person)

    def serialize(self, filePath):

        # get person data
        content = {'name': str(self._person.name), 'address': str(self._person.address), 'phone': str(self._person.phone)}

        # read existing content and append person data
        root = self.read(filePath)
        ET.SubElement(root, 'person', attrib=content)

        # write new content to file
        self.write(filePath, root)

    def deserialize(self, filePath):

        # read people file
        root = self.read(filePath)

        peopleList = []
        for elem in list(root):
            peopleList.append(lib.person.Person(name=elem.attrib['name'], address=elem.attrib['address'], phone=elem.attrib['phone']))
            root.remove(elem)

        # write clean list back to file
        self.write(filePath, root)

        return peopleList

    def read(self, filePath):
        try:
            root = ET.parse(filePath).getroot()
        except ET.ParseError:
            root = ET.Element('root')

        return root

    def write(self, filePath, root):
        tree = ET.ElementTree(root)
        tree.write(filePath, method='xml')