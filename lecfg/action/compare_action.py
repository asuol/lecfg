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


class CompareAction(Action):
    """
    Action to call diff utility to compare the src and dest configuration files
    """

    def __init__(self, name: str, cmp_file_cmd: ActionCmd,
                 cmp_dir_cmd: ActionCmd):
        """
        Constructor

        Parameters
        ----------
        name: str
            name of the action
        cmp_file_cmd: ActionCmd
            system command to compare file contents when this action is run
            against two files
        cmp_dir_cmd: ActionCmd
            system command to compare directory contents when this action isi
            run against two directories
        """
        super().__init__(name)
        self._cmp_file_cmd = cmp_file_cmd
        self._cmp_dir_cmd = cmp_dir_cmd

    def run(self, conf: Conf) -> ActionResult:
        if os.path.isfile(conf.src_path) and os.path.isfile(conf.dest_path):
            cmd = self._cmp_file_cmd
        elif os.path.isdir(conf.src_path) and os.path.isdir(conf.dest_path):
            cmd = self._cmp_dir_cmd

        try:
            run_cmd = cmd.runnable_command([conf.dest_path,
                                            conf.src_path])
            subprocess.run(run_cmd,
                           check=True, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            # diff uses exitcode 1 to signal that the files differ
            # and not that an error occurred
            if e.returncode != 1:
                raise ActionException(e.cmd, e.returncode,
                                      e.stderr.decode('ascii'))

        # repeat the question after the comparison
        return ActionResult.REPEAT
