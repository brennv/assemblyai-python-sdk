# assemblyai-python-sdk

![](https://img.shields.io/pypi/v/assemblyai.svg)
![](https://img.shields.io/travis/AssemblyAI/assemblyai-python-sdk.svg)
![](https://readthedocs.org/projects/assemblyai-python-sdk/badge/?version=latest)
![](https://pyup.io/repos/github/AssemblyAI/assemblyai-python-sdk/shield.svg)

Transcribe audio into text. Create custom language models for higher accuracy.

- Documentation: https://assemblyai-python-sdk.readthedocs.io.

## Quickstart

```python
import assemblyai

aai = assemblyai.Client(token='your-secret-token')

transcript = aai.transcribe('https://example.com/sample.wav')

while transcript.status is not 'completed':
    transcript = transcript.get()

text = transcript.text
```

Transcripts take about half the duration of the audio to complete.


## Custom language models

The quickstart example transcribes audio using a generic English language model.

In order to retain accuracy with unique word sets, create a custom language model.

For this example we'll train a new model using Pokemon characters from Wikipedia.

```python
import assemblyai
import wikipedia

aai = assemblyai.Client(token='your-secret-token')

phrases = wikipedia.page("Pokemon characters").content.split('. ')

model = aai.train(phrases)

transcript = aai.transcribe('https://example.com/pokemon.wav', model=model)

while transcript.status is not 'completed':
    transcript = transcript.get()

text = transcript.text
```

Initially, models take six minutes to train, but afterwords they can be invoked by ID.
