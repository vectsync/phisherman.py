import asyncio
import logging
import sys
import typing as t

import aiohttp

from .exceptions import InvalidRequest, MissingPermission
from .route import Route

logger = logging.getLogger(__name__)

__all__: t.Tuple[str, ...] = ("Client",)

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

        self.token = token

        self._session = None
        self._lock = asyncio.Lock()

    async def close(self) -> None:
        """Close the client session with this async function"""

        if self._session is not None:
            await self._session.close()

    async def fetch(self, route: Route, **kwargs) -> t.Optional[dict]:
        """
        Fetching a response from the API

        Parameters
        ----------
        route : Route
            The API route you want to make a call to

        Returns
        -------
        t.Optional[dict]
        """

        headers = kwargs.pop("headers", {})
        data = kwargs.pop("data", None)
        text_response = kwargs.pop("text_response", False)
        return_status = kwargs.pop("return_status", False)
        auth_required = kwargs.pop("auth_required", True)

        headers = {
            "User-Agent": self.USER_AGENT,
            **headers
        }

        if auth_required:
            headers["Authorization"] = f"Bearer {self.token}"

        if not self._session:
            self._session = aiohttp.ClientSession()

        async with self._lock:
            async with self._session.request(
                route.method,
                route.url,
                headers=headers,
                data=data,
                **kwargs
            ) as res:
                if return_status:
                    return res.status

                if res.status == 200 or 201:
                    if text_response:
                        data = await res.text()
                    else:
                        data = await res.json()

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

        data = await self.fetch(
            Route("GET", f"/domains/{domain}"),
            auth_required=False
        )

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
            Domain you want to look for

        Returns
        -------
        dict
        """

        domain = domain.replace("https://", "").replace("http://", "")

        data = await self.fetch(Route("GET", f"/domains/info/{domain}"))

        if not data:
            return {}

        success = data.get("success", False)
        if not success:
            if data.get("message", "") == "missing permission":
                raise InvalidRequest("Invalid Request, Check your domain.")

        return data[domain]

    async def report_phish(self, domain: str, guild: t.Optional[int] = None) -> bool:
        """
        Report a site for phishing

        Parameters
        ----------
        domain : str
            Domain you want to look for (Don't include 'https://')
        guild : t.Optional[int]
            Discord Guild ID you found the site link in

        Returns
        -------
        bool
        """

        data = None

        if guild:
            data = {"guild": str(guild)}

        status_code = await self.fetch(Route("POST", f"/domains/report/{domain}"), data=data)

        if status_code == 204:
            logger.info(f"Successfully reported the site `{guild}`")
            return True
        else:
            return False
