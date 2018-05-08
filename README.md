# assemblyai-python-sdk

![](https://img.shields.io/pypi/v/assemblyai.svg)
![](https://img.shields.io/travis/AssemblyAI/assemblyai-python-sdk.svg)
![](https://readthedocs.org/projects/assemblyai-python-sdk/badge/?version=latest)
![](https://pyup.io/repos/github/AssemblyAI/assemblyai-python-sdk/shield.svg)

Transcribe audio into text. Create custom language models for higher accuracy.

- Documentation: https://assemblyai-python-sdk.readthedocs.io
- Issues: https://github.com/assemblyai/assemblyai-python-sdk
- Support: https://assemblyai.com
- Community: https://assemblyaicommunity.slack.com


## Getting started

Obtain an API token from https://assemblyai.com and run pip install.

```shell
pip install -U assemblyai
```

## Quickstart

```python
import assemblyai

aai = assemblyai.Client(token='secret-token')

transcript = aai.transcribe('https://example.com/sample.wav')

while transcript.status != 'completed':
    transcript = transcript.get()

text = transcript.text
```

Transcripts take about half the duration of the audio to complete.


## Custom language models

The quickstart example transcribes audio using a generic English language model.

In order to retain accuracy with unique word sets, create a custom language model.

For this example we'll train a new model using a list of phrases from wikipedia.

```python
import assemblyai
import wikipedia

aai = assemblyai.Client(token='secret-token')

phrases = wikipedia.page("Pokemon characters").content.split('. ')

model = aai.train(phrases)

transcript = aai.transcribe('https://example.com/pokemon.wav', model=model)

while transcript.status != 'completed':
    transcript = transcript.get()

text = transcript.text
```


## Model and Transcript attributes

Initially, models take six minutes to train, after which they can be invoked by ID.

```python
model = assemblyai.Model(id=model_id)
```

Prior transcripts can also be called by ID.

```python
transcript = assemblyai.Transcript(id=transcript_id)
```

To inspect additional attributes, like `transcript.confidence` try:

```Python
help(model)
help(transcript)
```

Or inspect the raw API responses using:

```Python
model.dict
transcript.dict
```

For additional background see: https://docs.assemblyai.com
