import pytest
import os


@pytest.fixture
def setup(tmpdir):
    def create_file(file_name: str, file_contents: str,
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

    return create_file


@pytest.fixture
def create_dir(tmpdir):
    def create_empty_dir(dir_name: str) -> str:
        dir_path = os.path.join(str(tmpdir), dir_name)

        os.mkdir(dir_path)

        return dir_path

    return create_empty_dir
