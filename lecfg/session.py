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
        AssertionError
            if the session file format is invalid
        """
        self._file_path = file_path

        with open(file_path, "r") as session_file:
            fields = list(map(lambda l: l.strip(),
                              session_file.readline().split(",")))

            assert len(fields) > 1 and len(fields) <= 2, (
                "Invalid session file format")

            self._package_dir = fields[0]
            if len(fields) > 1:
                self._line_num = int(fields[1])
            else:
                self._line_num = None

    @property
    def package_dir(self) -> str:
        """
        Package dir path where to resume
        """
        return self._package_dir

    @property
    def line_num(self) -> int:
        """
        Line number where to resume
        """
        return self._line_num
