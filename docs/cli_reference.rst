CLI Reference
=============

The Upstox TOTP SDK includes a command-line interface (CLI) tool for quick token generation and environment validation.

Installation
------------

The CLI is automatically installed when you install the package:

.. code-block:: bash

   # Install the package
   pip install upstox-totp

   # Or with uv
   uv add upstox-totp

   # CLI is now available
   upstox_cli --help

Global Installation
~~~~~~~~~~~~~~~~~~~

For CLI-only usage, install globally:

.. code-block:: bash

   # Using pipx (recommended)
   pipx install upstox-totp

   # Using pip
   pip install --user upstox-totp

   # Using uv
   uv tool install upstox-totp

Basic Usage
-----------

The CLI provides a simple interface for common operations:

.. code-block:: bash

   # Show help
   upstox_cli --help

   # Check environment configuration
   upstox_cli check-env

   # Generate access token
   upstox_cli generate-token

   # Show version
   upstox_cli --version

Commands
--------

check-env
~~~~~~~~~

Validates your environment configuration.

**Usage:**

.. code-block:: bash

   upstox_cli check-env

**Example Output:**

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

**Error Example:**

.. code-block:: text

   ❌ Environment Check Results:

   Required Variables:
   ❌ UPSTOX_USERNAME: Not set
   ✅ UPSTOX_PASSWORD: ********** (length: 12)
   ❌ UPSTOX_PIN_CODE: Not set
   ✅ UPSTOX_TOTP_SECRET: ********** (length: 16)
   ✅ UPSTOX_CLIENT_ID: ********-****-****
   ✅ UPSTOX_CLIENT_SECRET: ********** (length: 32)
   ✅ UPSTOX_REDIRECT_URI: https://myapp.com/callback

   💡 Missing Variables:
   - UPSTOX_USERNAME: Your 10-digit mobile number
   - UPSTOX_PIN_CODE: Your Upstox PIN code

   Please set these environment variables and try again.

generate-token
~~~~~~~~~~~~~~

Generates an Upstox access token using TOTP authentication.

**Usage:**

.. code-block:: bash

   upstox_cli generate-token

**Options:**

.. code-block:: bash

   upstox_cli generate-token --help

**Example Output:**

.. code-block:: text

   🚀 Generating Upstox access token...

   🎉 Access token generated successfully!

   Token Details:
   Access Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
   User ID: BAT123
   User Name: Batman
   User Type: individual
   Broker: UPSTOX
   Email: batman@arkham.com
   Products: D, I, CO, MIS
   Exchanges: NSE_EQ, BSE_EQ, NSE_FO, NSE_CD, BSE_FO, BSE_CD, MCX_FO
   Is Active: True

   💡 You can now use this access token to make authenticated API calls to Upstox.

**Error Example:**

.. code-block:: text

   🚀 Generating Upstox access token...

   ❌ Token generation failed!

   Error: Invalid credentials provided
   
   Troubleshooting:
   1. Verify your username (10-digit mobile number)
   2. Check your password is correct
   3. Ensure PIN code is valid
   4. Verify TOTP secret from your authenticator app
   5. Run 'upstox_cli check-env' to validate configuration

--version
~~~~~~~~~

Shows the installed version of the package.

**Usage:**

.. code-block:: bash

   upstox_cli --version

**Output:**

.. code-block:: text

   upstox-totp, version 1.0.3

Global Options
--------------

The CLI supports these global options:

--help
~~~~~~

Shows help information for commands.

.. code-block:: bash

   # Global help
   upstox_cli --help

   # Command-specific help
   upstox_cli generate-token --help
   upstox_cli check-env --help

--version
~~~~~~~~~

Shows version information.

.. code-block:: bash

   upstox_cli --version

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

The CLI reads configuration from environment variables or `.env` files:

.. code-block:: bash

   # Required variables
   export UPSTOX_USERNAME=9876543210
   export UPSTOX_PASSWORD=your-password
   export UPSTOX_PIN_CODE=your-pin
   export UPSTOX_TOTP_SECRET=your-totp-secret
   export UPSTOX_CLIENT_ID=your-client-id
   export UPSTOX_CLIENT_SECRET=your-client-secret
   export UPSTOX_REDIRECT_URI=https://your-app.com/callback

   # Optional variables
   export UPSTOX_DEBUG=false
   export UPSTOX_SLEEP_TIME=1000

.env File Support
~~~~~~~~~~~~~~~~~

Create a `.env` file in your current directory:

.. code-block:: bash

   # .env
   UPSTOX_USERNAME=9876543210
   UPSTOX_PASSWORD=your-password
   UPSTOX_PIN_CODE=your-pin
   UPSTOX_TOTP_SECRET=your-totp-secret
   UPSTOX_CLIENT_ID=your-client-id
   UPSTOX_CLIENT_SECRET=your-client-secret
   UPSTOX_REDIRECT_URI=https://your-app.com/callback

The CLI will automatically load this file.

Exit Codes
----------

The CLI uses standard exit codes:

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - Code
     - Meaning
   * - 0
     - Success
   * - 1
     - General error
   * - 2
     - Configuration error
   * - 3
     - Validation error
   * - 4
     - Authentication error
   * - 5
     - Network error

**Example Usage in Scripts:**

.. code-block:: bash

   #!/bin/bash

   # Check environment first
   if ! upstox_cli check-env; then
       echo "Environment configuration failed"
       exit 1
   fi

   # Generate token
   if upstox_cli generate-token > token.txt; then
       echo "Token generated successfully"
   else
       echo "Token generation failed"
       exit 1
   fi

Output Formats
--------------

JSON Output
~~~~~~~~~~~

For programmatic usage, you can request JSON output:

.. code-block:: bash

   # Generate token with JSON output (future feature)
   upstox_cli generate-token --output json

**Example JSON Output:**

.. code-block:: json

   {
     "success": true,
     "data": {
       "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
       "user_id": "BAT123",
       "user_name": "Batman",
       "email": "batman@arkham.com",
       "broker": "UPSTOX",
       "user_type": "individual",
       "products": ["D", "I", "CO", "MIS"],
       "exchanges": ["NSE_EQ", "BSE_EQ", "NSE_FO"],
       "is_active": true
     },
     "error": null
   }

Quiet Mode
~~~~~~~~~~

Suppress verbose output:

.. code-block:: bash

   # Quiet mode (future feature)
   upstox_cli generate-token --quiet

   # Only output the token
   eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

Integration Examples
--------------------

Shell Scripts
~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # get_upstox_token.sh

   set -e

   echo "🔍 Checking Upstox configuration..."
   if ! upstox_cli check-env; then
       echo "❌ Configuration check failed"
       exit 1
   fi

   echo "🚀 Generating access token..."
   if token=$(upstox_cli generate-token 2>/dev/null | grep "Access Token:" | cut -d' ' -f3); then
       echo "✅ Token generated successfully"
       echo "Token: $token"
       
       # Save to file
       echo "$token" > upstox_token.txt
       echo "💾 Token saved to upstox_token.txt"
   else
       echo "❌ Token generation failed"
       exit 1
   fi

Python Scripts
~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   # get_token.py

   import subprocess
   import sys
   import json

   def run_cli_command(command):
       """Run CLI command and return output."""
       try:
           result = subprocess.run(
               ['upstox_cli'] + command,
               capture_output=True,
               text=True,
               check=True
           )
           return result.stdout.strip()
       except subprocess.CalledProcessError as e:
           print(f"CLI command failed: {e}")
           print(f"Error output: {e.stderr}")
           return None

   def main():
       # Check environment
       print("Checking environment...")
       if run_cli_command(['check-env']) is None:
           print("Environment check failed")
           sys.exit(1)

       # Generate token
       print("Generating token...")
       output = run_cli_command(['generate-token'])
       if output is None:
           print("Token generation failed")
           sys.exit(1)

       # Extract token from output
       for line in output.split('\n'):
           if line.startswith('Access Token:'):
               token = line.split(':', 1)[1].strip()
               print(f"Token: {token}")
               return token

       print("Could not extract token from output")
       sys.exit(1)

   if __name__ == "__main__":
       token = main()

Docker Usage
~~~~~~~~~~~~

.. code-block:: dockerfile

   FROM python:3.12-slim

   # Install upstox-totp
   RUN pip install upstox-totp

   # Set environment variables
   ENV UPSTOX_USERNAME=9876543210
   ENV UPSTOX_PASSWORD=your-password
   # ... other env vars

   # Create script to generate token
   RUN echo '#!/bin/bash\nupstox_cli generate-token' > /usr/local/bin/get-token
   RUN chmod +x /usr/local/bin/get-token

   # Use the CLI
   CMD ["get-token"]

.. code-block:: bash

   # Build and run
   docker build -t upstox-cli .
   docker run --env-file .env upstox-cli

CI/CD Integration
~~~~~~~~~~~~~~~~~

**GitHub Actions:**

.. code-block:: yaml

   name: Get Upstox Token
   on: [push]

   jobs:
     token:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.12'
             
         - name: Install upstox-totp
           run: pip install upstox-totp
           
         - name: Check environment
           run: upstox_cli check-env
           env:
             UPSTOX_USERNAME: ${{ secrets.UPSTOX_USERNAME }}
             UPSTOX_PASSWORD: ${{ secrets.UPSTOX_PASSWORD }}
             UPSTOX_PIN_CODE: ${{ secrets.UPSTOX_PIN_CODE }}
             UPSTOX_TOTP_SECRET: ${{ secrets.UPSTOX_TOTP_SECRET }}
             UPSTOX_CLIENT_ID: ${{ secrets.UPSTOX_CLIENT_ID }}
             UPSTOX_CLIENT_SECRET: ${{ secrets.UPSTOX_CLIENT_SECRET }}
             UPSTOX_REDIRECT_URI: ${{ secrets.UPSTOX_REDIRECT_URI }}
             
         - name: Generate token
           run: upstox_cli generate-token
           env:
             UPSTOX_USERNAME: ${{ secrets.UPSTOX_USERNAME }}
             # ... other secrets

**GitLab CI:**

.. code-block:: yaml

   stages:
     - token

   generate_token:
     stage: token
     image: python:3.12
     before_script:
       - pip install upstox-totp
     script:
       - upstox_cli check-env
       - upstox_cli generate-token
     variables:
       UPSTOX_USERNAME: $UPSTOX_USERNAME
       UPSTOX_PASSWORD: $UPSTOX_PASSWORD
       # ... other variables

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Command not found**

.. code-block:: bash

   # Error: upstox_cli: command not found
   
   # Solutions:
   # 1. Ensure package is installed
   pip install upstox-totp
   
   # 2. Check if it's in PATH
   which upstox_cli
   
   # 3. Use full path
   python -m upstox_totp.cli check-env

**Permission denied**

.. code-block:: bash

   # Error: Permission denied
   
   # Solutions:
   # 1. Install with --user flag
   pip install --user upstox-totp
   
   # 2. Use virtual environment
   python -m venv venv
   source venv/bin/activate
   pip install upstox-totp

**Configuration errors**

.. code-block:: bash

   # Always check configuration first
   upstox_cli check-env

   # Look for specific error messages
   # Set missing environment variables

Debug Mode
~~~~~~~~~~

Enable debug output:

.. code-block:: bash

   # Set debug environment variable
   export UPSTOX_DEBUG=true
   upstox_cli generate-token

   # Or inline
   UPSTOX_DEBUG=true upstox_cli generate-token

Verbose Output
~~~~~~~~~~~~~~

Get more detailed output:

.. code-block:: bash

   # Enable verbose mode (future feature)
   upstox_cli generate-token --verbose

Getting Help
~~~~~~~~~~~~

.. code-block:: bash

   # General help
   upstox_cli --help

   # Command help
   upstox_cli generate-token --help
   upstox_cli check-env --help

   # Version information
   upstox_cli --version

Advanced Usage
--------------

Custom Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Use specific .env file
   UPSTOX_ENV_FILE=.env.production upstox_cli generate-token

   # Override specific values
   UPSTOX_DEBUG=true upstox_cli generate-token

Batch Operations
~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # batch_tokens.sh

   # Generate multiple tokens with different configs
   for env_file in .env.dev .env.staging .env.prod; do
       echo "Generating token for $env_file..."
       UPSTOX_ENV_FILE=$env_file upstox_cli generate-token > "token_$(basename $env_file .env).txt"
   done

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Reduce sleep time for faster generation
   UPSTOX_SLEEP_TIME=500 upstox_cli generate-token

   # Use cached session (future feature)
   upstox_cli generate-token --cache-session

Best Practices
--------------

1. **Always run check-env first** before generating tokens
2. **Use environment variables** instead of command-line arguments for secrets
3. **Handle exit codes** properly in scripts
4. **Store tokens securely** - never log them
5. **Use CI/CD secrets** for automated environments
6. **Test CLI commands** in development before production
7. **Monitor token expiry** and regenerate as needed
8. **Use quiet mode** for automated scripts
9. **Enable debug mode** only when troubleshooting
10. **Keep CLI updated** to the latest version

Future Features
---------------

Planned CLI enhancements:

- JSON output format
- Quiet mode
- Token caching
- Configuration file support
- Multiple environment management
- Token validation
- Batch operations
- Shell completion
- Color output options
- Progress indicators

See Also
--------

- :doc:`quickstart` - Getting started guide
- :doc:`configuration` - Configuration options
- :doc:`troubleshooting` - Troubleshooting guide
- :doc:`api/client` - Python API reference
