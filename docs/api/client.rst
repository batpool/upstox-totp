Client API Reference
====================

This section provides detailed documentation for the main client classes and methods.

UpstoxTOTP
----------

.. autoclass:: upstox_totp.UpstoxTOTP
   :members:
   :undoc-members:
   :show-inheritance:

The main client class for handling Upstox TOTP authentication and token generation.

Constructor
~~~~~~~~~~~

.. automethod:: upstox_totp.UpstoxTOTP.__init__
   :no-index:

Class Methods
~~~~~~~~~~~~~

.. automethod:: upstox_totp.UpstoxTOTP.from_env_file
   :no-index:

Instance Methods
~~~~~~~~~~~~~~~~

TOTP Operations
^^^^^^^^^^^^^^^

.. automethod:: upstox_totp.UpstoxTOTP.generate_totp_secret
   :no-index:

Session Management
^^^^^^^^^^^^^^^^^^

.. automethod:: upstox_totp.UpstoxTOTP.reset_session
   :no-index:
.. automethod:: upstox_totp.UpstoxTOTP.generate_request_id
   :no-index:

Context Manager Support
^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: upstox_totp.UpstoxTOTP.__enter__
   :no-index:
.. automethod:: upstox_totp.UpstoxTOTP.__exit__
   :no-index:

Properties
~~~~~~~~~~

.. autoproperty:: upstox_totp.UpstoxTOTP.session
   :no-index:

Usage Examples
~~~~~~~~~~~~~~

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Initialize with auto-loaded configuration
   upx = UpstoxTOTP()

   # Generate access token
   response = upx.app_token.get_access_token()
   if response.success:
       access_token = response.data.access_token
       print(f"Token: {access_token}")

Manual Configuration
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   from pydantic import SecretStr

   upx = UpstoxTOTP(
       username="9876543210",
       password=SecretStr("your-password"),
       pin_code=SecretStr("your-pin"),
       totp_secret=SecretStr("your-totp-secret"),
       client_id="your-client-id",
       client_secret=SecretStr("your-client-secret"),
       redirect_uri="https://your-app.com/callback"
   )

Environment File Loading
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Load from specific environment file
   upx = UpstoxTOTP.from_env_file(".env.production")

Context Manager Usage
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   with UpstoxTOTP() as upx:
       response = upx.app_token.get_access_token()
       # Session automatically cleaned up

Session Customization
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()

   # Access underlying session
   session = upx.session
   session.timeout = (10, 30)
   session.headers.update({'User-Agent': 'MyApp/1.0'})

   # Reset session if needed
   upx.reset_session()

TOTP Management
^^^^^^^^^^^^^^^

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()

   # Generate current TOTP
   totp_code = upx.generate_totp_secret()
   print(f"Current TOTP: {totp_code}")

AppTokenAPI
-----------

.. autoclass:: upstox_totp._api.app_token.AppTokenAPI
   :members:
   :undoc-members:
   :show-inheritance:

The AppTokenAPI class handles the OAuth flow and access token generation.

Methods
~~~~~~~

.. automethod:: upstox_totp._api.app_token.AppTokenAPI.get_access_token
   :no-index:

Usage Examples
~~~~~~~~~~~~~~

Direct Usage
^^^^^^^^^^^^

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   
   # Access the app_token instance
   app_token = upx.app_token
   
   # Generate access token
   response = app_token.get_access_token()

Error Handling
^^^^^^^^^^^^^^

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError

   upx = UpstoxTOTP()

   try:
       response = upx.app_token.get_access_token()
       if response.success:
           token = response.data.access_token
       else:
           print(f"Error: {response.error}")
   except UpstoxError as e:
       print(f"Upstox API Error: {e}")

BaseAPI
-------

.. autoclass:: upstox_totp._api.base.BaseAPI
   :members:
   :undoc-members:
   :show-inheritance:

Base class for all API clients, providing common functionality.

Configuration Parameters
------------------------

The UpstoxTOTP class accepts the following configuration parameters:

Required Parameters
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Type
     - Description
   * - ``username``
     - ``str``
     - 10-digit mobile number registered with Upstox
   * - ``password``
     - ``SecretStr``
     - Upstox login password
   * - ``pin_code``
     - ``SecretStr``
     - Upstox PIN code (4-6 digits)
   * - ``totp_secret``
     - ``SecretStr``
     - TOTP secret key from authenticator app
   * - ``client_id``
     - ``str``
     - API key from Upstox Developer App
   * - ``client_secret``
     - ``SecretStr``
     - API secret from Upstox Developer App
   * - ``redirect_uri``
     - ``str``
     - Redirect URI configured in Upstox app

Optional Parameters
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Default
     - Description
   * - ``debug``
     - ``bool``
     - ``False``
     - Enable debug logging
   * - ``sleep_time``
     - ``int``
     - ``1000``
     - Delay between requests (milliseconds)

Configuration Validation
~~~~~~~~~~~~~~~~~~~~~~~~~

All parameters are validated using Pydantic models:

- **Username**: Must be exactly 10 digits
- **Password**: Must be non-empty string
- **PIN Code**: Must be 4-6 digits
- **TOTP Secret**: Must be valid base32 string
- **Client ID**: Must be non-empty string
- **Client Secret**: Must be non-empty string  
- **Redirect URI**: Must be valid URL format
- **Sleep Time**: Must be between 100-10000 milliseconds

Error Handling
--------------

The client provides comprehensive error handling:

Configuration Errors
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP, ConfigurationError

   try:
       upx = UpstoxTOTP(username="invalid")  # Invalid format
   except ConfigurationError as e:
       print(f"Configuration error: {e}")

API Errors
~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError

   upx = UpstoxTOTP()

   try:
       response = upx.app_token.get_access_token()
   except UpstoxError as e:
       print(f"API error: {e}")
       # Error includes helpful troubleshooting information

Network Errors
~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   import requests

   upx = UpstoxTOTP()

   try:
       response = upx.app_token.get_access_token()
   except requests.RequestException as e:
       print(f"Network error: {e}")

Thread Safety
-------------

The UpstoxTOTP client is **not thread-safe** by default. For concurrent usage:

Thread-Safe Usage
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import threading
   from upstox_totp import UpstoxTOTP

   # Create separate instances for each thread
   def worker():
       upx = UpstoxTOTP()  # Create new instance per thread
       response = upx.app_token.get_access_token()
       return response

   # Use with threading
   threads = []
   for i in range(5):
       thread = threading.Thread(target=worker)
       threads.append(thread)
       thread.start()

   for thread in threads:
       thread.join()

Session Sharing (Advanced)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import threading
   from upstox_totp import UpstoxTOTP

   # Shared session with thread-local storage
   thread_local = threading.local()

   def get_client():
       if not hasattr(thread_local, 'upx'):
           thread_local.upx = UpstoxTOTP()
       return thread_local.upx

   def worker():
       upx = get_client()
       response = upx.app_token.get_access_token()
       return response

Performance Considerations
--------------------------

Session Reuse
~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Reuse the same client instance for multiple calls
   upx = UpstoxTOTP()

   # Multiple token generations reuse the session
   for i in range(5):
       response = upx.app_token.get_access_token()

Connection Pooling
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   from requests.adapters import HTTPAdapter

   upx = UpstoxTOTP()

   # Configure connection pooling
   adapter = HTTPAdapter(
       pool_connections=10,
       pool_maxsize=20
   )
   upx.session.mount("https://", adapter)

Memory Management
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Use context manager for automatic cleanup
   with UpstoxTOTP() as upx:
       response = upx.app_token.get_access_token()
       # Session automatically cleaned up

   # Or manually reset session
   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()
   upx.reset_session()  # Clear session data

Debugging
---------

Enable Debug Mode
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Enable debug logging
   upx = UpstoxTOTP(debug=True)

   # Or via environment variable
   # UPSTOX_DEBUG=true

Access Logs
~~~~~~~~~~~

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP

   # Configure logging to see debug information
   logging.basicConfig(level=logging.DEBUG)

   upx = UpstoxTOTP(debug=True)
   response = upx.app_token.get_access_token()

Request/Response Inspection
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP(debug=True)

   # Access session for custom logging
   session = upx.session

   # Add custom request/response logging
   def log_request(request):
       print(f"Request: {request.method} {request.url}")

   def log_response(response):
       print(f"Response: {response.status_code}")

   # Hook into session events
   session.hooks['response'].append(log_response)

Best Practices
--------------

1. **Use environment variables** for configuration in production
2. **Enable debug mode** only in development
3. **Reuse client instances** for better performance  
4. **Use context managers** for automatic cleanup
5. **Handle all exception types** appropriately
6. **Validate configuration** before deployment
7. **Monitor token expiry** and refresh proactively
8. **Use connection pooling** for high-volume applications
9. **Implement retry logic** for resilient applications
10. **Clear sensitive data** from memory when possible

See Also
--------

- :doc:`models` - Response and data models
- :doc:`errors` - Exception classes and error handling
- :doc:`../configuration` - Configuration guide
- :doc:`../advanced_usage` - Advanced usage patterns
