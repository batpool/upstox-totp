"""
A lightweight Python package that simplifies Upstox API authentication by handling TOTP-based
login and token generation automatically. With this library, you can securely generate
and refresh access tokens required to connect to the Upstox trading platform without manual intervention.

Features:

    🔐 Automated TOTP Authentication – Generate secure time-based one-time passwords (TOTP) for Upstox login.

    ⚡ Token Management – Fetch, refresh, and store Upstox access tokens with ease.

    🛠️ Simple API – Minimal, developer-friendly methods for quick integration.

    📈 Trading Ready – Instantly plug into Upstox APIs for real-time market data, order placement, and portfolio management.

    🐍 Pythonic Design – Built with modern async/session handling for robust performance.



▌   ▗
▛▌▀▌▜▘▛▛▌▀▌▛▌
▙▌█▌▐▖▌▌▌█▌▌▌

"""

from upstox_totp.client import UpstoxTOTP
from upstox_totp.errors import ConfigurationError, UpstoxError, ValidationError
from upstox_totp.models import (
    AccessTokenResponse,
    OAuthAuthorizationResponse,
    OTPGenerationResponse,
    OTPValidationData,
    OTPValidationResponse,
    OTPValidationUserProfile,
    TwoFactorAuthenticationData,
)

__version__ = "0.1.0"


__all__ = [
    "UpstoxTOTP",
    "ConfigurationError",
    "UpstoxError",
    "ValidationError",
    "OTPGenerationResponse",
    "OTPValidationResponse",
    "OTPValidationUserProfile",
    "OTPValidationData",
    "TwoFactorAuthenticationData",
    "OAuthAuthorizationResponse",
    "AccessTokenResponse",
]


def main() -> None:
    """Entry point for the CLI."""
    from upstox_totp.cli import cli

    cli()
