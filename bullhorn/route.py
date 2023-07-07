from typing import Dict
from urllib.parse import quote as _uriquote
from urllib.parse import urlencode


class Route:
    """
    Represents an API route, including the HTTP method, the endpoint, and any
    parameters required for the route.
    """

    def __init__(
        self,
        method: str,
        path: str,
        path_params: Dict[str, str] = {},
        query_params: Dict[str, str] = {},
    ) -> None:
        """
        Initialise a Route object representing the API method, endpoint and parameters.

        Args:
            method (str):
                The HTTP method used for the route (e.g., GET, POST, PUT, DELETE).

            path (str):
                The path or endpoint of the API route.

            **parameters (Any):
                Additional parameters or variables required for the route, if any.
                These parameters will be included in the URL by formatting the path.

        """
        self.method: str = method
        self.path: str = path
        url = self.path
        if path_params:
            url = url.format_map(
                {
                    k: _uriquote(v) if isinstance(v, str) else v
                    for k, v in path_params.items()
                }
            )
        if query_params:
            url += "?"
            url += urlencode(query_params)
        self.url: str = url

    @property
    def key(self) -> str:
        """
        Get the key representing the route.

        The key is a combination of the HTTP method and the path.

        Returns:
            str:
                The key representing the route.

        """
        return f"{self.method} {self.path}"
