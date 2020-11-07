from lecfg.lecfg import Lecfg, ExitCode
import pytest
import os
import io

TEST_PACKAGE_CONF = """
# README.lc
.vimrc |  - |  - | %s/.vimrc | Vim Configuration
.vimrc_gentoo | 8.0 | Gentoo | %s/.vimrc_gentoo | Vim Configuration

.vimrc_work | 8.0 | Debian,Gentoo | %s/.vimrc_work | Vim configuration
"""

ONE_SYSTEM_CONF = """
Debian | grep "Debian" /etc/os-release
"""

TWO_SYSTEM_CONF = """
Debian | grep "Debian" /etc/os-release
Gentoo | -
"""


@pytest.fixture
def _setup(tmpdir):
    def _create_file(file_name: str, file_contents: str,
                     parent_dir: str = None) -> str:
        if parent_dir is None:
            dir_path = str(tmpdir)
        else:
            dir_path = os.path.join(str(tmpdir), parent_dir)

            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)

        file_path = os.path.join(dir_path, file_name)

        with open(file_path, "w") as file:
            for line in file_contents:
                file.write(line)

        return dir_path

    return _create_file


@pytest.fixture
def _create_dir(tmpdir):
    def _create_empty_dir(dir_name: str) -> str:
        dir_path = os.path.join(str(tmpdir), dir_name)

        os.mkdir(dir_path)

        return dir_path

    return _create_empty_dir


def file_exists(parent_dir: str, file_name: str) -> bool:
    path = os.path.join(parent_dir, file_name)

    return os.path.isfile(path)


def test_empty_work_dir(tmpdir):
    lcfg = Lecfg(str(tmpdir))
    with pytest.raises(SystemExit) as e:
        lcfg.process()

    assert e.value.code == ExitCode.SYSTEMS_FILE_NOT_FOUND.value


def test_empty_systems_file(_setup):
    work_dir = _setup("lecfg.systems", "")
    lcfg = Lecfg(work_dir)
    with pytest.raises(SystemExit) as e:
        lcfg.process()

    assert e.value.code == ExitCode.EMPTY_SYSTEMS_FILE.value


def test_single_system_conf(_setup, capsys):
    work_dir = _setup("lecfg.systems", ONE_SYSTEM_CONF)

    lecfg = Lecfg(work_dir)
    lecfg.process()

    capture = capsys.readouterr()

    assert "Current system: [ Debian ]" in capture.out


def test_multiple_system_conf(_setup, capsys, monkeypatch):
    work_dir = _setup("lecfg.systems", TWO_SYSTEM_CONF)

    # select the second system
    monkeypatch.setattr('sys.stdin', io.StringIO('2'))

    lecfg = Lecfg(work_dir)
    lecfg.process()

    capture = capsys.readouterr()

    assert "Current system: [ Gentoo ]" in capture.out


def test_package_deploy(_setup, _create_dir, capsys, monkeypatch):
    work_dir = _setup("lecfg.systems", ONE_SYSTEM_CONF, parent_dir="work_dir")
    system_dir = _create_dir("SYSTEM")

    package_dir = os.path.join(work_dir, "vim")

    _setup("README.lc",
           TEST_PACKAGE_CONF % (system_dir, system_dir, system_dir),
           parent_dir=package_dir)

    _setup(".vimrc", "", parent_dir=package_dir)
    _setup(".vimrc_gentoo", "", parent_dir=package_dir)
    _setup(".vimrc_work", "", parent_dir=package_dir)

    # Deploy the two files that apply to the current system
    monkeypatch.setattr('sys.stdin', io.StringIO('2\n2'))

    assert file_exists(system_dir, ".vimrc") is False
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is False

    lecfg = Lecfg(work_dir)
    lecfg.process()

    assert file_exists(system_dir, ".vimrc") is True
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is True


def test_session():
    pass


def test_package_replace():
    pass
