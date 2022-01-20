import asyncio
import logging
import sys
import typing as t

import aiohttp

from .exceptions import InvalidRequest, MissingPermission
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
        headers: dict = None,
        data: dict = None,
        text_response: bool = False,
        return_status: str = False,
        auth_required: bool = True,
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
        auth_required : bool
            Whether or not the auth token is required, Defaults to True

        Returns
        -------
        t.Optional[dict]
        """
        if headers is None:
            headers = {}

        headers = {"User-Agent": self.USER_AGENT, **headers}

        # TODO: Remove this auth_required logic. Redundant, as if the endpoint doesn't require auth,
        # it'll never be read, and hence passing it won't change anything.
        if auth_required:
            headers["Authorization"] = f"Bearer {self.token}"

        if not self._session:
            self._session = aiohttp.ClientSession()

        async with self._lock:
            async with self._session.request(
                method=route.method, url=route.url, headers=headers, data=data
            ) as res:
                if return_status:
                    return res.status

                if res.status in [200, 201]:
                    if text_response:
                        data = await res.text()
                    else:
                        data = await res.json()

                else:
                    data = None

        return data

    # Utility methods.
    @staticmethod
    def clean_domain(domain: str) -> str:
        return domain.replace("https://", "").replace("http://", "")

    # Main methods.
    async def check_domain(self, domain: str) -> bool:
        """
        Checks a domain, Returns True if its suspicious else False.

        Parameters
        ----------
        domain : str
            Domain you want to look for.

        Returns
        -------
        bool

        Notes
        -----
        Even if the function returns `False`, that doesn't mean the domain is always suspicious.
        If the domain is not registered in the API database, or incorrect domain is entered,
        the function will return `False`
        """
        domain = self.clean_domain(domain)

        data = await self.fetch(
            Route("GET", f"/domains/{domain}"),
            text_response=True,
            auth_required=False,
            headers={
                "Content-Type": "text/plain"
            }
        )

        if not data:
            return False

        if "missing permission" in data:
            raise MissingPermission("You don't have permission to access this API")

        return True if data == 'true' else False

    async def fetch_info(self, domain: str) -> dict:
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
