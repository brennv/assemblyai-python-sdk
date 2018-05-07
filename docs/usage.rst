=====
Usage
=====

To use assemblyai in a project::

    import assemblyai

    aai = assemblyai.Client(token='your-secret-token')

    audio_url = 'https://example.com/sample.wav'
    transcript = aai.transcribe(audio_url)

    while transcript['status'] not in ['completed', 'error']:
        transcript = aai.poll()

    print(transcript)
