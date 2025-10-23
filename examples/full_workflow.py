"""
Example: Complete workflow using Yapp SDK

This example demonstrates a complete workflow:
1. Transcribe an audio file
2. Modify the transcription
3. Generate new speech from the modified text
"""

import yapp

# Initialize the client
client = yapp.Yapp(api_key="your-api-key-here")

print("=== Complete Yapp SDK Workflow ===\n")

# Step 1: Transcribe audio
print("Step 1: Transcribing audio...")
transcription = client.audio.transcriptions.create(
    "parakeet",  # Model first
    file="original_audio.wav",
    start_time=0,
    end_time=10  # First 10 seconds
)
print(f"Original transcription: {transcription.text}\n")

# Step 2: Modify the transcription
modified_text = transcription.text.upper()  # Convert to uppercase as example
print(f"Modified text: {modified_text}\n")

# Step 3: Generate speech with Kokoro
print("Step 3a: Generating speech with Kokoro...")
kokoro_response = client.audio.speech.create(
    "kokoro",  # Model first
    modified_text,
    voice="af_bella",
    speed=1.0
)
kokoro_response.save("output_kokoro.wav")
print("Saved Kokoro output to output_kokoro.wav\n")

# Step 4: Generate speech with ResembleAI for comparison
print("Step 3b: Generating speech with ResembleAI...")
resemble_response = client.audio.speech.create(
    "resemble",  # Model first
    modified_text,
    exaggeration=0.6,
    cfg_weight=0.5
)
resemble_response.save("output_resemble.wav")
print("Saved ResembleAI output to output_resemble.wav\n")

# Step 5: Voice cloning - transcribe + clone
print("Step 4: Voice cloning workflow...")
# Use the original audio as a voice reference
cloned_response = client.audio.speech.resemble(
    text="This is a new sentence in the cloned voice.",
    audio_prompt="original_audio.wav",
    cfg_weight=0.9  # High adherence to original voice
)
cloned_response.save("cloned_voice.wav")
print("Saved cloned voice to cloned_voice.wav\n")

print("=== Workflow Complete ===")
print("\nGenerated files:")
print("  - output_kokoro.wav")
print("  - output_resemble.wav")
print("  - cloned_voice.wav")
