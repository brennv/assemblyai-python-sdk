=====================
assemblyai-python-sdk
=====================


.. image:: https://img.shields.io/pypi/v/assemblyai.svg
        :target: https://pypi.python.org/pypi/assemblyai

.. image:: https://img.shields.io/travis/AssemblyAI/assemblyai-python-sdk.svg
        :target: https://travis-ci.org/AssemblyAI/assemblyai-python-sdk

.. image:: https://readthedocs.org/projects/assemblyai-python-sdk/badge/?version=latest
        :target: https://assemblyai-python-sdk.readthedocs.io/en/latest/?badge=latest

.. image:: https://pyup.io/repos/github/AssemblyAI/assemblyai-python-sdk/shield.svg
     :target: https://pyup.io/repos/github/AssemblyAI/assemblyai-python-sdk/


Python wrapper for the AssemblyAI API

* Documentation: https://assemblyai-python-sdk.readthedocs.io.


Quickstart
----------

    import assemblyai

    aai = assemblyai.Client(token='your-secret-token')
    transcript = aai.transcribe('https://example.com/sample.wav')

    while transcript['status'] not in ['completed', 'error']:
        transcript = aai.poll()

    print(transcript)


Features
--------

* Transcribe audio into text
