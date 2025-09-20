"""Base API class for all endpoints."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, TypeVar

from curl_cffi.requests.models import Response
from curl_cffi.requests.utils import HttpMethod
from pydantic import BaseModel

from upstox_totp.errors import UpstoxError
from upstox_totp.logging import logger
from upstox_totp.models import ResponseBase

if TYPE_CHECKING:
    from typing import Any

    from upstox_totp.client import UpstoxTOTP

T = TypeVar("T", bound=BaseModel)


class BaseAPI:
    """Base class for API endpoints."""

    def __init__(self, client: UpstoxTOTP) -> None:
        """Initialize the base API."""
        self.client = client
        self.config = client.config
        self.session = client.session

    def _request(
        self,
        method: HttpMethod,
        url: str,
        model: type[T] | None = None,
        params: dict[str, Any] | None = None,
        data: str | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        allow_redirects: bool = False,
    ) -> T | dict[str, Any] | Response | Any:
        """Make a request to the API."""

        logger.debug(f"Making API request to {url}")
        logger.debug(f"Method: {method}")
        logger.debug(f"Params: {params}")
        logger.debug(f"Data: {data}")
        logger.debug(f"Json: {json}")

        response: Response = self.session.request(  # pyright: ignore[reportUnknownMemberType]
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            allow_redirects=allow_redirects,
            headers=headers,
        )

        time.sleep(self.config.sleep_time / 1000)

        # response.raise_for_status()

        logger.debug(f"Response status: {response.status_code}")

        if response.headers.get("Content-Type") == "application/json":
            response_data: dict[str, Any] = response.json()  # pyright: ignore[reportUnknownMemberType]

            if "success" not in response_data:
                response_data = {
                    "success": True,
                    "data": response_data,
                }

            upstox_respone = ResponseBase.model_validate(response_data)

            # Check for explicit failure
            if not upstox_respone.success:
                raise UpstoxError.from_response(response_data)  # pyright: ignore[reportUnknownArgumentType]

            if upstox_respone.data and isinstance(upstox_respone.data, dict) and upstox_respone.data.get("status") == "error":
                raise UpstoxError.from_response(response_data)

            if model:
                return model.model_validate(upstox_respone.model_dump())  # pyright: ignore[reportUnknownMemberType]

            return upstox_respone  # pyright: ignore[reportReturnType]

        return response
