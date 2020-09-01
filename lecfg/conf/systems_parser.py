"""
MIT License

Copyright (c) 2020 André Lousa Marques <andre.lousa.marques at gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from lecfg.conf.conf_parser import ConfParser
from lecfg.conf.conf_exception import ConfException
import os

SYSTEMS_FILE_NAME = "lecfg.systems"

SYSTEMS_FILE_NOT_FOUND = ("The provided work directory is missing "
                          "the systems file: %s" % SYSTEMS_FILE_NAME)


class SystemsParser(ConfParser):
    """
    Parser class for LECFG system.lecfg files
    """
    def __init__(self, work_dir_path):
        try:
            super().__init__(self._systems_file_path(work_dir_path))
        except FileNotFoundError:
            raise ConfException(self._systems_file_path(work_dir_path),
                                SYSTEMS_FILE_NOT_FOUND)
        self.systems = []
        for line in super().lines():
            self.systems.append(line[0])

    def get_systems(self):
        return self.systems

    def is_valid(self, system_name):
        return system_name in self.systems

    def _systems_file_path(self, work_dir_path):
        return os.path.join(work_dir_path, SYSTEMS_FILE_NAME)
