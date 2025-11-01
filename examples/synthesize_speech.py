"""
Example: Synthesize speech from text using Yapp SDK

This example demonstrates how to use the Yapp SDK to generate
speech from text using different TTS models.
"""

import hathora

# Initialize the client
client = hathora.Yapp(api_key="your-api-key-here")

# Example 1: Simple speech synthesis with Kokoro (default)
print("Example 1: Simple speech synthesis (Kokoro)")
response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "Hello world! This is a test of the Yapp text-to-speech API."
)
response.save("output_kokoro.wav")
print("Saved to output_kokoro.wav")
print()

# Example 2: Speech synthesis with Kokoro-specific parameters
print("Example 2: Custom voice and speed with Kokoro")
response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "The quick brown fox jumps over the lazy dog.",
    voice="af_bella",  # Kokoro parameter
    speed=1.2          # Kokoro parameter - 20% faster
)
response.save("output_fast.wav")
print("Saved to output_fast.wav")
print()

# Example 3: Using Kokoro directly
print("Example 3: Using Kokoro model directly")
response = client.text_to_speech.kokoro(
    text="This is using the Kokoro model directly.",
    voice="af_bella",
    speed=0.8  # 20% slower
)
response.save("output_slow.wav")
print("Saved to output_slow.wav")
print()

# Example 4: Working with audio bytes directly
print("Example 4: Working with audio bytes")
response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "Getting the raw audio bytes."
)
audio_bytes = response.content
print(f"Generated {len(audio_bytes)} bytes of audio data")
# You can now process the audio bytes as needed
print()

# Example 5: Using ResembleAI model via create()
print("Example 5: Using ResembleAI via create()")
response = client.text_to_speech.convert(
    "resemble",  # Model first
    "This uses the ResembleAI model.",
    exaggeration=0.6,  # ResembleAI parameter
    cfg_weight=0.5     # ResembleAI parameter
)
response.save("output_resemble.wav")
print("Saved to output_resemble.wav")
print()

# Example 6: Using stream_to_file (alias for save)
print("Example 6: Using stream_to_file")
response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "This demonstrates the stream_to_file method."
)
response.stream_to_file("output_stream.wav")
print("Saved to output_stream.wav")
