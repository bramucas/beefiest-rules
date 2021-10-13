"""This file is intended to declare global (scope='session', autouse=True) 
fixtures for the tests. 
"""

import pytest
from pathlib import Path
from tests_beefiest_rules import get_sandbox_dir, rec_rmdir


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
