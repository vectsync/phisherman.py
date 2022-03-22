import asyncio
import logging
import sys
import typing as t

import aiohttp

from .exceptions import InvalidRequest, MissingPermission
from .models import DomainCheck
from .route import Route

__all__: t.Tuple[str, ...] = ("Client",)

# Logging.
logger = logging.getLogger(__name__)

PYTHON_VERSION = (
    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
)


class Client:
    """
    Client class for the Phisherman API Wrapper.

    Attributes
    ----------
    token : str
        API Token from phisherman.gg
    base_url : str
        Base URL to access the API
    session : aiohttp.ClientSession
        For creating client session and to make requests
    """

    USER_AGENT = f"Phisherman API wrapper - Python/{PYTHON_VERSION} AIOHTTP/{aiohttp.__version__}"

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

        # Session with lock for preventing deadlocks.
        self._session = None
        self._lock = asyncio.Lock()

    async def close(self) -> None:
        """Close the client session."""
        if self._session is not None:
            await self._session.close()

    async def fetch(
        self,
        route: Route,
        *,
        headers: t.Optional[dict] = None,
        data: t.Optional[dict] = None,
        text_response: bool = False,
        return_status: bool = False
    ) -> t.Optional[dict]:
        """
        Fetching a response from the API

        Parameters
        ----------
        route : Route
            The API route you want to make a call to
        headers : dict
            Headers for the API call, Defaults to None
        data : dict
            Data for the API call, Defaults to None
        text_response : bool
            Whether or not to expect text response, Defaults to False

        Returns
        -------
        t.Optional[dict]
        """
        if headers is None:
            headers = {}

        headers = {
            "User-Agent": self.USER_AGENT,
            "Authorization": f"Bearer {self.token}",
            **headers
        }

        if not self._session:
            self._session = aiohttp.ClientSession()

        async with self._lock:
            async with self._session.request(
                method=route.method, url=route.url, headers=headers, data=data
            ) as res:
                if return_status:
                    return res.status

                # Handle status codes
                if res.status in [200, 201, 204]:
                    if text_response:
                        data = await res.text()
                    else:
                        data = await res.json()

                if res.status == 400:
                    raise InvalidRequest("Bad request - Request performed was invalid.")

                if res.status == 401:
                    raise MissingPermission("Request not authenticated - Check your API token.")

                if res.status == 403:
                    raise MissingPermission("Permission not exists - Check your Permissions for API.")

                if res.status == 429:
                    raise InvalidRequest("Too many requests - Slow down your requests.")

                if res.status == 500:
                    raise InvalidRequest("Internal Server Error - Something went wrong.")

        return data

    # Utility methods.
    @staticmethod
    def clean_domain(domain: str) -> str:
        return domain.replace("https://", "").replace("http://", "")

    # Main methods.
    async def check_domain(self, domain: str) -> t.Optional[DomainCheck]:
        """
        Checks a domain, Returns DomainCheck model with data.

        Parameters
        ----------
        domain : str
            Domain you want to look for.

        Returns
        -------
        DomainCheck
        """
        domain = self.clean_domain(domain)

        data = await self.fetch(
            Route("GET", f"/domains/check/{domain}"),
        )

        if not data:
            return None

        return DomainCheck.from_dict(data)

    async def fetch_info(self, domain: str) -> t.Optional[dict]:  # TODO: Convert to custom dataclass.
        """
        Fetch the information for a domain.

        Parameters
        ----------
        domain : str
            Domain you want to look for

        Returns
        -------
        dict
        """
        domain = self.clean_domain(domain)

        data = await self.fetch(Route("GET", f"/domains/info/{domain}"))

        if not data:
            return None

        return data[domain]

    async def report_phish(self, domain: str, guild: t.Optional[int] = None) -> bool:
        """
        Report a site for phishing

        Parameters
        ----------
        domain : str
            Domain you want to report as a phising site.
        guild : t.Optional[int]
            Discord Guild ID where you discovered the site link.

        Returns
        -------
        bool
        """
        domain = self.clean_domain(domain)
        data = None

        if guild:
            data = {"guild": str(guild)}

        status_code = await self.fetch(
            Route("POST", f"/domains/report/{domain}"), data=data
        )

        if status_code == 204:
            logger.info(f"Successfully reported the site `{guild}`")
            return True
        else:
            return False
