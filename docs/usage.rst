=====
Usage
=====

To use assemblyai in a project::

    import assemblyai

    aai = assemblyai.Client(token='your-secret-token')
    transcript = aai.transcribe('https://example.com/sample.wav')

    while transcript['status'] not in ['completed', 'error']:
        transcript = aai.poll()

    print(transcript)
