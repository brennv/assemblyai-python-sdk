"""WIP module for token handling."""

import json
import logging

import requests

from assemblyai.exceptions import InvalidTokenError


def validate_token(token):
    url = ASSEMBLY_URL + '/token/' + token
    response = requests.get(url)
    # _ = handle_warnings(response, 'trial')
    response = response.json()['token']
    token, expires = response['token'], response['expires']
    valid, type = response['valid'], response['type']
    logging.debug('%s token expires %s' % (type, expires))
    if not vaild:
        raise InvalidTokenError(token)


def trial_token():
    url = ASSEMBLY_URL + '/trial'
    response = requests.post(url)
    # _ = handle_warnings(response, 'trial')
    response = response.json()['trial']
    token, expires = response['token'], response['expires']
    logging.warning('Trial token expires %s' % expires)
    logging.warning('Please create an account at assemblyai.com to validate token.')
    return token
