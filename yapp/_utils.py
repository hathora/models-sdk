"""Internal utilities for Yapp SDK"""

from typing import Union, BinaryIO, Tuple
from pathlib import Path
import mimetypes

from yapp.exceptions import FileError


def prepare_audio_file(file: Union[str, Path, BinaryIO, bytes]) -> Tuple[BinaryIO, str]:
    """
    Prepare an audio file for upload.

    Args:
        file: File path, Path object, file-like object, or bytes

    Returns:
        Tuple of (file_object, mime_type)

    Raises:
        FileError: If the file cannot be read or format is invalid
    """
    # Handle bytes
    if isinstance(file, bytes):
        from io import BytesIO
        return BytesIO(file), "audio/wav"

    # Handle file path (string or Path)
    if isinstance(file, (str, Path)):
        path = Path(file)
        if not path.exists():
            raise FileError(f"File not found: {file}")

        mime_type, _ = mimetypes.guess_type(str(path))
        if mime_type is None or not mime_type.startswith("audio/"):
            # Default to common audio types based on extension
            ext = path.suffix.lower()
            ext_to_mime = {
                ".wav": "audio/wav",
                ".mp3": "audio/mpeg",
                ".mp4": "audio/mp4",
                ".m4a": "audio/mp4",
                ".ogg": "audio/ogg",
                ".flac": "audio/flac",
                ".pcm": "audio/pcm",
            }
            mime_type = ext_to_mime.get(ext, "audio/wav")

        return open(path, 'rb'), mime_type

    # Handle file-like objects
    if hasattr(file, 'read'):
        # Try to get mime type from name attribute if available
        mime_type = "audio/wav"
        if hasattr(file, 'name'):
            guessed_type, _ = mimetypes.guess_type(file.name)
            if guessed_type and guessed_type.startswith("audio/"):
                mime_type = guessed_type

        return file, mime_type

    raise FileError(f"Unsupported file type: {type(file)}")


def validate_audio_format(file_path: Union[str, Path]) -> bool:
    """
    Validate that a file appears to be a supported audio format.

    Args:
        file_path: Path to the audio file

    Returns:
        True if the format appears valid
    """
    path = Path(file_path)
    supported_extensions = {".wav", ".mp3", ".mp4", ".m4a", ".ogg", ".flac", ".pcm"}
    return path.suffix.lower() in supported_extensions
