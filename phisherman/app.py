import asyncio
import logging
import sys
import typing as t

import aiohttp

from .exceptions import InvalidRequest, MissingPermission
from .route import Route

# Logger.
logger = logging.getLogger(__name__)

# Star imports.
__all__: t.Tuple[str, ...] = ("Client",)

# Constants.
PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


class Client:
    """
    Client class for the Phiserman API Wrapper.

    Attributes
    ----------
    token : str
        API Token from phisherman.gg
    base_url : str
        Base URL to access the API
    session : aiohttp.ClientSession
        For creating client session and to make requests
    """
    USER_AGENT = f"Phisherman API wrapper. Python/{PYTHON_VERSION} Aiohttp/{aiohttp.__version__}"

    def __init__(self, token: str) -> None:
        """
        Construct an application

        Parameters
        ----------
        token : str
            Phisherman.gg API Token
        version : t.Optional[int]
            Optional Argument for the API Version, Default to 1 for now
        """
        # Token.
        self.token = token

        # Session and Lock.
        self._session = None
        self._lock = asyncio.Lock()

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()

    async def fetch(self, route: Route, **kwargs) -> t.Optional[dict]:
        headers = kwargs.pop("headers", {})
        data = kwargs.pop("data", None)
        text_response = kwargs.pop("text_response", False)
        return_status = kwargs.pop("return_status", False)

        # Initialize headers.
        headers = {
            "User-Agent": self.USER_AGENT,
            "Authorization": f"Bearer {self.token}",
            **headers
        }

        # Initialize session.
        if not self._session:
            self._session = aiohttp.ClientSession()

        # Fetch.
        async with self._lock:
            async with self._session.request(
                route.method,
                route.url,
                headers=headers,
                data=data,
                **kwargs
            ) as res:
                # If return status is True, return the status code.
                if return_status:
                    return res.status

                # If status code is between 200 and 300.
                if 300 > res.status >= 200:
                    if text_response:
                        data = await res.text()
                    else:
                        data = await res.json()

                # Else, set to None.
                else:
                    data = None

        return data


    async def check_domain(self, domain: str) -> bool:
        """
        Checks a domain, Returns True if its suspicious else False

        NOTE: Even if it returns false doesn't mean the domain isn't suspicious
        it's just that the domain isn't registered in the API's Database or you
        might have entered incorrect domain

        Parameters
        ----------
        domain : str
            Domain you want to look for (Don't include 'https://')

        Returns
        -------
        bool
        """
        data = await self.fetch(Route("GET", "/domains/{domain}"), text_response=True)

        if not data:
            return False

        if "missing permission" in data:
            raise MissingPermission("You don't have permission to access this API")

        return True if data == b"true" else False

    async def fetch_info(self, domain: str) -> dict:
        """
        Fetch's Information for a domain

        Parameters
        ----------
        domain : str
            Domain you want to look for (Don't include 'https://')

        Returns
        -------
        dict
        """

        res = await self.session.get(
            self.base_url + f"/domains/info/{domain}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "Phisherman.py (https://github.com/QristaLabs/phisherman.py)",
            },
        )

        # Strip `http://` or `https://` from the domain.
        domain = domain.replace("https://", "").replace("http://", "")

        data = await self.fetch(Route("GET", f"/domains/info/{domain}"))

        if not data:
            return {}

        success = data.get("success", False)
        if not success:
            if data.get("message", "") == "missing permission":
                raise MissingPermission("Invalid Request, Check your domain.")

        return data[domain]

    async def report_phish(self, domain: str, guild: t.Optional[int]) -> bool:
        """
        Report a site for phishing

        Parameters
        ----------
        domain : str
            Domain you want to look for (Don't include 'https://')
        guild : t.Optional[int]
            Discord Guild ID you found the site link in
        """
        data = None

        if guild:
            data = {"guild": str(guild)}

        status_code = await self.fetch(Route("POST", f"/domains/report/{domain}"), data=data)

        if status_code == 204:
            return True
        else:
            return False
