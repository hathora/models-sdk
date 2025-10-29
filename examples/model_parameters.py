"""
Example: Understanding model-specific parameters

This example demonstrates the different parameters for each TTS model
and how to use them correctly.
"""

import hathora

# Initialize the client
client = hathora.Yapp(api_key="your-api-key-here")

print("=== Model-Specific Parameters Demo ===\n")

# ============================================================================
# KOKORO MODEL PARAMETERS
# ============================================================================
print("1. KOKORO MODEL")
print("-" * 50)
print("Parameters: voice, speed")
print()

# Kokoro with default parameters
print("  a) Default parameters:")
response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "Hello, this uses default Kokoro settings."
    # Defaults: voice="af_bella", speed=1.0
)
response.save("kokoro_default.wav")
print("     Saved to kokoro_default.wav")
print()

# Kokoro with custom voice
print("  b) Custom voice:")
response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "This uses a specific voice.",
    voice="af_bella"  # Specify voice
)
response.save("kokoro_custom_voice.wav")
print("     Saved to kokoro_custom_voice.wav")
print()

# Kokoro with custom speed
print("  c) Custom speed:")
response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "This is spoken at a faster speed.",
    speed=1.5  # 50% faster
)
response.save("kokoro_fast.wav")
print("     Saved to kokoro_fast.wav")
print()

response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "This is spoken at a slower speed.",
    speed=0.7  # 30% slower
)
response.save("kokoro_slow.wav")
print("     Saved to kokoro_slow.wav")
print()

# ============================================================================
# RESEMBLE AI MODEL PARAMETERS
# ============================================================================
print("2. RESEMBLE AI MODEL")
print("-" * 50)
print("Parameters: audio_prompt, exaggeration, cfg_weight")
print()

# ResembleAI with default parameters
print("  a) Default parameters:")
response = client.text_to_speech.convert(
    "resemble",  # Model first
    "Hello, this uses default ResembleAI settings."
    # Defaults: exaggeration=0.5, cfg_weight=0.5, no audio_prompt
)
response.save("resemble_default.wav")
print("     Saved to resemble_default.wav")
print()

# ResembleAI with custom exaggeration
print("  b) High exaggeration (emotional intensity):")
response = client.text_to_speech.convert(
    "resemble",  # Model first
    "Wow! This is so exciting!",
    exaggeration=0.9  # Very expressive (0.0 - 1.0)
)
response.save("resemble_expressive.wav")
print("     Saved to resemble_expressive.wav")
print()

print("  c) Low exaggeration (neutral tone):")
response = client.text_to_speech.convert(
    "resemble",  # Model first
    "This is a neutral statement.",
    exaggeration=0.2  # Less expressive
)
response.save("resemble_neutral.wav")
print("     Saved to resemble_neutral.wav")
print()

# ResembleAI with voice cloning
print("  d) Voice cloning with audio_prompt:")
response = client.text_to_speech.convert(
    "resemble",  # Model first
    "This should match the reference voice closely.",
    audio_prompt="reference_voice.wav",  # Your reference audio
    cfg_weight=0.9  # High adherence to reference (0.0 - 1.0)
)
response.save("resemble_cloned.wav")
print("     Saved to resemble_cloned.wav")
print()

# ============================================================================
# USING MODEL-SPECIFIC METHODS
# ============================================================================
print("3. USING MODEL-SPECIFIC METHODS")
print("-" * 50)
print("Instead of create(), you can call model methods directly:")
print()

# Direct Kokoro method call
print("  a) Direct kokoro() method:")
response = client.text_to_speech.kokoro(
    text="Using kokoro method directly.",
    voice="af_bella",
    speed=1.0
)
response.save("direct_kokoro.wav")
print("     Saved to direct_kokoro.wav")
print()

# Direct ResembleAI method call
print("  b) Direct resemble() method:")
response = client.text_to_speech.resemble(
    text="Using resemble method directly.",
    exaggeration=0.6,
    cfg_weight=0.5
)
response.save("direct_resemble.wav")
print("     Saved to direct_resemble.wav")
print()

# ============================================================================
# PARAMETER VALIDATION
# ============================================================================
print("4. PARAMETER VALIDATION")
print("-" * 50)
print("The SDK validates parameters for each model:")
print()

try:
    # This will raise ValidationError - speed is not valid for resemble
    response = client.text_to_speech.convert(
        "resemble",  # Model first
        "This will fail",
        speed=1.5  # ERROR: speed is Kokoro parameter!
    )
except hathora.ValidationError as e:
    print(f"  ✗ Error (as expected): {e}")
print()

try:
    # This will raise ValidationError - exaggeration is not valid for kokoro
    response = client.text_to_speech.convert(
        "kokoro",  # Model first
        "This will fail",
        exaggeration=0.5  # ERROR: exaggeration is ResembleAI parameter!
    )
except hathora.ValidationError as e:
    print(f"  ✗ Error (as expected): {e}")
print()

print("=== Demo Complete ===")
print("\nSummary:")
print("  Kokoro:     voice, speed")
print("  ResembleAI: audio_prompt, exaggeration, cfg_weight")
