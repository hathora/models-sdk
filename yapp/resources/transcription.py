"""Transcription (STT) resource"""

from typing import Optional, Union
from pathlib import Path

from yapp.types import AudioFile, TranscriptionResponse
from yapp._utils import prepare_audio_file
from yapp.exceptions import APIError, ValidationError


class Transcription:
    """Handles speech-to-text transcription using the Parakeet model"""

    def __init__(self, client):
        self._client = client
        # Parakeet STT model URL
        self._parakeet_url = "https://app-1c7bebb9-6977-4101-9619-833b251b86d1.app.hathora.dev"

    def create(
        self,
        model: str,
        file: AudioFile,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        **kwargs,
    ) -> TranscriptionResponse:
        """
        Transcribe audio to text using the specified STT model.

        Args:
            model: STT model to use (currently: "parakeet")
            file: Audio file to transcribe. Can be:
                - File path (str or Path)
                - File-like object
                - Raw bytes
            start_time: Optional start time in seconds for the transcription window
            end_time: Optional end time in seconds for the transcription window
            **kwargs: Additional model-specific parameters (reserved for future use)

        Returns:
            TranscriptionResponse with the transcribed text

        Example:
            >>> client = Yapp(api_key="your-api-key")
            >>> response = client.audio.transcriptions.create(
            ...     "parakeet",
            ...     file="audio.wav",
            ...     start_time=3.0,
            ...     end_time=9.0
            ... )
            >>> print(response.text)
        """
        # Currently only parakeet is supported
        if model != "parakeet":
            from yapp.exceptions import ValidationError
            raise ValidationError(f"Unknown STT model: {model}. Currently supported: 'parakeet'")

        # Route to parakeet (future: add other models here)
        return self._transcribe_parakeet(file, start_time, end_time, **kwargs)

    def _transcribe_parakeet(
        self,
        file: AudioFile,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        **kwargs,
    ) -> TranscriptionResponse:
        """Internal method to transcribe using Parakeet model"""
        # Prepare the file for upload
        file_obj, mime_type = prepare_audio_file(file)

        # Build query parameters
        params = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time

        # Prepare multipart form data
        files = {
            'file': ('audio', file_obj, mime_type)
        }

        # Validate unknown parameters
        if kwargs:
            unknown = ", ".join(kwargs.keys())
            from yapp.exceptions import ValidationError
            raise ValidationError(
                f"Unknown parameters for Parakeet model: {unknown}. "
                f"Valid parameters: start_time, end_time"
            )

        # Make the request
        try:
            response = self._client._request(
                method="POST",
                url=f"{self._parakeet_url}/v1/transcribe",
                params=params,
                files=files,
            )

            # Parse response
            if isinstance(response, dict):
                text = response.get("text", "")
                metadata = {k: v for k, v in response.items() if k != "text"}
                return TranscriptionResponse(text=text, metadata=metadata)
            else:
                # If response is just text
                return TranscriptionResponse(text=str(response))

        finally:
            # Close file if we opened it
            if isinstance(file, (str, Path)) and hasattr(file_obj, 'close'):
                file_obj.close()
