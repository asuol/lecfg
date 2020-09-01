from lecfg.conf.package_parser import PackageParser
from lecfg.conf.package_parser import README_FILE_NOT_FOUND
from lecfg.conf.systems_parser import SystemsParser
from lecfg.conf.systems_parser import SYSTEMS_FILE_NOT_FOUND
from lecfg.conf.conf_exception import ConfException
import pytest
import os

TEST_PACKAGE_CONF = """
# README.lc
.vimrc |  - |  - | ~/.vimrc | Vim Configuration
.vimrc_gentoo | 8.0 | Gentoo | ~/.vimrc | Vim Configuration

.vimrc_work | 8.0 | Debian,Gentoo | ~/.vimrc | Vim configuration """

TEST_PACKAGE_ERROR_CONF = TEST_PACKAGE_CONF + """
.vimrc || - | ~.vimrc """


@pytest.fixture
def _setup(tmpdir):
    def _create_file(file_contents):
        package_dir = str(tmpdir)
        conf_file = os.path.join(package_dir, "README.lc")

        with open(conf_file, "w") as file:
            for line in file_contents:
                file.write(line)

        return package_dir

    return _create_file


def test_parse(_setup):
    package_dir = _setup(TEST_PACKAGE_CONF)

    vim_package = PackageParser(package_dir, "Debian")

    conf_objs = []

    for conf in vim_package.configurations():
        print("test iter")
        conf_objs.append(conf)

    assert len(conf_objs) == 2


def test_parse_error(_setup):
    package_dir = _setup(TEST_PACKAGE_ERROR_CONF)

    vim_package = PackageParser(package_dir, "Debian")

    conf_objs = []

    with pytest.raises(ConfException) as error:
        for conf in vim_package.configurations():
            conf_objs.append(conf)

    assert error.value.line_num == 6

    assert len(conf_objs) == 2


def test_invalid_system_file():
    with pytest.raises(ConfException, match=SYSTEMS_FILE_NOT_FOUND):
        SystemsParser("")


def test_invalid_package_file():
    with pytest.raises(ConfException, match=README_FILE_NOT_FOUND):
        PackageParser("", "Debian")
