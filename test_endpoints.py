"""
Test all Yapp SDK endpoints with live API
"""
import yapp
import os
from pathlib import Path

# Initialize client with API key
API_KEY = "hathora_org_st_MptP21iXyFRpMCqBPcEopttIxNxCdClcVkmTs7hU3oxXsLzUTS_31b833e024b6fde723bc3547d0de75a5"
client = yapp.Yapp(api_key=API_KEY)

print("=" * 70)
print("YAPP SDK ENDPOINT TESTING")
print("=" * 70)
print()

# =============================================================================
# TEST 1: Kokoro TTS (Text-to-Speech)
# =============================================================================
print("TEST 1: Kokoro TTS - Simple text-to-speech")
print("-" * 70)
try:
    response = client.audio.speech.create(
        "kokoro",
        "Hello world! This is a test of the Kokoro text to speech model.",
        voice="af_bella",
        speed=1.0
    )

    # Save the audio
    output_file = "test_kokoro_output.wav"
    response.save(output_file)

    print(f"✅ SUCCESS")
    print(f"   Generated audio: {len(response.content)} bytes")
    print(f"   Content type: {response.content_type}")
    print(f"   Saved to: {output_file}")

except Exception as e:
    print(f"❌ FAILED: {e}")

print()

# =============================================================================
# TEST 2: Kokoro TTS with different speed
# =============================================================================
print("TEST 2: Kokoro TTS - Custom speed (1.5x faster)")
print("-" * 70)
try:
    response = client.audio.speech.create(
        "kokoro",
        "This speech is faster than normal.",
        voice="af_bella",
        speed=1.5
    )

    output_file = "test_kokoro_fast.wav"
    response.save(output_file)

    print(f"✅ SUCCESS")
    print(f"   Generated audio: {len(response.content)} bytes")
    print(f"   Saved to: {output_file}")

except Exception as e:
    print(f"❌ FAILED: {e}")

print()

# =============================================================================
# TEST 3: ResembleAI TTS (Text-to-Speech without voice cloning)
# =============================================================================
print("TEST 3: ResembleAI TTS - Simple generation")
print("-" * 70)
try:
    response = client.audio.speech.create(
        "resemble",
        "This is ResembleAI speaking with natural voice synthesis.",
        exaggeration=0.5,
        cfg_weight=0.5
    )

    output_file = "test_resemble_output.wav"
    response.save(output_file)

    print(f"✅ SUCCESS")
    print(f"   Generated audio: {len(response.content)} bytes")
    print(f"   Content type: {response.content_type}")
    print(f"   Saved to: {output_file}")

except Exception as e:
    print(f"❌ FAILED: {e}")

print()

# =============================================================================
# TEST 4: ResembleAI TTS with high exaggeration
# =============================================================================
print("TEST 4: ResembleAI TTS - High exaggeration (emotional)")
print("-" * 70)
try:
    response = client.audio.speech.create(
        "resemble",
        "Wow! This is amazing! So exciting!",
        exaggeration=0.9,
        cfg_weight=0.5
    )

    output_file = "test_resemble_expressive.wav"
    response.save(output_file)

    print(f"✅ SUCCESS")
    print(f"   Generated audio: {len(response.content)} bytes")
    print(f"   Saved to: {output_file}")

except Exception as e:
    print(f"❌ FAILED: {e}")

print()

# =============================================================================
# TEST 5: Parakeet STT (Speech-to-Text)
# =============================================================================
print("TEST 5: Parakeet STT - Transcribe generated audio")
print("-" * 70)
try:
    # Use one of the generated audio files
    test_audio = "test_kokoro_output.wav"

    if os.path.exists(test_audio):
        response = client.audio.transcriptions.create(
            "parakeet",   # Model (positional)
            test_audio    # File (positional)
        )

        print(f"✅ SUCCESS")
        print(f"   Transcription: \"{response.text}\"")
        if response.metadata:
            print(f"   Metadata: {response.metadata}")
    else:
        print(f"⚠️  SKIPPED: Audio file not found ({test_audio})")

except Exception as e:
    print(f"❌ FAILED: {e}")

print()

# =============================================================================
# TEST 6: Parakeet STT with time window
# =============================================================================
print("TEST 6: Parakeet STT - Transcribe with time window")
print("-" * 70)
try:
    test_audio = "test_kokoro_output.wav"

    if os.path.exists(test_audio):
        response = client.audio.transcriptions.create(
            "parakeet",   # Model (positional)
            test_audio,   # File (positional)
            start_time=0.0,
            end_time=3.0
        )

        print(f"✅ SUCCESS")
        print(f"   Transcription (0-3s): \"{response.text}\"")
    else:
        print(f"⚠️  SKIPPED: Audio file not found")

except Exception as e:
    print(f"❌ FAILED: {e}")

print()

# =============================================================================
# TEST 7: Parameter Discovery
# =============================================================================
print("TEST 7: Model Parameter Discovery")
print("-" * 70)
try:
    # List models
    models = client.audio.speech.list_models()
    print(f"✅ TTS Models available: {models}")

    # Get Kokoro parameters
    print()
    print("Kokoro parameters:")
    params = client.audio.speech.get_model_parameters("kokoro")
    for param_name, param_info in params.items():
        print(f"  - {param_name} ({param_info['type']}): {param_info['description']}")
        print(f"    Default: {param_info['default']}")

except Exception as e:
    print(f"❌ FAILED: {e}")

print()

# =============================================================================
# TEST 8: Error Handling - Wrong parameters
# =============================================================================
print("TEST 8: Error Handling - Wrong parameters for model")
print("-" * 70)
try:
    # This should fail - speed is not valid for ResembleAI
    response = client.audio.speech.create(
        "resemble",
        "This will fail",
        speed=1.5  # Wrong parameter!
    )
    print(f"❌ UNEXPECTED: Should have raised ValidationError")

except yapp.ValidationError as e:
    print(f"✅ SUCCESS: Correctly caught error")
    print(f"   Error message: {e}")

except Exception as e:
    print(f"❌ FAILED: Wrong exception type: {e}")

print()

# =============================================================================
# SUMMARY
# =============================================================================
print("=" * 70)
print("TESTING COMPLETE")
print("=" * 70)
print()
print("Generated files:")
for file in ["test_kokoro_output.wav", "test_kokoro_fast.wav",
             "test_resemble_output.wav", "test_resemble_expressive.wav"]:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"  ✓ {file} ({size:,} bytes)")
