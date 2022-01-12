import aiohttp
import logging
import typing as t

from .errors import InvalidRequest, MissingPermission

logger = logging.getLogger(__name__)

__all__: t.List[str] = ["Application"]


class Application:
    """
    Application class for the API Wrapper

    Attributes
    ----------
    token : str
        API Token from phisherman.gg
    base_url : str
        Base URL to access the API
    session : aiohttp.ClientSession
        For creating client session and to make requests

    """

    def __init__(self, token: str, version: t.Optional[int] = 1) -> None:
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
        self.base_url = f"https://api.phisherman.gg/v{version}"
        self.session = aiohttp.ClientSession()

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

        res = await self.session.get(
            self.base_url + f"/domains/{domain}",
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Phisherman.py (https://github.com/QristaLabs/phisherman.py)",
            },
        )

        data = await res.read()

        if "missing permissions" in data.decode("utf-8"):
            await self.session.close()

            raise MissingPermission("Missing permission for the API call")

        await self.session.close()

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

        data = await res.json()

        try:
            if data["success"] is False:
                await self.session.close()

                if data["message"] == "invalid request":
                    raise InvalidRequest("Invalid Request, Check your domain")

        except KeyError:
            await self.session.close()

            return data[domain]

    async def report_phish(self, domain: str, guild: t.Optional[int]) -> None:
        """
        Report a site for phishing

        Parameters
        ----------
        domain : str
            Domain you want to look for (Don't include 'https://')
        guild : t.Optional[int]
            Discord Guild ID you found the site link in
        """

        if guild:
            res = await self.session.put(
                self.base_url + f"/domains/{domain}",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                    "User-Agent": "Phisherman.py (https://github.com/QristaLabs/phisherman.py)",
                },
                data={"guild": f"{guild}"},
            )
        else:
            res = await self.session.put(
                self.base_url + f"/domains/{domain}",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                    "User-Agent": "Phisherman.py (https://github.com/QristaLabs/phisherman.py)",
                },
            )

        if res.status == 204:
            logger.info(f"Reported site '{domain}' successfully")
