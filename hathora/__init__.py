"""Hathora AI Python SDK - Voice and LLM capabilities"""

from hathora.client import Hathora
from hathora.exceptions import HathoraError, APIError, AuthenticationError, ValidationError

__version__ = "0.4.0"
__all__ = ["Hathora", "HathoraError", "APIError", "AuthenticationError", "ValidationError"]
