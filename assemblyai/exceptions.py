"""Exceptions for the assemblyai library."""
import logging


class ClientError(Exception):
    """Base exception for all errors raised."""

    def __init__(self, msg=None):
        if msg is None:
            # default error message
            msg = "An error occurred in the assemblyai library"
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


class InvalidTokenError(ClientError, ValueError):
    """Error raised when API token is not valid."""

    def __init__(self, token):
        super(InvalidTokenError, self).__init__(
            "API token is not valid: {0}".format(token)
        )
        self.token = token


def handle_warnings(response, object):
    """Handle  warnings and exceptions."""
    warning = None
    if response.status_code >= 400 and response.status_code < 500:
        msg = 'Authentication error'
        raise ParseResponseError(msg)
    if response.status_code >= 500:
        msg = 'Server error'
        raise ParseResponseError(msg)
    if response:
        response = response.json()[object]
    if 'warning' in response:
        warning = response['warning']
        logging.warning('Warning: %s' % warning)
    if response['status'] == 'error':
        msg = response['error']
        raise ParseResponseError(msg)
    return warning
