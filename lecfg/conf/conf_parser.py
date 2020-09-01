"""
MIT License

Copyright (c) 2020 André Lousa Marques <andre.lousa.marques at gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class ConfParser():
    """
    Configuration parser
    """
    def __init__(self, conf_path):
        self.conf_path = conf_path
        self.conf_file = open(conf_path, "r")
        self.line_num = 0

    def lines(self):
        """
        Reads the next line from the configuration file
        """
        for line_num, line in enumerate(self.conf_file):
            # ignore empty lines and comments
            if line.isspace() or line.lstrip().startswith("#"):
                continue
            self.line_num = line_num
            yield list(map(lambda l: l.strip(), line.split('|')))

        self.conf_file.close()

    def get_file_path(self):
        return self.conf_path
