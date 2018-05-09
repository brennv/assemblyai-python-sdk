"""Client module."""

import json
import logging

import requests

from assemblyai.config import ASSEMBLY_URL, ASSEMBLY_TOKEN
from assemblyai.exceptions import handle_warnings
# from assemblyai.token import trial_token, validate_token


class Model(object):
    """Language model object."""

    def __init__(self, headers, id=None):
        self.headers = headers
        self.id = id
        self.status = None
        self.name = None
        self.phrases = None
        self.closed_domain = None
        self.warning = None
        self.dict = None

    def __repr__(self):
        return 'Model(id=%s, status=%s)' % (self.id, self.status)

    def get(self):
        """Get a language model."""
        if not self.id:
            # TODO raise error if not self.id
            pass
        url = ASSEMBLY_URL + '/model/' + str(self.id)
        response = requests.get(url, headers=self.headers)
        self.warning = handle_warnings(response, 'model')
        response = response.json()['model']
        self.dict = response
        self.status = response['status']
        logging.debug('Model %s %s' % (self.id, self.status))
        return self


class Transcript(object):
    """Transcript object."""

    def __init__(self, headers, id=None):
        self.headers = headers
        self.id = id
        self.status = None
        self.audio_url = None
        self.model_id = None
        self.warning = None
        self.model = None
        self.text = None
        self.text_raw = None
        self.confidece = None
        self.segments = None
        self.speaker_count = None
        self.dict = None

    def __repr__(self):
        return 'Transcript(id=%s, status=%s, text=%s)' % (
            self.id, self.status, self.text)

    def get(self):
        """Get a transcript."""
        data = {}
        if self.model and self.model['status'] not in ['trained', 'error']:
            self.model = self.model.get()
        if self.model and self.model['status'] == 'trained':
            data['model_id'] = self.model.id
            if not self.id and self.audio_url:
                self = self.create(audio_url=self.audio_url, model=self.model)
        if not self.id and self.audio_url and not self.model:
            self = self.create(audio_url=self.audio_url)
        elif self.id:
            url = ASSEMBLY_URL + '/transcript/' + str(self.id)
            response = requests.get(url, headers=self.headers)
            self.warning = handle_warnings(response, 'transcript')
            response = response.json()['transcript']
            self.dict = response
            self.id, self.status = response['id'], response['status']
            # if self.status == 'completed':
            self.text_raw = response['text']
            self.text = response['text_formatted']
            self.confidece = response['confidence']
            self.segments = response['segments']
            self.speaker_count = response['speaker_count']
        logging.debug('Transcript %s %s' % (self.id, self.status))
        return self


class Client(object):
    """Client for the AssemblyAI API."""

    def __init__(self, token=None, email=None):
        """Initialize client."""
        self.token = token or ASSEMBLY_TOKEN  # or trial_token()
        # validate_token(self.token)
        self.headers = {'authorization': self.token}
        self.api = ASSEMBLY_URL
        self.model = Model(self.headers)
        self.transcript = Transcript(self.headers)

    def __repr__(self):
        return 'Client(token=%s)' % self.token[0:8] + '...'

    def train(self, phrases, closed_domain=None, name=None):
        """Create a custom language model."""
        data = {}
        # TODO validate phrases
        data["phrases"] = phrases
        if name:
            data['name'] = name
        if closed_domain:
            data['closed_domain'] = closed_domain
        payload = json.dumps(data)
        url = ASSEMBLY_URL + '/model'
        response = requests.post(url, data=payload, headers=self.headers)
        self.model.warning = handle_warnings(response, 'model')
        response = response.json()['model']
        self.model.id, self.model.status = response['id'], response['status']
        logging.debug('Model %s %s' % (self.model.id, self.model.status))
        return self.model

    def transcribe(self, audio_url, model=None):
        """Create a transcript request. If the transcript depends on a
        custom language model, defer creation until model is trained."""
        data = {}
        if model and model.status == 'trained':
            data['model_id'] = model.id
        elif model and model.status == 'error':
            raise model.error
        elif model and model.status not in ['trained', 'error']:
            pass
        else:
            data["audio_src_url"] = audio_url or self.audio_url
            # TODO raise error if not audio_url
            payload = json.dumps(data)
            url = ASSEMBLY_URL + '/transcript'
            response = requests.post(url, data=payload, headers=self.headers)
            self.warning = handle_warnings(response, 'transcript')
            response = response.json()['transcript']
            self.transcript.id = response['id']
            self.transcript.status = response['status']
            logging.debug('Transcript %s %s' % (
                self.transcript.id, self.transcript.status))
        return self.transcript
