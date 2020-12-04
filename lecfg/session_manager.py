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

from datetime import datetime
from lecfg.session import Session
from pathlib import Path
from lecfg.utilities import user_input

SAVE_FILE_SUFFIX = "_lecfg.sav"


class SessionManager():
    """
    LeCfg session manager
    """

    def __init__(self, work_dir_path: str):
        """
        Constructor

        Parameters
        ----------
        work_dir_path: str
            path to the work directory
        """
        self._work_dir_path = work_dir_path

    def get_previous_session(self) -> Session:
        """
        Get the previous session. If multiple sessions exist let the user
        select.

        Returns
        -------
        Session
            Return the previous session or None if none exists
        """
        previous_sessions = list(Path(self._work_dir_path).glob(
            "*%s" % SAVE_FILE_SUFFIX))
        session_count = len(previous_sessions)

        if session_count > 1:
            question = ["Multiple sessions available. Please select one:"]

            selection = user_input(question, previous_sessions)

            return Session(str(previous_sessions[selection]))

        if session_count == 1:
            return Session(str(previous_sessions[0]))

        return None

    def save_session(self, package_dir: str, line_num: int) -> None:
        """
        Save current session to resume later

        Parameters
        ----------
        package_dir: str
            package directory path being processed
        line_num: int
            current line number in the given package README file

        Returns
        -------
        None
        """

        file_name = datetime.utcnow().strftime("%d-%m-%Y_%H-%M")
        file_name += SAVE_FILE_SUFFIX

        save_file_path = str(Path(self._work_dir_path) / file_name)

        with open(save_file_path, "w") as save_file:
            save_file.write(package_dir + "," + str(line_num))
