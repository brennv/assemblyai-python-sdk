"""Main module."""

import json
import logging

import requests

from assemblyai.exceptions import ParseResponseError


LOG = logging.getLogger(__name__)


class Client(object):
    """Make calls to the AssemblyAI API."""

    def __init__(self, token):
        """Initialize client."""
        self.token = token
