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
from lecfg.action.deploy_action import DeployAction
from lecfg.action.action_exception import ActionException
from pathlib import Path


OLD_FILE_SUFFIX = ".lecfg.bak"


class ReplaceAction(DeployAction):
    """
    Action to replace an existing configuration with the src configuration file
    while keeping the existing configuration
    """

    def __init__(self, name: str):
        """
        Constructor

        Parameters
        ----------
        name: str
            name of the action
        """
        super().__init__(name)

    def run(self, conf: Conf) -> ActionResult:
        dest_path = Path(conf.dest_path)

        if dest_path.samefile(conf.src_path):
            # If the destination file is already a sym link to the src, just
            # return
            return ActionResult.NEXT

        dest_bak = dest_path.parent / (dest_path.name + OLD_FILE_SUFFIX)

        if Path(dest_bak).exists():
            raise ActionException("There is already a previous lecfg file "
                                  "backup at the destination. Please "
                                  "remove or rename it: %s" % dest_bak)

        dest_path = dest_path.replace(dest_bak)

        return self._deploy_conf(conf.src_path, conf.dest_path)
