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

from lecfg.lecfg import Lecfg
import argparse


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
