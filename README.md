# assemblyai-python-sdk

![](https://img.shields.io/pypi/v/assemblyai.svg)
![](https://img.shields.io/travis/AssemblyAI/assemblyai-python-sdk.svg)
![](https://readthedocs.org/projects/assemblyai-python-sdk/badge/?version=latest)
![](https://pyup.io/repos/github/AssemblyAI/assemblyai-python-sdk/shield.svg)

Python wrapper for the AssemblyAI API

- Documentation: https://assemblyai-python-sdk.readthedocs.io.

## Quickstart

```python
import assemblyai

aai = assemblyai.Client(token='your-secret-token')
transcript = aai.transcribe('https://example.com/sample.wav')

while transcript['status'] not in ['completed', 'error']:
    transcript = aai.poll()

print(transcript)
```

## Features

- Transcribe audio into text
