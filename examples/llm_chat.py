"""
Example of using Hathora SDK for LLM chat completions.

This example demonstrates how to use the Qwen LLM model for chat completions.
"""

import hathora
import os

# Initialize the client
client = hathora.Hathora(
    api_key=os.environ.get("HATHORA_API_KEY", "your-api-key-here")
)

# Configure the LLM endpoint
# Replace with your actual Hathora app endpoint
LLM_ENDPOINT = "https://app-362f7ca1-6975-4e18-a605-ab202bf2c315.app.hathora.dev"
client.llm.set_endpoint(LLM_ENDPOINT)

print("=" * 60)
print("Hathora LLM Chat Examples")
print("=" * 60)

# Example 1: Simple question
print("\n1. Simple Question")
print("-" * 60)
response = client.llm.chat(
    "qwen",
    "What is Python? Give a brief answer."
)
print(f"Question: What is Python?")
print(f"Response: {response.content}")

# Example 2: Chat with message history
print("\n2. Chat with Message History")
print("-" * 60)
messages = [
    {"role": "user", "content": "Hello! Can you help me with programming?"},
    {"role": "assistant", "content": "Of course! I'd be happy to help you with programming. What would you like to know?"},
    {"role": "user", "content": "What's the difference between a list and a tuple in Python?"}
]

response = client.llm.chat(
    "qwen",
    messages,
    max_tokens=500,
    temperature=0.7
)
print("Conversation:")
for msg in messages:
    print(f"  {msg['role']}: {msg['content']}")
print(f"\nResponse: {response.content}")

# Example 3: Creative writing with higher temperature
print("\n3. Creative Writing (high temperature)")
print("-" * 60)
response = client.llm.chat(
    "qwen",
    "Write a haiku about artificial intelligence",
    max_tokens=100,
    temperature=0.9
)
print(f"Prompt: Write a haiku about artificial intelligence")
print(f"Response:\n{response.content}")

# Example 4: Precise answer with low temperature
print("\n4. Precise Answer (low temperature)")
print("-" * 60)
response = client.llm.chat(
    "qwen",
    "What is 15 * 23?",
    max_tokens=50,
    temperature=0.1
)
print(f"Question: What is 15 * 23?")
print(f"Response: {response.content}")

# Example 5: Using ChatMessage objects
print("\n5. Using ChatMessage Objects")
print("-" * 60)
from hathora.resources.llm import ChatMessage

conversation = [
    ChatMessage("system", "You are a helpful coding assistant."),
    ChatMessage("user", "How do I read a file in Python?")
]

response = client.llm.chat(
    "qwen",
    conversation,
    max_tokens=300
)
print("Response:", response.content)

# Example 6: Accessing response metadata
print("\n6. Response Metadata")
print("-" * 60)
response = client.llm.chat(
    "qwen",
    "Explain machine learning in one sentence."
)
print(f"Content: {response.content}")
print(f"Model used: {response.model}")
if response.usage:
    print(f"Tokens used: {response.usage}")

# Example 7: List available models
print("\n7. Available Models")
print("-" * 60)
models = client.llm.list_models()
print(f"Available LLM models: {models}")

for model in models:
    info = client.llm.get_model_info(model)
    print(f"\n{model}:")
    print(f"  Name: {info['name']}")
    print(f"  Description: {info['description']}")

print("\n" + "=" * 60)
print("Examples completed!")
print("=" * 60)
