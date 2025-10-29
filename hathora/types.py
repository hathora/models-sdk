"""Type definitions for Yapp SDK"""

from typing import Optional, Union, BinaryIO
from pathlib import Path
from io import IOBase

# Type aliases for audio inputs
AudioFile = Union[str, Path, BinaryIO, bytes]


class AudioResponse:
    """Response object for audio generation endpoints"""

    def __init__(self, content: bytes, content_type: str = "audio/wav"):
        self._content = content
        self.content_type = content_type

    @property
    def content(self) -> bytes:
        """Get the raw audio bytes"""
        return self._content

    def save(self, file_path: Union[str, Path]) -> None:
        """
        Save audio to a file.

        Args:
            file_path: Path where the audio should be saved
        """
        path = Path(file_path)
        with open(path, 'wb') as f:
            f.write(self._content)

    def stream_to_file(self, file_path: Union[str, Path]) -> None:
        """
        Stream audio content to a file (alias for save).

        Args:
            file_path: Path where the audio should be saved
        """
        self.save(file_path)


class TranscriptionResponse:
    """Response object for transcription endpoints"""

    def __init__(self, text: str, metadata: Optional[dict] = None):
        self.text = text
        self.metadata = metadata or {}

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"TranscriptionResponse(text={self.text!r})"
