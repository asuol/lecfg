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
from lecfg.conf.conf_exception import ConfException
from typing import List
import os

SYSTEMS_FILE_NAME = "lecfg.systems"

SYSTEMS_FILE_NOT_FOUND = ("The provided work directory is missing "
                          "the systems file: %s" % SYSTEMS_FILE_NAME)


class SystemsParser(ConfParser):
    """
    Parser class for LECFG system.lecfg files
    """

    def __init__(self, work_dir_path: str):
        """
        Constructor

        Parameters
        ----------
        work_dir_path: str
            path to the work directory

        Raises
        ------
        ConfException
            Raised if the work directory does not have a systems file
        """
        try:
            super().__init__(self._systems_file_path(work_dir_path))
        except FileNotFoundError:
            raise ConfException(self._systems_file_path(work_dir_path),
                                SYSTEMS_FILE_NOT_FOUND)
        self._systems = []

        for line in super().lines():
            self._systems.append(line[0])

    @property
    def systems(self) -> List[str]:
        """
        List of systems configured for the given work directory
        """
        return self._systems

    @systems.setter
    def systems(self, value: List[str]) -> None:
        self._systems = value

    def is_valid(self, system_name: str) -> bool:
        """
        Check if a given system is a valid system for the given work directory

        Parameters
        ----------
        system_name: str
            any system name

        Returns
        -------
        bool
            True if the given system was configured on the work directory
            systems file
        """
        return system_name in self.systems

    def _systems_file_path(self, work_dir_path: str) -> str:
        """
        Build path to the package README file

        Parameters
        ----------
        work_dir_path: str
            path to the work directory

        Returns
        -------
        str
            path to the work directory systems file
        """
        return os.path.join(work_dir_path, SYSTEMS_FILE_NAME)
