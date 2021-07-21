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

from lecfg.conf.systems_parser import SystemsParser
from lecfg.conf.package_parser import PackageParser, README_FILE_NAME
from lecfg.conf.conf_exception import ConfException
from lecfg.session_manager import SessionManager
from lecfg.session import Session
from lecfg.conf.conf import Conf
from lecfg.action.read_src_action import ReadSrcAction
from lecfg.action.read_dest_action import ReadDestAction
from lecfg.action.save_exit_action import SaveExitAction
from lecfg.action.next_action import NextAction
from lecfg.action.next_package import NextPackage
from lecfg.action.deploy_action import DeployAction
from lecfg.action.no_parent_deploy_action import NoParentDeployAction
from lecfg.action.replace_action import ReplaceAction
from lecfg.action.compare_action import CompareAction
from lecfg.action.action_result import ActionResult
from lecfg.action.action import Action
from lecfg.action.action_cmd import ActionCmd
from lecfg.action.action_exception import ActionException
from lecfg.utilities import user_input
from lecfg.exit_code import ExitCode
from pathlib import Path
from typing import List
import os

READ_CMD_FILE = "read.cmd"
COMPARE_CMD_FILE = "compare.cmd"

READ_CMD_FILE_PARAM_CNT = 1
CMP_CMD_FILE_PARAM_CNT = 2

DEFAULT_READ_CMD = "less"
DEFAULT_CMP_CMD = "diff -u"


class Lecfg():
    """
    Lecfg main class
    """
    _question = "Please select an action:"
    _replace_question = "A file already exists at the destination. %s" % (
        _question)
    _deploy_question = "No file exists at the destination yet. %s" % (
        _question)
    _no_parent_deploy_question = ("No file exists at the destination yet "
                                  "(dest dir also does not exist). %s" %
                                  _question)

    def __init__(self, work_dir: str):
        """
        Constructor

        Parameters
        ----------
        work_dir: str
            path to the work directory
        """
        self.work_dir = work_dir
        self._session_man = SessionManager(work_dir)

    def _select_system(self, sys_parser: SystemsParser) -> str:
        """
        Select the name of current system

        Parameters
        ----------
        sys_parser: SystemsParser
            SystemsParser object for the current work directory

        Returns
        -------
        str
            The name of the current system
        """
        system_count = len(sys_parser.systems)
        if system_count == 1:
            return sys_parser.systems[0]
        elif system_count == 0:
            print("Systems file \"%s\" is empty! Please indicate at least the "
                  "name of one system" % sys_parser.file_path)
            exit(ExitCode.EMPTY_SYSTEMS_FILE.value)

        question = ["Select the current system:\n"]

        selection = user_input(question, sys_parser.systems)

        return sys_parser.systems[selection]

    def _save_and_exit(self, package_name: str, line_num: int,
                       exit_code: int = ExitCode.SAVE_AND_EXIT.value) -> None:
        """
        Save the current progress and exit

        Parameters
        ----------
        package_name: str
            name of the package being processed
        line_num: int
            current line number in the given package README file
        exit_code: int
            exit code to return while exiting lecfg

        Returns
        -------
        None
        """
        self._session_man.save_session(package_name, line_num)

        exit(exit_code)

    def _error_save_and_exit(self, package_name: str, error_msg: str,
                             exit_code: int,
                             package: PackageParser = None) -> None:
        """
        Print error, save the current progress and exit

        Parameters
        ----------
        package_name: str
            name of the package being processed
        error_msg: str
            error message
        exit_code: int
            exit code to return while exiting lecfg
        package: PackageParser
            package parser object

        Returns
        -------
        None
        """
        if package is not None:
            line_num = package.line_num
            print("Error while processing file \"%s\" at line %d: %s" %
                  (package.file_path, line_num, error_msg))
        else:
            print(error_msg)
            line_num = None

        print("The current state has been saved and once you correct the "
              "error lecfg will resume from this point")

        self._save_and_exit(package_name, line_num, exit_code)

    def _ask_question(self, question: str, options: List[Action], conf: Conf):
        """
        Ask a question to the user about the configuration under process

        Parameters
        ----------
        question: str
            question to present to the user
        options: List[Action]
            list of actions that the user can select to answer the question
        conf: Conf
            configuration under process

        Returns
        -------
        None
        """
        print("   --------------------------------------------\n")
        print("Handling configuration file:\n")
        print("* Source path [src]:       %s" % conf.src_path)
        print("* Destination path [dest]: %s\n" % conf.dest_path)

        if conf.description is not None:
            print("* Description:             %s" % conf.description)

        print("* Applies to versions:     %s\n" % conf.version)
        query = []
        query.append(question + "\n")

        selection = user_input(query, options)

        return options[selection].run(conf)

    def _process_package(self, package_dir: str, current_system: str,
                         previous_session: Session) -> None:
        """
        Process a package directory

        Parameters
        ----------
        package_dir: str
            path to the current package directory. It acts as the package name
        current_system: str
            name of the current system
        previous_session: Session
            previous session or None if there is no previous
            session

        Returns
        -------
        Session
            previous session (if one was provided and the system has not
            resumed it yet), or None if no previous_session was provided or if
            the system has already resumed it
        """
        if (previous_session is not None
           and previous_session.package_dir != package_dir):
            # we are resuming a previous session and this is not the package we
            # left on
            print("Resuming previous session ... skipping [ %s ]..." %
                  package_dir)
            return previous_session

        print("Processing package directory: [ %s ]\n" % package_dir)

        try:
            if previous_session is not None:
                package = PackageParser(package_dir, current_system,
                                        previous_session.line_num)
            else:
                package = PackageParser(package_dir, current_system)
        except ConfException as e:
            error_msg = "Error creating package parser: %s" % str(e)
            self._error_save_and_exit(package_dir, error_msg,
                                      ExitCode.README_FILE_NOT_FOUND.value)

        has_configuration = False

        try:
            for conf in package.configurations():
                has_configuration = True
                if(Path(conf.dest_path).exists()
                   or
                   Path(conf.dest_path).is_symlink()
                   ):
                    question = self._replace_question
                    options = self._replace_options
                elif Path(conf.dest_path).parent.exists():
                    question = self._deploy_question
                    options = self._deploy_options
                else:
                    question = self._no_parent_deploy_question
                    options = self._no_parent_deploy_options

                while True:
                    result = self._ask_question(question, options, conf)

                    if result is not ActionResult.REPEAT:
                        break

                if result is ActionResult.SAVE_AND_EXIT:
                    self._save_and_exit(package_dir, package.line_num)
                elif result is ActionResult.NEXT_PACKAGE:
                    break
        except ActionException as e:
            self._error_save_and_exit(package_dir, str(e),
                                      ExitCode.ACTION_ERROR.value, package)
        except ConfException as e:
            self._error_save_and_exit(package_dir, str(e),
                                      ExitCode.INVALID_README_FORMAT.value,
                                      package)

        if not has_configuration:
            print("No configuration defined for package [ %s ]."
                  " Skipping...\n" % package_dir)

        return None

    def _read_cmd_conf(self, conf_file_name: str,
                       file_param_count: int) -> ActionCmd:
        file_path = os.path.join(self.work_dir, conf_file_name)

        if os.path.exists(file_path):
            with open(file_path, "r") as conf:
                cmd = conf.readline()
                if cmd == "":
                    print("%s file found, but it is empty. Ignoring..." %
                          conf_file_name)
                    return None
            return ActionCmd(cmd, file_param_count)

        return None

    def process(self) -> None:
        """
        Process the given work directory

        Returns
        -------
        None
        """
        print("  _            _____ ______  _____ ")
        print(" | |          /  __ \\|  ___||  __ \\")
        print(" | |      ___ | /  \\/| |_   | |  \\/")
        print(" | |     / _ \\| |    |  _|  | | __")
        print(" | |____|  __/| \\__/\\| |    | |_\\ \\")
        print(" \\_____/ \\___| \\____/\\_|     \\____/")
        print("\n")

        print("\nChecking the systems file...\n")

        try:
            sys_parser = SystemsParser(self.work_dir)
        except ConfException as e:
            print(str(e))
            exit(ExitCode.SYSTEMS_FILE_NOT_FOUND.value)

        current_system = self._select_system(sys_parser)
        print("\nCurrent system: [ %s ]\n" % current_system)

        read_cmd = self._read_cmd_conf(READ_CMD_FILE, READ_CMD_FILE_PARAM_CNT)
        compare_cmd = self._read_cmd_conf(COMPARE_CMD_FILE,
                                          CMP_CMD_FILE_PARAM_CNT)

        if read_cmd is None:
            read_cmd = ActionCmd(DEFAULT_READ_CMD, READ_CMD_FILE_PARAM_CNT)

        if compare_cmd is None:
            compare_cmd = ActionCmd(DEFAULT_CMP_CMD, CMP_CMD_FILE_PARAM_CNT)

        self._replace_options = [ReadSrcAction("Read src", read_cmd),
                                 ReadDestAction("Read dest", read_cmd),
                                 CompareAction("Compare", compare_cmd),
                                 ReplaceAction("Replace"),
                                 NextAction("Skip"),
                                 NextPackage("Skip to next package"),
                                 SaveExitAction("Save & exit")]

        self._deploy_options = [ReadSrcAction("Read src", read_cmd),
                                DeployAction("Deploy"),
                                NextAction("Skip"),
                                NextPackage("Skip to next package"),
                                SaveExitAction("Save & exit")]

        self._no_parent_deploy_options = [
            ReadSrcAction("Read src", read_cmd),
            NoParentDeployAction("Create dest directory and deploy"),
            NextAction("Skip"),
            NextPackage("Skip to next package"),
            SaveExitAction("Save & exit")]

        prev_session = self._session_man.get_previous_session()

        print("\nDetected package directories:")

        (_, sub_directories, _) = next(os.walk(self.work_dir))
        package_directories = []

        for sub_dir in sub_directories:
            sub_dir_path = os.path.join(self.work_dir, sub_dir)
            readme_file = Path(sub_dir_path) / README_FILE_NAME

            if readme_file.exists():
                package_directories.append(sub_dir_path)
                print("    [ %s ]" % sub_dir)

        print("\n>>>>>>>>>>>>>>>>>>>>LeCFG START>>>>>>>>>>>>>>>>>>>>\n")

        for package_dir in package_directories:
            prev_session = self._process_package(package_dir, current_system,
                                                 prev_session)

        print("\n<<<<<<<<<<<<<<<<<<<<<LeCFG END<<<<<<<<<<<<<<<<<<<<<\n")
