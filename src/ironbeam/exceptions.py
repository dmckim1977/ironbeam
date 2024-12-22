from typing import Optional


class IronbeamAPIError(Exception):
    """Base exception for Ironbeam API errors."""

    pass


class IronbeamResponseError(IronbeamAPIError):
    """Exception for API response errors."""

    def __init__(self, status: str, message: str, error: Optional[str | None] = None):
        self.status = status
        self.message = message
        self.error = error
        super().__init__(
            f"Status: {status}, Message: {message}"
            + (f", Error: {error}" if error else "")
        )
