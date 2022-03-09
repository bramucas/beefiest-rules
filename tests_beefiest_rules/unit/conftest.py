"""This file configures some test environment variables, declares global (scope='session', autouse=True) 
fixtures and provides some utilities for the tests.
"""

import pytest
from pathlib import Path

# Config
SANDBOX_DIRNAME = 'sandbox'


# Utils
def get_sandbox_dir(dirname: str = SANDBOX_DIRNAME) -> Path:
    """Returns the current test sandbox directory. This directory is intended 
    to be used for temporal file storing at test time. The directory is created
    if does not already exists.

    Args:
        dirname (str, optional): name for the directory. Defaults to SANDBOX_DIRNAME='sandbox'.

    Returns:
        Path: the path object of the directory (see [pathlib](https://docs.python.org/3/library/pathlib.html)).
    """
    path = Path.cwd() / dirname
    path.mkdir(parents=False, exist_ok=True)
    return path


def rec_rmdir(path: Path) -> None:
    """A recursive version of rmdir for Path objects.

    Args:
        path (Path): path object of the directory to be removed.
    """
    for sub in path.iterdir():
        if sub.is_dir():
            rec_rmdir(sub)
        else:
            sub.unlink()
    path.rmdir()


# Global fixtures
@pytest.fixture(scope='session', autouse=True)
def sandbox_dir():
    # Before tests
    sandbox_dir = get_sandbox_dir()
    yield sandbox_dir
    # After tests
    rec_rmdir(sandbox_dir)


@pytest.fixture(scope='session')
def sandbox_file() -> Path:
    def _sandbox_file(filename: str) -> Path:
        return get_sandbox_dir() / filename

    return _sandbox_file
