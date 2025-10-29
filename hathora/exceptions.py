"""Hathora SDK Exceptions"""


class HathoraError(Exception):
    """Base exception for all Hathora SDK errors"""
    pass


class APIError(HathoraError):
    """Raised when the API returns an error response"""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(HathoraError):
    """Raised when authentication fails"""
    pass


class ValidationError(HathoraError):
    """Raised when request validation fails"""
    pass


class FileError(HathoraError):
    """Raised when there's an issue with file handling"""
    pass
