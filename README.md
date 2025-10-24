# Yapp Python SDK

The official Python SDK for the Yapp Voice AI API. Easily integrate speech-to-text (STT) and text-to-speech (TTS) capabilities into your Python applications.

## Features

- **Simple, intuitive API** - Clean, Pythonic interface
- **Multiple TTS models** - Kokoro-82M and ResembleAI Chatterbox
- **Model-specific parameters** - Each model has its own unique parameters with validation
- **Voice cloning** with ResembleAI's audio prompt feature
- **Flexible audio handling** - Works with file paths, file objects, or raw bytes
- **Type hints** for better IDE support
- **Comprehensive error handling**

## Available Models

### Speech-to-Text (STT)
- **Parakeet** - Multilingual automatic speech recognition with word-level timestamps

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
pip install yapp
```

Or install from source:

```bash
git clone https://github.com/yourusername/yapp-sdk.git
cd yapp-sdk
pip install -e .
```

## Quick Start

```python
import yapp

# Initialize the client
client = yapp.Yapp(api_key="your-api-key")

# Transcribe audio to text
transcription = client.audio.transcriptions.create("parakeet", "audio.wav")
print(transcription.text)

# Generate speech from text
response = client.audio.speech.create("kokoro", "Hello world!")
response.save("output.wav")
```

## Authentication

You can provide your API key in two ways:

### 1. Pass it directly to the client:
```python
client = yapp.Yapp(api_key="your-api-key")
```

### 2. Set it as an environment variable:
```bash
export YAPP_API_KEY="your-api-key"
```

```python
client = yapp.Yapp()  # Will use YAPP_API_KEY from environment
```

## Usage Examples

### Speech-to-Text (Transcription)

#### Basic Transcription

The SDK uses the **Parakeet** multilingual STT model for transcription.

```python
import yapp

client = yapp.Yapp(api_key="your-api-key")

# Transcribe an entire audio file using Parakeet
response = client.audio.transcriptions.create("parakeet", "audio.wav")
print(response.text)
```

#### Transcription with Time Window

```python
# Transcribe only a specific time range
response = client.audio.transcriptions.create(
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
response = client.audio.transcriptions.create("parakeet", "audio.wav")

# From pathlib.Path
from pathlib import Path
response = client.audio.transcriptions.create("parakeet", Path("audio.mp3"))

# From file object
with open("audio.wav", "rb") as f:
    response = client.audio.transcriptions.create("parakeet", f)

# From bytes
audio_bytes = open("audio.wav", "rb").read()
response = client.audio.transcriptions.create("parakeet", audio_bytes)
```

### Text-to-Speech (Synthesis)

#### Using Kokoro-82M Model

Kokoro parameters: `voice`, `speed`

```python
import yapp

client = yapp.Yapp(api_key="your-api-key")

# Simple synthesis (uses defaults)
response = client.audio.speech.create(
    "kokoro",  # Model first
    "Hello world!"
)
response.save("output.wav")

# With custom voice and speed
response = client.audio.speech.create(
    "kokoro",  # Model first
    "The quick brown fox jumps over the lazy dog.",
    voice="af_bella",  # Kokoro parameter
    speed=1.2          # Kokoro parameter - 20% faster
)
response.save("output_fast.wav")

# Or use the kokoro() method directly
response = client.audio.speech.kokoro(
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
response = client.audio.speech.create(
    "resemble",  # Model first
    "Hello world!",
    exaggeration=0.5,  # Emotional intensity (0.0 - 1.0)
    cfg_weight=0.5     # Adherence to reference voice (0.0 - 1.0)
)
response.save("output.wav")

# Voice cloning with audio prompt
response = client.audio.speech.create(
    "resemble",  # Model first
    "This should sound like the reference voice.",
    audio_prompt="reference_voice.wav",  # Reference audio for cloning
    cfg_weight=0.9                       # High adherence to reference
)
response.save("cloned_voice.wav")

# Highly expressive speech
response = client.audio.speech.create(
    "resemble",  # Model first
    "Wow! This is amazing!",
    exaggeration=0.9,  # High emotional intensity
    cfg_weight=0.5
)
response.save("expressive.wav")

# Or use the resemble() method directly
response = client.audio.speech.resemble(
    text="Direct method call",
    audio_prompt="reference.wav",
    exaggeration=0.7,
    cfg_weight=0.8
)
response.save("output.wav")
```

#### Discovering Model Parameters

The SDK provides methods to discover what parameters are available for each model:

```python
# List all available models
models = client.audio.speech.list_models()
print(models)  # ['kokoro', 'resemble']

# Print help for a specific model
client.audio.speech.print_model_help("kokoro")
# Output:
# Model: kokoro
# Parameters:
#   - voice (str, default='af_bella'): Voice to use for synthesis
#   - speed (float, default=1.0): Speech speed multiplier (0.5 = half speed, 2.0 = double speed)

client.audio.speech.print_model_help("resemble")
# Output:
# Model: resemble
# Parameters:
#   - audio_prompt (AudioFile, default=None): Reference audio file for voice cloning (optional)
#   - exaggeration (float, default=0.5): Emotional intensity, range 0.0-1.0
#   - cfg_weight (float, default=0.5): Adherence to reference voice, range 0.0-1.0

# Get parameter specifications programmatically
params = client.audio.speech.get_model_parameters("kokoro")
for param_name, param_info in params.items():
    print(f"{param_name}: {param_info['description']}")
```

#### Parameter Validation

The SDK validates that you're using the correct parameters for each model:

```python
# This works - correct Kokoro parameters
response = client.audio.speech.create(
    "kokoro", "Hello", voice="af_bella", speed=1.2
)

# This raises ValidationError with helpful message
try:
    response = client.audio.speech.create(
        "resemble", "Hello", speed=1.2  # ERROR!
    )
except ValidationError as e:
    print(e)
    # Output: Unknown parameters for ResembleAI model: speed.
    #         Valid parameters: audio_prompt, exaggeration, cfg_weight
    #         Use client.audio.speech.print_model_help('resemble') for more details.

# This also raises ValidationError
response = client.audio.speech.create(
    "kokoro", "Hello", exaggeration=0.5  # ERROR!
)
```

### Working with Audio Responses

```python
# Save to file
response = client.audio.speech.create("kokoro", "Hello world!")
response.save("output.wav")

# Or use stream_to_file (alias for save)
response.stream_to_file("output.wav")

# Get raw bytes
audio_bytes = response.content
print(f"Generated {len(audio_bytes)} bytes")

# Check content type
print(response.content_type)  # e.g., "audio/wav"
```

## API Reference

### `yapp.Yapp`

Main client class for the Yapp API.

**Parameters:**
- `api_key` (str, optional): Your Yapp API key
- `timeout` (int, default=30): Request timeout in seconds

**Properties:**
- `audio`: Audio namespace containing transcription and speech resources

---

### `client.audio.transcriptions.create()`

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
response = client.audio.transcriptions.create("parakeet", "audio.wav")
```

**Available Models:**
- `"parakeet"` - nvidia/parakeet-tdt-0.6b-v3 - Multilingual ASR with word-level timestamps

**Returns:** `TranscriptionResponse`
- `.text`: The transcribed text
- `.metadata`: Additional metadata from the API (may include word-level timestamps)

**Supported audio formats:** WAV, MP3, MP4, M4A, OGG, FLAC, PCM

---

### `client.audio.speech.create()`

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
response = client.audio.speech.create(
    "kokoro", "Hello", voice="af_bella", speed=1.2
)

# ResembleAI - model comes first!
response = client.audio.speech.create(
    "resemble", "Hello", exaggeration=0.7, cfg_weight=0.6
)
```

**See also:** Use `print_model_help()` to discover parameters

---

### `client.audio.speech.list_models()`

List all available TTS models.

**Returns:** `list` - List of model names

**Example:**
```python
models = client.audio.speech.list_models()
print(models)  # ['kokoro', 'resemble']
```

---

### `client.audio.speech.get_model_parameters()`

Get parameter specifications for a specific model.

**Parameters:**
- `model` (str): Model name

**Returns:** `dict` - Parameter specifications with types, defaults, and descriptions

**Example:**
```python
params = client.audio.speech.get_model_parameters("kokoro")
for name, info in params.items():
    print(f"{name}: {info['description']}")
```

---

### `client.audio.speech.print_model_help()`

Print helpful information about a model's parameters to console.

**Parameters:**
- `model` (str): Model name

**Example:**
```python
client.audio.speech.print_model_help("kokoro")
# Prints:
# Model: kokoro
# Parameters:
#   - voice (str, default='af_bella'): Voice to use for synthesis
#   - speed (float, default=1.0): Speech speed multiplier...
```

---

### `client.audio.speech.kokoro()`

Generate speech using the Kokoro-82M model.

**Parameters:**
- `text` (str): Text to convert to speech
- `voice` (str, default="af_bella"): Voice to use
- `speed` (float, default=1.0): Speech speed multiplier

**Returns:** `AudioResponse`

---

### `client.audio.speech.resemble()`

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
import yapp

# Initialize client
client = yapp.Yapp(api_key="your-api-key")

# 1. Transcribe audio
transcription = client.audio.transcriptions.create(
    "parakeet",      # Model (positional)
    "original.wav",  # File (positional)
    start_time=0,
    end_time=10
)
print(f"Original: {transcription.text}")

# 2. Modify the text
modified_text = transcription.text.upper()

# 3. Generate new speech with Kokoro
response = client.audio.speech.create(
    "kokoro", modified_text, voice="af_bella", speed=1.0
)
response.save("output_kokoro.wav")

# 4. Clone voice from original audio
cloned = client.audio.speech.create(
    "resemble", "New text in the original voice",
    audio_prompt="original.wav", cfg_weight=0.9
)
cloned.save("cloned_voice.wav")
```

## Error Handling

The SDK provides specific exception types for different error scenarios:

```python
from yapp import YappError, APIError, AuthenticationError, ValidationError

try:
    response = client.audio.speech.create(text="Hello world!")
    response.save("output.wav")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except APIError as e:
    print(f"API error (status {e.status_code}): {e.message}")
except YappError as e:
    print(f"Yapp SDK error: {e}")
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
git clone https://github.com/yourusername/yapp-sdk.git
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
- GitHub Issues: https://github.com/yourusername/yapp-sdk/issues
- Documentation: https://docs.yapp.ai
- Email: support@yapp.ai
