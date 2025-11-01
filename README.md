# Hathora Python SDK

The official Python SDK for the Hathora AI API. Easily integrate speech-to-text (STT), text-to-speech (TTS), and large language models (LLM) into your Python applications.

## Features

- **Simple, intuitive API** - Clean, Pythonic interface
- **Multiple AI models**:
  - **TTS**: Kokoro-82M and ResembleAI Chatterbox
  - **STT**: Parakeet multilingual transcription
  - **LLM**: Qwen3-30B for chat completions
- **Model-specific parameters** - Each model has its own unique parameters with validation
- **Voice cloning** with ResembleAI's audio prompt feature
- **Flexible audio handling** - Works with file paths, file objects, or raw bytes
- **Chat completions** with message history and temperature control
- **Type hints** for better IDE support
- **Comprehensive error handling**

## Available Models

### Speech-to-Text (STT)

| Model | Parameters | Description |
|-------|-----------|-------------|
| **Parakeet** | `file` | Audio file to transcribe (required, positional) |
| | `start_time` | Start time in seconds for transcription window (optional) |
| | `end_time` | End time in seconds for transcription window (optional) |

**Example:**
```python
# Basic usage
client.speech_to_text.convert("parakeet", "audio.wav")

# With time window
client.speech_to_text.convert("parakeet", "audio.wav", start_time=3.0, end_time=9.0)
```

### Text-to-Speech (TTS)

| Model | Parameters | Description |
|-------|-----------|-------------|
| **Kokoro** | `voice` | Voice ID (default: "af_bella") |
| | `speed` | Speech speed multiplier: 0.5-2.0 (default: 1.0) |
| **ResembleAI** | `audio_prompt` | Reference audio file for voice cloning (optional) |
| | `exaggeration` | Emotional intensity: 0.0-1.0 (default: 0.5) |
| | `cfg_weight` | Adherence to reference voice: 0.0-1.0 (default: 0.5) |

## Installation

Install from PyPI:

```bash
pip install hathora
```

Or install from source:

```bash
git clone https://github.com/hathora/yapp-sdk.git
cd yapp-sdk
pip install -e .
```

## Quick Start

```python
import hathora

# Initialize the client
client = hathora.Hathora(api_key="your-api-key")

# Transcribe audio to text
transcription = client.speech_to_text.convert("parakeet", "audio.wav")
print(transcription.text)

# Generate speech from text
response = client.text_to_speech.convert("kokoro", "Hello world!")
response.save("output.wav")
```

## Authentication

You can provide your API key in two ways:

### 1. Pass it directly to the client:
```python
client = hathora.Hathora(api_key="your-api-key")
```

### 2. Set it as an environment variable:
```bash
export HATHORA_API_KEY="your-api-key"
```

```python
client = hathora.Hathora()  # Will use HATHORA_API_KEY from environment
```

## Usage Examples

### Speech-to-Text (Transcription)

#### Basic Transcription

The SDK uses the **Parakeet** multilingual STT model for transcription.

```python
import hathora

client = hathora.Hathora(api_key="your-api-key")

# Transcribe an entire audio file using Parakeet
response = client.speech_to_text.convert("parakeet", "audio.wav")
print(response.text)
```

#### Transcription with Time Window

```python
# Transcribe only a specific time range
response = client.speech_to_text.convert(
    "parakeet",   # Model (positional)
    "audio.wav",  # File (positional)
    start_time=3.0,  # Start at 3 seconds
    end_time=9.0     # End at 9 seconds
)
print(response.text)
```

#### Multiple Audio Formats

The SDK automatically handles various audio formats:

```python
# From file path (string)
response = client.speech_to_text.convert("parakeet", "audio.wav")

# From pathlib.Path
from pathlib import Path
response = client.speech_to_text.convert("parakeet", Path("audio.mp3"))

# From file object
with open("audio.wav", "rb") as f:
    response = client.speech_to_text.convert("parakeet", f)

# From bytes
audio_bytes = open("audio.wav", "rb").read()
response = client.speech_to_text.convert("parakeet", audio_bytes)
```

### Text-to-Speech (Synthesis)

#### Using Kokoro-82M Model

Kokoro parameters: `voice`, `speed`

```python
import hathora

client = hathora.Hathora(api_key="your-api-key")

# Simple synthesis (uses defaults)
response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "Hello world!"
)
response.save("output.wav")

# With custom voice and speed
response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "The quick brown fox jumps over the lazy dog.",
    voice="af_bella",  # Kokoro parameter
    speed=1.2          # Kokoro parameter - 20% faster
)
response.save("output_fast.wav")

# Or use the kokoro() method directly
response = client.text_to_speech.kokoro(
    text="Direct method call",
    voice="af_bella",
    speed=0.8  # 20% slower
)
response.save("output_slow.wav")
```

#### Using ResembleAI Model (with Voice Cloning)

ResembleAI parameters: `audio_prompt`, `exaggeration`, `cfg_weight`

```python
# Simple generation
response = client.text_to_speech.convert(
    "resemble",  # Model first
    "Hello world!",
    exaggeration=0.5,  # Emotional intensity (0.0 - 1.0)
    cfg_weight=0.5     # Adherence to reference voice (0.0 - 1.0)
)
response.save("output.wav")

# Voice cloning with audio prompt
response = client.text_to_speech.convert(
    "resemble",  # Model first
    "This should sound like the reference voice.",
    audio_prompt="reference_voice.wav",  # Reference audio for cloning
    cfg_weight=0.9                       # High adherence to reference
)
response.save("cloned_voice.wav")

# Highly expressive speech
response = client.text_to_speech.convert(
    "resemble",  # Model first
    "Wow! This is amazing!",
    exaggeration=0.9,  # High emotional intensity
    cfg_weight=0.5
)
response.save("expressive.wav")

# Or use the resemble() method directly
response = client.text_to_speech.resemble(
    text="Direct method call",
    audio_prompt="reference.wav",
    exaggeration=0.7,
    cfg_weight=0.8
)
response.save("output.wav")
```

#### Discovering Model Parameters

The SDK provides methods to discover what parameters are available for each TTS model:

```python
# Parakeet (STT) parameters
# Model: parakeet
# Parameters:
#   - file (required): Audio file to transcribe
#   - start_time (optional): Start time in seconds
#   - end_time (optional): End time in seconds
client.speech_to_text.convert("parakeet", "audio.wav", start_time=0, end_time=10)

# List all available TTS models
models = client.text_to_speech.list_models()
print(models)  # ['kokoro', 'resemble']

# Print help for a specific TTS model
client.text_to_speech.print_model_help("kokoro")
# Output:
# Model: kokoro
# Parameters:
#   - voice (str, default='af_bella'): Voice to use for synthesis
#   - speed (float, default=1.0): Speech speed multiplier (0.5 = half speed, 2.0 = double speed)

client.text_to_speech.print_model_help("resemble")
# Output:
# Model: resemble
# Parameters:
#   - audio_prompt (AudioFile, default=None): Reference audio file for voice cloning (optional)
#   - exaggeration (float, default=0.5): Emotional intensity, range 0.0-1.0
#   - cfg_weight (float, default=0.5): Adherence to reference voice, range 0.0-1.0

# Get parameter specifications programmatically
params = client.text_to_speech.get_model_parameters("kokoro")
for param_name, param_info in params.items():
    print(f"{param_name}: {param_info['description']}")
```

#### Parameter Validation

The SDK validates that you're using the correct parameters for each model:

```python
# This works - correct Kokoro parameters
response = client.text_to_speech.convert(
    "kokoro", "Hello", voice="af_bella", speed=1.2
)

# This raises ValidationError with helpful message
try:
    response = client.text_to_speech.convert(
        "resemble", "Hello", speed=1.2  # ERROR!
    )
except ValidationError as e:
    print(e)
    # Output: Unknown parameters for ResembleAI model: speed.
    #         Valid parameters: audio_prompt, exaggeration, cfg_weight
    #         Use client.text_to_speech.print_model_help('resemble') for more details.

# This also raises ValidationError
response = client.text_to_speech.convert(
    "kokoro", "Hello", exaggeration=0.5  # ERROR!
)
```

### Working with Audio Responses

```python
# Save to file
response = client.text_to_speech.convert("kokoro", "Hello world!")
response.save("output.wav")

# Or use stream_to_file (alias for save)
response.stream_to_file("output.wav")

# Get raw bytes
audio_bytes = response.content
print(f"Generated {len(audio_bytes)} bytes")

# Check content type
print(response.content_type)  # e.g., "audio/wav"
```

### Large Language Models (LLM)

The SDK supports chat completions with Qwen and other LLMs.

#### Setting up LLM Endpoint

```python
import hathora

client = hathora.Hathora(api_key="your-api-key")

# Configure your LLM endpoint
client.llm.set_endpoint("https://your-app.app.hathora.dev")
```

#### Simple Chat

```python
# Simple question
response = client.llm.chat("qwen", "What is Python?")
print(response.content)
```

#### Chat with Message History

```python
# Conversation with context
messages = [
    {"role": "user", "content": "Hello! Can you help me with programming?"},
    {"role": "assistant", "content": "Of course! I'd be happy to help."},
    {"role": "user", "content": "What's the difference between a list and tuple?"}
]

response = client.llm.chat(
    "qwen",
    messages,
    max_tokens=500,
    temperature=0.7
)
print(response.content)
```

#### Controlling Output

```python
# Creative output (higher temperature)
response = client.llm.chat(
    "qwen",
    "Write a poem about AI",
    temperature=0.9,
    max_tokens=200
)

# Precise output (lower temperature)
response = client.llm.chat(
    "qwen",
    "Calculate 15 * 23",
    temperature=0.1,
    max_tokens=50
)
```

#### Using ChatMessage Objects

```python
from hathora.resources.llm import ChatMessage

conversation = [
    ChatMessage("system", "You are a helpful coding assistant."),
    ChatMessage("user", "How do I read a file in Python?")
]

response = client.llm.chat("qwen", conversation)
print(response.content)
```

#### Response Properties

```python
response = client.llm.chat("qwen", "Explain machine learning")

# Get the response text
print(response.content)

# Get the full message object
print(response.message)

# Get token usage info
print(response.usage)

# Get the model used
print(response.model)

# Get raw response data
print(response.raw)
```

#### Available Models

```python
# List all LLM models
models = client.llm.list_models()
print(models)  # ['qwen']

# Get model info
info = client.llm.get_model_info("qwen")
print(info)

# Print model help
client.llm.print_model_help("qwen")
```

## API Reference

### `hathora.Hathora`

Main client class for the Hathora API.

**Parameters:**
- `api_key` (str, optional): Your Hathora API key
- `timeout` (int, default=30): Request timeout in seconds

**Properties:**
- `speech_to_text`: Speech-to-text (STT) resource for audio transcription
- `text_to_speech`: Text-to-speech (TTS) resource for audio synthesis

---

### `client.speech_to_text.convert()`

Transcribe audio to text using the Parakeet STT model.

**Parameters:**
- `model` (str): STT model to use (currently: "parakeet") - **positional, required**
- `file` (str | Path | BinaryIO | bytes): Audio file to transcribe - **positional, required**
- `start_time` (float, optional): Start time in seconds for transcription window
- `end_time` (float, optional): End time in seconds for transcription window
- `**kwargs`: Additional model-specific parameters (reserved for future use)

**Example:**
```python
# Both model and file are positional
response = client.speech_to_text.convert("parakeet", "audio.wav")
```

**Available Models:**
- `"parakeet"` - nvidia/parakeet-tdt-0.6b-v3 - Multilingual ASR with word-level timestamps

**Returns:** `TranscriptionResponse`
- `.text`: The transcribed text
- `.metadata`: Additional metadata from the API (may include word-level timestamps)

**Supported audio formats:** WAV, MP3, MP4, M4A, OGG, FLAC, PCM

---

### `client.text_to_speech.convert()`

Generate speech from text. This is a unified interface that routes to the appropriate model.

**Parameters:**
- `model` (str): Model to use ("kokoro" or "resemble") - **required, first parameter**
- `text` (str): Text to convert to speech
- `**kwargs`: Model-specific parameters (see below)

**Model-Specific Parameters:**

**For Kokoro model:**
- `voice` (str, default="af_bella"): Voice to use for synthesis
- `speed` (float, default=1.0): Speech speed multiplier (0.5 = half speed, 2.0 = double speed)

**For ResembleAI model:**
- `audio_prompt` (str | Path | BinaryIO | bytes, optional): Reference audio for voice cloning
- `exaggeration` (float, default=0.5): Emotional intensity, range 0.0-1.0
- `cfg_weight` (float, default=0.5): Adherence to reference voice, range 0.0-1.0

**Returns:** `AudioResponse`

**Examples:**
```python
# Kokoro - model comes first!
response = client.text_to_speech.convert(
    "kokoro", "Hello", voice="af_bella", speed=1.2
)

# ResembleAI - model comes first!
response = client.text_to_speech.convert(
    "resemble", "Hello", exaggeration=0.7, cfg_weight=0.6
)
```

**See also:** Use `print_model_help()` to discover parameters

---

### `client.text_to_speech.list_models()`

List all available TTS models.

**Returns:** `list` - List of model names

**Example:**
```python
models = client.text_to_speech.list_models()
print(models)  # ['kokoro', 'resemble']
```

---

### `client.text_to_speech.get_model_parameters()`

Get parameter specifications for a specific model.

**Parameters:**
- `model` (str): Model name

**Returns:** `dict` - Parameter specifications with types, defaults, and descriptions

**Example:**
```python
params = client.text_to_speech.get_model_parameters("kokoro")
for name, info in params.items():
    print(f"{name}: {info['description']}")
```

---

### `client.text_to_speech.print_model_help()`

Print helpful information about a model's parameters to console.

**Parameters:**
- `model` (str): Model name

**Example:**
```python
client.text_to_speech.print_model_help("kokoro")
# Prints:
# Model: kokoro
# Parameters:
#   - voice (str, default='af_bella'): Voice to use for synthesis
#   - speed (float, default=1.0): Speech speed multiplier...
```

---

### `client.text_to_speech.kokoro()`

Generate speech using the Kokoro-82M model.

**Parameters:**
- `text` (str): Text to convert to speech
- `voice` (str, default="af_bella"): Voice to use
- `speed` (float, default=1.0): Speech speed multiplier

**Returns:** `AudioResponse`

---

### `client.text_to_speech.resemble()`

Generate speech using ResembleAI Chatterbox with voice cloning.

**Parameters:**
- `text` (str): Text to convert to speech
- `audio_prompt` (str | Path | BinaryIO | bytes, optional): Reference audio for voice cloning
- `exaggeration` (float, default=0.5): Emotional intensity (0.0 - 1.0)
- `cfg_weight` (float, default=0.5): Adherence to reference voice (0.0 - 1.0)

**Returns:** `AudioResponse`

---

### `AudioResponse`

Response object containing generated audio.

**Properties:**
- `content`: Raw audio bytes
- `content_type`: MIME type of the audio

**Methods:**
- `save(file_path)`: Save audio to file
- `stream_to_file(file_path)`: Alias for `save()`

---

### `TranscriptionResponse`

Response object containing transcribed text.

**Properties:**
- `text`: The transcribed text
- `metadata`: Additional metadata

## Complete Workflow Example

```python
import hathora

# Initialize client
client = hathora.Hathora(api_key="your-api-key")

# 1. Transcribe audio
transcription = client.speech_to_text.convert(
    "parakeet",      # Model (positional)
    "original.wav",  # File (positional)
    start_time=0,
    end_time=10
)
print(f"Original: {transcription.text}")

# 2. Modify the text
modified_text = transcription.text.upper()

# 3. Generate new speech with Kokoro
response = client.text_to_speech.convert(
    "kokoro", modified_text, voice="af_bella", speed=1.0
)
response.save("output_kokoro.wav")

# 4. Clone voice from original audio
cloned = client.text_to_speech.convert(
    "resemble", "New text in the original voice",
    audio_prompt="original.wav", cfg_weight=0.9
)
cloned.save("cloned_voice.wav")
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from yapp import HathoraError, APIError, AuthenticationError, ValidationError

try:
    response = client.text_to_speech.convert("kokoro", "Hello world!")
    response.save("output.wav")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except APIError as e:
    print(f"API error (status {e.status_code}): {e.message}")
except HathoraError as e:
    print(f"Hathora SDK error: {e}")
```

## Supported Audio Formats

### Input (Transcription)
- WAV (.wav)
- MP3 (.mp3)
- MP4 Audio (.mp4, .m4a)
- OGG (.ogg)
- FLAC (.flac)
- PCM (.pcm)

### Output (Synthesis)
- WAV (default output format)

## Development

### Running Examples

```bash
cd examples
python discover_parameters.py   # Learn about model parameters
python transcribe_audio.py      # Speech-to-text examples
python synthesize_speech.py     # Text-to-speech examples
python voice_cloning.py         # Voice cloning with ResembleAI
python model_parameters.py      # Model-specific parameter examples
python full_workflow.py         # Complete workflow
```

### Installing for Development

```bash
git clone https://github.com/hathora/yapp-sdk.git
cd yapp-sdk
pip install -e .
```

## Roadmap

- [ ] Add streaming support for real-time TTS
- [ ] Support for additional TTS models
- [ ] Async client support
- [ ] Audio format conversion utilities
- [ ] Batch processing capabilities
- [ ] WebSocket support for real-time conversations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/hathora/yapp-sdk/issues
- Documentation: https://docs.hathora.com
- Email: support@hathora.com
