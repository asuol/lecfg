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


class ConfException(Exception):
    """
    LeCFG configuration exception
    """

    def __init__(self, conf_file_path: str, message: str,
                 line_num: int = None):
        """
        Constructor

        Parameters
        ----------
        conf_file_path: str
            path to the configuration file
        message: str
            exception message
        lin_num: int
            line of the configuration file where the error occurred
        """
        super().__init__(self._build_msg(conf_file_path, message, line_num))
        # for testing purposes
        self.line_num = line_num

    def _build_msg(self, conf_file_path: str, message: str,
                   line_num: int) -> str:
        """
        Builds an error message

        Parameters
        ----------
        conf_file_path: str
            path to the configuration file
        message: str
            exception message
        lin_num: int
            line of the configuration file where the error occurred

        Returns
        -------
        str
            the built error message
        """
        line_info = ""

        if line_num is not None:
            line_info = " at line %d" % line_num

        return "Error processing file \"%s\"%s: %s" % (conf_file_path,
                                                       line_info, message)
