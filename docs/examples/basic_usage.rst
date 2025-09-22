Basic Usage Examples
====================

This section provides comprehensive examples for common use cases of the Upstox TOTP SDK.

Getting Started
---------------

Simple Token Generation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Initialize client (loads from environment or .env file)
   upx = UpstoxTOTP()

   # Generate access token
   response = upx.app_token.get_access_token()

   if response.success and response.data:
       print(f"✅ Token: {response.data.access_token}")
       print(f"👤 User: {response.data.user_name}")
       print(f"📧 Email: {response.data.email}")
   else:
       print(f"❌ Error: {response.error}")

With Error Handling
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError, ConfigurationError

   def get_upstox_token():
       """Get Upstox access token with proper error handling."""
       try:
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           
           if response.success and response.data:
               return response.data.access_token
           else:
               print(f"API Error: {response.error}")
               return None
               
       except ConfigurationError as e:
           print(f"Configuration Error: {e}")
           print("💡 Check your .env file or environment variables")
           return None
           
       except UpstoxError as e:
           print(f"Upstox Error: {e}")
           return None
           
       except Exception as e:
           print(f"Unexpected Error: {e}")
           return None

   # Usage
   token = get_upstox_token()
   if token:
       print(f"Success! Token: {token[:20]}...")
   else:
       print("Failed to get token")

Configuration Examples
----------------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from upstox_totp import UpstoxTOTP

   # Set environment variables programmatically
   os.environ['UPSTOX_USERNAME'] = '9876543210'
   os.environ['UPSTOX_PASSWORD'] = 'your-password'
   os.environ['UPSTOX_PIN_CODE'] = '1234'
   os.environ['UPSTOX_TOTP_SECRET'] = 'JBSWY3DPEHPK3PXP'
   os.environ['UPSTOX_CLIENT_ID'] = 'your-client-id'
   os.environ['UPSTOX_CLIENT_SECRET'] = 'your-client-secret'
   os.environ['UPSTOX_REDIRECT_URI'] = 'https://your-app.com/callback'

   # Initialize client
   upx = UpstoxTOTP()

Manual Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   from pydantic import SecretStr

   # Manual configuration (not recommended for production)
   upx = UpstoxTOTP(
       username="9876543210",
       password=SecretStr("your-password"),
       pin_code=SecretStr("1234"),
       totp_secret=SecretStr("JBSWY3DPEHPK3PXP"),
       client_id="your-client-id",
       client_secret=SecretStr("your-client-secret"),
       redirect_uri="https://your-app.com/callback",
       debug=True,
       sleep_time=1000
   )

   response = upx.app_token.get_access_token()

Multiple Environment Files
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Development environment
   upx_dev = UpstoxTOTP.from_env_file(".env.development")

   # Production environment  
   upx_prod = UpstoxTOTP.from_env_file(".env.production")

   # Staging environment
   upx_staging = UpstoxTOTP.from_env_file(".env.staging")

   # Generate tokens for different environments
   environments = {
       'dev': upx_dev,
       'prod': upx_prod,
       'staging': upx_staging
   }

   for env_name, client in environments.items():
       try:
           response = client.app_token.get_access_token()
           if response.success:
               print(f"✅ {env_name}: Token generated")
           else:
               print(f"❌ {env_name}: {response.error}")
       except Exception as e:
           print(f"❌ {env_name}: {e}")

Context Manager Examples
------------------------

Basic Context Manager
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Automatic cleanup with context manager
   with UpstoxTOTP() as upx:
       response = upx.app_token.get_access_token()
       
       if response.success:
           token = response.data.access_token
           print(f"Token: {token}")
           
           # Use token for API calls
           # Session is automatically cleaned up when exiting

Multiple Operations
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   def perform_upstox_operations():
       """Perform multiple operations with single client."""
       with UpstoxTOTP() as upx:
           # Generate token
           response = upx.app_token.get_access_token()
           
           if not response.success:
               raise Exception(f"Token generation failed: {response.error}")
           
           token = response.data.access_token
           
           # Generate TOTP for verification
           totp_code = upx.generate_totp_secret()
           
           # Reset session if needed
           upx.reset_session()
           
           # Generate new request ID
           request_id = upx.generate_request_id()
           
           return {
               'token': token,
               'totp': totp_code,
               'request_id': request_id
           }

   # Usage
   try:
       result = perform_upstox_operations()
       print(f"Operations completed: {result}")
   except Exception as e:
       print(f"Operations failed: {e}")

Custom Context Manager
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from contextlib import contextmanager
   from upstox_totp import UpstoxTOTP
   import logging

   @contextmanager
   def upstox_client_with_logging(log_level=logging.INFO):
       """Custom context manager with logging."""
       
       # Setup logging
       logging.basicConfig(level=log_level)
       logger = logging.getLogger(__name__)
       
       logger.info("🚀 Initializing Upstox client...")
       
       try:
           upx = UpstoxTOTP(debug=True)
           logger.info("✅ Upstox client initialized")
           yield upx
           
       except Exception as e:
           logger.error(f"❌ Error with Upstox client: {e}")
           raise
           
       finally:
           logger.info("🧹 Cleaning up Upstox client...")

   # Usage
   with upstox_client_with_logging(logging.DEBUG) as upx:
       response = upx.app_token.get_access_token()

Working with Responses
----------------------

Response Inspection
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   # Check response structure
   print(f"Success: {response.success}")
   print(f"Data type: {type(response.data)}")
   print(f"Error: {response.error}")

   if response.success and response.data:
       data = response.data
       
       # Access all available fields
       print(f"Access Token: {data.access_token}")
       print(f"User ID: {data.user_id}")
       print(f"User Name: {data.user_name}")
       print(f"Email: {data.email}")
       print(f"Broker: {data.broker}")
       print(f"User Type: {data.user_type}")
       print(f"Is Active: {data.is_active}")
       
       # Lists
       print(f"Products: {data.products}")
       print(f"Exchanges: {data.exchanges}")
       
       # Additional fields (if available)
       if hasattr(data, 'order_types'):
           print(f"Order Types: {data.order_types}")

Response Serialization
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   import json

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   if response.success:
       # Serialize to JSON
       json_data = response.model_dump_json(indent=2)
       print("Full Response:")
       print(json_data)
       
       # Serialize to dict
       dict_data = response.model_dump()
       
       # Save to file
       with open('upstox_response.json', 'w') as f:
           json.dump(dict_data, f, indent=2)
       
       # Exclude sensitive data
       safe_data = response.model_dump(
           exclude={'data': {'access_token'}},
           exclude_none=True
       )
       print("Safe Response (no token):")
       print(json.dumps(safe_data, indent=2))

Response Validation
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   def validate_token_response(response):
       """Validate that response contains expected data."""
       
       if not response.success:
           return False, f"Request failed: {response.error}"
       
       if not response.data:
           return False, "No data in response"
       
       data = response.data
       
       # Check required fields
       required_fields = ['access_token', 'user_id', 'user_name', 'email']
       for field in required_fields:
           if not getattr(data, field, None):
               return False, f"Missing required field: {field}"
       
       # Validate token format (basic check)
       if not data.access_token.startswith('eyJ'):
           return False, "Invalid token format (not JWT)"
       
       # Check token length
       if len(data.access_token) < 100:
           return False, "Token seems too short"
       
       return True, "Response is valid"

   # Usage
   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   is_valid, message = validate_token_response(response)
   if is_valid:
       print("✅ Response validation passed")
       token = response.data.access_token
   else:
       print(f"❌ Response validation failed: {message}")

API Integration Examples
------------------------

Basic API Call
~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   from upstox_totp import UpstoxTOTP

   def make_upstox_api_call(endpoint, token):
       """Make authenticated API call to Upstox."""
       headers = {
           'Authorization': f'Bearer {token}',
           'Content-Type': 'application/json'
       }
       
       response = requests.get(f'https://api.upstox.com/v2{endpoint}', headers=headers)
       response.raise_for_status()
       return response.json()

   # Get token
   upx = UpstoxTOTP()
   token_response = upx.app_token.get_access_token()

   if token_response.success:
       token = token_response.data.access_token
       
       try:
           # Get user profile
           profile = make_upstox_api_call('/user/profile', token)
           print(f"User Profile: {profile}")
           
           # Get positions
           positions = make_upstox_api_call('/portfolio/long-term-positions', token)
           print(f"Positions: {positions}")
           
       except requests.RequestException as e:
           print(f"API call failed: {e}")

Complete Trading Example
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   from upstox_totp import UpstoxTOTP

   class UpstoxAPIClient:
       def __init__(self):
           self.token = None
           self.base_url = 'https://api.upstox.com/v2'
           
       def authenticate(self):
           """Authenticate and get access token."""
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           
           if response.success and response.data:
               self.token = response.data.access_token
               return True
           else:
               print(f"Authentication failed: {response.error}")
               return False
       
       def _make_request(self, method, endpoint, **kwargs):
           """Make authenticated request."""
           if not self.token:
               raise Exception("Not authenticated. Call authenticate() first.")
           
           headers = {
               'Authorization': f'Bearer {self.token}',
               'Content-Type': 'application/json'
           }
           
           url = f'{self.base_url}{endpoint}'
           response = requests.request(method, url, headers=headers, **kwargs)
           response.raise_for_status()
           return response.json()
       
       def get_profile(self):
           """Get user profile."""
           return self._make_request('GET', '/user/profile')
       
       def get_holdings(self):
           """Get holdings."""
           return self._make_request('GET', '/portfolio/long-term-holdings')
       
       def get_positions(self):
           """Get positions."""
           return self._make_request('GET', '/portfolio/short-term-positions')
       
       def get_funds(self):
           """Get fund information."""
           return self._make_request('GET', '/user/get-funds-and-margin')

   # Usage
   def main():
       client = UpstoxAPIClient()
       
       # Authenticate
       if not client.authenticate():
           print("Failed to authenticate")
           return
       
       try:
           # Get user data
           profile = client.get_profile()
           print(f"User: {profile['data']['user_name']}")
           
           # Get portfolio data
           holdings = client.get_holdings()
           print(f"Holdings count: {len(holdings['data'])}")
           
           positions = client.get_positions()
           print(f"Positions count: {len(positions['data'])}")
           
           funds = client.get_funds()
           print(f"Available margin: {funds['data']['equity']['available_margin']}")
           
       except Exception as e:
           print(f"Error: {e}")

   if __name__ == "__main__":
       main()

Session Management Examples
---------------------------

Session Reuse
~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Create client once
   upx = UpstoxTOTP()

   # Generate multiple tokens (reuses session)
   tokens = []
   for i in range(3):
       print(f"Generating token {i+1}...")
       response = upx.app_token.get_access_token()
       
       if response.success:
           tokens.append(response.data.access_token)
           print(f"✅ Token {i+1} generated")
       else:
           print(f"❌ Token {i+1} failed: {response.error}")

   print(f"Generated {len(tokens)} tokens")

Session Reset
~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()

   # First token generation
   response1 = upx.app_token.get_access_token()
   print(f"First token: {response1.success}")

   # Reset session (clears cookies, etc.)
   upx.reset_session()

   # Second token generation with fresh session
   response2 = upx.app_token.get_access_token()
   print(f"Second token: {response2.success}")

Custom Session Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   from requests.adapters import HTTPAdapter
   from urllib3.util.retry import Retry

   upx = UpstoxTOTP()

   # Configure session with retries
   retry_strategy = Retry(
       total=3,
       backoff_factor=1,
       status_forcelist=[429, 500, 502, 503, 504]
   )

   adapter = HTTPAdapter(max_retries=retry_strategy)
   upx.session.mount("http://", adapter)
   upx.session.mount("https://", adapter)

   # Set custom timeout
   upx.session.timeout = (10, 30)  # (connect, read)

   # Add custom headers
   upx.session.headers.update({
       'User-Agent': 'MyTradingApp/2.0',
       'Accept-Language': 'en-US'
   })

   # Generate token with configured session
   response = upx.app_token.get_access_token()

TOTP Examples
-------------

Manual TOTP Generation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   import time

   upx = UpstoxTOTP()

   # Generate current TOTP
   current_totp = upx.generate_totp_secret()
   print(f"Current TOTP: {current_totp}")

   # Wait for next TOTP window
   print("Waiting for next TOTP...")
   time.sleep(30)

   next_totp = upx.generate_totp_secret()
   print(f"Next TOTP: {next_totp}")

TOTP Validation
~~~~~~~~~~~~~~~

.. code-block:: python

   import pyotp
   from upstox_totp import UpstoxTOTP

   def validate_totp_setup(expected_code=None):
       """Validate TOTP setup by comparing with expected code."""
       upx = UpstoxTOTP()
       
       # Generate TOTP using our secret
       generated_code = upx.generate_totp_secret()
       print(f"Generated TOTP: {generated_code}")
       
       if expected_code:
           if generated_code == expected_code:
               print("✅ TOTP validation successful")
               return True
           else:
               print("❌ TOTP validation failed")
               print(f"Expected: {expected_code}, Got: {generated_code}")
               return False
       
       # Manual verification
       user_code = input("Enter TOTP from your authenticator app: ")
       if generated_code == user_code:
           print("✅ TOTP setup is correct")
           return True
       else:
           print("❌ TOTP codes don't match")
           return False

   # Usage
   validate_totp_setup()

TOTP Secret Verification
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pyotp
   from upstox_totp import UpstoxTOTP

   def verify_totp_secret():
       """Verify TOTP secret is working correctly."""
       upx = UpstoxTOTP()
       
       # Get the secret
       secret = upx.totp_secret.get_secret_value()
       print(f"TOTP Secret: {secret}")
       
       # Create TOTP object manually
       totp = pyotp.TOTP(secret)
       
       # Generate codes using both methods
       sdk_code = upx.generate_totp_secret()
       manual_code = totp.now()
       
       print(f"SDK generated: {sdk_code}")
       print(f"Manual generated: {manual_code}")
       
       if sdk_code == manual_code:
           print("✅ TOTP secret is working correctly")
           return True
       else:
           print("❌ TOTP secret verification failed")
           return False

   # Usage
   verify_totp_secret()

Debugging Examples
------------------

Enable Debug Mode
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   import logging

   # Enable debug logging
   logging.basicConfig(level=logging.DEBUG)

   # Create client with debug mode
   upx = UpstoxTOTP(debug=True)

   # Generate token with debug output
   response = upx.app_token.get_access_token()

Request/Response Logging
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   import logging

   # Configure detailed logging
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )

   # Enable urllib3 debugging for HTTP details
   logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)

   upx = UpstoxTOTP(debug=True)

   # This will show detailed HTTP request/response information
   response = upx.app_token.get_access_token()

Session State Inspection
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   def inspect_session_state(upx):
       """Inspect current session state."""
       session = upx.session
       
       print("=== Session State ===")
       print(f"Cookies: {dict(session.cookies)}")
       print(f"Headers: {dict(session.headers)}")
       print(f"Timeout: {session.timeout}")
       
       # Check adapters
       for prefix, adapter in session.adapters.items():
           print(f"Adapter {prefix}: {type(adapter).__name__}")

   upx = UpstoxTOTP()

   print("Initial session state:")
   inspect_session_state(upx)

   # Generate token
   response = upx.app_token.get_access_token()

   print("\nSession state after token generation:")
   inspect_session_state(upx)

Error Debugging
~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError
   import traceback

   def debug_token_generation():
       """Debug token generation with detailed error information."""
       try:
           upx = UpstoxTOTP(debug=True)
           
           print("🔍 Starting debug token generation...")
           print(f"Username: {upx.username}")
           print(f"Client ID: {upx.client_id}")
           print(f"Redirect URI: {upx.redirect_uri}")
           
           # Generate TOTP first
           totp = upx.generate_totp_secret()
           print(f"Generated TOTP: {totp}")
           
           # Attempt token generation
           response = upx.app_token.get_access_token()
           
           if response.success:
               print("✅ Token generation successful")
               return response.data.access_token
           else:
               print(f"❌ Token generation failed: {response.error}")
               return None
               
       except Exception as e:
           print(f"❌ Exception during token generation: {e}")
           print("Full traceback:")
           traceback.print_exc()
           return None

   # Usage
   token = debug_token_generation()

Utility Functions
-----------------

Token Validation
~~~~~~~~~~~~~~~~

.. code-block:: python

   import jwt
   from datetime import datetime

   def validate_jwt_token(token):
       """Validate JWT token structure (without signature verification)."""
       try:
           # Decode without verification to inspect claims
           decoded = jwt.decode(token, options={"verify_signature": False})
           
           print("=== Token Claims ===")
           for key, value in decoded.items():
               if key == 'exp':
                   # Convert timestamp to readable date
                   exp_date = datetime.fromtimestamp(value)
                   print(f"{key}: {value} ({exp_date})")
               else:
                   print(f"{key}: {value}")
           
           # Check expiry
           if 'exp' in decoded:
               exp_time = datetime.fromtimestamp(decoded['exp'])
               if exp_time > datetime.now():
                   print("✅ Token is not expired")
               else:
                   print("⚠️ Token is expired")
           
           return True
           
       except jwt.DecodeError as e:
           print(f"❌ Invalid JWT format: {e}")
           return False

   # Usage
   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   if response.success:
       token = response.data.access_token
       validate_jwt_token(token)

Environment Checker
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from upstox_totp import UpstoxTOTP, ConfigurationError

   def check_environment_setup():
       """Check if environment is properly configured."""
       required_vars = [
           'UPSTOX_USERNAME',
           'UPSTOX_PASSWORD', 
           'UPSTOX_PIN_CODE',
           'UPSTOX_TOTP_SECRET',
           'UPSTOX_CLIENT_ID',
           'UPSTOX_CLIENT_SECRET',
           'UPSTOX_REDIRECT_URI'
       ]
       
       missing_vars = []
       for var in required_vars:
           if not os.getenv(var):
               missing_vars.append(var)
       
       if missing_vars:
           print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
           return False
       
       # Try to create client
       try:
           upx = UpstoxTOTP()
           print("✅ Environment configuration is valid")
           return True
       except ConfigurationError as e:
           print(f"❌ Configuration error: {e}")
           return False

   # Usage
   if check_environment_setup():
       print("Ready to generate tokens!")
   else:
       print("Please fix configuration before proceeding")

Token Manager
~~~~~~~~~~~~~

.. code-block:: python

   import json
   import os
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP

   class SimpleTokenManager:
       def __init__(self, cache_file="upstox_token.json"):
           self.cache_file = cache_file
           self.upx = UpstoxTOTP()
       
       def get_cached_token(self):
           """Get token from cache if still valid."""
           if not os.path.exists(self.cache_file):
               return None
           
           try:
               with open(self.cache_file, 'r') as f:
                   data = json.load(f)
               
               # Check expiry (with 1 hour buffer)
               expiry = datetime.fromisoformat(data['expiry'])
               if expiry > datetime.now() + timedelta(hours=1):
                   print("✅ Using cached token")
                   return data['token']
               else:
                   print("⚠️ Cached token expired")
                   os.remove(self.cache_file)
                   return None
                   
           except (json.JSONDecodeError, KeyError, ValueError):
               print("⚠️ Invalid cache file")
               os.remove(self.cache_file)
               return None
       
       def cache_token(self, token):
           """Cache token with 24-hour expiry."""
           expiry = datetime.now() + timedelta(hours=24)
           data = {
               'token': token,
               'expiry': expiry.isoformat(),
               'created': datetime.now().isoformat()
           }
           
           with open(self.cache_file, 'w') as f:
               json.dump(data, f, indent=2)
           
           print("💾 Token cached successfully")
       
       def get_fresh_token(self):
           """Get token from cache or generate new one."""
           # Try cache first
           token = self.get_cached_token()
           if token:
               return token
           
           # Generate new token
           print("🔄 Generating new token...")
           response = self.upx.app_token.get_access_token()
           
           if response.success and response.data:
               token = response.data.access_token
               self.cache_token(token)
               return token
           else:
               raise Exception(f"Token generation failed: {response.error}")

   # Usage
   def main():
       manager = SimpleTokenManager()
       
       try:
           token = manager.get_fresh_token()
           print(f"Token available: {token[:20]}...")
           return token
       except Exception as e:
           print(f"Failed to get token: {e}")
           return None

   if __name__ == "__main__":
       token = main()

Best Practices Summary
----------------------

1. **Always use error handling** for robust applications
2. **Use context managers** for automatic cleanup
3. **Cache tokens** to avoid unnecessary regeneration
4. **Validate responses** before using data
5. **Enable debug mode** only during development
6. **Use environment variables** for configuration
7. **Handle token expiry** gracefully
8. **Test with different scenarios** (network issues, invalid credentials)
9. **Log appropriately** for production monitoring
10. **Keep secrets secure** and never log them

See Also
--------

- :doc:`../quickstart` - Quick start guide
- :doc:`../configuration` - Configuration options
- :doc:`../advanced_usage` - Advanced usage patterns
- :doc:`integration` - Integration examples
- :doc:`token_caching` - Token caching strategies
