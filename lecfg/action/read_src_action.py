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


from lecfg.action.action_result import ActionResult
from lecfg.conf.conf import Conf
from lecfg.action.action import Action
from lecfg.action.action_exception import ActionException
import subprocess


class ReadSrcAction(Action):
    """
    Action to call file reader on the src configuration file
    """

    def __init__(self, name: str, number: int, action_cmd: str):
        """
        Constructor

        Parameters
        ----------
        name: str
            name of the action
        number: int
            number of the action
        action_cmd: str
            system command to open a file reader when the this action is run
        """
        super().__init__(name, number)
        self.action_cmd = action_cmd

    def _read_file(self, file_path: str):
        try:
            subprocess.run([self.action_cmd, file_path], check=True,
                           stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise ActionException(e.cmd, e.returncode,
                                  e.stderr.decode('ascii'))

        # repeat the question after the edit
        return ActionResult.REPEAT

    def run(self, conf: Conf) -> ActionResult:
        return self._read_file(conf.src_path)
