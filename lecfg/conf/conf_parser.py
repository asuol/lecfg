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


class ConfParser():
    """
    Configuration parser
    """

    def __init__(self, file_path: str):
        """
        Constructor

        Parameters
        ----------
        file_path: str
            configuration file path

        Raises
        ------
        FileNotFoundException
            if the given file path does not exist
        """
        self._file_path = file_path
        self._conf_file = open(file_path, "r")
        self._line_num = 0

    @property
    def file_path(self) -> str:
        """
        Configuration file path
        """
        return self._file_path

    @file_path.setter
    def file_path(self, value) -> None:
        self._file_path = value

    @property
    def line_num(self) -> int:
        """
        Return the current file number
        """
        return self._line_num

    @line_num.setter
    def line_num(self, value) -> None:
        self._line_num = value

    def lines(self) -> str:
        """
        Generator function

        Returns
        -------
        str
            the next line from the configuration file
        """
        for line_num, line in enumerate(self._conf_file):
            # ignore empty lines and comments
            if line.isspace() or line.lstrip().startswith("#"):
                continue
            self._line_num = line_num
            yield list(map(lambda l: l.strip(), line.split('|')))

        self._conf_file.close()
