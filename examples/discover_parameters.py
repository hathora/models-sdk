"""
Example: Discovering model parameters

This example demonstrates how to discover what parameters are available
for each model using the SDK's built-in help methods.
"""

import hathora

# Initialize the client
client = hathora.Yapp(api_key="your-api-key-here")

print("=== Model Parameter Discovery ===\n")

# ============================================================================
# 1. LIST ALL AVAILABLE MODELS
# ============================================================================
print("1. List all available TTS models:")
print("-" * 50)
models = client.text_to_speech.list_models()
print(f"Available models: {models}")
print()

# ============================================================================
# 2. GET HELP FOR SPECIFIC MODEL
# ============================================================================
print("2. Get detailed parameter info for each model:")
print("-" * 50)

# Kokoro model help
client.text_to_speech.print_model_help("kokoro")

# ResembleAI model help
client.text_to_speech.print_model_help("resemble")

# ============================================================================
# 3. PROGRAMMATICALLY ACCESS PARAMETER INFO
# ============================================================================
print("3. Programmatically access parameter specifications:")
print("-" * 50)

# Get Kokoro parameters
kokoro_params = client.text_to_speech.get_model_parameters("kokoro")
print("Kokoro parameters:")
for param_name, param_info in kokoro_params.items():
    print(f"  {param_name}:")
    print(f"    Type: {param_info['type']}")
    print(f"    Default: {param_info['default']}")
    print(f"    Description: {param_info['description']}")
print()

# Get ResembleAI parameters
resemble_params = client.text_to_speech.get_model_parameters("resemble")
print("ResembleAI parameters:")
for param_name, param_info in resemble_params.items():
    print(f"  {param_name}:")
    print(f"    Type: {param_info['type']}")
    print(f"    Default: {param_info['default']}")
    print(f"    Description: {param_info['description']}")
print()

# ============================================================================
# 4. HELPFUL ERROR MESSAGES
# ============================================================================
print("4. Error messages guide you to correct parameters:")
print("-" * 50)

try:
    # Try to use wrong parameter for Kokoro
    response = client.text_to_speech.convert(
        "kokoro",  # Model first
        "This will fail",
        exaggeration=0.5  # ERROR: This is a ResembleAI parameter!
    )
except hathora.ValidationError as e:
    print(f"Error caught: {e}\n")

try:
    # Try to use wrong parameter for ResembleAI
    response = client.text_to_speech.convert(
        "resemble",  # Model first
        "This will fail",
        speed=1.5  # ERROR: This is a Kokoro parameter!
    )
except hathora.ValidationError as e:
    print(f"Error caught: {e}\n")

try:
    # Try to use unknown model
    response = client.text_to_speech.convert(
        "unknown_model",  # Model first - ERROR: Model doesn't exist!
        "This will fail"
    )
except hathora.ValidationError as e:
    print(f"Error caught: {e}\n")

# ============================================================================
# 5. BUILDING DYNAMIC CALLS
# ============================================================================
print("5. Build dynamic API calls based on discovered parameters:")
print("-" * 50)

# Get default values for Kokoro and use them
kokoro_params = client.text_to_speech.get_model_parameters("kokoro")
default_voice = kokoro_params["voice"]["default"]
default_speed = kokoro_params["speed"]["default"]

print(f"Using Kokoro defaults: voice={default_voice}, speed={default_speed}")
response = client.text_to_speech.convert(
    "kokoro",  # Model first
    "Using discovered default values",
    voice=default_voice,
    speed=default_speed
)
response.save("output_defaults.wav")
print("Saved to output_defaults.wav")
print()

print("=== Discovery Complete ===")
print("\nQuick reference:")
print("  - client.text_to_speech.list_models() - List all models")
print("  - client.text_to_speech.print_model_help(model) - Print parameter help")
print("  - client.text_to_speech.get_model_parameters(model) - Get parameter specs")
