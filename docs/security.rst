Security Best Practices
=======================

This guide covers security considerations and best practices when using the Upstox TOTP SDK.

Overview
--------

The Upstox TOTP SDK handles sensitive financial data and credentials. Following security best practices is essential to protect your trading account and API access.

Credential Security
-------------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

**✅ Do:**

.. code-block:: bash

   # Use environment variables
   export UPSTOX_USERNAME=9876543210
   export UPSTOX_PASSWORD=secure-password
   export UPSTOX_PIN_CODE=1234
   export UPSTOX_TOTP_SECRET=JBSWY3DPEHPK3PXP
   export UPSTOX_CLIENT_ID=your-client-id
   export UPSTOX_CLIENT_SECRET=your-client-secret

**❌ Don't:**

.. code-block:: python

   # Never hardcode credentials in source code
   upx = UpstoxTOTP(
       username="9876543210",
       password=SecretStr("my-password"),  # Don't do this!
       # ...
   )

.env Files
~~~~~~~~~~

**✅ Do:**

.. code-block:: bash

   # Create .env file with proper permissions
   touch .env
   chmod 600 .env  # Owner read/write only

   # Add to .gitignore
   echo ".env" >> .gitignore
   echo ".env.*" >> .gitignore

**❌ Don't:**

.. code-block:: bash

   # Never commit .env files
   git add .env  # Don't do this!

File Permissions
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Secure configuration files
   chmod 600 .env
   chmod 600 config.json
   chmod 700 ~/.upstox/

   # Check permissions
   ls -la .env
   # Should show: -rw------- (600)

Version Control Security
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
   
   # Configuration files
   config.json
   secrets.yaml
   credentials.ini
   
   # Token caches
   *.token
   upstox_token.json
   token_cache/
   
   # Logs with sensitive data
   debug.log
   upstox.log

SecretStr Usage
---------------

The SDK uses Pydantic's SecretStr to protect sensitive data:

.. code-block:: python

   from pydantic import SecretStr
   from upstox_totp import UpstoxTOTP

   # SecretStr automatically masks values in logs
   password = SecretStr("my-password")
   print(password)  # Output: SecretStr('**********')

   # Access actual value only when needed
   actual_password = password.get_secret_value()

   # Use with UpstoxTOTP
   upx = UpstoxTOTP(
       username="9876543210",
       password=password,  # Automatically protected
       # ...
   )

Token Security
--------------

Token Storage
~~~~~~~~~~~~~

**✅ Secure storage:**

.. code-block:: python

   import json
   import os
   from cryptography.fernet import Fernet

   class SecureTokenStorage:
       def __init__(self, key_file="token.key", token_file="token.enc"):
           self.key_file = key_file
           self.token_file = token_file
           self.key = self._load_or_create_key()
           self.cipher = Fernet(self.key)

       def _load_or_create_key(self):
           if os.path.exists(self.key_file):
               with open(self.key_file, 'rb') as f:
                   return f.read()
           else:
               key = Fernet.generate_key()
               with open(self.key_file, 'wb') as f:
                   f.write(key)
               os.chmod(self.key_file, 0o600)
               return key

       def store_token(self, token):
           encrypted_token = self.cipher.encrypt(token.encode())
           with open(self.token_file, 'wb') as f:
               f.write(encrypted_token)
           os.chmod(self.token_file, 0o600)

       def load_token(self):
           if not os.path.exists(self.token_file):
               return None
           
           with open(self.token_file, 'rb') as f:
               encrypted_token = f.read()
           
           decrypted_token = self.cipher.decrypt(encrypted_token)
           return decrypted_token.decode()

   # Usage
   storage = SecureTokenStorage()
   
   # Store token securely
   from upstox_totp import UpstoxTOTP
   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()
   if response.success:
       storage.store_token(response.data.access_token)

**❌ Insecure storage:**

.. code-block:: python

   # Don't store tokens in plain text
   with open('token.txt', 'w') as f:
       f.write(token)  # Insecure!

   # Don't log tokens
   print(f"Token: {token}")  # Don't do this!

Token Expiry
~~~~~~~~~~~~

.. code-block:: python

   import jwt
   from datetime import datetime, timedelta

   def check_token_expiry(token):
       """Check if token is close to expiry."""
       try:
           # Decode without verification to check expiry
           decoded = jwt.decode(token, options={"verify_signature": False})
           
           if 'exp' in decoded:
               exp_time = datetime.fromtimestamp(decoded['exp'])
               now = datetime.now()
               
               # Check if token expires within 1 hour
               if exp_time - now < timedelta(hours=1):
                   return True, "Token expires soon"
               
               return False, f"Token valid until {exp_time}"
           
           return None, "No expiry information in token"
           
       except jwt.DecodeError:
           return None, "Invalid token format"

   # Usage
   needs_refresh, message = check_token_expiry(token)
   if needs_refresh:
       # Refresh token proactively
       new_response = upx.app_token.get_access_token()

Token Cleanup
~~~~~~~~~~~~~

.. code-block:: python

   import gc

   def secure_token_cleanup(token_var):
       """Securely clear token from memory."""
       if token_var:
           # Overwrite memory (Python doesn't guarantee this)
           token_var = 'x' * len(token_var)
           del token_var
           gc.collect()

   # Usage
   token = response.data.access_token
   # Use token...
   
   # Clean up when done
   secure_token_cleanup(token)
   token = None

Network Security
----------------

HTTPS Only
~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   import requests

   # Verify SSL certificates (default behavior)
   upx = UpstoxTOTP()
   
   # Don't disable SSL verification
   # upx.session.verify = False  # Never do this!

   # Use proper SSL context if needed
   import ssl
   context = ssl.create_default_context()
   context.check_hostname = True
   context.verify_mode = ssl.CERT_REQUIRED

Custom Session Security
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   from requests.adapters import HTTPAdapter
   from urllib3.util.ssl_ import create_urllib3_context

   class SecureHTTPAdapter(HTTPAdapter):
       def init_poolmanager(self, *args, **kwargs):
           ctx = create_urllib3_context()
           ctx.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')
           kwargs['ssl_context'] = ctx
           return super().init_poolmanager(*args, **kwargs)

   upx = UpstoxTOTP()
   upx.session.mount('https://', SecureHTTPAdapter())

Request Headers Security
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()

   # Remove potentially identifying headers
   upx.session.headers.update({
       'User-Agent': 'TradingApp/1.0',  # Use generic user agent
       'X-Forwarded-For': '',          # Don't expose IP
       'X-Real-IP': ''                 # Don't expose real IP
   })

Production Security
-------------------

Secrets Management
~~~~~~~~~~~~~~~~~~

**AWS Secrets Manager:**

.. code-block:: python

   import boto3
   import json
   from upstox_totp import UpstoxTOTP
   from pydantic import SecretStr

   def get_upstox_credentials():
       """Get credentials from AWS Secrets Manager."""
       client = boto3.client('secretsmanager', region_name='us-east-1')
       
       try:
           response = client.get_secret_value(SecretId='upstox-credentials')
           secrets = json.loads(response['SecretString'])
           
           return UpstoxTOTP(
               username=secrets['username'],
               password=SecretStr(secrets['password']),
               pin_code=SecretStr(secrets['pin_code']),
               totp_secret=SecretStr(secrets['totp_secret']),
               client_id=secrets['client_id'],
               client_secret=SecretStr(secrets['client_secret']),
               redirect_uri=secrets['redirect_uri']
           )
           
       except Exception as e:
           raise Exception(f"Failed to get credentials: {e}")

**Azure Key Vault:**

.. code-block:: python

   from azure.keyvault.secrets import SecretClient
   from azure.identity import DefaultAzureCredential
   from upstox_totp import UpstoxTOTP
   from pydantic import SecretStr

   def get_upstox_from_keyvault():
       """Get credentials from Azure Key Vault."""
       credential = DefaultAzureCredential()
       client = SecretClient(
           vault_url="https://your-vault.vault.azure.net/", 
           credential=credential
       )
       
       return UpstoxTOTP(
           username=client.get_secret("upstox-username").value,
           password=SecretStr(client.get_secret("upstox-password").value),
           pin_code=SecretStr(client.get_secret("upstox-pin").value),
           totp_secret=SecretStr(client.get_secret("upstox-totp-secret").value),
           client_id=client.get_secret("upstox-client-id").value,
           client_secret=SecretStr(client.get_secret("upstox-client-secret").value),
           redirect_uri=client.get_secret("upstox-redirect-uri").value
       )

Environment Isolation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from upstox_totp import UpstoxTOTP

   class EnvironmentManager:
       @staticmethod
       def get_client(environment='production'):
           """Get client for specific environment."""
           env_map = {
               'development': '.env.development',
               'staging': '.env.staging', 
               'production': '.env.production'
           }
           
           env_file = env_map.get(environment)
           if not env_file:
               raise ValueError(f"Unknown environment: {environment}")
           
           if not os.path.exists(env_file):
               raise FileNotFoundError(f"Environment file not found: {env_file}")
           
           return UpstoxTOTP.from_env_file(env_file)

   # Usage
   if os.getenv('ENV') == 'production':
       upx = EnvironmentManager.get_client('production')
   else:
       upx = EnvironmentManager.get_client('development')

Monitoring and Auditing
-----------------------

Security Logging
~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import hashlib
   from datetime import datetime
   from upstox_totp import UpstoxTOTP

   # Configure security logger
   security_logger = logging.getLogger('security')
   security_handler = logging.FileHandler('security.log')
   security_formatter = logging.Formatter(
       '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
   )
   security_handler.setFormatter(security_formatter)
   security_logger.addHandler(security_handler)
   security_logger.setLevel(logging.INFO)

   class SecureUpstoxClient:
       def __init__(self):
           self.upx = UpstoxTOTP()
           self.session_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]

       def get_token(self):
           """Get token with security logging."""
           security_logger.info(f"Token generation started - Session: {self.session_id}")
           
           try:
               response = self.upx.app_token.get_access_token()
               
               if response.success:
                   security_logger.info(f"Token generation successful - Session: {self.session_id}")
                   return response.data.access_token
               else:
                   security_logger.warning(f"Token generation failed - Session: {self.session_id}")
                   return None
                   
           except Exception as e:
               security_logger.error(f"Token generation error - Session: {self.session_id} - Error: {str(e)}")
               raise

Rate Limiting
~~~~~~~~~~~~~

.. code-block:: python

   import time
   from collections import defaultdict
   from datetime import datetime, timedelta

   class RateLimiter:
       def __init__(self, max_requests=10, time_window=60):
           self.max_requests = max_requests
           self.time_window = time_window
           self.requests = defaultdict(list)

       def allow_request(self, identifier):
           """Check if request is allowed under rate limit."""
           now = datetime.now()
           user_requests = self.requests[identifier]
           
           # Remove old requests
           cutoff = now - timedelta(seconds=self.time_window)
           user_requests[:] = [req_time for req_time in user_requests if req_time > cutoff]
           
           if len(user_requests) >= self.max_requests:
               return False
           
           user_requests.append(now)
           return True

   class RateLimitedUpstoxClient:
       def __init__(self, user_id):
           self.upx = UpstoxTOTP()
           self.user_id = user_id
           self.rate_limiter = RateLimiter(max_requests=5, time_window=300)  # 5 requests per 5 minutes

       def get_token(self):
           """Get token with rate limiting."""
           if not self.rate_limiter.allow_request(self.user_id):
               raise Exception("Rate limit exceeded. Please try again later.")
           
           return self.upx.app_token.get_access_token()

Access Control
~~~~~~~~~~~~~~

.. code-block:: python

   import os
   import stat
   from pathlib import Path

   def secure_file_permissions(filepath):
       """Set secure permissions on sensitive files."""
       path = Path(filepath)
       
       # Owner read/write only (600)
       path.chmod(stat.S_IRUSR | stat.S_IWUSR)
       
       # Verify permissions
       file_stat = path.stat()
       mode = stat.filemode(file_stat.st_mode)
       
       if mode != '-rw-------':
           raise Exception(f"Failed to set secure permissions on {filepath}")

   # Usage
   secure_file_permissions('.env')
   secure_file_permissions('token.json')

Incident Response
-----------------

Security Breach Detection
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import hashlib
   import json
   from datetime import datetime

   class SecurityMonitor:
       def __init__(self):
           self.config_hash = None
           self.last_token_time = None

       def check_config_integrity(self, config_file='.env'):
           """Check if configuration file has been tampered with."""
           try:
               with open(config_file, 'r') as f:
                   content = f.read()
               
               current_hash = hashlib.sha256(content.encode()).hexdigest()
               
               if self.config_hash is None:
                   self.config_hash = current_hash
                   return True
               
               if current_hash != self.config_hash:
                   self._log_security_incident("Configuration file modified")
                   return False
               
               return True
               
           except Exception as e:
               self._log_security_incident(f"Config check failed: {e}")
               return False

       def check_unusual_activity(self):
           """Check for unusual token generation patterns."""
           now = datetime.now()
           
           if self.last_token_time:
               time_diff = (now - self.last_token_time).total_seconds()
               
               # Alert if tokens generated too frequently
               if time_diff < 30:  # Less than 30 seconds
                   self._log_security_incident("Frequent token generation detected")
           
           self.last_token_time = now

       def _log_security_incident(self, message):
           """Log security incident."""
           incident = {
               'timestamp': datetime.now().isoformat(),
               'message': message,
               'severity': 'HIGH'
           }
           
           with open('security_incidents.log', 'a') as f:
               f.write(json.dumps(incident) + '\n')

   # Usage
   monitor = SecurityMonitor()

   # Check before token generation
   if monitor.check_config_integrity():
       monitor.check_unusual_activity()
       # Proceed with token generation
   else:
       # Handle security incident
       raise Exception("Security check failed")

Credential Rotation
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from datetime import datetime, timedelta
   import json

   class CredentialRotationManager:
       def __init__(self, rotation_file='last_rotation.json'):
           self.rotation_file = rotation_file

       def needs_rotation(self, days=90):
           """Check if credentials need rotation."""
           try:
               with open(self.rotation_file, 'r') as f:
                   data = json.load(f)
               
               last_rotation = datetime.fromisoformat(data['last_rotation'])
               
               if datetime.now() - last_rotation > timedelta(days=days):
                   return True
               
               return False
               
           except (FileNotFoundError, KeyError, ValueError):
               # No rotation record, assume needs rotation
               return True

       def record_rotation(self):
           """Record that credentials were rotated."""
           data = {
               'last_rotation': datetime.now().isoformat(),
               'rotated_by': 'automated_system'
           }
           
           with open(self.rotation_file, 'w') as f:
               json.dump(data, f, indent=2)

       def alert_rotation_needed(self):
           """Alert that credential rotation is needed."""
           print("⚠️  SECURITY ALERT: Credentials need rotation")
           print("Please update your Upstox password and regenerate TOTP secret")

   # Usage
   rotation_manager = CredentialRotationManager()

   if rotation_manager.needs_rotation():
       rotation_manager.alert_rotation_needed()
       # Implement rotation process

Testing Security
----------------

Security Test Cases
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   import os
   from upstox_totp import UpstoxTOTP, ConfigurationError

   def test_no_credentials_in_logs(caplog):
       """Ensure credentials don't appear in logs."""
       upx = UpstoxTOTP(debug=True)
       
       # Generate token with debug logging
       try:
           response = upx.app_token.get_access_token()
       except:
           pass  # Error is fine, we're testing logging
       
       # Check logs don't contain sensitive data
       log_output = caplog.text.lower()
       
       assert 'password' not in log_output
       assert 'secret' not in log_output
       assert 'pin' not in log_output

   def test_secretstr_masking():
       """Test that SecretStr properly masks sensitive data."""
       from pydantic import SecretStr
       
       secret = SecretStr("sensitive-data")
       str_repr = str(secret)
       
       assert "sensitive-data" not in str_repr
       assert "**********" in str_repr

   def test_environment_variable_isolation():
       """Test that environment variables are properly isolated."""
       # Backup original environment
       original_env = dict(os.environ)
       
       try:
           # Clear sensitive variables
           for key in list(os.environ.keys()):
               if key.startswith('UPSTOX_'):
                   del os.environ[key]
           
           # Should fail without credentials
           with pytest.raises(ConfigurationError):
               UpstoxTOTP()
               
       finally:
           # Restore environment
           os.environ.clear()
           os.environ.update(original_env)

Penetration Testing
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   from upstox_totp import UpstoxTOTP

   def test_ssl_security():
       """Test SSL/TLS configuration."""
       upx = UpstoxTOTP()
       session = upx.session
       
       # Test that SSL verification is enabled
       assert session.verify is True
       
       # Test that session uses secure protocols
       adapter = session.get_adapter('https://')
       assert hasattr(adapter, 'init_poolmanager')

   def test_request_headers():
       """Test that request headers don't leak sensitive information."""
       upx = UpstoxTOTP()
       
       # Check default headers
       headers = dict(upx.session.headers)
       
       # Ensure no sensitive data in headers
       sensitive_patterns = ['password', 'secret', 'key', 'token']
       for header_name, header_value in headers.items():
           for pattern in sensitive_patterns:
               assert pattern.lower() not in header_name.lower()
               assert pattern.lower() not in str(header_value).lower()

Security Checklist
------------------

Configuration Security
~~~~~~~~~~~~~~~~~~~~~~

- [ ] Use environment variables for all credentials
- [ ] Never hardcode secrets in source code
- [ ] Set proper file permissions (600) on configuration files
- [ ] Add all sensitive files to .gitignore
- [ ] Use different credentials for different environments
- [ ] Regularly rotate credentials (every 90 days)

Application Security
~~~~~~~~~~~~~~~~~~~~

- [ ] Enable SSL certificate verification
- [ ] Use SecretStr for sensitive data
- [ ] Implement proper error handling (don't leak sensitive info)
- [ ] Clear sensitive data from memory when possible
- [ ] Use secure random number generation for session IDs
- [ ] Implement rate limiting for token generation

Token Security
~~~~~~~~~~~~~~

- [ ] Store tokens securely (encrypted if possible)
- [ ] Monitor token expiry and refresh proactively
- [ ] Don't log tokens or include them in error messages
- [ ] Use HTTPS only for API calls
- [ ] Implement token validation
- [ ] Clear tokens from memory after use

Production Security
~~~~~~~~~~~~~~~~~~~

- [ ] Use secrets management services (AWS Secrets Manager, Azure Key Vault)
- [ ] Implement security monitoring and alerting
- [ ] Regularly audit access logs
- [ ] Use separate credentials for each environment
- [ ] Monitor for unusual access patterns
- [ ] Have an incident response plan

Compliance Considerations
-------------------------

Data Protection
~~~~~~~~~~~~~~~

- Follow data protection regulations (GDPR, CCPA)
- Minimize data collection and retention
- Implement proper data encryption
- Provide data access and deletion capabilities
- Document data processing activities

Financial Regulations
~~~~~~~~~~~~~~~~~~~~~

- Comply with financial industry standards
- Implement proper audit trails
- Ensure data integrity and availability
- Follow broker-specific security requirements
- Maintain transaction logs for compliance

Regular Security Reviews
------------------------

Monthly Tasks
~~~~~~~~~~~~~

- Review access logs for unusual activity
- Check for failed authentication attempts
- Verify SSL certificate validity
- Update dependencies with security patches
- Review and rotate API keys if needed

Quarterly Tasks
~~~~~~~~~~~~~~~

- Rotate all credentials
- Review and update security policies
- Conduct security testing
- Update incident response procedures
- Review third-party dependencies

Annual Tasks
~~~~~~~~~~~~

- Comprehensive security audit
- Penetration testing
- Review and update security architecture
- Staff security training
- Compliance assessment

Emergency Procedures
--------------------

Suspected Compromise
~~~~~~~~~~~~~~~~~~~~

1. **Immediately disable compromised credentials**
2. **Generate new API keys and TOTP secrets**
3. **Review all recent transactions**
4. **Check access logs for unauthorized activity**
5. **Notify Upstox of potential security incident**
6. **Update all affected systems with new credentials**
7. **Document the incident for future reference**

Data Breach Response
~~~~~~~~~~~~~~~~~~~~

1. **Contain the breach immediately**
2. **Assess the scope of compromised data**
3. **Notify relevant authorities if required**
4. **Inform affected users**
5. **Implement additional security measures**
6. **Monitor for further suspicious activity**
7. **Conduct post-incident review**

Contact Information
-------------------

- **SDK Issues**: https://github.com/batpool/upstox-totp/issues
- **Security Vulnerabilities**: Report privately via GitHub Security tab

See Also
--------

- :doc:`configuration` - Configuration guide
- :doc:`troubleshooting` - Troubleshooting guide
- :doc:`api/errors` - Error handling
- :doc:`examples/token_caching` - Secure token caching
