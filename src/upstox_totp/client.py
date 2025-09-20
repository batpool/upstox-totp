"""Main Upstox TOTP client."""

from __future__ import annotations

import base64
import os
import random
import string
import textwrap
from functools import cached_property
from typing import TYPE_CHECKING, Any, Self

import pyotp
from curl_cffi import Session, requests
from pydantic import SecretStr

from upstox_totp.errors import ConfigurationError
from upstox_totp.logging import set_log_level
from upstox_totp.models import Config

if TYPE_CHECKING:
    from typing import Self

    from ._api.app_token import AppTokenAPI


class UpstoxTOTP:
    """Main Upstox TOTP client."""

    def __init__(
        self,
        *,
        username: str | None = None,
        password: SecretStr | str | None = None,
        pin_code: SecretStr | str | None = None,
        totp_secret: SecretStr | str | None = None,
        client_id: str | None = None,
        client_secret: SecretStr | str | None = None,
        redirect_uri: str | None = None,
        debug: bool = False,
        sleep_time: int = 1000,
    ) -> None:
        """
        Initialize the Upstox TOTP client.

        Args:
            username: The username for the Upstox account.
            password: The password for the Upstox account.
            pin_code: The pin code for the Upstox account.
            totp_secret: The TOTP secret for the Upstox account.
            client_id: The client ID for the Upstox account.
            redirect_uri: The redirect URI for the Upstox account.
            debug: Whether to enable debug mode.
            sleep_time: The time to sleep between requests in milliseconds.
        Raises:
            ConfigurationError: If the configuration is invalid.
        """
        try:
            self.config = Config.from_env(
                username=username,
                password=password,
                pin_code=pin_code,
                totp_secret=totp_secret,
                client_secret=client_secret,
                client_id=client_id,
                redirect_uri=redirect_uri,
                debug=debug,
                sleep_time=sleep_time,
            )
        except Exception as e:
            raise ConfigurationError(
                textwrap.dedent(
                    text="""
                    Failed to load configuration. Ensure you have set:
                    - UPSTOX_USERNAME
                    - UPSTOX_PASSWORD
                    - UPSTOX_PIN_CODE
                    - UPSTOX_TOTP_SECRET
                    - UPSTOX_CLIENT_ID
                    - UPSTOX_CLIENT_SECRET
                    - UPSTOX_REDIRECT_URI
                    - UPSTOX_DEBUG
                    Or pass them as parameters to the client.
                    """
                )
            ) from e

        self.base_domain: str = "https://{stage}.upstox.com"

        # Generate and store the request ID once for the entire lifecycle
        self._request_id: str = self._generate_new_request_id()

        self._headers: dict[str, str] = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.9",
            "content-type": "application/json",
            "origin": self.base_domain.format(stage="login"),
            "priority": "u=1, i",
            "referer": self.base_domain.format(stage="login"),
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "x-device-details": "platform=WEB|osName=Mac OS/10.15.7|osVersion=Chrome/140.0.0.0|appVersion=4.0.0|modelName=Chrome|manufacturer=Apple|uuid=3Z1IVTlV4rUUGbNp8KP0|userAgent=Upstox 3.0 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "x-request-id": self._request_id,
        }

        self._client: Session[Any] = requests.Session(impersonate="chrome131", headers=self._headers, debug=self.config.debug)

        if self.config.debug:

            set_log_level("DEBUG")

    @property
    def session(self) -> Session[Any]:
        """Public accessor for the underlying HTTP session."""
        return self._client

    @classmethod
    def from_env_file(cls, path: str = ".env") -> Self:
        """
        Create client from a specific env file.

        Args:
            path: Path to env file (default: .env)

        Returns:
            Configured Upstox TOTP client
        """
        from dotenv import load_dotenv

        _ = load_dotenv(path)

        raw_pin = os.getenv("UPSTOX_PIN_CODE", "")
        encoded_pin = cls._generate_encodeed_pin_code(raw_pin)

        return cls(
            username=os.getenv("UPSTOX_USERNAME", ""),
            password=SecretStr(os.getenv("UPSTOX_PASSWORD", "")),
            pin_code=SecretStr(encoded_pin),
            totp_secret=SecretStr(os.getenv("UPSTOX_TOTP_SECRET", "")),
            client_id=os.getenv("UPSTOX_CLIENT_ID", ""),
            client_secret=SecretStr(os.getenv("UPSTOX_CLIENT_SECRET", "")),
            redirect_uri=os.getenv("UPSTOX_REDIRECT_URI", ""),
            sleep_time=int(os.getenv("UPSTOX_SLEEP_TIME", "1000")),
            debug=os.getenv("UPSTOX_DEBUG", "false").lower() in ("true", "1", "yes", "on"),
        )

    @staticmethod
    def _generate_encodeed_pin_code(pin_code: str) -> str:
        """Generate an base64 encoded pin code."""
        return base64.b64encode(pin_code.encode()).decode(encoding="utf-8")

    @staticmethod
    def _generate_new_request_id() -> str:
        """Generate a new request ID."""
        return "WPRO-" + "".join(random.choices(string.ascii_letters + string.digits, k=10))

    def generate_request_id(self) -> str:
        """Return the same request ID for the entire lifecycle of this client instance."""
        return self._request_id

    def generate_totp_secret(self) -> str:
        """Generate a TOTP."""
        from upstox_totp.logging import logger

        totp_secret = self.config.totp_secret.get_secret_value()
        generated_totp = pyotp.TOTP(s=totp_secret).now()

        if self.config.debug:
            logger.debug(f"Generated TOTP: {generated_totp}")
            logger.debug(f"TOTP secret length: {len(totp_secret)}")

        return generated_totp

    def reset_session(self) -> None:
        """
        Reset the underlying HTTP session.

        This will clear all headers, cookies, and session state
        without closing the session.
        """
        # Clear all headers
        self._client.headers.clear()

        # Clear all cookies
        self._client.cookies.clear()

        # Reset any other session attributes that might interfere
        if hasattr(self._client, "auth"):
            self._client.auth = None

    @cached_property
    def app_token(self) -> AppTokenAPI:
        """App token management."""
        from upstox_totp._api.app_token import AppTokenAPI

        return AppTokenAPI(self)

    def __enter__(self) -> Self:
        """Enter context manager."""
        return self

    def __exit__(self, *args: object) -> None:
        """Exit context manager and clean up."""
        self._client.close()
