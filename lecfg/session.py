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


class Session():
    """
    LeCfg session
    """

    def __init__(self, file_path: str):
        """
        Constructor

        Parameters
        ----------
        file_path: str
            session file path

        Raises
        ------
        FileNotFoundException
            if the given file path does not exist
        """
        self._file_path = file_path

        with open(file_path, "r") as session_file:
            fields = list(map(lambda l: l.strip(),
                              session_file.readline().split(",")))

            self._package_name = fields[0]
            self._line_num = fields[1]

    @property
    def package_name(self) -> str:
        """
        Package name where to resume
        """
        return self._package_name

    @package_name.setter
    def package_name(self, value) -> None:
        self._package_name = value

    @property
    def line_num(self) -> int:
        """
        Line number where to resume
        """
        return self._line_num

    @line_num.setter
    def line_num(self, value) -> None:
        self._line_num = value