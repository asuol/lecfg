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
from lecfg.action.action_cmd import ActionCmd
from lecfg.action.action_exception import ActionException
import subprocess
import os


class ReadSrcAction(Action):
    """
    Action to call file reader on the src configuration file
    """

    def __init__(self, name: str, read_file_cmd: ActionCmd, read_dir_cmd:
                 ActionCmd):
        """
        Constructor

        Parameters
        ----------
        name: str
            name of the action
        read_file_cmd: ActionCmd
            system command to open a file reader when this action is run
            against a file
        read_dir_cmd: ActionCmd
            system command to list directory contents when this action is run
            against a directory
        """
        super().__init__(name)
        self._read_file_cmd = read_file_cmd
        self._read_dir_cmd = read_dir_cmd

    def _read(self, file_path: str):
        if os.path.isfile(file_path):
            cmd = self._read_file_cmd
        else:
            cmd = self._read_dir_cmd

        try:
            run_cmd = cmd.runnable_command([file_path])
            subprocess.run(run_cmd, check=True,
                           stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise ActionException(e.cmd, e.returncode,
                                  e.stderr.decode('ascii'))

        # repeat the question after the edit
        return ActionResult.REPEAT

    def run(self, conf: Conf) -> ActionResult:
        return self._read(conf.src_path)
