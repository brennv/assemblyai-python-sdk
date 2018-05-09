"""Tests for client."""

import os

import pytest

from assemblyai import Client
from assemblyai.exceptions import ClientAuthError


ASSEMBLY_URL = os.environ.get('ASSEMBLY_URL', 'https://api.assemblyai.com')
ASSEMBLY_TOKEN = os.environ.get('ASSEMBLY_TOKEN')
AUDIO_URL = 'https://s3-us-west-2.amazonaws.com/assemblyai.prooflab/office_nine_degrees.wav'


def test_client_auth_error():
    """Test client without token throws auth error."""
    with pytest.raises(ClientAuthError):
        aai = Client(token='foobar')
        aai.transcribe(AUDIO_URL)


def test_client_transcribe():
    """Test client token authenticates and creates transcript."""
    aai = Client(token=ASSEMBLY_TOKEN)
    transcript = aai.transcribe(AUDIO_URL)
    assert transcript.status == 'queued'
    transcript_id = transcript.id
    while transcript.status != 'completed':
        transcript = transcript.get()
    assert transcript.status == 'completed'
    assert transcript_id == transcript.id


def test_client_train():
    """Test client token authenticates and creates transcript."""
    aai = Client(token=ASSEMBLY_TOKEN)
    model = aai.train(['foo', 'bar'])
    assert model.status == 'training'
    model_id = model.id
    model = model.get()
    assert model.status == 'queued'
    assert model_id == model.id


def test_client_train_transcribe():
    """Test client token authenticates and creates transcript."""
    aai = Client(token=ASSEMBLY_TOKEN)
    model = aai.train(['foo', 'bar'])
    assert model.status == 'training'
    model_id = model.id
    model = model.get()
    assert model.status == 'queued'
    assert model_id == model.id
    transcript = aai.transcribe(AUDIO_URL, model=model)
    assert transcript.id is None
    transcript = transcript.get()
    assert transcript.id is None
