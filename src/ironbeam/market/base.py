from typing import List

import httpx

from ironbeam.exceptions import IronbeamAPIError
from ironbeam.market.models import QuoteRequest, QuoteResponse


class Market:
    """Handles market data endpoints for Ironbeam API."""

    def __init__(self, mode: str = "demo"):
        self._mode = mode
        self.base_url = f"https://{'demo' if mode == 'demo' else 'live'}.ironbeamapi.com/v2"

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

            params = {
                "symbols": request.symbols
            }

            headers = {
                "Authorization": f"Bearer {bearer_token}"
            }

            response = httpx.get(
                f"{self.base_url}/market/quotes",
                params=params,
                headers=headers
            ).raise_for_status().json()

            # This will raise IronbeamResponseError if status is ERROR
            return QuoteResponse(**response)

        except httpx.HTTPError as e:
            raise IronbeamAPIError(f"HTTP request failed: {str(e)}") from e
        except ValueError as e:
            raise ValueError(f"Invalid input: {str(e)}") from e
