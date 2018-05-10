"""Exceptions for the assemblyai library."""

import logging


def handle_warnings(response, object):
    """Handle  warnings and exceptions."""
    warning = None
    if response.status_code >= 400 and response.status_code < 500:
        msg = response.json()
        raise ClientError(msg)
    if response.status_code >= 500:
        msg = 'Server error, developers have been alerted.'
        raise ServerError(msg)
    if response:
        response = response.json()[object]
    if 'warning' in response:
        warning = response['warning']
        logging.warning('Warning: %s' % warning)
    if response['status'] == 'error':
        msg = response['error']
        raise ServerError(msg)
    return warning


class ClientError(Exception):
    pass


class ServerError(Exception):
    pass
