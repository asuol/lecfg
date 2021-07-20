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
from pathlib import Path


class NoParentDeployAction(DeployAction):
    """
    Action to deploy the src configuration file into the dest path when the
    dest path is missing at least one parent directory
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

    def _create_parent_and_deploy(self, src_path: str, dest_path: str
                                  ) -> ActionResult:
        # ensure the dest path parent directories are created
        dest_parent = Path(dest_path).parent
        dest_parent.mkdir(parents=True, exist_ok=True)

        # deploy the configuration
        return super()._deploy_conf(src_path, dest_path)

    def run(self, conf: Conf) -> ActionResult:
        return self._create_parent_and_deploy(conf.src_path, conf.dest_path)
