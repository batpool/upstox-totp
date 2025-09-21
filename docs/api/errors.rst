Error Handling Reference
========================

This section documents all the exception classes and error handling patterns in the Upstox TOTP SDK.

Exception Hierarchy
-------------------

.. code-block:: text

   BaseException
   └── Exception
       └── UpstoxError (base for all SDK errors)
           ├── ConfigurationError
           ├── ValidationError
           ├── AuthenticationError
           ├── NetworkError
           └── APIError

Core Exceptions
---------------

UpstoxError
~~~~~~~~~~~

.. autoclass:: upstox_totp.errors.UpstoxError
   :members:
   :undoc-members:
   :show-inheritance:

Base exception class for all Upstox TOTP SDK errors.

**Attributes:**

- ``message`` (str): Human-readable error message
- ``details`` (dict, optional): Additional error details
- ``suggestions`` (list, optional): Troubleshooting suggestions

**Example:**

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError

   try:
       upx = UpstoxTOTP()
       response = upx.app_token.get_access_token()
   except UpstoxError as e:
       print(f"Error: {e}")
       print(f"Details: {e.details}")
       print(f"Suggestions: {e.suggestions}")

ConfigurationError
~~~~~~~~~~~~~~~~~~

.. autoclass:: upstox_totp.errors.ConfigurationError
   :members:
   :undoc-members:
   :show-inheritance:

Raised when there are issues with configuration setup.

**Common Causes:**

- Missing environment variables
- Invalid credential format
- Malformed configuration values
- File permission issues

**Example:**

.. code-block:: python

   from upstox_totp import UpstoxTOTP, ConfigurationError

   try:
       # Missing required environment variables
       upx = UpstoxTOTP()
   except ConfigurationError as e:
       print(f"Configuration error: {e}")
       
       # Check what's missing
       if "UPSTOX_USERNAME" in str(e):
           print("Please set UPSTOX_USERNAME environment variable")

ValidationError
~~~~~~~~~~~~~~~

.. autoclass:: upstox_totp.errors.ValidationError
   :members:
   :undoc-members:
   :show-inheritance:

Raised when input validation fails.

**Common Causes:**

- Invalid username format (not 10 digits)
- Invalid PIN code format
- Invalid TOTP secret format
- Invalid URL format for redirect_uri

**Example:**

.. code-block:: python

   from upstox_totp import UpstoxTOTP, ValidationError
   from pydantic import SecretStr

   try:
       upx = UpstoxTOTP(
           username="invalid",  # Should be 10 digits
           password=SecretStr("password"),
           # ... other fields
       )
   except ValidationError as e:
       print(f"Validation error: {e}")

Error Handling Patterns
-----------------------

Basic Error Handling
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError

   def safe_get_token():
       try:
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           
           if response.success:
               return response.data.access_token
           else:
               print(f"API returned error: {response.error}")
               return None
               
       except UpstoxError as e:
           print(f"SDK error: {e}")
           return None
       except Exception as e:
           print(f"Unexpected error: {e}")
           return None

   token = safe_get_token()
   if token:
       print("Token generated successfully")

Specific Error Handling
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import (
       UpstoxTOTP, 
       ConfigurationError, 
       ValidationError, 
       UpstoxError
   )

   def handle_specific_errors():
       try:
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           return response
           
       except ConfigurationError as e:
           print("Configuration Issue:")
           print(f"  Error: {e}")
           print("  Solutions:")
           print("  - Check your .env file")
           print("  - Verify environment variables")
           print("  - Run: upstox_cli check-env")
           
       except ValidationError as e:
           print("Validation Issue:")
           print(f"  Error: {e}")
           print("  Solutions:")
           print("  - Check credential formats")
           print("  - Verify TOTP secret")
           print("  - Ensure username is 10 digits")
           
       except UpstoxError as e:
           print("Upstox API Issue:")
           print(f"  Error: {e}")
           if e.suggestions:
               print("  Suggestions:")
               for suggestion in e.suggestions:
                   print(f"  - {suggestion}")

Retry Logic with Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from upstox_totp import UpstoxTOTP, UpstoxError

   def get_token_with_retry(max_retries=3, delay=5):
       """Get token with retry logic for different error types."""
       
       for attempt in range(1, max_retries + 1):
           try:
               upx = UpstoxTOTP()
               response = upx.app_token.get_access_token()
               
               if response.success:
                   return response.data.access_token
               else:
                   error = response.error
                   print(f"Attempt {attempt}: API error - {error}")
                   
                   # Don't retry for certain errors
                   if error and "invalid_credentials" in str(error):
                       print("Invalid credentials - not retrying")
                       break
                       
           except ConfigurationError:
               print("Configuration error - not retrying")
               break  # Don't retry configuration errors
               
           except ValidationError:
               print("Validation error - not retrying")  
               break  # Don't retry validation errors
               
           except UpstoxError as e:
               print(f"Attempt {attempt}: Upstox error - {e}")
               # Retry for network/temporary errors
               
           except Exception as e:
               print(f"Attempt {attempt}: Unexpected error - {e}")
               
           if attempt < max_retries:
               print(f"Retrying in {delay} seconds...")
               time.sleep(delay)
       
       raise Exception(f"Failed to get token after {max_retries} attempts")

Error Context and Details
-------------------------

Error Messages
~~~~~~~~~~~~~~

The SDK provides detailed error messages with context:

.. code-block:: python

   from upstox_totp import UpstoxTOTP, ConfigurationError

   try:
       upx = UpstoxTOTP()
   except ConfigurationError as e:
       # Error messages include specific missing variables
       print(e)  # "Missing required environment variables: UPSTOX_USERNAME, UPSTOX_PASSWORD"

Error Details
~~~~~~~~~~~~~

Many errors include additional details:

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError

   try:
       upx = UpstoxTOTP()
       response = upx.app_token.get_access_token()
   except UpstoxError as e:
       if e.details:
           print("Error details:")
           for key, value in e.details.items():
               print(f"  {key}: {value}")

Troubleshooting Suggestions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Errors often include helpful suggestions:

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError

   try:
       upx = UpstoxTOTP()
       response = upx.app_token.get_access_token()
   except UpstoxError as e:
       print(f"Error: {e}")
       
       if e.suggestions:
           print("\nTroubleshooting suggestions:")
           for i, suggestion in enumerate(e.suggestions, 1):
               print(f"{i}. {suggestion}")

Common Error Scenarios
----------------------

Missing Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Error: ConfigurationError
   # Message: Missing required environment variables: UPSTOX_USERNAME
   # Solution: Set the missing environment variable

   import os
   os.environ['UPSTOX_USERNAME'] = '9876543210'

Invalid Username Format
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Error: ValidationError  
   # Message: Username must be exactly 10 digits
   # Solution: Use your 10-digit mobile number

   from upstox_totp import UpstoxTOTP
   from pydantic import SecretStr

   upx = UpstoxTOTP(
       username="9876543210",  # Must be 10 digits
       password=SecretStr("password"),
       # ... other fields
   )

Invalid TOTP Secret
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Error: ValidationError
   # Message: Invalid TOTP secret format
   # Solution: Ensure secret is base32 encoded, no spaces

   # Wrong: "JBSW Y3DP EHPK 3PXP"
   # Right: "JBSWY3DPEHPK3PXP"

Network Connection Issues
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   from upstox_totp import UpstoxTOTP, UpstoxError

   try:
       upx = UpstoxTOTP()
       response = upx.app_token.get_access_token()
   except requests.ConnectionError:
       print("Network connection error")
       print("Check your internet connection")
   except requests.Timeout:
       print("Request timeout")
       print("Try again or increase timeout")

Authentication Failures
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   if not response.success:
       error = response.error
       
       if "invalid_credentials" in str(error):
           print("Invalid username/password")
       elif "invalid_totp" in str(error):
           print("Invalid TOTP code")
           print("Check your TOTP secret configuration")
       elif "invalid_pin" in str(error):
           print("Invalid PIN code")

Client ID / OAuth Issues
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   if not response.success:
       error = response.error
       
       if "invalid_client" in str(error):
           print("Invalid client ID or secret")
           print("Check your Upstox Developer App credentials")
       elif "redirect_uri_mismatch" in str(error):
           print("Redirect URI mismatch")
           print("Ensure redirect_uri matches your app settings")

Custom Error Handling
---------------------

Custom Exception Classes
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp.errors import UpstoxError

   class TokenExpiredError(UpstoxError):
       """Raised when access token has expired."""
       pass

   class RateLimitError(UpstoxError):
       """Raised when rate limit is exceeded."""
       pass

   def enhanced_get_token():
       upx = UpstoxTOTP()
       response = upx.app_token.get_access_token()
       
       if not response.success:
           error = response.error
           
           if "token_expired" in str(error):
               raise TokenExpiredError("Access token has expired")
           elif "rate_limit" in str(error):
               raise RateLimitError("Rate limit exceeded")
           else:
               raise UpstoxError(f"Token generation failed: {error}")
       
       return response.data.access_token

Error Logging
~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP, UpstoxError

   # Configure logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(levelname)s - %(message)s'
   )
   logger = logging.getLogger(__name__)

   def logged_token_generation():
       try:
           logger.info("Starting token generation...")
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           
           if response.success:
               logger.info("Token generated successfully")
               return response.data.access_token
           else:
               logger.error(f"Token generation failed: {response.error}")
               return None
               
       except UpstoxError as e:
           logger.error(f"Upstox error: {e}", exc_info=True)
           return None
       except Exception as e:
           logger.error(f"Unexpected error: {e}", exc_info=True)
           return None

Error Recovery Strategies
-------------------------

Automatic Retry
~~~~~~~~~~~~~~~

.. code-block:: python

   from functools import wraps
   import time

   def retry_on_error(max_retries=3, delay=1, backoff=2):
       def decorator(func):
           @wraps(func)
           def wrapper(*args, **kwargs):
               retries = 0
               current_delay = delay
               
               while retries < max_retries:
                   try:
                       return func(*args, **kwargs)
                   except (ConnectionError, TimeoutError) as e:
                       retries += 1
                       if retries >= max_retries:
                           raise e
                       
                       time.sleep(current_delay)
                       current_delay *= backoff
                       
               return func(*args, **kwargs)
           return wrapper
       return decorator

   @retry_on_error(max_retries=3, delay=2)
   def resilient_token_generation():
       upx = UpstoxTOTP()
       response = upx.app_token.get_access_token()
       
       if not response.success:
           raise Exception(f"Token generation failed: {response.error}")
       
       return response.data.access_token

Fallback Mechanisms
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError

   def get_token_with_fallback():
       """Try multiple strategies to get a token."""
       
       # Strategy 1: Normal generation
       try:
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           if response.success:
               return response.data.access_token
       except Exception as e:
           print(f"Strategy 1 failed: {e}")
       
       # Strategy 2: Reset session and retry
       try:
           upx.reset_session()
           response = upx.app_token.get_access_token()
           if response.success:
               return response.data.access_token
       except Exception as e:
           print(f"Strategy 2 failed: {e}")
       
       # Strategy 3: New client instance
       try:
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           if response.success:
               return response.data.access_token
       except Exception as e:
           print(f"Strategy 3 failed: {e}")
       
       raise Exception("All token generation strategies failed")

Debugging Errors
----------------

Enable Debug Mode
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Enable debug logging
   upx = UpstoxTOTP(debug=True)

   # Or via environment variable
   import os
   os.environ['UPSTOX_DEBUG'] = 'true'
   upx = UpstoxTOTP()

Capture Request/Response
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP

   # Enable HTTP debugging
   logging.basicConfig(level=logging.DEBUG)
   logging.getLogger("urllib3").setLevel(logging.DEBUG)

   upx = UpstoxTOTP(debug=True)

Inspect Session State
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()

   # Inspect session
   print(f"Session cookies: {dict(upx.session.cookies)}")
   print(f"Session headers: {dict(upx.session.headers)}")

   try:
       response = upx.app_token.get_access_token()
   except Exception as e:
       print(f"Error occurred: {e}")
       print(f"Session state: {dict(upx.session.cookies)}")

Testing Error Conditions
------------------------

Mock Errors for Testing
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from unittest.mock import patch
   from upstox_totp import UpstoxTOTP, UpstoxError

   def test_configuration_error():
       with patch.dict('os.environ', {}, clear=True):
           with pytest.raises(ConfigurationError):
               UpstoxTOTP()

   def test_network_error():
       with patch('requests.Session.post') as mock_post:
           mock_post.side_effect = ConnectionError("Network error")
           
           upx = UpstoxTOTP()
           with pytest.raises(ConnectionError):
               upx.app_token.get_access_token()

Error Monitoring
----------------

Health Checks
~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP, ConfigurationError

   def health_check():
       """Check if the SDK is properly configured."""
       try:
           upx = UpstoxTOTP()
           return {"status": "healthy", "configuration": "valid"}
       except ConfigurationError as e:
           return {"status": "unhealthy", "error": str(e)}
       except Exception as e:
           return {"status": "error", "error": str(e)}

Metrics Collection
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   from collections import defaultdict
   from upstox_totp import UpstoxTOTP, UpstoxError

   class ErrorMetrics:
       def __init__(self):
           self.error_counts = defaultdict(int)
           self.last_errors = []
           
       def record_error(self, error):
           error_type = type(error).__name__
           self.error_counts[error_type] += 1
           self.last_errors.append({
               'type': error_type,
               'message': str(error),
               'timestamp': time.time()
           })
           
           # Keep only last 100 errors
           if len(self.last_errors) > 100:
               self.last_errors.pop(0)
       
       def get_summary(self):
           return {
               'error_counts': dict(self.error_counts),
               'last_errors': self.last_errors[-10:]  # Last 10 errors
           }

   metrics = ErrorMetrics()

   def monitored_token_generation():
       try:
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           return response
       except Exception as e:
           metrics.record_error(e)
           raise

Best Practices
--------------

1. **Always handle specific exception types** before generic ones
2. **Provide meaningful error messages** to users
3. **Log errors with sufficient context** for debugging
4. **Don't retry configuration/validation errors** - fix them instead
5. **Use exponential backoff** for retries
6. **Monitor error rates** in production
7. **Test error conditions** thoroughly
8. **Document expected errors** for API users
9. **Clean up resources** even when errors occur
10. **Validate input early** to provide better error messages

See Also
--------

- :doc:`client` - Client API reference
- :doc:`models` - Data models
- :doc:`../troubleshooting` - Troubleshooting guide
- :doc:`../configuration` - Configuration guide
