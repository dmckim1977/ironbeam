# src/ironbeam/tests/test_auth.py

from ironbeam.auth.base import Auth


def test_auth_initialization(mock_env_vars):
    auth = Auth(username="test_user", apikey="test_key")
    assert auth.username == "test_user"
    assert auth.apikey == "test_key"
    assert auth.token is None


def test_auth_full_flow(mock_env_vars):
    """
    This test demonstrates a full authentication flow.
    This docstring can be used in documentation as an example.
    """
    auth = Auth(username="test_user", apikey="test_key")
    # Add your test assertions here
