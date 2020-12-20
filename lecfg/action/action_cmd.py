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

from typing import List


class ActionCmd():
    """
    Action command
    """

    def __init__(self, cmd: str, file_param_count: int):
        """
        Constructor

        Parameters
        ----------
        cmd: List[str]
            system command with parameters
        file_param_count: int
            number of file parameters to be received by the system command
            after the system command parameters

        """
        self.cmd = cmd.split(" ")
        self.file_param_count = file_param_count

    def runnable_command(self, file_params: List[str]) -> List[str]:
        """
        Returns a complete runnable command

        Parameters
        ----------
        file_params: List[str]
            file paths to be passed as arguments to the system command

        Returns
        -------
        A complete runnable command

        Raises
        ------
        AssertionError
            Raised if the number of provided file parameters does not match the
            expected number configured for the system command
        """
        assert(len(file_params) == self.file_param_count)

        run_cmd = self.cmd.copy()
        run_cmd.extend(file_params)

        return run_cmd
