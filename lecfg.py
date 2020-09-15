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
from datetime import datetime
from pathlib import Path
from enum import Enum
import argparse
import os

SAVE_FILE_SUFFIX = "_lecfg.sav"


class ExitCode(Enum):
    SYSTEMS_FILE_NOT_FOUND = 1
    EMPTY_SYSTEMS_FILE = 2
    README_FILE_NOT_FOUND = 3


class Lecfg():
    """
    Lecfg main class
    """

    def __init__(self, work_dir: str):
        """
        Constructor

        Parameters
        ----------
        work_dir: str
            path to the work directory
        """
        self.work_dir = work_dir

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

    def _save_and_exit(self, package_readme: str, line_num: int,
                       exit_code: int) -> None:
        """
        Save the current progress and exit

        Parameters
        ----------
        package_readme: str
            path to the current package README file
        line_num: int
            current line number in the given package README file
        exit_code: int
            exit code to return while exiting lecfg

        Returns
        -------
        None
        """
        file_name = datetime.utcnow().strftime("%d-%m-%Y_%H-%M")
        file_name += SAVE_FILE_SUFFIX

        save_file_path = str(Path(self.work_dir) / file_name)

        with open(save_file_path, "w") as save_file:
            save_file.write(package_readme + "," + line_num)

        exit(exit_code)

    def _error_save_and_quit(self, package_readme: str, line_num: int,
                             error_msg: str, exit_code: int) -> None:
        """
        Print error, save the current progress and exit

        Parameters
        ----------
        package_readme: str
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
              (package_readme, line_num, error_msg))
        print("The current state has been saved to and once you correct the "
              "error lecfg will resume from this point")

        self._save_and_exit(package_readme, line_num, exit_code)

    def _process_package(self, package_dir: str, current_system: str) -> None:
        """
        Process a package directory

        Parameters
        ----------
        package_dir: str
            path to the current package directory
        current_system: str
            name of the current system

        Returns
        -------
        None
        """
        print("Processing [ %s ]\n" % package_dir)

        try:
            package = PackageParser(package_dir, current_system)
        except ConfException as e:
            self.error_save_and_exit(e, ExitCode.README_FILE_NOT_FOUND.value)

        for conf in package.configurations():
            print("Conf is: %s | %s | %s | %s" % (conf.src_path,
                                                  conf.dest_path,
                                                  conf.description,
                                                  conf.version))

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

        print("\nDetected package directories:")

        (_, sub_directories, _) = next(os.walk(self.work_dir))
        package_directories = []

        for sub_dir in sub_directories:
            package_directories.append(os.path.join(self.work_dir, sub_dir))
            print("    [ %s ]" % sub_dir)

        print("\n>>>>>>>>>>>>>>>>>>>>LeCFG START>>>>>>>>>>>>>>>>>>>>\n")

        for package_dir in package_directories:
            self._process_package(package_dir, current_system)

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
