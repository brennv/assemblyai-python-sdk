# assemblyai

[![](https://img.shields.io/pypi/v/assemblyai.svg)](https://pypi.org/project/assemblyai/)
[![](https://codecov.io/gh/AssemblyAI/assemblyai-python-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/AssemblyAI/assemblyai-python-sdk)
[![](https://img.shields.io/travis/AssemblyAI/assemblyai-python-sdk.svg)](https://travis-ci.org/AssemblyAI/assemblyai-python-sdk/builds)
[![](https://readthedocs.org/projects/assemblyai-python-sdk/badge/?version=latest)](https://readthedocs.org/projects/assemblyai-python-sdk)
[![](https://pyup.io/repos/github/AssemblyAI/assemblyai-python-sdk/shield.svg)](https://pyup.io/repos/github/AssemblyAI/assemblyai-python-sdk)

Transcribe audio into text. Recognize made-up words and boost accuracy using custom language models.

- Documentation: https://assemblyai-python-sdk.readthedocs.io
- Issues: https://github.com/assemblyai/assemblyai-python-sdk
- Support: https://assemblyai.com
- Community: https://assemblyaicommunity.slack.com


## Getting started

Run pip install and get an API token from https://assemblyai.com

```shell
pip install -U assemblyai
```


## Quickstart

Start transcribing:

```python
import assemblyai

aai = assemblyai.Client(token='your-secret-api-token')

transcript = aai.transcribe('https://example.com/sample.wav')
```

Get the completed transcript. Transcripts take about half the duration of the
audio to complete.

```python
while transcript.status != 'completed':
    transcript = transcript.get()

text = transcript.text
```


## Custom models

The quickstart example transcribes audio using a generic English model.

In order to retain accuracy with unique word sets, create a custom model.

For this example, we create a model using a list of words/sentences found on a wikipedia page.

Create the custom model.

```python
import assemblyai
import wikipedia

aai = assemblyai.Client(token='your-secret-api-token')

phrases = wikipedia.page("List of Pokemon characters").content.split('. ')

model = aai.train(phrases)
```

Check to see that the model has finished training -- models take about six
minutes to complete.

```Python
while model.status != 'trained':
    model = model.get()
```

Reference the model when creating a transcript.

```python
transcript = aai.transcribe('https://example.com/pokemon.wav', model=model)
```


## Model and Transcript attributes

Initially, models take six minutes to train, after which they can be invoked by ID.

```python
model = aai.model(id=model_id)
```

Prior transcripts can also be called by ID.

```python
transcript = aai.transcript(id=transcript_id)
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
