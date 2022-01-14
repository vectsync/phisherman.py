class Route:
    """
    Class used for constructing API endpoints with a given base URL

    Attributes
    ----------
    method : str
        Method for the API Call
    path : str
        Endpoints for the API
    """

    BASE_URL = "https://api.phisherman.gg/v1"

    def __init__(self, method: str, path: str) -> None:
        """
        Construct a route

        Parameters
        ----------
        method : str
            Method for the API Call
        path : str
            Endpoints for the API
        """

        self.method = method
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
        """Return's the route i.e the base URL plus the given path"""

        return self.base_url + self.path
