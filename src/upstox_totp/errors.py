"""Upstox API error handling."""

from enum import Enum
from typing import Any


class ErrorCode(Enum):
    """Known Upstox error codes with explanations based on official documentation.

    Reference: https://upstox.com/developer/api-documentation/error-codes/
    """

    BAD_REQUEST = "UDAPI10000"
    INVALID_CREDENTIALS = "UDAPI100016"
    TOO_MANY_REQUESTS = "UDAPI10005"
    API_VERSION_NOT_EXIST = "UDAPI100015"
    INVALID_TOKEN = "UDAPI100050"
    EXTENDED_TOKEN_NOT_PERMITTED = "UDAPI100067"
    INVALID_INPUT_36 = "UDAPI100036"
    INVALID_INPUT_38 = "UDAPI100038"
    INACTIVE_CLIENT_ID = "UDAPI100073"
    UNKNOWN = "UDAPI100500"

    CLIENT_ID_REDIRECT_URI_ERROR = "UDAPI100068"


class UpstoxError(Exception):
    """Base class for all Upstox API errors."""

    def __init__(self, error_code: ErrorCode, message: str, details: dict[str, Any] | None = None):
        """Initialize error with code, message and optional details."""
        self.error_code: ErrorCode = error_code
        self.message: str = message
        self.details: dict[str, Any] | None = details or {}
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format the error message with help if available."""
        msg: str = f"{self.error_code.value}: {self.message}"

        if self.error_code == ErrorCode.CLIENT_ID_REDIRECT_URI_ERROR:
            msg += "\n💡 Tip: Verify your client_id and redirect_uri in your .env file match your Upstox developer app settings."
        elif self.error_code == ErrorCode.INVALID_CREDENTIALS:
            msg += "\n💡 Tip: Check your username, password, and PIN in your .env file."
        elif self.error_code == ErrorCode.INVALID_TOKEN:
            msg += "\n💡 Tip: Your access token may have expired. Try regenerating it."
        elif self.error_code == ErrorCode.INACTIVE_CLIENT_ID:
            msg += "\n💡 Tip: Contact Upstox support to activate your client_id."
        elif self.error_code == ErrorCode.TOO_MANY_REQUESTS:
            msg += "\n💡 Tip: You've exceeded rate limits. Wait before making more requests."
        elif self.error_code == ErrorCode.UNKNOWN and "mobile number" in self.message.lower():
            msg += "\n💡 Tip: Check your UPSTOX_USERNAME in .env - it should be your 10-digit mobile number (e.g., 9876543210)."
        elif self.error_code == ErrorCode.UNKNOWN and "attempts left" in self.message.lower():
            msg += "\n💡 Tip: Check your UPSTOX_TOTP_SECRET in .env - it should be the TOTP secret key from your Upstox app setup. Make sure your system time is correct."
        elif self.error_code == ErrorCode.UNKNOWN and "client_secret" in self.message.lower():
            msg += "\n💡 Tip: Verify your UPSTOX_CLIENT_ID and UPSTOX_CLIENT_SECRET in .env match your Upstox developer app credentials."

        return msg

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> "UpstoxError":
        """Create error from API response data.

        Handles both old format and new format error responses.
        """
        if "data" in data and isinstance(data["data"], dict) and "errors" in data["data"]:
            errors = data["data"]["errors"]
            if errors and isinstance(errors, list) and len(errors) > 0:
                error_info = errors[0]
                error_code_str = error_info.get("errorCode", error_info.get("error_code", "UDAPI100500"))
                message = error_info.get("message", "Unknown error")

                try:
                    error_code = ErrorCode(error_code_str)
                except ValueError:
                    error_code = ErrorCode.UNKNOWN

                return cls(
                    error_code=error_code,
                    message=message,
                    details=data,
                )

        error_info = data.get("error", {})
        if error_info:
            error_code_str = error_info.get("code", "UDAPI100500")
            message = error_info.get("message", "Unknown error")

            try:
                error_code = ErrorCode(error_code_str)
            except ValueError:
                error_code = ErrorCode.UNKNOWN

            return cls(
                error_code=error_code,
                message=message,
                details=data,
            )

        return cls(
            error_code=ErrorCode.UNKNOWN,
            message="An unknown error occurred.",
            details=data,
        )


class ConfigurationError(Exception):
    """Raised when client configuration is invalid."""

    pass


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass
