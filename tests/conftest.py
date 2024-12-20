import doctest

import pytest


def pytest_collect_file(parent, path):
    if path.ext == ".py":
        return DoctestModule.from_parent(parent, fspath=path)


class DoctestModule(pytest.Module):
    def collect(self):
        if self.fspath.basename == "__init__.py":
            module = self.fspath.pyimport()
            yield from doctest.DocTestFinder().find(module)


# Add fixtures that can be used across all tests
@pytest.fixture
def mock_env_vars():
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("IRONBEAM_USERNAME", "test_user")
        mp.setenv("IRONBEAM_APIKEY", "test_key")
        yield


def pytest_configure(config):
    """
    Register doctests for Sphinx documentation.
    """
    import doctest
    import ironbeam

    doctest.DocTestFinder().find(ironbeam)
