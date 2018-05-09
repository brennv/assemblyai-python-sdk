"""Tests for cli."""

import os

import pytest

from click.testing import CliRunner

from assemblyai import cli


ASSEMBLY_URL = os.environ.get('ASSEMBLY_URL', 'https://api.assemblyai.com')
ASSEMBLY_TOKEN = os.environ.get('ASSEMBLY_TOKEN')
AUDIO_URL = 'https://s3-us-west-2.amazonaws.com/assemblyai.prooflab/office_nine_degrees.wav'


@pytest.fixture
def response():
    """Sample pytest fixture."""


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'WIP' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
