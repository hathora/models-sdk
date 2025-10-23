"""Yapp SDK Client"""

from typing import Optional, Dict, Any
import requests

from yapp.resources.transcription import Transcription
from yapp.resources.synthesis import Synthesis
from yapp.exceptions import APIError, AuthenticationError


class Audio:
    """Audio namespace containing transcriptions and speech resources"""

    def __init__(self, client):
        self._client = client
        self.transcriptions = Transcription(client)
        self.speech = Synthesis(client)


class Yapp:
    """
    Main client for the Yapp Voice AI API.

    This client provides access to speech-to-text (transcription) and
    text-to-speech (synthesis) capabilities.

    Args:
        api_key: Your Yapp API key (optional, can also be set via environment variable)
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> import yapp
        >>> client = yapp.Yapp(api_key="your-api-key")
        >>>
        >>> # Transcribe audio
        >>> transcription = client.audio.transcriptions.create(file="audio.wav")
        >>> print(transcription.text)
        >>>
        >>> # Generate speech
        >>> response = client.audio.speech.create(text="Hello world")
        >>> response.save("output.wav")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        self.api_key = api_key or self._get_api_key_from_env()
        self.timeout = timeout

        # Initialize resources
        self.audio = Audio(self)

    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variable"""
        import os
        return os.environ.get("YAPP_API_KEY")

    def _request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make an HTTP request to the Yapp API.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Full URL to request
            headers: Optional headers dict
            params: Optional query parameters
            json: Optional JSON body
            files: Optional files for multipart upload
            data: Optional form data

        Returns:
            Response data (dict, bytes, or str)

        Raises:
            APIError: If the API returns an error
            AuthenticationError: If authentication fails
        """
        # Prepare headers
        request_headers = {
            "accept": "application/json",
        }
        if headers:
            request_headers.update(headers)

        # Add authentication if API key is set
        # Note: Update this based on your actual auth mechanism
        if self.api_key:
            request_headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=request_headers,
                params=params,
                json=json,
                files=files,
                data=data,
                timeout=self.timeout,
            )

            # Handle authentication errors
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key or authentication failed")

            # Handle other HTTP errors
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    error_message = error_data.get("error", {}).get("message", response.text)
                except Exception:
                    error_message = response.text

                raise APIError(
                    message=error_message,
                    status_code=response.status_code,
                    response=error_data if 'error_data' in locals() else None,
                )

            # Parse response based on content type
            content_type = response.headers.get("content-type", "")

            if "application/json" in content_type:
                return response.json()
            elif "audio" in content_type or response.content[:4] == b'RIFF' or response.content[:4] == b'\xff\xfb':
                # Return audio content as bytes
                return response.content
            else:
                # Return text for other content types
                return response.text

        except requests.exceptions.Timeout:
            raise APIError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")


# Convenience aliases for simpler imports
class YappClient(Yapp):
    """Alias for Yapp client"""
    pass
