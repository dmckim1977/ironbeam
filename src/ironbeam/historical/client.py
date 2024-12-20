import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


class Historical:
    """Provides a client class for requesting historical data from Ironbeam's API.

    :param some_param: Description

    :return:

    :Examples
    """

    def __init__(
            self,
            mode: str = "demo",
            username: Optional[str] = None,
            apikey: Optional[str] = None,
            api_secret: Optional[str] = None,
    ):
        self.__api_secret = api_secret
        self.__username = username
        self.__apikey = apikey
        self.mode = mode

        self.demo_auth_url: str = "https://demo.ironbeamapi.com/v2/auth"
        self.demo_url: str = ""

        self.live_auth_url: str = ""
        self.live_url: str = ""

        logger.info("Setting up Ironbean Historical Client.")

        self.token: str | None = None

    @property
    def apikey(self) -> str:
        return self.__apikey

    @property
    def api_secret(self) -> str:
        return self.__secret

    @property
    def username(self) -> str:
        return self.__username

    def authorize(self) -> str | None:

        payload = {
            "Username": self.__username,
            "ApiKey": self.__apikey,
        }

        headers = {"Content-Type": "application/json"}

        try:
            res = httpx.post(
                url=self.demo_auth_url, json=payload, headers=headers
            ).raise_for_status().json()

            logger.info(f"Authorization successful. Token: {res['token']}")

            return res

        except httpx.HTTPError as exc:
            logger.error(f"Error while requesting {exc.request.url!r}.")
