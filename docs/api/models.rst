Data Models Reference
======================

This section documents all the data models and response types used in the Upstox TOTP SDK.

Response Models
---------------

AccessTokenResponse
~~~~~~~~~~~~~~~~~~~

.. autoclass:: upstox_totp.models.AccessTokenResponse
   :members:
   :undoc-members:
   :show-inheritance:

Response model for access token generation.

**Fields:**

- ``success`` (bool): Whether the request was successful
- ``data`` (AccessTokenData | None): Token data if successful
- ``error`` (dict | None): Error details if request failed

**Example:**

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   if response.success and response.data:
       print(f"Token: {response.data.access_token}")
       print(f"User: {response.data.user_name}")
   else:
       print(f"Error: {response.error}")

AccessTokenData
~~~~~~~~~~~~~~~

.. autoclass:: upstox_totp.models.AccessTokenData
   :members:
   :undoc-members:
   :show-inheritance:

Contains the actual access token data and user information.

**Key Fields:**

- ``access_token`` (str): The JWT access token for API calls
- ``user_id`` (str): Unique user identifier
- ``user_name`` (str): Display name of the user
- ``email`` (str): User's email address
- ``broker`` (str): Broker name (typically "UPSTOX")
- ``user_type`` (str): Account type (e.g., "individual")
- ``products`` (List[str]): Available product types
- ``exchanges`` (List[str]): Available exchanges
- ``is_active`` (bool): Whether the account is active

**Example:**

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   if response.success:
       data = response.data
       print(f"Access Token: {data.access_token}")
       print(f"User ID: {data.user_id}")
       print(f"User Name: {data.user_name}")
       print(f"Email: {data.email}")
       print(f"Products: {', '.join(data.products)}")
       print(f"Exchanges: {', '.join(data.exchanges)}")

OTPGenerationResponse
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: upstox_totp.models.OTPGenerationResponse
   :members:
   :undoc-members:
   :show-inheritance:

Response model for OTP generation during authentication flow.

OTPValidationResponse
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: upstox_totp.models.OTPValidationResponse
   :members:
   :undoc-members:
   :show-inheritance:

Response model for OTP validation.

OTPValidationData
~~~~~~~~~~~~~~~~~

.. autoclass:: upstox_totp.models.OTPValidationData
   :members:
   :undoc-members:
   :show-inheritance:

Contains OTP validation result data.

OTPValidationUserProfile
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: upstox_totp.models.OTPValidationUserProfile
   :members:
   :undoc-members:
   :show-inheritance:

User profile information returned during OTP validation.

TwoFactorAuthenticationData
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: upstox_totp.models.TwoFactorAuthenticationData
   :members:
   :undoc-members:
   :show-inheritance:

Two-factor authentication data model.

OAuthAuthorizationResponse
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: upstox_totp.models.OAuthAuthorizationResponse
   :members:
   :undoc-members:
   :show-inheritance:

OAuth authorization response model.

Base Models
-----------

ResponseBase
~~~~~~~~~~~~

.. autoclass:: upstox_totp.models.ResponseBase
   :members:
   :undoc-members:
   :show-inheritance:

Base response class that all API responses inherit from.

**Common Fields:**

- ``success`` (bool): Indicates if the request was successful
- ``data`` (T | None): Response data (varies by endpoint)
- ``error`` (dict | None): Error information if request failed

**Usage Pattern:**

.. code-block:: python

   # All responses follow this pattern
   response = api_method()

   if response.success:
       # Use response.data
       data = response.data
   else:
       # Handle response.error
       error = response.error

Model Validation
----------------

All models use Pydantic v2 for strict validation and type checking.

Validation Features
~~~~~~~~~~~~~~~~~~~

- **Strict mode**: No automatic type coercion
- **Field validation**: All fields are validated according to their types
- **Custom validators**: Special validation rules for specific fields
- **Error messages**: Clear, helpful error messages for validation failures

Example Validation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp.models import AccessTokenData
   from pydantic import ValidationError

   try:
       # This will fail validation
       data = AccessTokenData(
           access_token="",  # Empty string not allowed
           user_id=123,      # Should be string, not int
           # ... other fields
       )
   except ValidationError as e:
       print(f"Validation error: {e}")

Serialization
-------------

JSON Serialization
~~~~~~~~~~~~~~~~~~

All models support JSON serialization:

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   if response.success:
       # Serialize to JSON
       json_data = response.model_dump_json(indent=2)
       print(json_data)

       # Serialize to dict
       dict_data = response.model_dump()
       print(dict_data)

Custom Serialization
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   if response.success:
       # Exclude sensitive fields
       safe_data = response.model_dump(
           exclude={'access_token'},  # Don't include token
           exclude_none=True,         # Skip None values
           exclude_unset=True         # Skip unset values
       )
       print(safe_data)

Deserialization
---------------

From JSON
~~~~~~~~~

.. code-block:: python

   from upstox_totp.models import AccessTokenResponse
   import json

   # From JSON string
   json_str = '{"success": true, "data": {...}, "error": null}'
   response = AccessTokenResponse.model_validate_json(json_str)

   # From dict
   data_dict = json.loads(json_str)
   response = AccessTokenResponse.model_validate(data_dict)

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp.models import AccessTokenResponse
   from pydantic import ValidationError

   try:
       response = AccessTokenResponse.model_validate_json(invalid_json)
   except ValidationError as e:
       print(f"Failed to parse response: {e}")

Field Types
-----------

Common Field Types
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Type
     - Example
     - Description
   * - ``str``
     - ``"ABC123"``
     - String fields
   * - ``bool``
     - ``true``
     - Boolean flags
   * - ``int``
     - ``42``
     - Integer numbers
   * - ``List[str]``
     - ``["NSE", "BSE"]``
     - List of strings
   * - ``dict``
     - ``{"key": "value"}``
     - Dictionary objects
   * - ``datetime``
     - ``"2023-01-01T00:00:00Z"``
     - ISO datetime strings
   * - ``Optional[T]``
     - ``null`` or ``T``
     - Nullable fields

Custom Field Types
~~~~~~~~~~~~~~~~~~

The SDK defines several custom field types:

- **SecretStr**: For sensitive data that's masked in logs
- **EmailStr**: Validates email format
- **HttpUrl**: Validates URL format

.. code-block:: python

   from pydantic import SecretStr, EmailStr, HttpUrl

   # SecretStr usage
   password = SecretStr("secret")
   print(password)  # SecretStr('**********')
   print(password.get_secret_value())  # "secret"

Model Examples
--------------

Complete Access Token Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   if response.success and response.data:
       token_data = response.data
       
       print("=== Access Token Information ===")
       print(f"Token: {token_data.access_token[:20]}...")
       print(f"User ID: {token_data.user_id}")
       print(f"Name: {token_data.user_name}")
       print(f"Email: {token_data.email}")
       print(f"Broker: {token_data.broker}")
       print(f"Type: {token_data.user_type}")
       print(f"Active: {token_data.is_active}")
       
       print("\n=== Available Products ===")
       for product in token_data.products:
           print(f"- {product}")
       
       print("\n=== Available Exchanges ===")
       for exchange in token_data.exchanges:
           print(f"- {exchange}")

Error Response Example
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError

   upx = UpstoxTOTP()

   try:
       response = upx.app_token.get_access_token()
   except UpstoxError as e:
       print("=== Error Response ===")
       print(f"Error: {e}")
       
       # Access underlying response if available
       if hasattr(e, 'response'):
           error_response = e.response
           if hasattr(error_response, 'error') and error_response.error:
               print(f"Error Code: {error_response.error.get('code')}")
               print(f"Error Message: {error_response.error.get('message')}")

Working with Raw Responses
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   import requests

   upx = UpstoxTOTP()

   # Get token
   response = upx.app_token.get_access_token()
   token = response.data.access_token

   # Use token for raw API calls
   headers = {'Authorization': f'Bearer {token}'}
   raw_response = requests.get(
       'https://api.upstox.com/v2/user/profile',
       headers=headers
   )

   # Parse response manually
   if raw_response.status_code == 200:
       profile_data = raw_response.json()
       print(f"Raw API response: {profile_data}")

Model Inheritance
-----------------

Response Hierarchy
~~~~~~~~~~~~~~~~~~

All response models inherit from ``ResponseBase``:

.. code-block:: text

   ResponseBase
   ├── AccessTokenResponse
   ├── OTPGenerationResponse
   ├── OTPValidationResponse
   └── OAuthAuthorizationResponse

Custom Response Models
~~~~~~~~~~~~~~~~~~~~~~

You can create custom response models:

.. code-block:: python

   from upstox_totp.models import ResponseBase
   from pydantic import BaseModel
   from typing import Optional

   class CustomData(BaseModel):
       message: str
       timestamp: str

   class CustomResponse(ResponseBase[CustomData]):
       pass

   # Usage
   response = CustomResponse(
       success=True,
       data=CustomData(message="Hello", timestamp="2023-01-01"),
       error=None
   )

Best Practices
--------------

1. **Always check success flag** before accessing data
2. **Handle validation errors** when creating models manually
3. **Use type hints** for better IDE support
4. **Serialize safely** by excluding sensitive fields
5. **Validate input data** before creating models
6. **Use model methods** for serialization/deserialization
7. **Handle None values** appropriately
8. **Log errors** for debugging purposes

Performance Considerations
--------------------------

Model Creation
~~~~~~~~~~~~~~

.. code-block:: python

   # Efficient - direct model creation
   response = AccessTokenResponse(success=True, data=data, error=None)

   # Less efficient - JSON parsing
   response = AccessTokenResponse.model_validate_json(json_string)

Memory Usage
~~~~~~~~~~~~

.. code-block:: python

   # Clear large objects when done
   response = upx.app_token.get_access_token()
   token = response.data.access_token
   
   # Clear response to free memory
   del response

Caching Models
~~~~~~~~~~~~~~

.. code-block:: python

   from functools import lru_cache

   @lru_cache(maxsize=100)
   def parse_response(json_data: str) -> AccessTokenResponse:
       return AccessTokenResponse.model_validate_json(json_data)

See Also
--------

- :doc:`client` - Client API reference
- :doc:`errors` - Error handling
- :doc:`../configuration` - Configuration guide
- :doc:`../examples/basic_usage` - Usage examples
