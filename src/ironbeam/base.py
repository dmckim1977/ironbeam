import logging
from typing import Optional

from .auth.base import Auth
from .info.base import Info
from .literals import MODE
from .market.base import Market

logger = logging.getLogger(__name__)


class Ironbeam:
    """Provides a client class for interacting with Ironbeam's API.

    Args:
        apikey: The IronBeam API key
        mode: The API mode ("demo" or "live")
        api_secret: Optional API secret for tenant users

    Examples:
        >>> import os
        >>> from dotenv import load_dotenv
        >>> load_dotenv()
        True
        >>> client = Ironbeam(apikey=os.getenv("IRONBEAM_APIKEY"))
        >>> client.authorize(username=os.getenv("IRONBEAM_USERNAME"))
        >>> print(client.token is not None)
        True
    """

    def __init__(
            self,
            apikey: Optional[str] = None,
            mode: Optional[MODE] = "demo",
            api_secret: Optional[str] = None,
    ):
        self._apikey = apikey
        self._mode = mode
        self._api_secret = api_secret
        self.__token: Optional[str] = None

        self._auth = Auth(mode=mode)
        self._market = Market(mode=mode)
        self._info = Info(mode=mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__token:
            try:
                self.logout()
            except Exception as e:
                logger.error(f"Error during logout: {e}")

    @property
    def token(self) -> Optional[str]:
        """The current authorization token."""
        return self.__token

    @property
    def mode(self) -> Optional[str]:
        """The current API mode."""
        return self._mode

    @property
    def market(self) -> Market:
        """Access market data endpoints."""
        return self._market

    @property
    def info(self) -> Info:
        """Access info endpoints."""
        return self._info

    def authorize(self, username: str, apikey: Optional[str] = None) -> "Ironbeam":
        """Authorize with the Ironbeam API.

        Args:
            username: The IronBeam username
            apikey: Optional API key (overrides the one provided at initialization)

        Returns:
            self: Returns the client instance for method chaining

        Raises:
            httpx.HTTPError: If the authorization request fails
        """
        apikey = apikey or self._apikey
        if not apikey:
            raise ValueError("No API key provided")

        self.__token = self._auth.authorize(username=username, apikey=apikey)
        return self

    def logout(self) -> None:
        """Logout and invalidate the current token.

        Raises:
            ValueError: If no token exists
            httpx.HTTPError: If the logout request fails
        """
        if not self.__token:
            raise ValueError("No token to invalidate")

        self._auth.logout(token=self.__token)
        self.__token = None
