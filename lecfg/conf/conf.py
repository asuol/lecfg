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


class Conf():
    """
    Representation of a package README configuration line
    """

    def __init__(self, src_path: str, dest_path: str, description: str,
                 version: str):
        """
        Constructor

        Parameters
        ----------
        src_path: str
            path to the configuration file
        dest_path: str
            path where the configuration file is to be deployed
        description: str
            description of the configuration file
        version: str
            version str for the package version to which the configuration file
            applies
        """
        self._src_path = src_path
        self._dest_path = dest_path
        self._description = description
        self._version = version

    @property
    def src_path(self) -> str:
        """
        Path to the configuration file
        """
        return self._src_path

    @src_path.setter
    def src_path(self, value) -> None:
        self._src_path = value

    @property
    def dest_path(self) -> str:
        """
        Path where the configuration file is to be deployed
        """
        return self._dest_path

    @dest_path.setter
    def dest_path(self, value) -> None:
        self._dest_path = value

    @property
    def description(self) -> str:
        """
        Description of the configuration file
        """
        return self._description

    @description.setter
    def description(self, value) -> None:
        self._description = value

    @property
    def version(self) -> str:
        """
        Version str for the package version to which the configuration file
        applies
        """
        return self._version

    @version.setter
    def version(self, value) -> None:
        self._version = value
