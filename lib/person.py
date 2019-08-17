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

# basic person class to hold contact info: name, address, phone
class Person(object):

    def __init__(self, name=None, address=None, phone=None):

        self.name = name
        self.address = address
        self.phone = phone

    def __eq__(self, other):

        return self.name == other.name and self.address == other.address and self.phone == other.phone

    def __str__(self):

        return '\nName: {}\nAddress: {}\nPhone: {}'.format(self.name, self.address, self.phone)