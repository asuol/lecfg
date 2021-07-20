# -*- coding: utf-8 -*-

###
# MIT License
#
# Copyright (c) 2020 André Lousa Marques <andre.lousa.marques at gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###


from lecfg.conf.conf_parser import ConfParser
from lecfg.conf.conf import Conf
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

    def __init__(self, package_dir_path: str, system_name: str,
                 first_line: int = 0):
        """
        Constructor

        Parameters
        ----------
        package_dir_path: str
            path to the package directory
        system_name: str
            name of the system where lecfg is running
        first_line: int
            first line of the file. Ignore all previous lines

        Raises
        ------
        ConfException
            Raised if the provided package directory does not have a README
            file
        """
        try:
            super().__init__(self._readme_file_path(package_dir_path),
                             first_line)
        except FileNotFoundError:
            raise ConfException(self._readme_file_path(package_dir_path),
                                README_FILE_NOT_FOUND)
        self._package_dir_path = package_dir_path
        self._system_name = system_name

    def configurations(self) -> Conf:
        """
        Reads the next package configuration from the configuration file

        Returns
        -------
        Conf
            Conf object representing the next configuration
        """
        for package_conf in super().lines():
            package_conf_field_count = len(package_conf)

            if package_conf_field_count != PACKAGE_CONF_FIELD_COUNT:
                message = ("Expected %d fields but got %d" %
                           (PACKAGE_CONF_FIELD_COUNT,
                            package_conf_field_count))

                raise ConfException(os.path.join(self._package_dir_path,
                                                 README_FILE_NAME), message,
                                    self.line_num)

            src_path = os.path.join(self._package_dir_path, package_conf[0])
            version = package_conf[1]
            system_list = package_conf[2].split(',')
            dest_path = package_conf[3]
            description = package_conf[4]

            if(system_list[0] == "-"
               or
               self._system_name in system_list
               ):
                yield Conf(src_path, dest_path, description, version)

    def _readme_file_path(self, work_dir_path: str) -> str:
        """
        Build path to the package README file

        Parameters
        ----------
        work_dir_path: str
            path to the work directory

        Returns
        -------
        str
            path to the package README File
        """
        return os.path.join(work_dir_path, README_FILE_NAME)
