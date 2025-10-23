# Yapp SDK Model Endpoints

This document describes the models used by the Yapp SDK and their API endpoints.

## Speech-to-Text (STT)

### Parakeet
**Model:** nvidia/parakeet-tdt-0.6b-v3
**Description:** Multilingual automatic speech recognition model with word-level timestamps
**Endpoint:** `https://app-1c7bebb9-6977-4101-9619-833b251b86d1.app.hathora.dev`
**API Path:** `/v1/transcribe`
**Method:** POST
**Content-Type:** multipart/form-data

**Parameters:**
- `file` (required): Audio file to transcribe
- `start_time` (optional): Start time in seconds
- `end_time` (optional): End time in seconds

**Supported Formats:** WAV, MP3, MP4, M4A, OGG, FLAC, PCM

**SDK Usage:**
```python
response = client.audio.transcriptions.create(
    file="audio.wav",
    start_time=3.0,
    end_time=9.0
)
```

---

## Text-to-Speech (TTS)

### Kokoro-82M
**Model:** hexgrad/Kokoro-82M
**Description:** Open-weight TTS model with 82 million parameters, optimized for natural and expressive voice synthesis
**Endpoint:** `https://app-01312daf-6e53-4b9d-a4ad-13039f35adc4.app.hathora.dev`
**API Path:** `/synthesize`
**Method:** POST
**Content-Type:** application/json

**Parameters:**
- `text` (required): Text to convert to speech
- `voice` (optional, default="af_bella"): Voice ID
- `speed` (optional, default=1.0): Speech speed multiplier (0.5 = half speed, 2.0 = double speed)

**SDK Usage:**
```python
response = client.audio.speech.create(
    "kokoro",
    "Hello world",
    voice="af_bella",
    speed=1.2
)
```

---

### ResembleAI Chatterbox
**Model:** ResembleAI/chatterbox
**Description:** Public TTS model optimized for natural and expressive voice synthesis with voice cloning capabilities
**Endpoint:** `https://app-efbc8fe2-df55-4f96-bbe3-74f6ea9d986b.app.hathora.dev`
**API Path:** `/v1/generate`
**Method:** POST
**Content-Type:** multipart/form-data

**Parameters:**
- `text` (required): Text to convert to speech
- `audio_prompt` (optional): Reference audio file for voice cloning
- `exaggeration` (optional, default=0.5): Emotional intensity (0.0-1.0)
- `cfg_weight` (optional, default=0.5): Adherence to reference voice (0.0-1.0)

**SDK Usage:**
```python
# Simple generation
response = client.audio.speech.create(
    "resemble",
    "Hello world",
    exaggeration=0.7
)

# Voice cloning
response = client.audio.speech.create(
    "resemble",
    "Hello world",
    audio_prompt="reference.wav",
    cfg_weight=0.9
)
```

---

## URL Configuration

Currently, the URLs are hardcoded in the SDK:

**Location in code:**
- Parakeet: `yapp/resources/transcription.py` line 16
- Kokoro: `yapp/resources/synthesis.py` line 50
- ResembleAI: `yapp/resources/synthesis.py` line 51

**To update URLs:**
1. Edit the respective files
2. Update the URL strings
3. Rebuild the package: `python3 -m build`
4. Publish new version to PyPI

**Future Enhancement:**
Consider making URLs configurable via:
- Environment variables
- Client initialization parameters
- Configuration file

## Authentication

All endpoints currently use Bearer token authentication:
```
Authorization: Bearer <api_key>
```

The SDK automatically adds this header when `api_key` is provided to the client.

## Model Information

| Model | Type | Parameters | License | Link |
|-------|------|-----------|---------|------|
| Parakeet | STT | 0.6B | Apache 2.0 | [nvidia/parakeet-tdt-0.6b-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) |
| Kokoro | TTS | 82M | Apache 2.0 | [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) |
| ResembleAI Chatterbox | TTS | - | Public | [ResembleAI/chatterbox](https://huggingface.co/ResembleAI/chatterbox) |
