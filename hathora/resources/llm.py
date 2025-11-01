"""LLM (Large Language Model) resource for chat completions"""

from typing import Optional, List, Dict, Any, Union
from pathlib import Path


class ChatMessage:
    """Represents a chat message"""

    def __init__(self, role: str, content: str):
        """
        Args:
            role: The role of the message sender (e.g., "user", "assistant", "system")
            content: The content of the message
        """
        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


class ChatCompletionResponse:
    """Response from chat completion"""

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @property
    def content(self) -> str:
        """Get the response message content"""
        try:
            return self._data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return ""

    @property
    def message(self) -> Dict[str, str]:
        """Get the full message object"""
        try:
            return self._data["choices"][0]["message"]
        except (KeyError, IndexError):
            return {}

    @property
    def raw(self) -> Dict[str, Any]:
        """Get the raw response data"""
        return self._data

    @property
    def usage(self) -> Optional[Dict[str, int]]:
        """Get token usage information"""
        return self._data.get("usage")

    @property
    def model(self) -> Optional[str]:
        """Get the model used"""
        return self._data.get("model")

    def __str__(self) -> str:
        return self.content


class LLM:
    """LLM resource for chat completions with language models"""

    # Available LLM models
    AVAILABLE_MODELS = {
        "qwen": {
            "name": "Qwen/Qwen3-30B-A3B",
            "description": "Qwen3 30B model - latest generation LLM with reasoning and multilingual support",
            "type": "chat",
        }
    }

    def __init__(self, client):
        """
        Initialize LLM resource.

        Args:
            client: The Hathora client instance
        """
        self.client = client
        self._base_url = None

    def set_endpoint(self, base_url: str):
        """
        Set the LLM endpoint URL.

        Args:
            base_url: Base URL for the LLM API (e.g., "https://app-xxx.app.hathora.dev")
        """
        self._base_url = base_url.rstrip('/')

    def chat(
        self,
        model: str,
        messages: Union[List[Dict[str, str]], List[ChatMessage], str],
        max_tokens: Optional[int] = 1000,
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = None,
        stream: bool = False,
        **kwargs
    ) -> ChatCompletionResponse:
        """
        Create a chat completion.

        Args:
            model: Model to use (e.g., "qwen" for Qwen/Qwen3-30B-A3B)
            messages: List of messages or a single user message string
            max_tokens: Maximum tokens to generate (default: 1000)
            temperature: Sampling temperature 0.0-1.0 (default: 0.7)
            top_p: Nucleus sampling parameter (optional)
            stream: Whether to stream the response (default: False)
            **kwargs: Additional model-specific parameters

        Returns:
            ChatCompletionResponse object

        Example:
            >>> # Simple usage with a string
            >>> response = client.llm.chat("qwen", "What is Python?")
            >>> print(response.content)

            >>> # With message history
            >>> messages = [
            ...     {"role": "user", "content": "Hello!"},
            ...     {"role": "assistant", "content": "Hi! How can I help?"},
            ...     {"role": "user", "content": "Tell me about AI"}
            ... ]
            >>> response = client.llm.chat("qwen", messages)
        """
        from hathora.exceptions import ValidationError

        if not self._base_url:
            raise ValidationError(
                "LLM endpoint not configured. Use client.llm.set_endpoint('https://your-app.app.hathora.dev') first."
            )

        # Validate model
        if model not in self.AVAILABLE_MODELS:
            available = ", ".join(self.AVAILABLE_MODELS.keys())
            raise ValidationError(
                f"Unknown LLM model: {model}. Available models: {available}\n"
                f"Use client.llm.list_models() for more details."
            )

        # Convert messages to proper format
        if isinstance(messages, str):
            # Simple string input - convert to user message
            formatted_messages = [{"role": "user", "content": messages}]
        elif isinstance(messages, list):
            formatted_messages = []
            for msg in messages:
                if isinstance(msg, ChatMessage):
                    formatted_messages.append(msg.to_dict())
                elif isinstance(msg, dict):
                    formatted_messages.append(msg)
                else:
                    raise ValidationError(
                        f"Invalid message type: {type(msg)}. Expected dict or ChatMessage."
                    )
        else:
            raise ValidationError(
                f"Invalid messages type: {type(messages)}. Expected str, list of dicts, or list of ChatMessage."
            )

        # Build payload
        payload = {
            "messages": formatted_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if top_p is not None:
            payload["top_p"] = top_p

        if stream:
            payload["stream"] = stream

        # Add any additional parameters
        payload.update(kwargs)

        # Make API request
        url = f"{self._base_url}/v1/chat/completions"

        response_data = self.client._request(
            method="POST",
            url=url,
            json=payload,
        )

        return ChatCompletionResponse(response_data)

    def list_models(self) -> List[str]:
        """
        List all available LLM models.

        Returns:
            List of model names
        """
        return list(self.AVAILABLE_MODELS.keys())

    def get_model_info(self, model: str) -> Dict[str, str]:
        """
        Get information about a specific model.

        Args:
            model: Model name

        Returns:
            Dict with model information
        """
        from hathora.exceptions import ValidationError

        if model not in self.AVAILABLE_MODELS:
            available = ", ".join(self.AVAILABLE_MODELS.keys())
            raise ValidationError(
                f"Unknown model: {model}. Available models: {available}"
            )

        return self.AVAILABLE_MODELS[model]

    def print_model_help(self, model: str):
        """
        Print helpful information about a model.

        Args:
            model: Model name
        """
        info = self.get_model_info(model)
        print(f"\nModel: {model}")
        print(f"Full Name: {info['name']}")
        print(f"Type: {info['type']}")
        print(f"Description: {info['description']}")
        print("\nUsage:")
        print(f"  response = client.llm.chat('{model}', 'Your prompt here')")
        print(f"  print(response.content)")
