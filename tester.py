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
import unittest
import shutil
import xml.etree.ElementTree as ET

import formatLib.jsonLib
reload(formatLib.jsonLib)
import formatLib.xmlLib
reload(formatLib.xmlLib)
import handler
reload(handler)
import lib.person
reload(lib.person)

class Tester(unittest.TestCase):

    # setup temp test directory and some init some variables
    def setUp(self):

        self._testFileDir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testFiles'))
        self._tempTestDir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test'))

        if not os.path.isdir(self._tempTestDir):
            os.makedirs(self._tempTestDir)

        self._testPerson  = lib.person.Person(name='Test name', address='Test address string', phone='123456789')

    # clean temp test directory
    def tearDown(self):
        shutil.rmtree(self._tempTestDir)

    # checking serialization for json file format
    def test_jsonSerialization(self):
        data = {'root':[]}
        # create json serializer object
        jsonSerializer = formatLib.jsonLib.Serializer()
        jsonSerializer._person = self._testPerson
        _file = os.path.join(self._tempTestDir, 'testJson.json')
        # create an empty json file with proper root key
        jsonSerializer.write(_file, data)
        # test serialize function
        jsonSerializer.serialize(_file)
        # read serialized data and compare to data in setup function
        newData = jsonSerializer.read(_file)['root'][0]
        self.assertEqual(newData['name'], self._testPerson.name)
        self.assertEqual(newData['address'], self._testPerson.address)
        self.assertEqual(newData['phone'], self._testPerson.phone)
        # remove test file
        os.remove(_file)

    # checking deserialization for json file format
    def test_jsonDeserialization(self):
        # create json deserializer object
        jsonDeserializer = formatLib.jsonLib.Serializer()
        _testFilePath = os.path.join(self._testFileDir, 'person.json')
        # read contents of test json file to compare deserialized data
        data = jsonDeserializer.read(_testFilePath)
        _file = os.path.join(self._tempTestDir, 'testJson.json')
        # copy test file to testing directory
        shutil.copyfile(_testFilePath, _file)
        # test deserialize function
        peopleList = jsonDeserializer.deserialize(_file)
        self.assertEqual(data['root'][0]['name'], peopleList[0].name)
        # remove test file
        os.remove(_file)

    # checking serialization for xml file format
    def test_xmlSerialization(self):
        data = ET.Element('root')
        # create xml serializer object
        xmlSerializer = formatLib.xmlLib.Serializer(self._testPerson)
        _file = os.path.join(self._tempTestDir, 'testXml.xml')
        # create xml file with root element
        xmlSerializer.write(_file, data)
        # test serialize function
        xmlSerializer.serialize(_file)
        # read serialized data and compare to data in setup function
        newData = xmlSerializer.read(_file)[0]
        self.assertEqual(newData.attrib['name'], self._testPerson.name)
        self.assertEqual(newData.attrib['address'], self._testPerson.address)
        self.assertEqual(newData.attrib['phone'], self._testPerson.phone)
        # remove test file
        os.remove(_file)

    # checking to see if we get same result from deserialization of two different file formats with same data
    def test_consistency(self):
        # create generic deserializer
        deserializer = handler.PersonSerializer()
        _testXMLFilePath = os.path.join(self._testFileDir, 'person.xml')
        _testJSONFilePath = os.path.join(self._testFileDir, 'person.json')
        # json deserialization
        jsonPeopleList = deserializer.deserialize(_testJSONFilePath)
        # xml deserialization
        xmlPeopleList = deserializer.deserialize(_testXMLFilePath)
        # compare two people list
        self.assertEqual(jsonPeopleList[0].name, xmlPeopleList[0].name)
        self.assertEqual(jsonPeopleList[1].name, xmlPeopleList[1].name)
        self.assertEqual(jsonPeopleList[2].address, xmlPeopleList[2].address)
        self.assertEqual(jsonPeopleList[3].phone, xmlPeopleList[3].phone)
        # serialize back to save the files
        for person in list(jsonPeopleList):
            serializer = handler.PersonSerializer(person)
            serializer.serialize(_testJSONFilePath)
            serializer.serialize(_testXMLFilePath)

if __name__ == '__main__':
    unittest.main()