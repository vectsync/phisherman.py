import typing as t


class Route:
    """
    Class used for constructing API endpoints with a given base URL

    Attributes
    ----------
    method : t.Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
        Method for the API Call
    path : str
        Endpoints for the API
    """

    BASE_URL = "https://api.phisherman.gg/v2"

    def __init__(
        self, method: t.Literal["GET", "POST", "PUT", "DELETE", "PATCH"], path: str
    ) -> None:
        """
        Construct a route

        Parameters
        ----------
        method : str
            Method for the API Call
        path : str
            Endpoints for the API
        """

        self.method = method.upper()
        self.path = path

    @property
    def base_url(self) -> str:
        """Base URL"""
        return self.BASE_URL

    @base_url.setter
    def base_url(self, url: str) -> None:
        """
        Base URL setter

        Parameters
        ----------
        url : str
            the URL you want to set
        """
        self.BASE_URL = url

    @property
    def url(self) -> str:
        """Returns the complete route with the"""
        return self.base_url + self.path
