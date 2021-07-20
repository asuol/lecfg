from lecfg.lecfg import Lecfg
from lecfg.exit_code import ExitCode
from pathlib import Path
import pytest
import os
import io
import glob
import subprocess

TEST_PACKAGE_CONF = """
# README.lc
.vimrc |  - |  - | %s/.vimrc | Vim Configuration
.vimrc_gentoo | 8.0 | Gentoo | %s/.vimrc_gentoo | Vim Configuration

.vimrc_work | 8.0 | Debian,Gentoo | %s/.vimrc_work | Vim configuration
"""

NO_PARENT_PACKAGE_CONF = """
dummy | - | - | %s/some/dir/dummy | Dummy conf
"""

ONE_SYSTEM_CONF = """
Debian | grep "Debian" /etc/os-release
"""

TWO_SYSTEM_CONF = """
Debian | grep "Debian" /etc/os-release
Gentoo | -
"""

MOCK_READ_CMD = "less"
MOCK_CMP_CMD = "diff -u"


def file_exists(parent_dir: str, file_name: str) -> bool:
    path = os.path.join(parent_dir, file_name)

    return len(glob.glob(path)) > 0


def check_file_contents(parent_dir: str, file_name: str,
                        file_contents: str) -> bool:
    path = os.path.join(parent_dir, file_name)

    return file_contents == open(path, 'r').read()


def test_empty_work_dir(tmpdir):
    lecfg = Lecfg(str(tmpdir))
    with pytest.raises(SystemExit) as e:
        lecfg.process()

    assert e.value.code == ExitCode.SYSTEMS_FILE_NOT_FOUND.value


def test_empty_systems_file(setup):
    work_dir = setup("lecfg.systems", "")
    lcfg = Lecfg(work_dir)
    with pytest.raises(SystemExit) as e:
        lcfg.process()

    assert e.value.code == ExitCode.EMPTY_SYSTEMS_FILE.value


def test_single_system_conf(setup, capsys):
    work_dir = setup("lecfg.systems", ONE_SYSTEM_CONF)

    lecfg = Lecfg(work_dir)
    lecfg.process()

    capture = capsys.readouterr()

    assert "Current system: [ Debian ]" in capture.out


def test_multiple_system_conf(setup, capsys, monkeypatch):
    work_dir = setup("lecfg.systems", TWO_SYSTEM_CONF)

    # select the second system
    monkeypatch.setattr('sys.stdin', io.StringIO('2'))

    lecfg = Lecfg(work_dir)
    lecfg.process()

    capture = capsys.readouterr()

    assert "Current system: [ Gentoo ]" in capture.out


def test_package_deploy_replace(setup, create_dir, monkeypatch):
    work_dir = setup("lecfg.systems", ONE_SYSTEM_CONF, parent_dir="work_dir")
    system_dir = create_dir("SYSTEM")

    package_dir = os.path.join(work_dir, "vim")

    setup("README.lc",
          TEST_PACKAGE_CONF % (system_dir, system_dir, system_dir),
          parent_dir=package_dir)

    replace_data = "some sample conf"

    # setup package dir
    setup(".vimrc", "", parent_dir=package_dir)
    setup(".vimrc_gentoo", "", parent_dir=package_dir)
    setup(".vimrc_work", replace_data, parent_dir=package_dir)

    # setup system dir
    setup(".vimrc_work", "", parent_dir=system_dir)

    # Deploy the first file and replace the second file
    # from the 2 files that apply to the current system
    monkeypatch.setattr('sys.stdin', io.StringIO('2\n4'))

    assert file_exists(system_dir, ".vimrc") is False
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is True
    assert check_file_contents(system_dir, ".vimrc_work", "") is True

    lecfg = Lecfg(work_dir)
    lecfg.process()

    assert file_exists(system_dir, ".vimrc") is True
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is True
    assert check_file_contents(system_dir, ".vimrc_work", replace_data) is True


def test_session(setup, create_dir, monkeypatch):
    work_dir = setup("lecfg.systems", ONE_SYSTEM_CONF, parent_dir="work_dir")
    system_dir = create_dir("SYSTEM")

    package_dir = os.path.join(work_dir, "vim")

    setup("README.lc",
          TEST_PACKAGE_CONF % (system_dir, system_dir, system_dir),
          parent_dir=package_dir)

    setup(".vimrc", "", parent_dir=package_dir)
    setup(".vimrc_gentoo", "", parent_dir=package_dir)
    setup(".vimrc_work", "", parent_dir=package_dir)

    # Deploy the first file that applies to the current system, and save and
    # exit
    monkeypatch.setattr('sys.stdin', io.StringIO('2\n4'))

    assert file_exists(system_dir, ".vimrc") is False
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is False

    lecfg = Lecfg(work_dir)

    with pytest.raises(SystemExit) as e:
        lecfg.process()

    assert e.value.code == ExitCode.SAVE_AND_EXIT.value

    assert file_exists(system_dir, ".vimrc") is True
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is False

    assert file_exists(work_dir, "*_lecfg.sav") is True

    # resume previous session, and deploy the remaining file
    monkeypatch.setattr('sys.stdin', io.StringIO('1\n2'))

    lecfg = Lecfg(work_dir)
    lecfg.process()

    assert file_exists(system_dir, ".vimrc") is True
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is True

    assert file_exists(work_dir, "*_lecfg.sav") is False


def test_multiple_sessions(setup, create_dir, monkeypatch):
    work_dir = setup("lecfg.systems", ONE_SYSTEM_CONF, parent_dir="work_dir")
    system_dir = create_dir("SYSTEM")

    first_session = "10-12-2020_20-20_lecfg.sav"
    second_session = "15-12-2020_21-21_lecfg.sav"

    package_dir = os.path.join(work_dir, "vim")

    setup(first_session, "%s,1" % package_dir, parent_dir=work_dir)
    setup(second_session, "%s,3" % package_dir, parent_dir=work_dir)

    setup("README.lc",
          TEST_PACKAGE_CONF % (system_dir, system_dir, system_dir),
          parent_dir=package_dir)

    setup(".vimrc", "", parent_dir=package_dir)
    setup(".vimrc_gentoo", "", parent_dir=package_dir)
    setup(".vimrc_work", "", parent_dir=package_dir)

    # resume previous session, select second session, which will skip the
    # first 2 lines, and deploy just the last applicable file
    monkeypatch.setattr('sys.stdin', io.StringIO('1\n2\n2'))

    lecfg = Lecfg(work_dir)
    lecfg.process()

    assert file_exists(system_dir, ".vimrc") is False
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is True

    assert file_exists(work_dir, first_session) is True
    assert file_exists(work_dir, second_session) is False


def test_read_action(setup, create_dir, monkeypatch, mocker):
    work_dir = setup("lecfg.systems", ONE_SYSTEM_CONF, parent_dir="work_dir")
    system_dir = create_dir("SYSTEM")

    package_dir = os.path.join(work_dir, "vim")

    setup("README.lc",
          TEST_PACKAGE_CONF % (system_dir, system_dir, system_dir),
          parent_dir=package_dir)

    setup(".vimrc", "", parent_dir=package_dir)
    setup(".vimrc_gentoo", "", parent_dir=package_dir)
    setup(".vimrc_work", "", parent_dir=package_dir)

    setup("read.cmd", MOCK_READ_CMD, parent_dir=work_dir)

    mocker.patch("subprocess.run")

    # read first file, and skip all files
    monkeypatch.setattr('sys.stdin', io.StringIO('1\n3\n3\n3'))

    lecfg = Lecfg(work_dir)
    lecfg.process()

    assert file_exists(system_dir, ".vimrc") is False
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is False

    file_path = os.path.join(package_dir, ".vimrc")

    subprocess.run.assert_called_once_with([MOCK_READ_CMD, file_path],
                                           check=True, stderr=subprocess.PIPE)


def test_compare_action(setup, create_dir, monkeypatch, mocker):
    work_dir = setup("lecfg.systems", ONE_SYSTEM_CONF, parent_dir="work_dir")
    system_dir = create_dir("SYSTEM")

    package_dir = os.path.join(work_dir, "vim")

    setup("README.lc",
          TEST_PACKAGE_CONF % (system_dir, system_dir, system_dir),
          parent_dir=package_dir)

    file_content = "content"

    # setup package dir
    setup(".vimrc", "", parent_dir=package_dir)
    setup(".vimrc_gentoo", "", parent_dir=package_dir)
    setup(".vimrc_work", file_content, parent_dir=package_dir)

    # setup system dir
    setup(".vimrc_work", "", parent_dir=system_dir)

    # setup work dir
    setup("compare.cmd", MOCK_CMP_CMD, parent_dir=work_dir)

    assert file_exists(system_dir, ".vimrc") is False
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is True

    mocker.patch("subprocess.run")

    # compare last file, and skip all files
    monkeypatch.setattr('sys.stdin', io.StringIO('3\n3\n5'))

    lecfg = Lecfg(work_dir)
    lecfg.process()

    assert file_exists(system_dir, ".vimrc") is False
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is True

    src_path = os.path.join(package_dir, ".vimrc_work")
    dest_path = os.path.join(system_dir, ".vimrc_work")

    cmd = MOCK_CMP_CMD.split(" ")
    cmd.append(dest_path)
    cmd.append(src_path)

    subprocess.run.assert_called_once_with(cmd, check=True,
                                           stderr=subprocess.PIPE)


def test_empty_readme(setup, capsys):
    work_dir = setup("lecfg.systems", ONE_SYSTEM_CONF)
    package_name = "FakePackage"
    package_dir = os.path.join(work_dir, package_name)

    setup("README.lc", "", parent_dir=package_dir)

    lecfg = Lecfg(work_dir)
    lecfg.process()

    capture = capsys.readouterr()

    assert "No configuration defined for package [ %s ]" % (
        package_dir) in capture.out


def test_no_parent_deploy(setup, create_dir, monkeypatch):
    work_dir = setup("lecfg.systems", ONE_SYSTEM_CONF, parent_dir="work_dir")
    system_dir = create_dir("SYSTEM")

    package_dir = os.path.join(work_dir, "dummy")

    setup("README.lc",
          NO_PARENT_PACKAGE_CONF % system_dir,
          parent_dir=package_dir)

    # setup package dir
    setup("dummy", "", parent_dir=package_dir)

    # Create the missing parent directories and deploy the conf file
    monkeypatch.setattr('sys.stdin', io.StringIO('2'))

    parent_dir = os.path.join(system_dir, "some", "dir")

    assert file_exists(parent_dir, "dummy") is False

    lecfg = Lecfg(work_dir)
    lecfg.process()

    assert file_exists(parent_dir, "dummy") is True


def test_replace_symlink(setup, create_dir, monkeypatch):
    work_dir = setup("lecfg.systems", ONE_SYSTEM_CONF, parent_dir="work_dir")
    system_dir = create_dir("SYSTEM")

    package_dir = os.path.join(work_dir, "vim")

    setup("README.lc",
          TEST_PACKAGE_CONF % (system_dir, system_dir, system_dir),
          parent_dir=package_dir)

    replace_data = "some sample conf"

    # setup package dir
    setup(".vimrc", "", parent_dir=package_dir)
    setup(".vimrc_gentoo", "", parent_dir=package_dir)
    setup(".vimrc_work", replace_data, parent_dir=package_dir)

    # setup system dir
    setup(".vimrc_work_orig", "", parent_dir=system_dir)
    symlink = Path(system_dir) / ".vimrc_work"
    orig_conf = Path(system_dir) / ".vimrc_work_orig"

    symlink.symlink_to(orig_conf)

    # Deploy the first file and replace the second file
    # from the 2 files that apply to the current system
    monkeypatch.setattr('sys.stdin', io.StringIO('2\n4'))

    assert file_exists(system_dir, ".vimrc") is False
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is True
    assert check_file_contents(system_dir, ".vimrc_work", "") is True
    assert symlink.is_symlink() is True

    lecfg = Lecfg(work_dir)
    lecfg.process()

    assert file_exists(system_dir, ".vimrc") is True
    assert file_exists(system_dir, ".vimrc_gentoo") is False
    assert file_exists(system_dir, ".vimrc_work") is True
    assert check_file_contents(system_dir, ".vimrc_work", replace_data) is True
    assert symlink.is_symlink() is True
