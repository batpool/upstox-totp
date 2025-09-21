Configuration Guide
===================

This guide covers all the ways to configure the Upstox TOTP Python SDK for your environment and use case.

Configuration Methods
---------------------

The SDK supports multiple configuration methods, listed in order of precedence:

1. **Direct instantiation** (highest priority)
2. **Environment variables**
3. **`.env` file** (lowest priority)

Environment Variables
---------------------

The SDK automatically loads configuration from environment variables. Here are all the supported variables:

Required Variables
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Description
   * - ``UPSTOX_USERNAME``
     - Your 10-digit mobile number registered with Upstox
   * - ``UPSTOX_PASSWORD``
     - Your Upstox login password
   * - ``UPSTOX_PIN_CODE``
     - Your Upstox PIN code (usually 4-6 digits)
   * - ``UPSTOX_TOTP_SECRET``
     - TOTP secret key from your authenticator app setup
   * - ``UPSTOX_CLIENT_ID``
     - API key from your Upstox Developer App
   * - ``UPSTOX_CLIENT_SECRET``
     - API secret from your Upstox Developer App
   * - ``UPSTOX_REDIRECT_URI``
     - Redirect URI configured in your Upstox Developer App

Optional Variables
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Variable
     - Default
     - Description
   * - ``UPSTOX_DEBUG``
     - ``false``
     - Enable debug logging (true/false)
   * - ``UPSTOX_SLEEP_TIME``
     - ``1000``
     - Delay between requests in milliseconds

Setting Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Linux/macOS:**

.. code-block:: bash

   # Set for current session
   export UPSTOX_USERNAME=9876543210
   export UPSTOX_PASSWORD=your-password
   export UPSTOX_PIN_CODE=1234
   # ... other variables

   # Add to shell profile for persistence
   echo 'export UPSTOX_USERNAME=9876543210' >> ~/.bashrc
   echo 'export UPSTOX_PASSWORD=your-password' >> ~/.bashrc

**Windows:**

.. code-block:: batch

   # Set for current session
   set UPSTOX_USERNAME=9876543210
   set UPSTOX_PASSWORD=your-password

   # Set permanently
   setx UPSTOX_USERNAME "9876543210"
   setx UPSTOX_PASSWORD "your-password"

.env File Configuration
-----------------------

Create a `.env` file in your project root for easy configuration:

Basic .env File
~~~~~~~~~~~~~~~

.. code-block:: bash

   # .env
   
   # Upstox Account Credentials
   UPSTOX_USERNAME=9876543210
   UPSTOX_PASSWORD=your-secure-password
   UPSTOX_PIN_CODE=1234
   
   # TOTP Configuration
   UPSTOX_TOTP_SECRET=JBSWY3DPEHPK3PXP
   
   # OAuth App Credentials (from Upstox Developer Console)
   UPSTOX_CLIENT_ID=your-client-id-here
   UPSTOX_CLIENT_SECRET=your-client-secret-here
   UPSTOX_REDIRECT_URI=https://your-app.com/callback
   
   # Optional Settings
   UPSTOX_DEBUG=false
   UPSTOX_SLEEP_TIME=1000

Environment-specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create separate `.env` files for different environments:

**`.env.development`:**

.. code-block:: bash

   # Development environment
   UPSTOX_USERNAME=9876543210
   UPSTOX_PASSWORD=dev-password
   UPSTOX_PIN_CODE=1234
   UPSTOX_TOTP_SECRET=DEV-TOTP-SECRET
   UPSTOX_CLIENT_ID=dev-client-id
   UPSTOX_CLIENT_SECRET=dev-client-secret
   UPSTOX_REDIRECT_URI=http://localhost:8080/callback
   UPSTOX_DEBUG=true
   UPSTOX_SLEEP_TIME=500

**`.env.production`:**

.. code-block:: bash

   # Production environment
   UPSTOX_USERNAME=9876543210
   UPSTOX_PASSWORD=prod-password
   UPSTOX_PIN_CODE=1234
   UPSTOX_TOTP_SECRET=PROD-TOTP-SECRET
   UPSTOX_CLIENT_ID=prod-client-id
   UPSTOX_CLIENT_SECRET=prod-client-secret
   UPSTOX_REDIRECT_URI=https://myapp.com/callback
   UPSTOX_DEBUG=false
   UPSTOX_SLEEP_TIME=1000

**`.env.staging`:**

.. code-block:: bash

   # Staging environment
   UPSTOX_USERNAME=9876543210
   UPSTOX_PASSWORD=staging-password
   UPSTOX_PIN_CODE=1234
   UPSTOX_TOTP_SECRET=STAGING-TOTP-SECRET
   UPSTOX_CLIENT_ID=staging-client-id
   UPSTOX_CLIENT_SECRET=staging-client-secret
   UPSTOX_REDIRECT_URI=https://staging.myapp.com/callback
   UPSTOX_DEBUG=true
   UPSTOX_SLEEP_TIME=750

Python Configuration
--------------------

Auto-loading Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Auto-loads from environment variables or .env file
   upx = UpstoxTOTP()

Loading from Specific .env File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Load from specific environment file
   upx = UpstoxTOTP.from_env_file(".env.production")

   # Load from different path
   upx = UpstoxTOTP.from_env_file("/path/to/config/.env")

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

Partial Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   from pydantic import SecretStr

   # Override specific values while auto-loading others
   upx = UpstoxTOTP(
       debug=True,  # Override debug mode
       sleep_time=500  # Override sleep time
       # Other values loaded from environment/env file
   )

Configuration Validation
------------------------

Check Environment Setup
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP, ConfigurationError

   try:
       upx = UpstoxTOTP()
       print("✅ Configuration is valid")
   except ConfigurationError as e:
       print(f"❌ Configuration error: {e}")

Using the CLI
~~~~~~~~~~~~~

.. code-block:: bash

   # Check environment configuration
   upstox_cli check-env

Example output:

.. code-block:: text

   ✅ Environment Check Results:

   Required Variables:
   ✅ UPSTOX_USERNAME: ********3210
   ✅ UPSTOX_PASSWORD: ********** (length: 12)
   ✅ UPSTOX_PIN_CODE: ****
   ✅ UPSTOX_TOTP_SECRET: ********** (length: 16)
   ✅ UPSTOX_CLIENT_ID: ********-****-****
   ✅ UPSTOX_CLIENT_SECRET: ********** (length: 32)
   ✅ UPSTOX_REDIRECT_URI: https://myapp.com/callback

   Optional Variables:
   ✅ UPSTOX_DEBUG: false
   ✅ UPSTOX_SLEEP_TIME: 1000

   🎉 All required environment variables are properly configured!

Advanced Configuration
----------------------

Custom Configuration Class
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pydantic import BaseModel, SecretStr, Field
   from upstox_totp import UpstoxTOTP

   class CustomConfig(BaseModel):
       username: str = Field(..., min_length=10, max_length=10)
       password: SecretStr
       pin_code: SecretStr
       totp_secret: SecretStr
       client_id: str
       client_secret: SecretStr
       redirect_uri: str = Field(..., regex=r'^https?://')
       debug: bool = False
       sleep_time: int = Field(default=1000, ge=100, le=5000)

   # Load config
   config = CustomConfig(
       username="9876543210",
       password=SecretStr("password"),
       # ... other fields
   )

   # Use with UpstoxTOTP
   upx = UpstoxTOTP(**config.dict())

Configuration with Secrets Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Using Azure Key Vault:**

.. code-block:: python

   from azure.keyvault.secrets import SecretClient
   from azure.identity import DefaultAzureCredential
   from upstox_totp import UpstoxTOTP
   from pydantic import SecretStr

   # Initialize Key Vault client
   credential = DefaultAzureCredential()
   client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)

   # Retrieve secrets
   config = {
       "username": client.get_secret("upstox-username").value,
       "password": SecretStr(client.get_secret("upstox-password").value),
       "pin_code": SecretStr(client.get_secret("upstox-pin").value),
       "totp_secret": SecretStr(client.get_secret("upstox-totp-secret").value),
       "client_id": client.get_secret("upstox-client-id").value,
       "client_secret": SecretStr(client.get_secret("upstox-client-secret").value),
       "redirect_uri": client.get_secret("upstox-redirect-uri").value,
   }

   upx = UpstoxTOTP(**config)

**Using AWS Secrets Manager:**

.. code-block:: python

   import boto3
   import json
   from upstox_totp import UpstoxTOTP
   from pydantic import SecretStr

   # Initialize Secrets Manager client
   client = boto3.client('secretsmanager', region_name='us-east-1')

   # Retrieve secret
   response = client.get_secret_value(SecretId='upstox-credentials')
   secrets = json.loads(response['SecretString'])

   upx = UpstoxTOTP(
       username=secrets['username'],
       password=SecretStr(secrets['password']),
       pin_code=SecretStr(secrets['pin_code']),
       totp_secret=SecretStr(secrets['totp_secret']),
       client_id=secrets['client_id'],
       client_secret=SecretStr(secrets['client_secret']),
       redirect_uri=secrets['redirect_uri']
   )

Docker Configuration
--------------------

Using Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: dockerfile

   FROM python:3.12-slim

   # Install package
   RUN pip install upstox-totp

   # Set environment variables
   ENV UPSTOX_USERNAME=9876543210
   ENV UPSTOX_PASSWORD=your-password
   ENV UPSTOX_PIN_CODE=1234
   ENV UPSTOX_TOTP_SECRET=your-totp-secret
   ENV UPSTOX_CLIENT_ID=your-client-id
   ENV UPSTOX_CLIENT_SECRET=your-client-secret
   ENV UPSTOX_REDIRECT_URI=https://your-app.com/callback

   # Copy and run your app
   COPY . /app
   WORKDIR /app
   CMD ["python", "main.py"]

Using .env File
~~~~~~~~~~~~~~~

.. code-block:: dockerfile

   FROM python:3.12-slim

   RUN pip install upstox-totp

   COPY .env /app/.env
   COPY . /app
   WORKDIR /app

   CMD ["python", "main.py"]

Docker Compose
~~~~~~~~~~~~~~

.. code-block:: yaml

   # docker-compose.yml
   version: '3.8'

   services:
     upstox-app:
       build: .
       environment:
         - UPSTOX_USERNAME=${UPSTOX_USERNAME}
         - UPSTOX_PASSWORD=${UPSTOX_PASSWORD}
         - UPSTOX_PIN_CODE=${UPSTOX_PIN_CODE}
         - UPSTOX_TOTP_SECRET=${UPSTOX_TOTP_SECRET}
         - UPSTOX_CLIENT_ID=${UPSTOX_CLIENT_ID}
         - UPSTOX_CLIENT_SECRET=${UPSTOX_CLIENT_SECRET}
         - UPSTOX_REDIRECT_URI=${UPSTOX_REDIRECT_URI}
       env_file:
         - .env

Configuration Security
----------------------

Best Practices
~~~~~~~~~~~~~~

1. **Never commit secrets to version control**
2. **Use environment variables in production**
3. **Rotate credentials regularly**
4. **Use secrets management services**
5. **Limit access to configuration files**

.gitignore Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   # .gitignore
   
   # Environment files
   .env
   .env.local
   .env.development
   .env.staging
   .env.production
   .env.*.local
   
   # Configuration files with secrets
   config.json
   secrets.yaml
   credentials.ini

File Permissions
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Secure .env file permissions
   chmod 600 .env
   
   # Secure config directory
   chmod 700 config/
   chmod 600 config/*.env

Configuration Templates
-----------------------

Example .env Template
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # .env.example - Template file (safe to commit)
   
   # Upstox Account Credentials
   UPSTOX_USERNAME=your-mobile-number-here
   UPSTOX_PASSWORD=your-password-here
   UPSTOX_PIN_CODE=your-pin-here
   
   # TOTP Configuration
   UPSTOX_TOTP_SECRET=your-totp-secret-here
   
   # OAuth App Credentials (from Upstox Developer Console)
   UPSTOX_CLIENT_ID=your-client-id-here
   UPSTOX_CLIENT_SECRET=your-client-secret-here
   UPSTOX_REDIRECT_URI=your-redirect-uri-here
   
   # Optional Settings
   UPSTOX_DEBUG=false
   UPSTOX_SLEEP_TIME=1000

Setup Script
~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # setup-env.sh - Environment setup script
   
   if [ ! -f .env ]; then
       echo "Creating .env file from template..."
       cp .env.example .env
       echo "Please edit .env file with your actual credentials"
       echo "Then run: chmod 600 .env"
   else
       echo ".env file already exists"
   fi

Configuration Validation Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # validate_config.py
   
   import os
   from upstox_totp import UpstoxTOTP, ConfigurationError

   def validate_environment():
       """Validate environment configuration."""
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
       
       try:
           upx = UpstoxTOTP()
           print("✅ Configuration is valid")
           return True
       except ConfigurationError as e:
           print(f"❌ Configuration error: {e}")
           return False

   if __name__ == "__main__":
       validate_environment()

Troubleshooting Configuration
-----------------------------

Common Issues
~~~~~~~~~~~~~

**"Configuration Error: Missing environment variables"**

.. code-block:: bash

   # Check which variables are set
   env | grep UPSTOX

   # Use the CLI to check configuration
   upstox_cli check-env

**"Invalid TOTP secret format"**

- Ensure TOTP secret is base32 encoded
- Remove any spaces or special characters
- Check that it's the correct secret from your authenticator app

**"Client ID / Redirect URI mismatch"**

- Verify credentials in Upstox Developer Console
- Ensure redirect_uri exactly matches (including protocol, domain, path)
- Check that your app is approved and active

**Permission denied errors**

.. code-block:: bash

   # Check file permissions
   ls -la .env
   
   # Fix permissions
   chmod 600 .env

Testing Configuration
---------------------

Unit Tests
~~~~~~~~~~

.. code-block:: python

   # test_config.py
   
   import pytest
   from upstox_totp import UpstoxTOTP, ConfigurationError
   from pydantic import SecretStr

   def test_valid_configuration():
       """Test valid configuration."""
       upx = UpstoxTOTP(
           username="9876543210",
           password=SecretStr("password"),
           pin_code=SecretStr("1234"),
           totp_secret=SecretStr("JBSWY3DPEHPK3PXP"),
           client_id="client-id",
           client_secret=SecretStr("client-secret"),
           redirect_uri="https://example.com/callback"
       )
       assert upx.username == "9876543210"

   def test_invalid_username():
       """Test invalid username format."""
       with pytest.raises(ConfigurationError):
           UpstoxTOTP(
               username="invalid",  # Should be 10 digits
               password=SecretStr("password"),
               # ... other fields
           )

Configuration Migration
-----------------------

From v1.0 to v1.1
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Old configuration (v1.0)
   upx = UpstoxTOTP(
       mobile="9876543210",  # Changed to 'username'
       password="password",
       pin="1234",           # Changed to 'pin_code'
       totp_key="secret"     # Changed to 'totp_secret'
   )

   # New configuration (v1.1+)
   upx = UpstoxTOTP(
       username="9876543210",
       password=SecretStr("password"),
       pin_code=SecretStr("1234"),
       totp_secret=SecretStr("secret")
   )

Need Help?
----------

If you're having configuration issues:

- Check the :doc:`troubleshooting` guide
- Review the :doc:`quickstart` for step-by-step setup
- Use ``upstox_cli check-env`` to diagnose issues
- Create an issue on `GitHub <https://github.com/batpool/upstox-totp/issues>`_
