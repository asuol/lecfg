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

from typing import List


def user_input(question: List[str], options: List[str]) -> int:
    option_count = len(options)

    while True:
        try:
            for q in question:
                print(q)

            for i, o in enumerate(options):
                print("[%d] %s" % (i + 1, o))

            selection = int(input("\n> "))

            assert (selection >= 1 and
                    selection <= option_count)

            return selection - 1
        except ValueError:
            print_error("Please introduce a number")
        except AssertionError:
            print_error(
                "Please introduce a number between 1 and %d!" %
                option_count)


def print_error(msg: str) -> None:
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
