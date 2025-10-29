"""
Example: Voice cloning with ResembleAI using Yapp SDK

This example demonstrates how to use the Yapp SDK to generate
speech with voice cloning capabilities using the ResembleAI model.
"""

import hathora

# Initialize the client
client = hathora.Yapp(api_key="your-api-key-here")

# Example 1: Simple generation with ResembleAI
print("Example 1: Simple ResembleAI generation")
response = client.text_to_speech.resemble(
    text="Hello world! This is ResembleAI speaking.",
    exaggeration=0.5,
    cfg_weight=0.5
)
response.save("resemble_simple.wav")
print("Saved to resemble_simple.wav")
print()

# Example 2: Voice cloning with audio prompt
print("Example 2: Voice cloning with reference audio")
response = client.text_to_speech.resemble(
    text="This should sound like the reference voice.",
    audio_prompt="reference_voice.wav",  # Your reference audio file
    exaggeration=0.3,  # Lower for more natural speech
    cfg_weight=0.8     # Higher to match reference voice more closely
)
response.save("cloned_voice.wav")
print("Saved to cloned_voice.wav")
print()

# Example 3: Highly expressive speech
print("Example 3: Highly expressive speech")
response = client.text_to_speech.resemble(
    text="Wow! This is amazing! I can't believe how good this sounds!",
    exaggeration=0.9,  # High exaggeration for emotional intensity
    cfg_weight=0.5
)
response.save("expressive.wav")
print("Saved to expressive.wav")
print()

# Example 4: Using via the general create method
print("Example 4: Using ResembleAI via create method")
response = client.text_to_speech.convert(
    "resemble",  # Model first
    "This uses the create method with model parameter.",
    exaggeration=0.6,
    cfg_weight=0.5
)
response.save("resemble_create.wav")
print("Saved to resemble_create.wav")
print()

# Example 5: Voice cloning with file object
print("Example 5: Voice cloning with file object")
with open("reference_voice.wav", "rb") as ref_audio:
    response = client.text_to_speech.resemble(
        text="Cloning voice from a file object.",
        audio_prompt=ref_audio,
        cfg_weight=0.9  # Very high adherence to reference
    )
    response.save("cloned_from_object.wav")
print("Saved to cloned_from_object.wav")
