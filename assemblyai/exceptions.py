"""Exceptions for the assemblyai library."""


class ClientError(Exception):
    """Base exception for all errors raised by the assemblyai library."""

    def __init__(self, msg=None):
        if msg is None:
            # default error message
            msg = "An error occurred in the SlackClient library"
        super(ClientError, self).__init__(msg)


class ParseResponseError(ClientError, ValueError):
    """Error raised when API responses cannot be parsed as valid JSON."""

    def __init__(self, response_body, original_exception):
        super(ParseResponseError, self).__init__(
            "API response body could not be parsed: {0}. Original exception: {1}".format(
                response_body, original_exception
            )
        )
        self.response_body = response_body
        self.original_exception = original_exception
