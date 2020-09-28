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
from lecfg.conf.package_parser import PackageParser
from lecfg.conf.conf_exception import ConfException
from lecfg.session_manager import SessionManager
from lecfg.conf.conf import Conf
from lecfg.action.read_src_action import ReadSrcAction
from lecfg.action.read_dest_action import ReadDestAction
from lecfg.action.save_exit_action import SaveExitAction
from lecfg.action.next_action import NextAction
from lecfg.action.deploy_action import DeployAction
from lecfg.action.replace_action import ReplaceAction
from lecfg.action.compare_action import CompareAction
from lecfg.action.action_result import ActionResult
from lecfg.action.action import Action
from lecfg.action.action_exception import ActionException
from pathlib import Path
from enum import Enum
from typing import List
import argparse
import os


class ExitCode(Enum):
    SAVE_AND_EXIT = 0
    SYSTEMS_FILE_NOT_FOUND = 1
    EMPTY_SYSTEMS_FILE = 2
    README_FILE_NOT_FOUND = 3


class Lecfg():
    """
    Lecfg main class
    """
    _question = "Please select an action:"
    _replace_question = "A file already exists at the destination. %s" % (
        _question)
    _deploy_question = "No file exists at the destination yet. %s" % (
        _question)

    _replace_options = [ReadSrcAction("Read src", 1, "less"),
                        ReadDestAction("Read dest", 2, "less"),
                        CompareAction("Compare", 3, "diff"),
                        ReplaceAction("Replace", 4),
                        NextAction("Skip", 5),
                        SaveExitAction("Save & exit", 6)]
    _deploy_options = [ReadSrcAction("Read src", 1, "less"),
                       DeployAction("Deploy", 2),
                       NextAction("Skip", 3),
                       SaveExitAction("Save & exit", 4)]

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

    def _print_error(self, msg: str) -> None:
        """
        Print error message

        Parameters
        ----------
        msg: str
            error message

        Returns
        -------
        None
        """
        print("\n** %s\n\n" % msg)

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
                  "name of one system" % sys_parser.get_file_path())
            exit(ExitCode.EMPTY_SYSTEMS_FILE.value)

        while True:
            try:
                print("Select the current system:\n")

                for i, s in enumerate(sys_parser.systems):
                    print("[%d] %s" % (i, s))

                selection = int(input("\n> "))

                assert (selection >= 0 and
                        selection < system_count)

                return sys_parser.systems[selection]
            except ValueError:
                self._print_error("Please introduce a number")
            except AssertionError:
                self._print_error(
                    "Please introduce a number between 0 and %d!" %
                    system_count)

    def _save_and_exit(self, package_name: str, line_num: int,
                       exit_code: int = ExitCode.SAVE_AND_EXIT) -> None:
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

    def _error_save_and_quit(self, package_name: str, package_readme_path: str,
                             line_num: int, error_msg: str,
                             exit_code: int) -> None:
        """
        Print error, save the current progress and exit

        Parameters
        ----------
        package_name: str
            name of the package being processed
        package_readme_path: str
            path to the current package README file
        line_num: int
            current line number in the given package README file
        error_msg: str
            error message
        exit_code: int
            exit code to return while exiting lecfg

        Returns
        -------
        None
        """
        print("Error while processing file \"%s\" at line %d: %s" %
              (package_readme_path, line_num, error_msg))
        print("The current state has been saved to and once you correct the "
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
        option_count = len(options)

        while True:
            try:
                print("\n\n\n[Configuration summary]")
                if conf.description is not None:
                    print("* Description:          %s" % conf.description)
                print("* File location:        %s" % conf.src_path)
                print("* Configuration target: %s" % conf.dest_path)
                print("* Applies to versions:  %s\n" % conf.version)

                print(question + "\n")

                print(" ".join([str(opt) for opt in options]))

                selection = int(input("\n> "))

                assert (selection >= 1 and
                        selection <= option_count)

                break
            except ValueError:
                self._print_error("Please introduce a number")
            except AssertionError:
                self._print_error(
                    "Please introduce a number between 1 and %d!" %
                    option_count)

        return options[selection - 1].run(conf)

    def _process_package(self, package_dir: str, current_system: str,
                         previous_session: str) -> None:
        """
        Process a package directory

        Parameters
        ----------
        package_dir: str
            path to the current package directory
        current_system: str
            name of the current system
        previous_session: str
            path to a previous session file or None if there is no previous
            session

        Returns
        -------
        None
        """
        print("Processing [ %s ]\n" % package_dir)

        try:
            package = PackageParser(package_dir, current_system)
        except ConfException as e:
            self.error_save_and_exit(e, ExitCode.README_FILE_NOT_FOUND.value)

        try:
            for conf in package.configurations():
                if Path(conf.dest_path).exists():
                    question = self._replace_question
                    options = self._replace_options
                else:
                    question = self._deploy_question
                    options = self._deploy_options

                while True:
                    result = self._ask_question(question, options, conf)

                    if result is not ActionResult.REPEAT:
                        break

                if result is ActionResult.SAVE_AND_EXIT:
                    self._save_and_exit(package_dir, package.line_num)
        except ActionException as e:
            print(str(e))
            # TODO: save and exit

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
            self._error_save_and_exit(e, ExitCode.SYSTEMS_FILE_NOT_FOUND.value)

        current_system = self._select_system(sys_parser)
        print("\nCurrent system: [ %s ]" % current_system)

        prev_session = self._session_man.get_previous_session()

        print("\nDetected package directories:")

        (_, sub_directories, _) = next(os.walk(self.work_dir))
        package_directories = []

        for sub_dir in sub_directories:
            package_directories.append(os.path.join(self.work_dir, sub_dir))
            print("    [ %s ]" % sub_dir)

        print("\n>>>>>>>>>>>>>>>>>>>>LeCFG START>>>>>>>>>>>>>>>>>>>>\n")

        for package_dir in package_directories:
            self._process_package(package_dir, current_system, prev_session)

        print("\n<<<<<<<<<<<<<<<<<<<<<LeCFG END<<<<<<<<<<<<<<<<<<<<<\n")


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-y, --replace-all", help="Assume \"Replace\" as"
                            " the answer for all questions regarding existing"
                            " configuration in the current system"
                            " configuration with a symbolic link",
                            action="store_true")
    arg_parser.add_argument("-n, --dry-run", help="Do a dry-run to ensure that"
                            " all the README.lc files are valid. Despite this"
                            " option, whenever the tool finds an error it"
                            " saves the current state while you correct the"
                            " detected problem and resumes where it left off"
                            " next time you load it.", action="store_true")
    arg_parser.add_argument("work_dir", help="Working directory from"
                            " which the script operates (defaults to the"
                            " current directory)", type=str)
    arg_parser.add_argument("-c, --checksum", help="Calculate SHA-512 hash of"
                            " the provided work directory and request"
                            " the user to confirm if the calculated hash is"
                            " the expected", action="store_true")

    args = arg_parser.parse_args()

    lecfg = Lecfg(args.work_dir)

    lecfg.process()
