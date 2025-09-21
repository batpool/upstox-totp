Troubleshooting Guide
=====================

This guide helps you diagnose and resolve common issues with the Upstox TOTP SDK.

Quick Diagnosis
---------------

Environment Check
~~~~~~~~~~~~~~~~~

First, always check your environment configuration:

.. code-block:: bash

   # Use the CLI to check configuration
   upstox_cli check-env

.. code-block:: python

   # Or programmatically
   from upstox_totp import UpstoxTOTP, ConfigurationError

   try:
       upx = UpstoxTOTP()
       print("✅ Configuration is valid")
   except ConfigurationError as e:
       print(f"❌ Configuration error: {e}")

Debug Mode
~~~~~~~~~~

Enable debug mode for detailed error information:

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Enable debug logging
   upx = UpstoxTOTP(debug=True)

.. code-block:: bash

   # Or via environment variable
   export UPSTOX_DEBUG=true
   upstox_cli generate-token

Common Issues
-------------

Configuration Errors
~~~~~~~~~~~~~~~~~~~~

**Missing Environment Variables**

*Error:*
.. code-block:: text

   ConfigurationError: Missing required environment variables: UPSTOX_USERNAME, UPSTOX_PASSWORD

*Solution:*

.. code-block:: bash

   # Check which variables are set
   env | grep UPSTOX

   # Set missing variables
   export UPSTOX_USERNAME=9876543210
   export UPSTOX_PASSWORD=your-password
   # ... other variables

   # Or create .env file
   cat > .env << EOF
   UPSTOX_USERNAME=9876543210
   UPSTOX_PASSWORD=your-password
   UPSTOX_PIN_CODE=1234
   UPSTOX_TOTP_SECRET=JBSWY3DPEHPK3PXP
   UPSTOX_CLIENT_ID=your-client-id
   UPSTOX_CLIENT_SECRET=your-client-secret
   UPSTOX_REDIRECT_URI=https://your-app.com/callback
   EOF

**Invalid Username Format**

*Error:*
.. code-block:: text

   ValidationError: Username must be exactly 10 digits

*Solution:*

.. code-block:: bash

   # Use your 10-digit mobile number (without country code)
   # Wrong: +919876543210, 919876543210
   # Right: 9876543210
   export UPSTOX_USERNAME=9876543210

**Invalid TOTP Secret**

*Error:*
.. code-block:: text

   ValidationError: Invalid TOTP secret format

*Solution:*

.. code-block:: bash

   # Ensure TOTP secret is base32 encoded without spaces
   # Wrong: "JBSW Y3DP EHPK 3PXP"
   # Right: "JBSWY3DPEHPK3PXP"
   export UPSTOX_TOTP_SECRET=JBSWY3DPEHPK3PXP

   # Test TOTP generation
   python -c "
   import pyotp
   totp = pyotp.TOTP('JBSWY3DPEHPK3PXP')
   print(f'TOTP: {totp.now()}')
   "

Authentication Errors
~~~~~~~~~~~~~~~~~~~~~

**Invalid Credentials**

*Error:*
.. code-block:: text

   Token generation failed: Invalid credentials provided

*Solutions:*

1. **Verify Username:**
   
   .. code-block:: bash
   
      # Must be 10-digit mobile number
      # Check in Upstox app: Profile → Settings → Personal Details
      echo $UPSTOX_USERNAME

2. **Verify Password:**
   
   .. code-block:: bash
   
      # Try logging into Upstox web platform manually
      # If login fails, reset password

3. **Verify PIN:**
   
   .. code-block:: bash
   
      # Usually 4-6 digits
      # Check in Upstox app: Profile → Settings → Security

**TOTP Validation Failed**

*Error:*
.. code-block:: text

   TOTP validation failed

*Solutions:*

1. **Check TOTP Secret:**
   
   .. code-block:: python
   
      import pyotp
      
      # Test TOTP generation
      secret = "YOUR_TOTP_SECRET"
      totp = pyotp.TOTP(secret)
      current_code = totp.now()
      print(f"Generated TOTP: {current_code}")
      
      # Compare with your authenticator app

2. **Check System Time:**
   
   .. code-block:: bash
   
      # TOTP is time-sensitive
      # Ensure system time is accurate
      date
      
      # Sync time (Linux)
      sudo ntpdate -s time.nist.gov
      
      # Sync time (macOS)
      sudo sntp -sS time.apple.com

3. **Try Different TOTP Window:**
   
   .. code-block:: python
   
      import pyotp
      import time
      
      secret = "YOUR_TOTP_SECRET"
      totp = pyotp.TOTP(secret)
      
      # Try current and next window
      for i in range(3):
          code = totp.at(time.time() + (i * 30))
          print(f"TOTP window {i}: {code}")

OAuth Errors
~~~~~~~~~~~~

**Invalid Client ID/Secret**

*Error:*
.. code-block:: text

   OAuth error: invalid_client

*Solutions:*

1. **Verify Client Credentials:**
   
   .. code-block:: bash
   
      # Check Upstox Developer Console
      # https://developer.upstox.com/
      echo "Client ID: $UPSTOX_CLIENT_ID"
      echo "Client Secret: $UPSTOX_CLIENT_SECRET"

2. **Check App Status:**
   
   - Login to Upstox Developer Console
   - Verify app is approved and active
   - Check API limits and restrictions

**Redirect URI Mismatch**

*Error:*
.. code-block:: text

   OAuth error: redirect_uri_mismatch

*Solution:*

.. code-block:: bash

   # Redirect URI must exactly match app settings
   # Check in Upstox Developer Console → Your App → Settings
   
   # Common mistakes:
   # Wrong: http://localhost:8080 (missing slash)
   # Right: http://localhost:8080/
   
   # Wrong: https://myapp.com/callback/ (extra slash)
   # Right: https://myapp.com/callback
   
   export UPSTOX_REDIRECT_URI=https://your-app.com/callback

Network Errors
~~~~~~~~~~~~~~

**Connection Timeout**

*Error:*
.. code-block:: text

   requests.exceptions.ConnectTimeout: HTTPSConnectionPool

*Solutions:*

1. **Check Internet Connection:**
   
   .. code-block:: bash
   
      # Test connectivity
      ping api.upstox.com
      curl -I https://api.upstox.com

2. **Configure Proxy:**
   
   .. code-block:: python
   
      from upstox_totp import UpstoxTOTP
      
      upx = UpstoxTOTP()
      upx.session.proxies = {
          'http': 'http://proxy.company.com:8080',
          'https': 'https://proxy.company.com:8080'
      }

3. **Increase Timeout:**
   
   .. code-block:: python
   
      from upstox_totp import UpstoxTOTP
      
      upx = UpstoxTOTP()
      upx.session.timeout = (30, 60)  # (connect, read) timeout

**SSL Certificate Errors**

*Error:*
.. code-block:: text

   requests.exceptions.SSLError: certificate verify failed

*Solutions:*

1. **Update Certificates:**
   
   .. code-block:: bash
   
      # Update certificates
      pip install --upgrade certifi
      
      # Or system-wide (Ubuntu)
      sudo apt-get update && sudo apt-get install ca-certificates

2. **Check System Time:**
   
   .. code-block:: bash
   
      # Ensure system time is correct
      date

**Rate Limiting**

*Error:*
.. code-block:: text

   HTTP 429: Too Many Requests

*Solution:*

.. code-block:: python

   import time
   from upstox_totp import UpstoxTOTP

   def get_token_with_backoff(max_retries=3):
       for attempt in range(max_retries):
           try:
               upx = UpstoxTOTP()
               response = upx.app_token.get_access_token()
               
               if response.success:
                   return response.data.access_token
               
           except Exception as e:
               if "429" in str(e) and attempt < max_retries - 1:
                   delay = 2 ** attempt  # Exponential backoff
                   print(f"Rate limited, waiting {delay} seconds...")
                   time.sleep(delay)
               else:
                   raise

Installation Issues
~~~~~~~~~~~~~~~~~~~

**Package Not Found**

*Error:*
.. code-block:: text

   No module named 'upstox_totp'

*Solutions:*

.. code-block:: bash

   # Check if package is installed
   pip list | grep upstox

   # Install package
   pip install upstox-totp

   # Check Python path
   python -c "import sys; print(sys.path)"

   # Use virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   pip install upstox-totp

**Permission Denied**

*Error:*
.. code-block:: text

   PermissionError: [Errno 13] Permission denied

*Solutions:*

.. code-block:: bash

   # Install for user only
   pip install --user upstox-totp

   # Or use virtual environment
   python -m venv venv
   source venv/bin/activate
   pip install upstox-totp

**CLI Command Not Found**

*Error:*
.. code-block:: text

   upstox_cli: command not found

*Solutions:*

.. code-block:: bash

   # Check if command is in PATH
   which upstox_cli

   # Find installation location
   pip show upstox-totp

   # Use full path
   python -m upstox_totp.cli check-env

   # Add to PATH
   export PATH=$PATH:/path/to/python/scripts

Token Issues
~~~~~~~~~~~~

**Token Expires Quickly**

*Issue:* Token seems to expire faster than expected

*Solution:*

.. code-block:: python

   import jwt
   from datetime import datetime

   def check_token_expiry(token):
       # Decode token to check expiry
       decoded = jwt.decode(token, options={"verify_signature": False})
       
       if 'exp' in decoded:
           exp_time = datetime.fromtimestamp(decoded['exp'])
           now = datetime.now()
           
           print(f"Token expires at: {exp_time}")
           print(f"Current time: {now}")
           print(f"Time remaining: {exp_time - now}")

   # Check your token
   check_token_expiry(your_token)

**Invalid Token Format**

*Error:*
.. code-block:: text

   Invalid token format

*Solution:*

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()

   if response.success and response.data:
       token = response.data.access_token
       
       # Verify token format
       if token.startswith('eyJ'):
           print("✅ Valid JWT token format")
       else:
           print("❌ Invalid token format")
       
       # Check token length
       if len(token) > 100:
           print("✅ Token has reasonable length")
       else:
           print("⚠️ Token seems too short")

Platform-Specific Issues
------------------------

Windows Issues
~~~~~~~~~~~~~~

**Path Separators**

.. code-block:: python

   import os
   from upstox_totp import UpstoxTOTP

   # Use os.path.join for cross-platform paths
   env_file = os.path.join("config", ".env")
   upx = UpstoxTOTP.from_env_file(env_file)

**Environment Variables**

.. code-block:: batch

   REM Set environment variables in Windows
   set UPSTOX_USERNAME=9876543210
   set UPSTOX_PASSWORD=your-password

   REM Or permanently
   setx UPSTOX_USERNAME "9876543210"

macOS Issues
~~~~~~~~~~~~

**Certificate Issues**

.. code-block:: bash

   # Update certificates on macOS
   /Applications/Python\ 3.x/Install\ Certificates.command

   # Or install certificates manually
   pip install --upgrade certifi

Linux Issues
~~~~~~~~~~~~

**SSL Context Issues**

.. code-block:: bash

   # Update CA certificates
   sudo apt-get update
   sudo apt-get install ca-certificates

   # Or for CentOS/RHEL
   sudo yum update ca-certificates

Docker Issues
~~~~~~~~~~~~~

**Environment Variables**

.. code-block:: dockerfile

   # Pass environment variables to container
   FROM python:3.12
   
   # Install package
   RUN pip install upstox-totp
   
   # Use .env file
   COPY .env /app/.env
   WORKDIR /app

.. code-block:: bash

   # Run with environment file
   docker run --env-file .env your-image

**Network Issues**

.. code-block:: dockerfile

   # Add DNS configuration if needed
   FROM python:3.12
   
   RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

Advanced Debugging
------------------

Enable All Logging
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP

   # Enable all debug logging
   logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )

   # Enable HTTP debugging
   import urllib3
   urllib3.disable_warnings()

   # Enable requests debugging
   import http.client as http_client
   http_client.HTTPConnection.debuglevel = 1

   upx = UpstoxTOTP(debug=True)

Network Traffic Analysis
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   import requests

   # Create session with event hooks
   class DebuggingUpstoxTOTP(UpstoxTOTP):
       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           
           # Add request/response hooks
           self.session.hooks['response'].append(self.log_response)

       def log_response(self, response, *args, **kwargs):
           print(f"Request: {response.request.method} {response.request.url}")
           print(f"Status: {response.status_code}")
           print(f"Headers: {dict(response.headers)}")
           
           if response.status_code >= 400:
               print(f"Error response: {response.text}")

   # Usage
   upx = DebuggingUpstoxTOTP(debug=True)

Memory and Performance Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import tracemalloc
   import time
   from upstox_totp import UpstoxTOTP

   def profile_memory_usage():
       tracemalloc.start()
       
       # Measure memory before
       snapshot1 = tracemalloc.take_snapshot()
       
       # Generate token
       upx = UpstoxTOTP()
       response = upx.app_token.get_access_token()
       
       # Measure memory after
       snapshot2 = tracemalloc.take_snapshot()
       
       # Compare
       top_stats = snapshot2.compare_to(snapshot1, 'lineno')
       
       print("Memory usage:")
       for stat in top_stats[:10]:
           print(stat)

   profile_memory_usage()

Testing Configuration
---------------------

Configuration Validation Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   """
   Comprehensive configuration validation script
   """
   
   import os
   import sys
   from upstox_totp import UpstoxTOTP, ConfigurationError, ValidationError

   def validate_environment():
       """Validate environment configuration."""
       print("🔍 Validating Upstox TOTP configuration...\n")
       
       # Check required environment variables
       required_vars = [
           'UPSTOX_USERNAME',
           'UPSTOX_PASSWORD', 
           'UPSTOX_PIN_CODE',
           'UPSTOX_TOTP_SECRET',
           'UPSTOX_CLIENT_ID',
           'UPSTOX_CLIENT_SECRET',
           'UPSTOX_REDIRECT_URI'
       ]
       
       print("📋 Environment Variables:")
       missing_vars = []
       for var in required_vars:
           value = os.getenv(var)
           if value:
               if 'PASSWORD' in var or 'SECRET' in var:
                   print(f"  ✅ {var}: ******** (length: {len(value)})")
               else:
                   masked_value = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '****'
                   print(f"  ✅ {var}: {masked_value}")
           else:
               print(f"  ❌ {var}: Not set")
               missing_vars.append(var)
       
       if missing_vars:
           print(f"\n❌ Missing variables: {', '.join(missing_vars)}")
           return False
       
       # Test TOTP generation
       print("\n🔐 Testing TOTP generation:")
       try:
           import pyotp
           secret = os.getenv('UPSTOX_TOTP_SECRET')
           totp = pyotp.TOTP(secret)
           code = totp.now()
           print(f"  ✅ TOTP generated: {code}")
       except Exception as e:
           print(f"  ❌ TOTP generation failed: {e}")
           return False
       
       # Test client initialization
       print("\n🚀 Testing client initialization:")
       try:
           upx = UpstoxTOTP()
           print("  ✅ Client initialized successfully")
       except ConfigurationError as e:
           print(f"  ❌ Configuration error: {e}")
           return False
       except ValidationError as e:
           print(f"  ❌ Validation error: {e}")
           return False
       except Exception as e:
           print(f"  ❌ Unexpected error: {e}")
           return False
       
       print("\n✅ All configuration checks passed!")
       return True

   def test_connectivity():
       """Test network connectivity."""
       print("\n🌐 Testing network connectivity:")
       
       import requests
       try:
           response = requests.get('https://api.upstox.com', timeout=10)
           print(f"  ✅ Upstox API reachable (status: {response.status_code})")
       except Exception as e:
           print(f"  ❌ Network error: {e}")
           return False
       
       return True

   def main():
       """Main validation function."""
       print("=" * 50)
       print("  Upstox TOTP Configuration Validator")
       print("=" * 50)
       
       if not validate_environment():
           print("\n💡 To fix configuration issues:")
           print("  1. Create .env file with required variables")
           print("  2. Run: upstox_cli check-env")
           print("  3. Verify credentials in Upstox app")
           sys.exit(1)
       
       if not test_connectivity():
           print("\n💡 To fix network issues:")
           print("  1. Check internet connection")
           print("  2. Verify firewall settings")
           print("  3. Check proxy configuration")
           sys.exit(1)
       
       print("\n🎉 Configuration is valid and ready for use!")

   if __name__ == "__main__":
       main()

Save this as `validate_config.py` and run:

.. code-block:: bash

   python validate_config.py

Performance Testing
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   """
   Performance testing script
   """
   
   import time
   import statistics
   from upstox_totp import UpstoxTOTP

   def benchmark_token_generation(num_runs=5):
       """Benchmark token generation performance."""
       print(f"🚀 Benchmarking token generation ({num_runs} runs)...")
       
       times = []
       success_count = 0
       
       for i in range(num_runs):
           start_time = time.time()
           
           try:
               upx = UpstoxTOTP()
               response = upx.app_token.get_access_token()
               
               if response.success:
                   success_count += 1
                   
           except Exception as e:
               print(f"  Run {i+1} failed: {e}")
               continue
               
           end_time = time.time()
           duration = end_time - start_time
           times.append(duration)
           
           print(f"  Run {i+1}: {duration:.2f}s")
       
       if times:
           print(f"\n📊 Performance Results:")
           print(f"  Success rate: {success_count}/{num_runs} ({success_count/num_runs*100:.1f}%)")
           print(f"  Average time: {statistics.mean(times):.2f}s")
           print(f"  Min time: {min(times):.2f}s")
           print(f"  Max time: {max(times):.2f}s")
           if len(times) > 1:
               print(f"  Std deviation: {statistics.stdev(times):.2f}s")

   if __name__ == "__main__":
       benchmark_token_generation()

Getting Help
------------

Self-Help Resources
~~~~~~~~~~~~~~~~~~~

1. **Check this troubleshooting guide thoroughly**
2. **Run the environment validator script**
3. **Enable debug mode for detailed error messages**
4. **Search existing GitHub issues**

Community Support
~~~~~~~~~~~~~~~~~

- **GitHub Issues**: https://github.com/batpool/upstox-totp/issues
- **Discussions**: https://github.com/batpool/upstox-totp/discussions  
- **Reddit**: https://www.reddit.com/user/iamdeadloop/

When Reporting Issues
~~~~~~~~~~~~~~~~~~~~~

Please include:

1. **Environment information:**
   
   .. code-block:: bash
   
      python --version
      pip show upstox-totp
      uname -a  # or systeminfo on Windows

2. **Configuration (without sensitive data):**
   
   .. code-block:: bash
   
      upstox_cli check-env

3. **Error messages and stack traces**

4. **Steps to reproduce the issue**

5. **Expected vs actual behavior**

**Template for issue reports:**

.. code-block:: text

   ## Environment
   - OS: [e.g., Ubuntu 20.04, Windows 10, macOS 12]
   - Python version: [e.g., 3.12.0]
   - upstox-totp version: [e.g., 1.0.3]
   
   ## Problem Description
   [Describe what you were trying to do and what went wrong]
   
   ## Steps to Reproduce
   1. [First step]
   2. [Second step]
   3. [etc.]
   
   ## Expected Behavior
   [What you expected to happen]
   
   ## Actual Behavior
   [What actually happened]
   
   ## Error Messages
   ```
   [Paste any error messages here]
   ```
   
   ## Configuration Check
   ```
   [Output of: upstox_cli check-env]
   ```
   
   ## Additional Context
   [Any other relevant information]

Emergency Contacts
~~~~~~~~~~~~~~~~~~

For critical security issues:

- **Security vulnerabilities**: Use GitHub Security tab
- **Upstox API issues**: Contact Upstox support directly
- **Trading platform issues**: Contact your broker

Recovery Procedures
-------------------

Complete Reset
~~~~~~~~~~~~~~

If all else fails, try a complete reset:

.. code-block:: bash

   # 1. Backup current configuration
   cp .env .env.backup

   # 2. Remove all upstox-totp related files
   rm -f .env upstox_token.* *.log

   # 3. Uninstall and reinstall package
   pip uninstall upstox-totp
   pip install upstox-totp

   # 4. Recreate configuration from scratch
   upstox_cli check-env  # This will show what's missing

   # 5. Test with minimal configuration
   cat > .env << EOF
   UPSTOX_USERNAME=your-username
   UPSTOX_PASSWORD=your-password
   UPSTOX_PIN_CODE=your-pin
   UPSTOX_TOTP_SECRET=your-secret
   UPSTOX_CLIENT_ID=your-client-id
   UPSTOX_CLIENT_SECRET=your-secret
   UPSTOX_REDIRECT_URI=your-uri
   EOF

   # 6. Test step by step
   upstox_cli check-env
   upstox_cli generate-token

Credential Reset
~~~~~~~~~~~~~~~~

If you suspect credential issues:

1. **Reset Upstox password** via web platform
2. **Regenerate TOTP secret** in Upstox app
3. **Create new Developer App** if needed
4. **Update all environment variables**
5. **Test with new credentials**

See Also
--------

- :doc:`quickstart` - Getting started guide
- :doc:`configuration` - Configuration options
- :doc:`security` - Security best practices
- :doc:`api/errors` - Error handling reference
- :doc:`cli_reference` - CLI tool usage
