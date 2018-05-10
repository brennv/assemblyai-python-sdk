"""Client module."""

import json
import logging

from assemblyai.config import ASSEMBLYAI_URL, ASSEMBLYAI_TOKEN
from assemblyai.exceptions import handle_warnings
# from assemblyai.token import trial_token, validate_token
import requests


class Model(object):
    """Language model object."""

    def __init__(self, headers):
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

    def reset(self, id=None):
        if id:
            self.id = id
            self.status = None
            self.name = None
            self.phrases = None
            self.closed_domain = None
            self.warning = None
            self.dict = None

    def get(self, id=None):
        """Get a language model."""
        self.reset(id)
        url = ASSEMBLYAI_URL + '/model/' + str(self.id)
        response = requests.get(url, headers=self.headers)
        self.warning = handle_warnings(response, 'model')
        response = response.json()['model']
        self.dict = response
        self.status = response['status']
        logging.debug('Model %s %s' % (self.id, self.status))
        return self

    def props(self):
        return [i for i in self.__dict__.keys() if i[:1] != '_']


class Transcript(object):
    """Transcript object."""

    def __init__(self, headers, audio_url=None, model=None):
        self.headers = headers
        self.id = None
        self.audio_url = audio_url
        self.model = model
        self.status = None
        self.audio_url = None
        self.warning = None
        self.text = None
        self.text_raw = None
        self.confidence = None
        self.segments = None
        self.speaker_count = None
        self.dict = None

    def __repr__(self):
        return 'Transcript(id=%s, status=%s, text=%s)' % (
            self.id, self.status, self.text)

    def reset(self, id=None):
        if id:
            self.id = id
            self.status = None
            self.audio_url = None
            self.warning = None
            self.model = None
            self.text = None
            self.text_raw = None
            self.confidence = None
            self.segments = None
            self.speaker_count = None
            self.dict = None

    def get(self, id=None):
        """Get a transcript."""
        self.reset(id)
        data = {}
        if self.model and self.model.status not in ['trained', 'error']:
            # Check for model updates if it's in training
            self.model = self.model.get()
            if self.model.status not in ['trained', 'error']:
                self.status = 'waiting for model'
        if self.model and self.model.status == 'trained':
            data['model_id'] = self.model.id
            # Request a transcript if the model is trained
            if not self.id and self.audio_url:
                self = self.create(audio_url=self.audio_url, model=self.model)
        # if not self.id and self.audio_url and not self.model:
        #     # Create a transcript in case transcribe was skipped
        #     self = self.create(audio_url=self.audio_url)
        elif self.id:
            url = ASSEMBLYAI_URL + '/transcript/' + str(self.id)
            response = requests.get(url, headers=self.headers)
            self.warning = handle_warnings(response, 'transcript')
            response = response.json()['transcript']
            self.dict = response
            self.id, self.status = response['id'], response['status']
            # if self.status == 'completed':
            self.text_raw = response['text']
            self.text = response['text_formatted']
            self.confidence = response['confidence']
            self.segments = response['segments']
            self.speaker_count = response['speaker_count']
        logging.debug('Transcript %s %s' % (self.id, self.status))
        return self

    def props(self):
        return [i for i in self.__dict__.keys() if i[:1] != '_']


class Client(object):
    """Client for the AssemblyAI API."""

    def __init__(self, token=None, email=None):
        """Initialize client."""
        self.token = token or ASSEMBLYAI_TOKEN  # or trial_token()
        # validate_token(self.token)
        self.headers = {'authorization': self.token}
        self.api = ASSEMBLYAI_URL
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
        url = ASSEMBLYAI_URL + '/model'
        response = requests.post(url, data=payload, headers=self.headers)
        self.model.warning = handle_warnings(response, 'model')
        response = response.json()['model']
        self.model.id, self.model.status = response['id'], response['status']
        logging.debug('Model %s %s' % (self.model.id, self.model.status))
        return self.model

    def create_transcript(self, data):
        payload = json.dumps(data)
        url = ASSEMBLYAI_URL + '/transcript'
        response = requests.post(url, data=payload, headers=self.headers)
        self.warning = handle_warnings(response, 'transcript')
        response = response.json()['transcript']
        self.transcript.id = response['id']
        self.transcript.status = response['status']
        logging.debug('Transcript %s %s' % (
            self.transcript.id, self.transcript.status))
        return self.transcript

    def transcribe(self, audio_url, model=None):
        """Create a transcript request. If the transcript depends on a
        custom language model, defer creation until model is trained."""
        data = {}
        data["audio_src_url"] = audio_url
        self.transcript = Transcript(self.headers, audio_url, model)
        # TODO remove model checking after api defaults to waiting for models
        if model:
            if model.status == 'trained':
                data['model_id'] = model.id
                self.transcript = self.create_transcript(data)
            elif model.status == 'error':
                raise model.error
            elif model.status not in ['trained', 'error']:
                self.transcript.status = 'waiting for model'
        else:
            self.transcript = self.create_transcript(data)
        return self.transcript
