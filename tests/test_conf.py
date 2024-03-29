from lecfg.conf.package_parser import PackageParser
from lecfg.conf.package_parser import README_FILE_NOT_FOUND
from lecfg.conf.systems_parser import SystemsParser
from lecfg.conf.systems_parser import SYSTEMS_FILE_NOT_FOUND
from lecfg.conf.conf_exception import ConfException
import pytest

TEST_PACKAGE_CONF = """
# README.lc
.vimrc |  - |  - | /tmp/.vimrc | Vim Configuration
.vimrc_gentoo | 8.0 | Gentoo | /tmp/.vimrc | Vim Configuration

.vimrc_work | 8.0 | Debian,Gentoo | /tmp/.vimrc | Vim configuration """

TEST_PACKAGE_ERROR_CONF = TEST_PACKAGE_CONF + """
.vimrc || - | /tmp/.vimrc """


def test_parse(setup):
    package_dir = setup("README.lc", TEST_PACKAGE_CONF)

    # setup package dir
    setup(".vimrc", "", parent_dir=package_dir)
    setup(".vimrc_gentoo", "", parent_dir=package_dir)
    setup(".vimrc_work", "", parent_dir=package_dir)

    vim_package = PackageParser(package_dir, "Debian")

    conf_objs = []

    for conf in vim_package.configurations():
        conf_objs.append(conf)

    assert len(conf_objs) == 2


def test_parse_error(setup):
    package_dir = setup("README.lc", TEST_PACKAGE_ERROR_CONF)

    # setup package dir
    setup(".vimrc", "", parent_dir=package_dir)
    setup(".vimrc_gentoo", "", parent_dir=package_dir)
    setup(".vimrc_work", "", parent_dir=package_dir)

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
