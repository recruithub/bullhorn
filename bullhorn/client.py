import json
import logging
import sys
import time
from typing import Any, Callable, Coroutine, Dict, List, Optional, TypeVar, Union

import requests

from . import __version__
from .exceptions import BullhornServerError, Forbidden, HTTPException, NotFound
from .route import Route
from .types import candidate, ping, placement

T = TypeVar("T")
Response = Coroutine[Any, Any, T]
ResponseT = TypeVar("ResponseT", bound=Callable[..., Response[Any]])

logger = logging.getLogger(__name__)


class BullhornClient:
    def __init__(
        self,
        token: Optional[str] = None,
        rest_url: Optional[str] = None,
    ) -> None:
        # Set token and namespace
        self.token: Optional[str] = token
        self.rest_url: Optional[str] = rest_url
        # Set user agent
        self.user_agent: str = self._get_user_agent()

    def _get_user_agent(
        self,
    ) -> str:
        """
        Get the user agent string for the HTTP client.

        Returns:
            str:
                The user agent string combining information about the Python wrapper,
                its version, the Python interpreter version, and the aiohttp version.
        """
        version_info = sys.version_info
        user_agent_strings = [
            "Python wrapper for Bullhorn API",
            f"(https://github.com/recruithub/bullhorn {__version__})",
            f"Python/{version_info.major}.{version_info.minor}.{version_info.micro}",
            f"requests/{requests.__version__}",
        ]
        user_agent = " ".join(user_agent_strings)
        return user_agent

    def request(
        self,
        route: Route,
        files=None,
        form=None,
        **kwargs,
    ) -> Any:
        # Get attributes from route
        method = route.method
        url = route.url
        # Set headers
        headers: Dict[str, str] = {}
        headers["User-Agent"] = self.user_agent
        if self.token is not None:
            headers["BhRestToken"] = self.token
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(
                kwargs.pop("json"), separators=(",", ":"), ensure_ascii=True
            )

        # Fetch response
        data: Optional[Union[Dict[str, Any], str]] = None
        for tries in range(5):
            # Files
            if files:
                for f in files:
                    f.reset(seek=tries)
            # Form
            if form:
                form_data = aiohttp.FormData(quote_fields=False)
                for params in form:
                    form_data.add_field(**params)
                kwargs["data"] = form_data
            # Execute request
            try:
                response = requests.get(url, headers=headers)
                logger.debug(
                    f"{method} {url} with {kwargs.get('data')} has returned {response.status_code}"
                )
                data = response.json()
                # Successful request
                if 300 > response.status_code >= 200:
                    logger.debug(f"{method} {url} has received {data}")
                    return data
                # Server error, so retry request with exponential back-off
                if response.status_code in {500, 502, 503, 504, 524}:
                    time.sleep(1 + tries * 2)
                    continue
                # Client error, so raise exception
                if response.status_code == 403:
                    raise Forbidden(response, data)
                elif response.status_code == 404:
                    raise NotFound(response, data)
                elif response.status_code >= 500:
                    raise BullhornServerError(response, data)
                else:
                    raise HTTPException(response, data)
            except OSError as e:
                # Connection reset by peer, so retry with exponential back-off
                if tries < 4 and e.errno in (54, 10054):
                    time.sleep(1 + tries * 2)
                    continue
                raise
        if response is not None:
            # Out of retries, so raise an appropriate exception
            if response.status_code >= 500:
                raise BullhornServerError(response, data)
            raise HTTPException(response, data)
        # Capture unhandled logic
        raise RuntimeError(response, "Unreachable code in HTTP handling")

    def ping(
        self,
    ) -> Response[ping.Ping]:
        """Ping used to test whether the client’s session is valid."""
        request = self.request(
            Route(
                "GET",
                self.rest_url + "ping",
            )
        )
        return request

    def get_candidates(
        self,
        query: str,
        fields: str,
    ) -> Response[List[candidate.Candidate]]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/Candidate?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request

    def get_placements(
        self,
        query: str,
        fields: str,
    ) -> Response[List[placement.Placement]]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/Placement?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request
