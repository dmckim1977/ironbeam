import json
import logging
from typing import Literal, Optional

import httpx

logger = logging.getLogger(__name__)


class Auth:
    """Provides a client class for requesting historical data from Ironbeam's API.

    `password` and `apikey` are the same.
    The API Key is used as a password in the request.

    # TODO: Need to implement for Tenant users.

    :param some_param: Description

    :return:

    :Examples
    """

    MODE = Literal['demo', 'live']

    def __init__(
            self,
            username: str,
            apikey: str,
            mode: Optional[MODE] = "demo",
            api_secret: Optional[str] = None,
    ):
        self.__api_secret = api_secret
        self.__username = username
        self.__apikey = apikey
        self.__mode = mode

        self.demo_url: str = "https://demo.ironbeamapi.com/v2/auth"
        self.live_url: str = "https://live.ironbeamapi.com/v2/auth"

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
    def username(self) -> str:
        return self.__username

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

    def authorize(self) -> str:
        """

        :return: Returns the api token.
        """

        payload = {
            "Username": self.__username,
            "ApiKey": self.__apikey,
        }

        headers = {"Content-Type": "application/json"}

        # Set url depending on mode
        if self.__mode == 'live':
            url = self.live_url
        elif self.__mode == 'demo':
            url = self.demo_url

        try:
            res = httpx.post(
                url=url, json=payload, headers=headers
            ).raise_for_status().json()

            logger.info(f"Authorization successful. Token: {res['token']}")

            self.__token = res['token']

            return res["token"]

        except httpx.HTTPError as exc:
            print(f"Error while requesting {exc.request.url!r}.")
            return {"error": "token could not be authenticated."}

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
