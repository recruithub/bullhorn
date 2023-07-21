from typing import Any, Dict, List, Optional, Tuple, Union

from aiohttp import ClientResponse


class BullhornException(Exception):
    """Base exception class for the Bullhorn REST API wrapper library.

    This class serves as the base exception that can be caught to handle any exceptions raised from this library.
    """

    pass


class HTTPException(BullhornException):
    """Exception raised for HTTP-related errors when interacting with the Bullhorn REST API.

    This exception class contains information about the HTTP response, status code, and error message.
    """

    def __init__(
        self,
        response: ClientResponse,
        message: Optional[Union[str, Dict[str, Any]]] = None,
    ):
        """
        Initialize an HTTPException object.

        Args:
            response (ClientResponse):
                The aiohttp ClientResponse object representing the HTTP response.

            message (Optional[Union[str, Dict[str, Any]]]):
                The error message associated with the exception.
                It can be either a string or a dictionary containing additional error details.

        Attributes:
            response (ClientResponse):
                The aiohttp ClientResponse object representing the HTTP response.

            status (int):
                The status code of the HTTP response.

            code (int):
                The error code associated with the exception.
                If the message is a dictionary, it is retrieved from the "code" key.
                Otherwise, it defaults to 0.

            text (str):
                The error message text associated with the exception.
                If the message is a dictionary, it is retrieved from the "message" key.
                Otherwise, it defaults to an empty string.

        Raises:
            None

        """
        self.response: ClientResponse = response
        self.status: int = response.status_code
        self.code: int
        self.text: str

        if isinstance(message, dict):
            self.code = message.get("code", 0)
            base = message.get("message", "")
            errors = message.get("errors")
            self._errors: Optional[Dict[str, Any]] = errors

            if errors:
                errors = _flatten_error_dict(errors)
                helpful = "\n".join("In %s: %s" % t for t in errors.items())
                self.text = base + "\n" + helpful
            else:
                self.text = base
        else:
            self.text = message or ""
            self.code = 0

        fmt = f"{self.response.status_code} {self.response.reason} (error code: {self.code})"
        if len(self.text):
            fmt += f": {self.text}"

        super().__init__(fmt)


class Forbidden(HTTPException):
    """Exception that is raised when a 403 Forbidden status code occurs."""

    pass


class LoginFailure(HTTPException):
    """Exception that is raised when improper credentials are passed to log in."""

    pass


class NotFound(HTTPException):
    """Exception that is raised when a 404 Not Found status code occurs."""

    pass


class BullhornServerError(HTTPException):
    """Exception that is raised when a status code in the 500 range occurs."""

    pass


def _flatten_error_dict(d: Dict[str, Any], key: str = "") -> Dict[str, str]:
    """
    Flatten a nested error dictionary into a flat dictionary.

    This function takes a nested dictionary of errors and flattens it into a flat dictionary
    where each key represents the path to the error and the value is the corresponding error message.

    Args:
        d (Dict[str, Any]):
            The nested dictionary of errors.

        key (str, optional):
            The current key being processed in the recursive call.
            Defaults to an empty string.

    Returns:
        Dict[str, str]:
            A flat dictionary where each key represents the path to the error and the value is the error message.

    """
    # Iterate over nested dictionary and flatten into a flat dictionary
    items: List[Tuple[str, str]] = []
    for k, v in d.items():
        # Keep track of path to each error
        new_key = key + "." + k if key else k
        if isinstance(v, dict):
            try:
                # Extract error message from nested dictionary
                _errors: List[Dict[str, Any]] = v["_errors"]
            except KeyError:
                # Not at top level, so recursively call
                items.extend(_flatten_error_dict(v, new_key).items())
            else:
                items.append((new_key, " ".join(x.get("message", "") for x in _errors)))
        else:
            items.append((new_key, v))
    # Return items list as the flattened error dictionary
    return dict(items)
