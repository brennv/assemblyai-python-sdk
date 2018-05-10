"""Client module."""

import json
import logging

from assemblyai.config import ASSEMBLYAI_URL, ASSEMBLYAI_TOKEN
from assemblyai.exceptions import handle_warnings
# from assemblyai.token import trial_token, validate_token
import requests


class Model(object):
    """Language model object."""

    def __init__(self, headers=None, phrases=None, closed_domain=None, name=None):
        self.headers = headers
        self.phrases = phrases
        self.closed_domain = closed_domain
        self.name = name
        self.id = None
        self.status = None
        self.warning = None
        self.dict = None

    def __repr__(self):
        return 'Model(id=%s, status=%s)' % (self.id, self.status)

    def props(self):
        return [i for i in self.__dict__.keys() if i[:1] != '_']

    def reset(self, id=None):
        if id:
            self.id = id
            self.status = None
            self.name = None
            self.phrases = None
            self.closed_domain = None
            self.warning = None
            self.dict = None

    def create(self):
        data = {}
        data["phrases"] = self.phrases  # TODO validate phrases
        if self.name:
            data['name'] = self.name
        if self.closed_domain:
            data['closed_domain'] = self.closed_domain
        payload = json.dumps(data)
        url = ASSEMBLYAI_URL + '/model'
        response = requests.post(url, data=payload, headers=self.headers)
        self.warning = handle_warnings(response, 'model')
        response = response.json()['model']
        self.id, self.status = response['id'], response['status']
        logging.debug('Model %s %s' % (self.id, self.status))
        return self

    def get(self, id=None):
        """Get a language model."""
        self.reset(id)
        url = ASSEMBLYAI_URL + '/model/' + str(self.id)
        response = requests.get(url, headers=self.headers)
        self.warning = handle_warnings(response, 'model')
        response = response.json()['model']
        # self.phrases = response['phrases']
        self.dict = response
        self.status = response['status']
        logging.debug('Model %s %s' % (self.id, self.status))
        return self


class Transcript(object):
    """Transcript object."""

    def __init__(self, headers=None, audio_url=None, model=None):
        self.headers = headers
        self.audio_url = audio_url
        self.model = model
        self.id = None
        self.status = None
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

    def props(self):
        return [i for i in self.__dict__.keys() if i[:1] != '_']

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

    def create(self):
        # TODO remove model checking after api defaults to waiting for models
        if self.model:
            self.model = self.model.get()
        if self.model and self.model.status != 'trained':
            self.status = 'waiting for model'
        else:
            data = {}
            data['audio_src_url'] = self.audio_url
            if self.model:
                data['model_id'] = self.model.id
            payload = json.dumps(data)
            url = ASSEMBLYAI_URL + '/transcript'
            response = requests.post(url, data=payload, headers=self.headers)
            self.warning = handle_warnings(response, 'transcript')
            logging.warning(response.status_code)
            logging.warning(response.json())
            response = response.json()['transcript']
            self.id, self.status = response['id'], response['status']
            logging.debug('Transcript %s %s' % (self.id, self.status))
        return self

    def check_model(self):
        # TODO remove model checking after api defaults to waiting for models
        self.model = self.model.get()
        if self.model.status == 'trained' and not self.id:
            self = self.create()
        else:
            self.status = 'waiting for model'

    def get(self, id=None):
        """Get a transcript."""
        self.reset(id)
        if self.model:
            self.check_model()
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


class Client(object):
    """Client for the AssemblyAI API."""

    def __init__(self, token=None, email=None):
        """Initialize client."""
        self.token = token or ASSEMBLYAI_TOKEN  # or trial_token()
        # validate_token(self.token)
        self.headers = {'authorization': self.token}
        self.api = ASSEMBLYAI_URL
        self.model = None
        self.transcript = None
        logging.warning(self.__dict__)

    def __repr__(self):
        return 'Client(token=%s)' % self.token[0:8] + '...'

    def train(self, phrases, closed_domain=None, name=None):
        """Create a custom language model."""
        self.model = Model(headers=self.headers, phrases=phrases,
                           closed_domain=closed_domain, name=name)
        self.model = self.model.create()
        return self.model

    def transcribe(self, audio_url, model=None):
        """Create a transcript request. If the transcript depends on a
        custom language model, defer creation until model is trained."""
        self.transcript = Transcript(headers=self.headers, audio_url=audio_url,
                                     model=model)
        self.transcript = self.transcript.create()
        return self.transcript
