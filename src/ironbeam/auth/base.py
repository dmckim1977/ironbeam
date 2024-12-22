import logging

import httpx

from ironbeam.literals import MODE

logger = logging.getLogger(__name__)


class Auth:
    """Handles authentication endpoints for Ironbeam API."""

    def __init__(self, mode: MODE | None = "demo"):
        self._mode = mode
        self.base_url = (
            f"https://{'demo' if mode == 'demo' else 'live'}.ironbeamapi.com/v2"
        )

    def authorize(self, username: str, apikey: str) -> str:
        """
        Authorize with the Ironbeam API.

        Args:
            username: The IronBeam API username
            apikey: The IronBeam API key (used as password)

        Returns:
            str: Authorization token

        Raises:
            httpx.HTTPError: If the request fails
        """
        payload = {
            "Username": username,
            "ApiKey": apikey,
        }

        headers = {"Content-Type": "application/json"}

        response = (
            httpx.post(f"{self.base_url}/auth", json=payload, headers=headers)
            .raise_for_status()
            .json()
        )

        return response["token"]

    def logout(self, token: str) -> None:
        """
        Logout and invalidate token.

        Args:
            token: The token to invalidate

        Raises:
            httpx.HTTPError: If the request fails
        """
        headers = {
            "Authorization": f"Bearer {token}",
        }

        httpx.post(f"{self.base_url}/logout", headers=headers).raise_for_status()
