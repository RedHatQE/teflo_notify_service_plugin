# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Red Hat, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
    Pykwalify extensions module.
    Module containing custom validation functions used for schema checking.
    :copyright: (c) 2020 Red Hat, Inc.
    :license: GPLv3, see LICENSE for more details.
"""


def check_targets(value, rule_obj, path):
    """Verify if the values of targets are from thi slist gchat/slack/email/irc/message_bus"""
    print(value)
    types = ['gchat', 'slack', 'email', 'irc', 'message_bus']
    list1 = value.replace(' ', '').split(',')

    if False in [item in types and isinstance(item, str) for item in list1]:
        raise AssertionError("Unknown target value found."
                             "Target should be one or more of this list: 'gchat,email,slack,irc,message_bus'")

    else:
        return True
