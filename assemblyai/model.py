"""Model module."""

import json
import logging

from assemblyai.config import ASSEMBLYAI_URL
from assemblyai.exceptions import handle_warnings
import requests


class Model(object):
    """Language model object."""

    def __init__(self, client, phrases=None, closed_domain=None, name=None):
        self.headers = client.headers
        self.api = client.api
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
