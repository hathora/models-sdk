"""
Example: Transcribe audio to text using Yapp SDK

This example demonstrates how to use the Yapp SDK to transcribe
audio files to text.
"""

import yapp

# Initialize the client
client = yapp.Yapp(api_key="your-api-key-here")

# Example 1: Simple transcription
print("Example 1: Simple transcription with Parakeet")
response = client.audio.transcriptions.create(
    "parakeet",   # Model (positional)
    "audio.wav"   # File (positional)
)
print(f"Transcription: {response.text}")
print()

# Example 2: Transcribe with time window
print("Example 2: Transcription with time window")
response = client.audio.transcriptions.create(
    "parakeet",   # Model (positional)
    "audio.wav",  # File (positional)
    start_time=3.0,  # Start at 3 seconds
    end_time=9.0     # End at 9 seconds
)
print(f"Transcription (3s-9s): {response.text}")
print()

# Example 3: Transcribe from file object
print("Example 3: Transcription from file object")
with open("audio.wav", "rb") as audio_file:
    response = client.audio.transcriptions.create(
        "parakeet",   # Model (positional)
        audio_file    # File (positional)
    )
    print(f"Transcription: {response.text}")
print()

# Example 4: Transcribe with metadata
print("Example 4: Transcription with metadata")
response = client.audio.transcriptions.create(
    "parakeet",   # Model (positional)
    "audio.wav",  # File (positional)
    start_time=0,
    end_time=30
)
print(f"Transcription: {response.text}")
if response.metadata:
    print(f"Metadata: {response.metadata}")
