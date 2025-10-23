"""Yapp SDK Exceptions"""


class YappError(Exception):
    """Base exception for all Yapp SDK errors"""
    pass


class APIError(YappError):
    """Raised when the API returns an error response"""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(YappError):
    """Raised when authentication fails"""
    pass


class ValidationError(YappError):
    """Raised when request validation fails"""
    pass


class FileError(YappError):
    """Raised when there's an issue with file handling"""
    pass
