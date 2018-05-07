"""Client module."""

import json
import logging
import os
import time

import requests

# from assemblyai.exceptions import ParseResponseError


# LOG = logging.getLogger(__name__)


class Client(object):
    """Make calls to the AssemblyAI API."""

    def __init__(self, token=None):
        """Initialize client."""
        self.token = token
        if not self.token:
            self.token = os.environ.get('ASSEMBLYAI_TOKEN')
        # TODO validate token
        if not self.token:
            pass  # TODO raise auth error
        self.headers = {'authorization': self.token}
        self.api = "https://api.assemblyai.com"
        self.transcript = None

    def transcribe(self, audio_url=None):
        """Request a transcript."""
        url = self.api + '/transcript'
        if not self.transcript:
            data = {"audio_src_url": audio_url}
            payload = json.dumps(data)
            response = requests.post(url, data=payload, headers=self.headers)
            self.transcript = response.json()['transcript']
            id, status = self.transcript['id'], self.transcript['status']
        elif self.transcript['status'] in ['completed', 'error']:
            id, status = self.transcript['id'], self.transcript['status']
            pass
        else:
            url += '/' + str(self.transcript['id'])
            response = requests.get(url, headers=self.headers)
            self.transcript = response.json()['transcript']
            id, status = self.transcript['id'], self.transcript['status']
            if status not in ['completed', 'error']:
                time.sleep(1)
        logging.debug('Transcript %s %s' % (id, status))
        return self.transcript

    def poll(self):
        """Request a transcript."""
        url = self.api + '/transcript'
        if not self.transcript:
            id, status = None, None
            pass  # TODO raise error
        elif self.transcript['status'] in ['completed', 'error']:
            id, status = self.transcript['id'], self.transcript['status']
            pass
        else:
            url += '/' + str(self.transcript['id'])
            response = requests.get(url, headers=self.headers)
            self.transcript = response.json()['transcript']
            id, status = self.transcript['id'], self.transcript['status']
            if status not in ['completed', 'error']:
                time.sleep(1)
        logging.debug('Transcript %s %s' % (id, status))
        return self.transcript
