from datetime import datetime
from typing import List

import httpx

from ironbeam.exceptions import IronbeamAPIError
from ironbeam.literals import MODE
from ironbeam.market.models import (
    DepthResponse,
    QuoteRequest,
    QuoteResponse,
    TradesResponse,
)


class Market:
    """Handles market data endpoints for Ironbeam API."""

    def __init__(self, mode: MODE | None = "demo"):
        self._mode = mode
        self.base_url = (
            f"https://{'demo' if mode == 'demo' else 'live'}.ironbeamapi.com/v2"
        )

    def get_quotes(self, symbols: List[str], bearer_token: str) -> QuoteResponse:
        """
        Get current quotes for specified symbols.

        Args:
            symbols: List of symbols (max 10) e.g. ["XCME:ES.H25", "XCME:NQ.H25"]
            bearer_token: The bearer token from authentication

        Returns:
            QuoteResponse: Parsed quote data that can be converted to pandas

        Raises:
            ValueError: If symbols validation fails
            IronbeamResponseError: If the API returns an error response
            IronbeamAPIError: For other API-related errors
            httpx.HTTPError: If the HTTP request fails
        """
        try:
            # Validate input
            request = QuoteRequest(symbols=symbols)

            params = {"symbols": request.symbols}

            headers = {"Authorization": f"Bearer {bearer_token}"}

            response = (
                httpx.get(
                    f"{self.base_url}/market/quotes", params=params, headers=headers
                )
                .raise_for_status()
                .json()
            )

            # This will raise IronbeamResponseError if status is ERROR
            return QuoteResponse(**response)

        except httpx.HTTPError as e:
            raise IronbeamAPIError(f"HTTP request failed: {str(e)}") from e
        except ValueError as e:
            raise ValueError(f"Invalid input: {str(e)}") from e

    def get_depth(self, symbols: List[str], bearer_token: str) -> DepthResponse:
        """
        Get market depth for specified symbols.

        Args:
            symbols: List of symbols (max 10) e.g. ["XCME:ES.H25", "XCME:NQ.H25"]
            bearer_token: The bearer token from authentication

        Returns:
            DepthResponse: Parsed depth data that can be converted to pandas

        Raises:
            ValueError: If symbols validation fails
            IronbeamResponseError: If the API returns an error response
            IronbeamAPIError: For other API-related errors
            httpx.HTTPError: If the HTTP request fails
        """
        try:
            # Validate input (reuse QuoteRequest since validation is same)
            request = QuoteRequest(symbols=symbols)

            params = {"symbols": request.symbols}

            headers = {"Authorization": f"Bearer {bearer_token}"}

            response = (
                httpx.get(
                    f"{self.base_url}/market/depth", params=params, headers=headers
                )
                .raise_for_status()
                .json()
            )

            # return response
            return DepthResponse(**response)

        except httpx.HTTPError as e:
            raise IronbeamAPIError(f"HTTP request failed: {str(e)}") from e
        except ValueError as e:
            raise ValueError(f"Invalid input: {str(e)}") from e

    def get_trades(
            self,
            symbol: str,
            from_time: datetime,
            to_time: datetime,
            bearer_token: str,
            max_trades: int = 100,
            earlier: bool = True,
    ) -> TradesResponse:
        """
        Get trades for a symbol within a time range.

        Args:
            symbol: Symbol e.g. "XCME:ES.H25"
            from_time: Start time for trades
            to_time: End time for trades
            max_trades: Maximum number of trades to return (1-5000)
            earlier: Get trades earlier than the specified trade id
            bearer_token: The bearer token from authentication

        Returns:
            TradesResponse: Parsed trade data that can be converted to pandas

        Raises:
            ValueError: If input validation fails
            IronbeamResponseError: If the API returns an error response
            IronbeamAPIError: For other API-related errors
            httpx.HTTPError: If the HTTP request fails
        """
        try:
            # Validate inputs
            if not 1 <= max_trades <= 5000:
                raise ValueError("max_trades must be between 1 and 5000")

            # Convert datetimes to milliseconds
            from_ms = int(from_time.timestamp() * 1000)
            to_ms = int(to_time.timestamp() * 1000)

            # Build URL with path parameters
            url = (
                f"{self.base_url}/market/trades/{symbol}/"
                f"{from_ms}/{to_ms}/{max_trades}/{str(earlier).lower()}"
            )

            headers = {"Authorization": f"Bearer {bearer_token}"}

            response = httpx.get(url, headers=headers).raise_for_status().json()

            # return response
            return TradesResponse(**response)

        except httpx.HTTPError as e:
            raise IronbeamAPIError(f"HTTP request failed: {str(e)}") from e
        except ValueError as e:
            raise ValueError(f"Invalid input: {str(e)}") from e
