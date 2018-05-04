"""Main module."""

import json
import logging

import requests

from assemblyai.exceptions import ParseResponseError


# LOG = logging.getLogger(__name__)


transcript_url = "https://api.assemblyai.com/v1/transcript"


class Client(object):
    """Make calls to the AssemblyAI API."""

    def __init__(self, token):
        """Initialize client."""
        self.token = token
        self.transcript = None

    def transcribe(self, audio_url):
        """Request a transcript."""
        data = {"audio_src_url": audio_url}
        payload = json.dumps(data)
        headers = {'authorization': self.token}
        self.transcript = requests.post(transcript_url, data=payload,
                                        headers=headers)
        return self.transcript

    def check(self, transcript_id=None):
        """Check on a transcript."""
        if self.transcript:
            headers = {'authorization': self.token}
            url = transcript_url + '/' + self.transcript.id
            self.transcript = requests.get(url, headers=headers)
            return self.transcript
        else:
            
