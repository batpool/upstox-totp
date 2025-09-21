Quick Start Guide
=================

This guide will get you up and running with the Upstox TOTP Python SDK in just a few minutes.

Prerequisites
-------------

Before you begin, make sure you have:

1. **Python 3.12+** installed
2. **Upstox trading account** with API access
3. **Upstox Developer App** created (for API credentials)
4. **TOTP app** configured (Google Authenticator, Authy, etc.)

Step 1: Install the Package
---------------------------

.. code-block:: bash

   # Using uv (recommended)
   uv add upstox-totp

   # Or using pip
   pip install upstox-totp

Step 2: Set Up Your Credentials
-------------------------------

Create a `.env` file in your project root:

.. code-block:: bash

   # Create .env file
   touch .env

Add your credentials to the `.env` file:

.. code-block:: bash

   # Required - Your Upstox account credentials
   UPSTOX_USERNAME=9876543210              # Your 10-digit mobile number
   UPSTOX_PASSWORD=your-password           # Your Upstox login password
   UPSTOX_PIN_CODE=your-pin                # Your Upstox PIN code

   # Required - TOTP secret from your Upstox app setup
   UPSTOX_TOTP_SECRET=your-totp-secret     # TOTP secret key

   # Required - OAuth app credentials from Upstox Developer Console
   UPSTOX_CLIENT_ID=your-client-id         # API key from app generation
   UPSTOX_CLIENT_SECRET=your-client-secret # API secret from app generation
   UPSTOX_REDIRECT_URI=https://your-app.com/callback  # Must match app settings

   # Optional
   UPSTOX_DEBUG=false                      # Enable debug logging
   UPSTOX_SLEEP_TIME=1000                  # Request delay in milliseconds

.. note::
   **Security**: Never commit your `.env` file to version control. Add it to your `.gitignore`:
   
   .. code-block:: bash
   
      echo ".env" >> .gitignore

Step 3: Your First Token Generation
-----------------------------------

Create a simple Python script:

.. code-block:: python

   # quickstart.py
   
   from upstox_totp import UpstoxTOTP
   
   def main():
       # Initialize client (auto-loads from .env file)
       upx = UpstoxTOTP()
       
       print("🚀 Generating Upstox access token...")
       
       try:
           # Get access token
           response = upx.app_token.get_access_token()
           
           if response.success and response.data:
               print("✅ Success! Token generated.")
               print(f"📊 User: {response.data.user_name}")
               print(f"🆔 User ID: {response.data.user_id}")
               print(f"📧 Email: {response.data.email}")
               print(f"🏢 Broker: {response.data.broker}")
               print(f"🔑 Access Token: {response.data.access_token[:20]}...")
               
               # Store token for later use
               access_token = response.data.access_token
               
           else:
               print("❌ Failed to generate token")
               if response.error:
                   print(f"Error: {response.error}")
                   
       except Exception as e:
           print(f"❌ Error: {e}")
   
   if __name__ == "__main__":
       main()

Run your script:

.. code-block:: bash

   python quickstart.py

Expected output:

.. code-block:: text

   🚀 Generating Upstox access token...
   ✅ Success! Token generated.
   📊 User: John Doe
   🆔 User ID: ABC123
   📧 Email: john@example.com
   🏢 Broker: UPSTOX
   🔑 Access Token: eyJ0eXAiOiJKV1QiLCJ...

Step 4: Using the CLI Tool
--------------------------

The package also includes a command-line interface:

.. code-block:: bash

   # Check your environment setup
   upstox_cli check-env

   # Generate a token
   upstox_cli generate-token

CLI output example:

.. code-block:: text

   ❯ upstox_cli generate-token

   🎉 Access token generated successfully!

   Token Details:
   Access Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
   User ID: ABC123
   User Name: John Doe
   User Type: individual
   Broker: UPSTOX
   Email: john@example.com
   Products: D, I, CO, MIS
   Exchanges: NSE_EQ, BSE_EQ, NSE_FO, NSE_CD, BSE_FO, BSE_CD, MCX_FO
   Is Active: True

   💡 You can now use this access token to make authenticated API calls to Upstox.

Step 5: Using the Token with Upstox API
---------------------------------------

Now use your token to make API calls:

.. code-block:: python

   # upstox_api_example.py
   
   import requests
   from upstox_totp import UpstoxTOTP
   
   def get_user_profile():
       # Get access token
       upx = UpstoxTOTP()
       token_response = upx.app_token.get_access_token()
       
       if not token_response.success:
           raise Exception("Failed to get access token")
       
       access_token = token_response.data.access_token
       
       # Set up headers for API calls
       headers = {
           'Authorization': f'Bearer {access_token}',
           'Content-Type': 'application/json'
       }
       
       # Get user profile
       response = requests.get(
           'https://api.upstox.com/v2/user/profile',
           headers=headers
       )
       
       if response.status_code == 200:
           profile = response.json()
           print("👤 User Profile:")
           print(f"   Name: {profile['data']['user_name']}")
           print(f"   Email: {profile['data']['email']}")
           print(f"   User Type: {profile['data']['user_type']}")
       else:
           print(f"❌ API Error: {response.status_code}")
           print(response.text)
   
   def get_portfolio_positions():
       # Get access token
       upx = UpstoxTOTP()
       token_response = upx.app_token.get_access_token()
       access_token = token_response.data.access_token
       
       headers = {
           'Authorization': f'Bearer {access_token}',
           'Content-Type': 'application/json'
       }
       
       # Get portfolio positions
       response = requests.get(
           'https://api.upstox.com/v2/portfolio/long-term-positions',
           headers=headers
       )
       
       if response.status_code == 200:
           positions = response.json()
           print("📊 Portfolio Positions:")
           for position in positions['data']:
               print(f"   {position['instrument_token']}: {position['quantity']}")
       else:
           print(f"❌ API Error: {response.status_code}")
   
   if __name__ == "__main__":
       get_user_profile()
       get_portfolio_positions()

Step 6: Context Manager Usage
-----------------------------

For automatic cleanup, use the context manager:

.. code-block:: python

   # context_manager_example.py
   
   from upstox_totp import UpstoxTOTP
   
   # Using context manager
   with UpstoxTOTP() as upx:
       response = upx.app_token.get_access_token()
       
       if response.success:
           access_token = response.data.access_token
           print(f"✅ Token: {access_token[:20]}...")
           
           # Use token for API calls
           # Session is automatically cleaned up when exiting the context

Common Configuration Patterns
-----------------------------

Environment-specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   
   # Load from specific environment file
   upx = UpstoxTOTP.from_env_file(".env.production")

Manual Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   from pydantic import SecretStr
   
   # Manual configuration (not recommended for production)
   upx = UpstoxTOTP(
       username="9876543210",
       password=SecretStr("your-password"),
       pin_code=SecretStr("your-pin"),
       totp_secret=SecretStr("your-totp-secret"),
       client_id="your-client-id",
       client_secret=SecretStr("your-client-secret"),
       redirect_uri="https://your-app.com/callback"
   )

Debug Mode
~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   
   # Enable debug logging
   upx = UpstoxTOTP(debug=True)

Error Handling Best Practices
-----------------------------

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError, ConfigurationError
   
   def robust_token_generation():
       try:
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           
           if response.success and response.data:
               return response.data.access_token
           else:
               print(f"Token generation failed: {response.error}")
               return None
               
       except ConfigurationError as e:
           print(f"Configuration Error: {e}")
           print("💡 Check your environment variables in .env file")
           return None
           
       except UpstoxError as e:
           print(f"Upstox API Error: {e}")
           # Error includes helpful troubleshooting tips
           return None
           
       except Exception as e:
           print(f"Unexpected Error: {e}")
           return None
   
   # Usage
   token = robust_token_generation()
   if token:
       print("✅ Token generated successfully")
   else:
       print("❌ Failed to generate token")

Next Steps
----------

Now that you have the basics working:

1. **Learn about advanced features**: See :doc:`advanced_usage`
2. **Explore configuration options**: See :doc:`configuration`
3. **Check out integration examples**: See :doc:`examples/integration`
4. **Read the full API reference**: See :doc:`api/client`
5. **Learn about token caching**: See :doc:`examples/token_caching`

Common Issues
-------------

**"Configuration Error: Missing environment variables"**

.. code-block:: bash

   # Check what's missing
   upstox_cli check-env

**"Invalid credentials" error**

- Verify your username is a 10-digit mobile number
- Check password and PIN are correct
- Ensure TOTP secret is from the correct Upstox app setup

**"Client ID / Redirect URI" error**

- Verify credentials in Upstox Developer Console
- Ensure redirect_uri exactly matches your app settings
- Check if your app is approved and active

**Token expires quickly**

.. note::
   Upstox access tokens expire after 24 hours. For production applications:
   
   - Implement token caching (see :doc:`examples/token_caching`)
   - Set up automatic refresh logic
   - Monitor token expiry

Getting Help
------------

If you run into issues:

- Check the :doc:`troubleshooting` guide
- Review the :doc:`configuration` documentation
- Look at more :doc:`examples/basic_usage`
- Create an issue on `GitHub <https://github.com/batpool/upstox-totp/issues>`_

Congratulations! 🎉
-------------------

You've successfully set up the Upstox TOTP Python SDK and generated your first access token. You're now ready to integrate with the Upstox API for trading, market data, and portfolio management.
