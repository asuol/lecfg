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
from collections import namedtuple
from lecfg.conf.conf_exception import ConfException
import os


PACKAGE_CONF_FIELDS = ["conf_file", "version",
                       "system_list", "dest_path",
                       "description"]

PACKAGE_CONF_FIELD_COUNT = len(PACKAGE_CONF_FIELDS)

README_FILE_NAME = "README.lc"

README_FILE_NOT_FOUND = ("The package directory is missing "
                         "the README file: %s" % README_FILE_NAME)


class PackageParser(ConfParser):
    """
    Parser class for package README files
    """
    def __init__(self, package_dir_path, system_name):
        try:
            super().__init__(self._readme_file_path(package_dir_path))
        except FileNotFoundError:
            raise ConfException(self._readme_file_path(package_dir_path),
                                README_FILE_NOT_FOUND)
        self.package_dir_path = package_dir_path
        self.system_name = system_name

    def configurations(self):
        """
        Reads the next package configuration from the configuration file
        """
        for package_conf in super().lines():
            package_conf_field_count = len(package_conf)

            if package_conf_field_count != PACKAGE_CONF_FIELD_COUNT:
                message = ("Expected %d fields but got %d" %
                           (PACKAGE_CONF_FIELD_COUNT,
                            package_conf_field_count))

                raise ConfException(self.package_dir_path, message,
                                    self.line_num)

            user_conf = namedtuple("package_conf", PACKAGE_CONF_FIELDS)

            user_conf.conf_file = package_conf[0]
            user_conf.version = package_conf[1]
            user_conf.system_list = package_conf[2]
            user_conf.dest_path = package_conf[3]
            user_conf.description = package_conf[4]

            if(user_conf.system_list.strip() == "-"
               or
               self.system_name in user_conf.system_list
               ):
                yield user_conf

    def _readme_file_path(self, work_dir_path):
        return os.path.join(work_dir_path, README_FILE_NAME)
