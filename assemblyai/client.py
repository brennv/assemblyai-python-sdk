"""Client module."""

# import logging

from assemblyai.config import ASSEMBLYAI_URL, ASSEMBLYAI_TOKEN
# from assemblyai.exceptions import handle_warnings
from assemblyai.model import Model
from assemblyai.transcript import Transcript
# from assemblyai.token import trial_token, validate_token


class Client(object):
    """Client for the AssemblyAI API."""

    def __init__(self, token=None, email=None):
        """Initialize client."""
        self.token = token or ASSEMBLYAI_TOKEN  # or trial_token()
        # validate_token(self.token)
        self.headers = {'authorization': self.token}
        self.api = ASSEMBLYAI_URL

    def __repr__(self):
        return 'Client(token=%s)' % self.token[0:8] + '...'

    def train(self, phrases, closed_domain=None, name=None):
        """Create a custom language model."""
        client = self
        self.model = Model(client, phrases=phrases,
                           closed_domain=closed_domain, name=name)
        self.model = self.model.create()
        return self.model

    def transcribe(self, audio_url, model=None):
        """Create a transcript request. If the transcript depends on a
        custom language model, defer creation until model is trained."""
        client = self
        self.transcript = Transcript(client, audio_url=audio_url,
                                     model=model)
        self.transcript = self.transcript.create()
        return self.transcript
