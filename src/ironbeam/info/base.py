import logging
from typing import List

import httpx

from ironbeam.exceptions import IronbeamAPIError
from ironbeam.info.models import (
    SecurityDefinitionsResponse,
    SecurityMarginAndValueResponse,
    TraderInfo,
    UserInfo,
)
from ironbeam.literals import MODE

logger = logging.getLogger(__name__)


class Info:
    """Handles info endpoints for Ironbeam API."""

    def __init__(self, mode: MODE | None = "demo"):
        self._mode = mode
        self.base_url = (
            f"https://{'demo' if mode == 'demo' else 'live'}.ironbeamapi.com/v2"
        )

    def get_trader_info(self, bearer_token: str) -> TraderInfo:
        """
        Get trader information.

        Args:
            bearer_token: The bearer token from authentication

        Returns:
            TraderInfo: Information about the trader including accounts

        Raises:
            IronbeamResponseError: If the API returns an error response
            IronbeamAPIError: For other API-related errors
            httpx.HTTPError: If the HTTP request fails
        """
        headers = {"Authorization": f"Bearer {bearer_token}"}

        try:
            response = (
                httpx.get(f"{self.base_url}/info/trader", headers=headers)
                .raise_for_status()
                .json()
            )

            return TraderInfo(**response)

        except httpx.HTTPError as e:
            raise IronbeamAPIError(f"HTTP request failed: {str(e)}") from e

    def get_user_info(self, bearer_token: str) -> UserInfo:
        """
        Get user general information.

        Args:
            bearer_token: The bearer token from authentication

        Returns:
            UserInfo: General information about the user

        Raises:
            IronbeamResponseError: If the API returns an error response
            IronbeamAPIError: For other API-related errors
            httpx.HTTPError: If the HTTP request fails
        """
        headers = {"Authorization": f"Bearer {bearer_token}"}

        try:
            response = (
                httpx.get(f"{self.base_url}/info/user", headers=headers)
                .raise_for_status()
                .json()
            )

            return UserInfo(**response)

        except httpx.HTTPError as e:
            raise IronbeamAPIError(f"HTTP request failed: {str(e)}") from e

    def get_security_definitions(
            self, symbols: List[str], bearer_token: str
    ) -> SecurityDefinitionsResponse:
        """
        Get security definitions for specified symbols.

        Args:
            symbols: List of symbols e.g. ["XCME:ES.H25"]
            bearer_token: The bearer token from authentication

        Returns:
            SecurityDefinitionsResponse: Detailed security information

        Raises:
            ValueError: If symbols validation fails
            IronbeamResponseError: If the API returns an error response
            IronbeamAPIError: For other API-related errors
            httpx.HTTPError: If the HTTP request fails
        """
        if not symbols:
            raise ValueError("Must provide at least one symbol")

        params = {"symbols": symbols}

        headers = {"Authorization": f"Bearer {bearer_token}"}

        try:
            response = (
                httpx.get(
                    f"{self.base_url}/info/security/definitions",
                    params=params,
                    headers=headers,
                )
                .raise_for_status()
                .json()
            )

            return SecurityDefinitionsResponse(**response)

        except httpx.HTTPError as e:
            raise IronbeamAPIError(f"HTTP request failed: {str(e)}") from e

    def get_security_margin(
            self, symbols: List[str], bearer_token: str
    ) -> SecurityMarginAndValueResponse:
        """
        Get security margin and value information for specified symbols.

        Args:
            symbols: List of symbols e.g. ["XCME:ES.H25"]
            bearer_token: The bearer token from authentication

        Returns:
            SecurityMarginAndValueResponse: Margin and value information for securities

        Raises:
            ValueError: If symbols validation fails
            IronbeamResponseError: If the API returns an error response
            IronbeamAPIError: For other API-related errors
            httpx.HTTPError: If the HTTP request fails
        """
        if not symbols:
            raise ValueError("Must provide at least one symbol")

        params = {"symbols": symbols}

        headers = {"Authorization": f"Bearer {bearer_token}"}

        try:
            response = (
                httpx.get(
                    f"{self.base_url}/info/security/margin",
                    params=params,
                    headers=headers,
                )
                .raise_for_status()
                .json()
            )

            return SecurityMarginAndValueResponse(**response)

        except httpx.HTTPError as e:
            raise IronbeamAPIError(f"HTTP request failed: {str(e)}") from e
