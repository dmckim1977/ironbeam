import json
import logging
from typing import Literal, Optional

import httpx

logger = logging.getLogger(__name__)


class Ironbeam:
    """Provides a client class for requesting historical data from Ironbeam's API.

    `password` and `apikey` are the same.
    The API Key is used as a password in the request.

    # TODO: Need to implement for Tenant users.

    Args:
        username (str): The IronBeam API username
        apikey (str): The IronBeam API key

    Examples
    --------
    >>> import os
    >>> from dotenv import load_dotenv
    >>> load_dotenv()
    True
    >>> auth = Auth(username=os.getenv("IRONBEAM_USERNAME"),
    ...            apikey=os.getenv("IRONBEAM_APIKEY"))
    >>> auth.username == os.getenv("IRONBEAM_USERNAME")
    True
    >>> token = auth.authorize()  # doctest: +SKIP
    >>> auth.token is not None  # doctest: +SKIP
    True
    >>> auth.save_token()  # doctest: +SKIP
    """

    MODE = Literal['demo', 'live']

    def __init__(
            self,
            apikey: Optional[str] = None,
            mode: Optional[MODE] = "demo",
            api_secret: Optional[str] = None,
    ):
        self.__api_secret = api_secret
        self.__apikey = apikey
        self.__mode = mode
        self._streamid: str | None = None

        self.demo_auth_url: str = "https://demo.ironbeamapi.com/v2/auth"
        self.live_auth_url: str = "https://live.ironbeamapi.com/v2/auth"

        self.demo_base_url: str = "https://demo.ironbeamapi.com/v2/logout"
        self.live_base_url: str = "https://live.ironbeamapi.com/v2/logout"

        self.__token: str | None = None

    @property
    def apikey(self) -> str:
        return self.__apikey

    @property
    def api_secret(self) -> str | None:
        if self.__api_secret is None:
            logging.error("No API secret provided")
        return self.__api_secret

    @property
    def mode(self) -> str | None:
        return self.__mode

    @property
    def token(self) -> str:
        """Create token if it doesn't exist"""
        if self.__token is None:
            self.authorize()
            assert self.__token is not None
        return self.__token

    def authorize(self, username: str, apikey: str) -> str:
        """

        :return: Returns the api token.
        """

        payload = {
            "Username": username,
            "ApiKey": apikey,
        }

        headers = {"Content-Type": "application/json"}

        # Set url depending on mode
        if self.__mode == 'live':
            url = self.live_auth_url
        elif self.__mode == 'demo':
            url = self.demo_auth_url

        try:
            res = httpx.post(
                url=url, json=payload, headers=headers
            ).raise_for_status().json()

            logger.info(f"Authorization successful. Token: {res['token']}")

            self.__token = res['token']

            return self

        except httpx.HTTPError as exc:
            logger.error(f"Error while requesting {exc.request.url!r}.")
            return self

    def save_token(self, filepath: Optional[str] = "ironbeam_token.json") -> None:
        """
        Saves the token to the given filepath.

        :param self:
        :param filepath:
        :return:
        """

        try:
            with open(filepath, "w") as f:
                json.dump({"token": self.__token}, f)
                f.flush()

                logger.info(f"Token saved to {filepath}")
        except IOError as exc:
            logger.error(f"Error while saving token to {filepath} {exc}")

    def logout(self, token: Optional[str] = None) -> None:
        """Logs out the token."""

        if self.__token is None and token is None:
            raise ValueError("No token provided")

        # Set url depending on mode
        if self.__mode == 'live':
            url = self.live_base_url
        elif self.__mode == 'demo':
            url = self.demo_base_url

        params = {"token": self.__token if token is None else token}

        try:
            res = httpx.post(url=url, params=params).raise_for_status().json()

            if res['status'] == "OK":
                logger.info(f"Logout successful. {res}")
            else:
                logger.warning(f"Logout failed. {res['status']}: {res['message']}")

        except httpx.HTTPError as exc:
            logger.info(f"Error while logging out {exc.request.url!r}.")