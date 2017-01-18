"""
Copyright 2017 PERSADA TERBILANG SDN. BHD.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
import time
import os
from stat import *
from web_analytics.models import RequestLog


class Tail:

    def __init__(self, filename):
        self.filename = filename
        self.fp = None
        self.stat = None
        self.location = None

    def open_file(self):
        if self.fp:
            self.fp.close()
        self.fp = open(self.filename)
        self.stat = os.stat(self.filename)
        self.location = self.fp.tell()

    def check_rotate(self):
        try:
            new_stat = os.stat(self.filename)
            if self.stat[ST_INO] != new_stat[ST_INO]:
                print("File change")
                self.open_file()
            elif new_stat[ST_SIZE] < self.location:
                print("File truncated")
                self.open_file()
        except FileNotFoundError:
            pass

    def run(self):
        self.open_file()
        while True:
            while True:
                line = self.fp.readline()
                if not line:
                    break
                self.process_line(line)
            self.location = self.fp.tell()
            time.sleep(5)
            self.check_rotate()

    def process_line(self, line):
        RequestLog.parse_log_entry(entry=line)