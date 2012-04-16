#!/usr/bin/env python
#
# Copyright 2011-2012 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys
import unittest

import splunklib.client as client
from utils import parse

opts = None # Command line options

class TestCase(unittest.TestCase):
    def check_content(self, entity, **kwargs):
        for k, v in kwargs.iteritems(): 
            self.assertEqual(entity[k], str(v))

    def test(self):
        event_types = client.connect(**opts.kwargs).event_types

        if 'sdk-test' in event_types:
            event_types.delete('sdk-test')
        self.assertFalse('sdk-test' in event_types)

        for event_type in event_types:
            event_type.content.description
            event_type.content.priority
            event_type.content.search

        kwargs = {}
        kwargs['search'] = "index=_internal *"
        kwargs['description'] = "An internal event"
        kwargs['disabled'] = 1
        kwargs['priority'] = 2

        event_type = event_types.create('sdk-test', **kwargs)
        self.assertTrue('sdk-test' in event_types)

        self.assertEqual('sdk-test', event_type.name)
        self.check_content(event_type, **kwargs)

        kwargs['search'] = "index=_audit *"
        kwargs['description'] = "An audit event"
        kwargs['priority'] = 3
        event_type.update(**kwargs)
        event_type.refresh()
        self.check_content(event_type, **kwargs)

        event_type.enable()
        event_type.refresh()
        self.check_content(event_type, disabled=0)

        event_types.delete('sdk-test')
        self.assertFalse('sdk-teset' in event_types)

if __name__ == "__main__":
    opts = parse(sys.argv[1:], {}, ".splunkrc")
    unittest.main(argv=sys.argv[:1])
