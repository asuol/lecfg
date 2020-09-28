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
from abc import ABC


class Action(ABC):
    """
    Action abstract class
    """

    def __init__(self, name: str, number: int):
        """
        Constructor

        Parameters
        ----------
        name: str
            name of the action
        number: int
            number of the action
        """
        self._name = name
        self._number = number

    def __str__(self) -> str:
        return "[%d] %s" % (self._number, self._name)

    def run(self, conf: Conf) -> ActionResult:
        """
        Run action (abstract method)

        Parameters
        ----------
        conf: Conf
            Configuration object under processing

        Returns
        -------
        ActionResult
            user decision on the action
        """
        pass
