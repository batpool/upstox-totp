"""Pydantic models for Upstox TOTP API responses."""

import os
from typing import Any, Generic, Self, TypeVar

from pydantic import BaseModel, Field, SecretStr
from pydantic.config import ConfigDict

T = TypeVar("T")


class Config(BaseModel):
    """Configuration model for Upstox TOTP API."""

    username: str = Field(description="Upstox username")
    password: SecretStr = Field(description="Upstox password or pin code")
    pin_code: SecretStr = Field(description="Upstox pin code | it may be same as password")
    totp_secret: SecretStr = Field(description="Upstox TOTP secret")
    client_id: str = Field(description="The API key obtained during the app generation process.")
    client_secret: SecretStr = Field(description="The API secret obtained during the app generation process.")
    redirect_uri: str = Field(description="The URL to which the user will be redirected post authentication; must match the URL provided during app generation.")
    debug: bool = Field(description="Whether to enable debug mode", default=False)
    redirect_uri_upstox: str = Field(
        description="Internal redirect URI for Upstox",
        default="https://api-v2.upstox.com/login/authorization/redirect",
    )
    sleep_time: int = Field(description="The time to sleep between requests in milliseconds", default=1000)

    model_config = ConfigDict(str_strip_whitespace=True, validate_default=True)

    @classmethod
    def from_env(cls, **overrides: Any) -> Self:
        """Load from environment with overrides."""
        from dotenv import dotenv_values

        env_values = dotenv_values()
        env_values.update(os.environ)

        def get_value(key: str, env_key: str, default: Any = None) -> Any:
            if key in overrides and overrides[key] is not None:
                return overrides[key]
            return env_values.get(env_key, default)

        def get_bool_value(key: str, env_key: str, default: bool = False) -> bool:
            if key in overrides and overrides[key] is not None:
                return bool(overrides[key])
            env_val = env_values.get(env_key, str(default))
            if env_val is None:
                return default
            return str(env_val).lower() in ("true", "1", "yes", "on")

        return cls(
            username=get_value("username", "UPSTOX_USERNAME"),
            password=get_value("password", "UPSTOX_PASSWORD"),
            pin_code=get_value("pin_code", "UPSTOX_PIN_CODE"),
            totp_secret=get_value("totp_secret", "UPSTOX_TOTP_SECRET"),
            client_id=get_value("client_id", "UPSTOX_CLIENT_ID"),
            client_secret=get_value("client_secret", "UPSTOX_CLIENT_SECRET"),
            redirect_uri=get_value("redirect_uri", "UPSTOX_REDIRECT_URI"),
            debug=get_bool_value("debug", "UPSTOX_DEBUG", False),
        )


class ResponseBase(BaseModel, Generic[T]):
    """Base response model for Upstox API."""

    success: bool = Field(description="Whether the request was successful")
    data: T | None = Field(default=None, description="Data of the response")
    error: dict[str, Any] | None = Field(default=None, description="Error of the response")


class OTPData(BaseModel):
    """OTP data model."""

    message: str
    validateOTPToken: str
    nextRequestInterval: int
    userType: str
    isTotpEnabled: bool


class OTPGenerationResponse(ResponseBase[OTPData]):
    """Response model for OTP generation endpoint."""


class OTPValidationUserProfile(BaseModel):
    profileId: int
    userId: str
    firstName: str
    lastName: str
    avatarUrl: str | None = None


class OTPValidationData(BaseModel):
    message: str
    userType: str
    userProfile: OTPValidationUserProfile
    isSecretPinSet: bool


class OTPValidationResponse(ResponseBase[OTPValidationData]):
    """Response model for OTP validation endpoint."""


class TwoFactorAuthenticationData(BaseModel):
    redirectUri: str | None = None
    userType: str
    customerStatus: str
    appStatus: str | None = None
    refreshTokenExpiry: int
    isPlusPlanFastWebsocketEnabled: bool
    isNewRefreshTokenCreated: bool
    isExternalClientOAuthApp: bool


class TwoFactorAuthenticationResponse(ResponseBase[TwoFactorAuthenticationData]):
    """Response model for two factor authentication endpoint."""


class PinSubmissionData(BaseModel):
    """Pin submission data model."""

    message: str
    userType: str


class PinSubmissionResponse(ResponseBase[PinSubmissionData]):
    """Response model for PIN submission endpoint."""


class OAuthAuthorizationData(BaseModel):
    redirectUri: str
    isApproved: bool


class OAuthAuthorizationResponse(ResponseBase[OAuthAuthorizationData]):
    """Response model for OAuth authorization endpoint."""


class AccessTokenData(BaseModel):
    email: str
    exchanges: list[str]
    products: list[str]
    broker: str
    user_id: str
    user_name: str
    order_types: list[str]
    user_type: str
    poa: bool
    ddpi: bool
    is_active: bool
    access_token: str
    extended_token: str | None = None


class AccessTokenResponse(ResponseBase[AccessTokenData]):
    """Response model for access token endpoint."""


class UserIdAndUserType(BaseModel):
    user_id: str
    client_id: str
    user_type: str

    model_config = ConfigDict(str_strip_whitespace=True, validate_default=True)
