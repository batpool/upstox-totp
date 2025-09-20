"""App token API."""

from __future__ import annotations

import base64
from typing import Any
from urllib.parse import parse_qs, urlparse

from curl_cffi.requests.models import Response

from upstox_totp._api.base import BaseAPI
from upstox_totp.errors import UpstoxError, ValidationError
from upstox_totp.logging import logger
from upstox_totp.models import (
    AccessTokenResponse,
    OAuthAuthorizationResponse,
    OTPGenerationResponse,
    OTPValidationResponse,
    ResponseBase,
    TwoFactorAuthenticationResponse,
    UserIdAndUserType,
)


class AppTokenAPI(BaseAPI):
    """App token API."""

    client_id: str | None = None

    def get_user_id_and_user_type(self) -> UserIdAndUserType:
        """Get user id and user type."""
        url: str = self.client.base_domain.format(stage="api") + "/v2/login/authorization/dialog"

        params: dict[str, Any] = {
            "response_type": "code",
            "client_id": self.client.config.client_id,
            "redirect_uri": self.client.config.redirect_uri,
        }

        logger.debug(f"Making authorization dialog request to: {url}")
        logger.debug(f"Request params: {params}")

        response = self._request(
            method="GET",
            url=url,
            params=params,
            allow_redirects=True,
        )

        if isinstance(response, Response):
            redirect_url = response.url  # Raw Response object
        else:
            if isinstance(response, ResponseBase):
                response_data = {"success": response.success, "data": response.data, "error": response.error}
                if not response.success or (response.data and isinstance(response.data, dict) and response.data.get("status") == "error"):
                    raise UpstoxError.from_response(response_data)
                else:
                    raise ValidationError(f"API returned JSON response instead of redirect. This suggests authentication failure or incorrect configuration. Response details: {response_data}")
            else:
                raise ValidationError(f"Unexpected response type: {type(response)}. Expected raw Response with redirect URL.")

        parsed_url = urlparse(redirect_url)

        params = parse_qs(parsed_url.query)

        # Extract required parameters with proper error handling
        user_id_list = params.get("user_id")
        client_id_list = params.get("client_id")
        user_type_list = params.get("user_type")

        if not user_id_list or not client_id_list or not user_type_list:
            raise ValidationError(f"Missing required parameters in redirect URL. Got params: {params}")

        payload = {
            "user_id": user_id_list[0],
            "client_id": client_id_list[0],
            "user_type": user_type_list[0],
        }

        self.client_id = client_id_list[0]

        return UserIdAndUserType.model_validate(payload)

    def generate_otp(self) -> OTPGenerationResponse:
        """Generate OTP."""
        url: str = self.client.base_domain.format(stage="service") + "/login/open/v6/auth/1fa/otp/generate"

        user_id_and_user_type: UserIdAndUserType = self.get_user_id_and_user_type()

        json_payload: dict[str, Any] = {
            "data": {
                "mobileNumber": self.client.config.username,
                "userId": user_id_and_user_type.user_id,
            }
        }

        response: OTPGenerationResponse = self._request(  # pyright: ignore[reportAssignmentType]
            method="POST",
            url=url,
            json=json_payload,
            model=OTPGenerationResponse,
        )

        return response

    def validate_otp(self) -> OTPValidationResponse:
        """Validate OTP."""
        otp_generation_response: OTPGenerationResponse = self.generate_otp()
        totp_secret: str = self.client.generate_totp_secret()
        url: str = self.client.base_domain.format(stage="service") + "/login/open/v4/auth/1fa/otp-totp/verify"

        if otp_generation_response.data is None:
            raise ValidationError("Failed to generate OTP - response data is None")

        json_payload: dict[str, Any] = {
            "data": {
                "otp": totp_secret,
                "validateOtpToken": otp_generation_response.data.validateOTPToken,
            }
        }

        response: OTPValidationResponse = self._request(  # pyright: ignore[reportAssignmentType]
            method="POST",
            url=url,
            json=json_payload,
            model=OTPValidationResponse,
        )

        return response

    def submit_pin(self) -> TwoFactorAuthenticationResponse:
        """Submit PIN for 2FA."""
        url: str = self.client.base_domain.format(stage="service") + "/login/open/v3/auth/2fa"

        _ = self.validate_otp()

        pin_encoded = base64.b64encode(self.client.config.pin_code.get_secret_value().encode()).decode()

        params: dict[str, Any] = {
            "client_id": self.client_id,
            "redirect_uri": self.client.config.redirect_uri_upstox,
        }

        json_payload: dict[str, Any] = {
            "data": {
                "twoFAMethod": "SECRET_PIN",
                "inputText": pin_encoded,
            }
        }

        response: TwoFactorAuthenticationResponse = self._request(  # pyright: ignore[reportAssignmentType]
            method="POST",
            url=url,
            params=params,
            json=json_payload,
            model=TwoFactorAuthenticationResponse,
            allow_redirects=True,
        )

        return response

    def oauth_authorization(self) -> OAuthAuthorizationResponse:
        """Two factor authentication."""

        _ = self.submit_pin()

        url: str = self.client.base_domain.format(stage="service") + "/login/v2/oauth/authorize"

        params: dict[str, Any] = {
            "client_id": self.client_id,
            "redirect_uri": self.client.config.redirect_uri_upstox,
            "requestId": self.client.generate_request_id(),
            "response_type": "code",
        }

        json_payload: dict[str, Any] = {
            "data": {
                "userOAuthApproval": True,
            }
        }

        response: OAuthAuthorizationResponse = self._request(  # pyright: ignore[reportAssignmentType]
            method="POST",
            url=url,
            params=params,
            json=json_payload,
            model=OAuthAuthorizationResponse,
            allow_redirects=True,
        )

        return response

    def get_access_token(self) -> AccessTokenResponse:
        """Get access token."""
        url: str = self.client.base_domain.format(stage="api") + "/v2/login/authorization/token"

        oauth_response: OAuthAuthorizationResponse = self.oauth_authorization()

        if oauth_response.data is None:
            raise ValidationError("OAuth response missing data")

        parsed = urlparse(oauth_response.data.redirectUri)
        params = parse_qs(parsed.query)

        code_list = params.get("code")
        if not code_list:
            raise ValidationError(f"Authorization code not found in redirect URI. Got params: {params}")

        code = code_list[0]

        data = f"code={code}&client_id={self.client.config.client_id}&client_secret={self.client.config.client_secret.get_secret_value()}&redirect_uri={self.client.config.redirect_uri}&grant_type=authorization_code"

        self.client.reset_session()

        headers: dict[str, str] = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
        }

        response: AccessTokenResponse = self._request(  # pyright: ignore[reportAssignmentType]
            method="POST",
            url=url,
            data=data,
            headers=headers,
            model=AccessTokenResponse,
        )

        return response
