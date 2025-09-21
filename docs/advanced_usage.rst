Advanced Usage Guide
====================

This guide covers advanced features and patterns for using the Upstox TOTP Python SDK in production environments.

Context Managers
----------------

Automatic Resource Cleanup
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the context manager for automatic session cleanup:

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Automatic cleanup when exiting the context
   with UpstoxTOTP() as upx:
       response = upx.app_token.get_access_token()
       
       if response.success:
           access_token = response.data.access_token
           # Use token for API calls
           # Session is automatically cleaned up

Custom Context Manager
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from contextlib import contextmanager
   from upstox_totp import UpstoxTOTP
   import logging

   @contextmanager
   def upstox_client_with_logging():
       """Custom context manager with logging."""
       logging.info("Initializing Upstox client...")
       
       try:
           upx = UpstoxTOTP(debug=True)
           logging.info("Upstox client initialized successfully")
           yield upx
       except Exception as e:
           logging.error(f"Error with Upstox client: {e}")
           raise
       finally:
           logging.info("Cleaning up Upstox client...")

   # Usage
   with upstox_client_with_logging() as upx:
       response = upx.app_token.get_access_token()

Session Management
------------------

Custom Session Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   import requests

   # Initialize client
   upx = UpstoxTOTP()

   # Access underlying session
   session = upx.session

   # Configure session timeouts
   session.timeout = (10, 30)  # (connection, read) timeout

   # Add custom headers
   session.headers.update({
       'User-Agent': 'MyApp/1.0',
       'Accept-Language': 'en-US,en;q=0.9'
   })

   # Add retry adapter
   from requests.adapters import HTTPAdapter
   from urllib3.util.retry import Retry

   retry_strategy = Retry(
       total=3,
       backoff_factor=1,
       status_forcelist=[429, 500, 502, 503, 504],
   )

   adapter = HTTPAdapter(max_retries=retry_strategy)
   session.mount("http://", adapter)
   session.mount("https://", adapter)

Session Persistence
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pickle
   from upstox_totp import UpstoxTOTP

   class PersistentUpstoxClient:
       def __init__(self, session_file="upstox_session.pkl"):
           self.session_file = session_file
           self.upx = UpstoxTOTP()
           self.load_session()

       def load_session(self):
           """Load session from file if it exists."""
           try:
               with open(self.session_file, 'rb') as f:
                   session_data = pickle.load(f)
                   self.upx.session.cookies.update(session_data['cookies'])
                   self.upx.session.headers.update(session_data['headers'])
           except FileNotFoundError:
               pass

       def save_session(self):
           """Save session to file."""
           session_data = {
               'cookies': dict(self.upx.session.cookies),
               'headers': dict(self.upx.session.headers)
           }
           with open(self.session_file, 'wb') as f:
               pickle.dump(session_data, f)

       def get_token(self):
           """Get token and save session."""
           response = self.upx.app_token.get_access_token()
           self.save_session()
           return response

Reset Session
~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   upx = UpstoxTOTP()

   # Reset session (clears cookies, headers, etc.)
   upx.reset_session()

   # Generate new request ID for tracking
   request_id = upx.generate_request_id()
   print(f"Request ID: {request_id}")

TOTP Management
---------------

Manual TOTP Generation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP
   import time

   upx = UpstoxTOTP()

   # Generate current TOTP
   current_totp = upx.generate_totp_secret()
   print(f"Current TOTP: {current_totp}")

   # Wait for next TOTP cycle
   time.sleep(30)
   next_totp = upx.generate_totp_secret()
   print(f"Next TOTP: {next_totp}")

TOTP Validation
~~~~~~~~~~~~~~~

.. code-block:: python

   import pyotp
   from upstox_totp import UpstoxTOTP

   def validate_totp_secret(secret_key, test_code):
       """Validate if TOTP secret generates expected code."""
       totp = pyotp.TOTP(secret_key)
       current_code = totp.now()
       return current_code == test_code

   upx = UpstoxTOTP()
   secret = upx.totp_secret.get_secret_value()

   # Test with known code
   if validate_totp_secret(secret, "123456"):
       print("✅ TOTP secret is valid")
   else:
       print("❌ TOTP secret validation failed")

Error Handling and Retry Logic
------------------------------

Custom Error Handling
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP, UpstoxError, ConfigurationError
   import time
   import logging

   class RobustUpstoxClient:
       def __init__(self, max_retries=3, retry_delay=5):
           self.max_retries = max_retries
           self.retry_delay = retry_delay
           self.upx = UpstoxTOTP()

       def get_token_with_retry(self):
           """Get token with retry logic."""
           for attempt in range(1, self.max_retries + 1):
               try:
                   response = self.upx.app_token.get_access_token()
                   
                   if response.success and response.data:
                       logging.info(f"Token generated successfully on attempt {attempt}")
                       return response.data.access_token
                   else:
                       logging.warning(f"Attempt {attempt} failed: {response.error}")
                       
               except UpstoxError as e:
                   logging.error(f"Attempt {attempt} - Upstox error: {e}")
                   
               except Exception as e:
                   logging.error(f"Attempt {attempt} - Unexpected error: {e}")

               if attempt < self.max_retries:
                   logging.info(f"Retrying in {self.retry_delay} seconds...")
                   time.sleep(self.retry_delay)

           raise Exception(f"Failed to get token after {self.max_retries} attempts")

   # Usage
   client = RobustUpstoxClient()
   token = client.get_token_with_retry()

Exponential Backoff
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import random
   from upstox_totp import UpstoxTOTP

   def exponential_backoff_retry(func, max_retries=5, base_delay=1, max_delay=60):
       """Execute function with exponential backoff retry."""
       for attempt in range(max_retries):
           try:
               return func()
           except Exception as e:
               if attempt == max_retries - 1:
                   raise e
               
               # Calculate delay with jitter
               delay = min(base_delay * (2 ** attempt), max_delay)
               jitter = random.uniform(0.1, 0.9)
               actual_delay = delay * jitter
               
               print(f"Attempt {attempt + 1} failed: {e}")
               print(f"Retrying in {actual_delay:.2f} seconds...")
               time.sleep(actual_delay)

   # Usage
   def get_token():
       upx = UpstoxTOTP()
       response = upx.app_token.get_access_token()
       if not response.success:
           raise Exception(f"Token generation failed: {response.error}")
       return response.data.access_token

   token = exponential_backoff_retry(get_token)

Rate Limiting
-------------

Token Bucket Algorithm
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import threading
   from upstox_totp import UpstoxTOTP

   class RateLimitedUpstoxClient:
       def __init__(self, tokens_per_minute=10):
           self.upx = UpstoxTOTP()
           self.tokens_per_minute = tokens_per_minute
           self.tokens = tokens_per_minute
           self.last_refill = time.time()
           self.lock = threading.Lock()

       def _refill_tokens(self):
           """Refill tokens based on elapsed time."""
           now = time.time()
           elapsed = now - self.last_refill
           tokens_to_add = elapsed * (self.tokens_per_minute / 60.0)
           
           with self.lock:
               self.tokens = min(self.tokens_per_minute, 
                               self.tokens + tokens_to_add)
               self.last_refill = now

       def _acquire_token(self):
           """Acquire a token for rate limiting."""
           self._refill_tokens()
           
           with self.lock:
               if self.tokens >= 1:
                   self.tokens -= 1
                   return True
               return False

       def get_access_token(self):
           """Get access token with rate limiting."""
           while not self._acquire_token():
               time.sleep(0.1)  # Wait 100ms and try again
           
           return self.upx.app_token.get_access_token()

   # Usage
   client = RateLimitedUpstoxClient(tokens_per_minute=5)
   response = client.get_access_token()

Caching and Token Management
----------------------------

Advanced Token Caching
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import json
   import hashlib
   from datetime import datetime, timedelta
   from pathlib import Path
   from upstox_totp import UpstoxTOTP

   class AdvancedTokenCache:
       def __init__(self, cache_dir="~/.upstox_cache"):
           self.cache_dir = Path(cache_dir).expanduser()
           self.cache_dir.mkdir(exist_ok=True)
           self.upx = UpstoxTOTP()

       def _get_cache_key(self):
           """Generate cache key based on credentials."""
           key_data = f"{self.upx.username}{self.upx.client_id}"
           return hashlib.md5(key_data.encode()).hexdigest()

       def _get_cache_file(self):
           """Get cache file path."""
           cache_key = self._get_cache_key()
           return self.cache_dir / f"token_{cache_key}.json"

       def get_cached_token(self):
           """Get token from cache if valid."""
           cache_file = self._get_cache_file()
           
           if not cache_file.exists():
               return None

           try:
               with open(cache_file, 'r') as f:
                   data = json.load(f)

               expiry = datetime.fromisoformat(data['expiry'])
               
               # Check if token is still valid (with 1-hour buffer)
               if expiry > datetime.now() + timedelta(hours=1):
                   return data['token']
               else:
                   cache_file.unlink()  # Remove expired cache
                   
           except (FileNotFoundError, KeyError, ValueError):
               pass

           return None

       def cache_token(self, token, expiry_hours=24):
           """Cache token with expiry."""
           cache_file = self._get_cache_file()
           expiry = datetime.now() + timedelta(hours=expiry_hours)
           
           data = {
               'token': token,
               'expiry': expiry.isoformat(),
               'created_at': datetime.now().isoformat()
           }
           
           with open(cache_file, 'w') as f:
               json.dump(data, f, indent=2)

       def get_fresh_token(self):
           """Get token from cache or generate new one."""
           # Try cache first
           cached_token = self.get_cached_token()
           if cached_token:
               print("✅ Using cached token")
               return cached_token

           # Generate new token
           print("🔄 Generating new token...")
           response = self.upx.app_token.get_access_token()
           
           if response.success and response.data:
               token = response.data.access_token
               self.cache_token(token)
               print("✅ New token generated and cached")
               return token
           else:
               raise Exception(f"Failed to generate token: {response.error}")

       def clear_cache(self):
           """Clear all cached tokens."""
           for cache_file in self.cache_dir.glob("token_*.json"):
               cache_file.unlink()
           print("🗑️  Cache cleared")

   # Usage
   cache = AdvancedTokenCache()
   token = cache.get_fresh_token()

Database Integration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import sqlite3
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP
   from contextlib import contextmanager

   class DatabaseTokenManager:
       def __init__(self, db_path="upstox_tokens.db"):
           self.db_path = db_path
           self.upx = UpstoxTOTP()
           self.init_database()

       def init_database(self):
           """Initialize database schema."""
           with self.get_connection() as conn:
               conn.execute('''
                   CREATE TABLE IF NOT EXISTS tokens (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id TEXT NOT NULL,
                       access_token TEXT NOT NULL,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       expires_at TIMESTAMP NOT NULL,
                       is_active BOOLEAN DEFAULT TRUE,
                       UNIQUE(user_id, is_active)
                   )
               ''')
               conn.commit()

       @contextmanager
       def get_connection(self):
           """Get database connection with context management."""
           conn = sqlite3.connect(self.db_path)
           conn.row_factory = sqlite3.Row
           try:
               yield conn
           finally:
               conn.close()

       def get_valid_token(self, user_id=None):
           """Get valid token from database."""
           if user_id is None:
               user_id = self.upx.username

           with self.get_connection() as conn:
               cursor = conn.execute('''
                   SELECT access_token, expires_at 
                   FROM tokens 
                   WHERE user_id = ? 
                     AND is_active = TRUE 
                     AND expires_at > datetime('now', '+1 hour')
                   ORDER BY created_at DESC 
                   LIMIT 1
               ''', (user_id,))
               
               row = cursor.fetchone()
               if row:
                   print("✅ Using cached token from database")
                   return row['access_token']

           return None

       def store_token(self, token, user_id=None, expiry_hours=24):
           """Store token in database."""
           if user_id is None:
               user_id = self.upx.username

           expires_at = datetime.now() + timedelta(hours=expiry_hours)

           with self.get_connection() as conn:
               # Deactivate old tokens
               conn.execute('''
                   UPDATE tokens 
                   SET is_active = FALSE 
                   WHERE user_id = ? AND is_active = TRUE
               ''', (user_id,))

               # Insert new token
               conn.execute('''
                   INSERT INTO tokens (user_id, access_token, expires_at)
                   VALUES (?, ?, ?)
               ''', (user_id, token, expires_at))
               
               conn.commit()

       def get_or_create_token(self, user_id=None):
           """Get token from database or create new one."""
           # Try database first
           token = self.get_valid_token(user_id)
           if token:
               return token

           # Generate new token
           print("🔄 Generating new token...")
           response = self.upx.app_token.get_access_token()
           
           if response.success and response.data:
               token = response.data.access_token
               self.store_token(token, user_id)
               print("✅ New token generated and stored")
               return token
           else:
               raise Exception(f"Failed to generate token: {response.error}")

       def cleanup_expired_tokens(self):
           """Remove expired tokens from database."""
           with self.get_connection() as conn:
               cursor = conn.execute('''
                   DELETE FROM tokens 
                   WHERE expires_at < datetime('now')
               ''')
               deleted_count = cursor.rowcount
               conn.commit()
               print(f"🗑️  Cleaned up {deleted_count} expired tokens")

   # Usage
   db_manager = DatabaseTokenManager()
   token = db_manager.get_or_create_token()

Async/Await Support
-------------------

Async Token Generation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   import aiohttp
   from upstox_totp import UpstoxTOTP

   class AsyncUpstoxClient:
       def __init__(self):
           self.upx = UpstoxTOTP()

       async def get_token_async(self):
           """Get token asynchronously."""
           # Run synchronous token generation in thread pool
           loop = asyncio.get_event_loop()
           response = await loop.run_in_executor(
               None, 
               self.upx.app_token.get_access_token
           )
           return response

       async def make_api_call(self, url, token):
           """Make async API call with token."""
           headers = {
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'
           }
           
           async with aiohttp.ClientSession() as session:
               async with session.get(url, headers=headers) as response:
                   return await response.json()

   # Usage
   async def main():
       client = AsyncUpstoxClient()
       
       # Get token
       response = await client.get_token_async()
       if response.success:
           token = response.data.access_token
           
           # Make API calls
           profile = await client.make_api_call(
               'https://api.upstox.com/v2/user/profile',
               token
           )
           print(profile)

   # Run async code
   asyncio.run(main())

Production Deployment
---------------------

Health Check Endpoint
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from flask import Flask, jsonify
   from upstox_totp import UpstoxTOTP, ConfigurationError

   app = Flask(__name__)

   @app.route('/health')
   def health_check():
       """Health check endpoint."""
       try:
           upx = UpstoxTOTP()
           # Quick validation without actual token generation
           return jsonify({
               'status': 'healthy',
               'timestamp': datetime.now().isoformat(),
               'configuration': 'valid'
           })
       except ConfigurationError as e:
           return jsonify({
               'status': 'unhealthy',
               'error': str(e),
               'timestamp': datetime.now().isoformat()
           }), 500

   @app.route('/token/generate')
   def generate_token():
       """Generate token endpoint."""
       try:
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           
           if response.success:
               return jsonify({
                   'success': True,
                   'token': response.data.access_token,
                   'user_id': response.data.user_id
               })
           else:
               return jsonify({
                   'success': False,
                   'error': response.error
               }), 400
               
       except Exception as e:
           return jsonify({
               'success': False,
               'error': str(e)
           }), 500

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8080)

Monitoring and Logging
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import time
   from datetime import datetime
   from upstox_totp import UpstoxTOTP

   # Configure logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('upstox.log'),
           logging.StreamHandler()
       ]
   )

   class MonitoredUpstoxClient:
       def __init__(self):
           self.upx = UpstoxTOTP()
           self.logger = logging.getLogger(__name__)
           self.metrics = {
               'total_requests': 0,
               'successful_requests': 0,
               'failed_requests': 0,
               'last_success': None,
               'last_failure': None
           }

       def get_token_with_monitoring(self):
           """Get token with monitoring and metrics."""
           start_time = time.time()
           self.metrics['total_requests'] += 1
           
           try:
               self.logger.info("Starting token generation...")
               response = self.upx.app_token.get_access_token()
               
               if response.success:
                   self.metrics['successful_requests'] += 1
                   self.metrics['last_success'] = datetime.now()
                   
                   duration = time.time() - start_time
                   self.logger.info(f"Token generated successfully in {duration:.2f}s")
                   
                   return response.data.access_token
               else:
                   self.metrics['failed_requests'] += 1
                   self.metrics['last_failure'] = datetime.now()
                   
                   self.logger.error(f"Token generation failed: {response.error}")
                   raise Exception(f"Token generation failed: {response.error}")
                   
           except Exception as e:
               self.metrics['failed_requests'] += 1
               self.metrics['last_failure'] = datetime.now()
               
               duration = time.time() - start_time
               self.logger.error(f"Token generation error after {duration:.2f}s: {e}")
               raise

       def get_metrics(self):
           """Get client metrics."""
           success_rate = (
               self.metrics['successful_requests'] / self.metrics['total_requests'] * 100
               if self.metrics['total_requests'] > 0 else 0
           )
           
           return {
               **self.metrics,
               'success_rate': f"{success_rate:.2f}%"
           }

   # Usage
   client = MonitoredUpstoxClient()
   token = client.get_token_with_monitoring()
   print(client.get_metrics())

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from dataclasses import dataclass
   from typing import Optional
   from upstox_totp import UpstoxTOTP

   @dataclass
   class UpstoxConfig:
       username: str
       password: str
       pin_code: str
       totp_secret: str
       client_id: str
       client_secret: str
       redirect_uri: str
       debug: bool = False
       sleep_time: int = 1000
       max_retries: int = 3
       cache_enabled: bool = True
       cache_ttl_hours: int = 24

   class ConfigManager:
       @staticmethod
       def from_environment() -> UpstoxConfig:
           """Load configuration from environment variables."""
           return UpstoxConfig(
               username=os.getenv('UPSTOX_USERNAME'),
               password=os.getenv('UPSTOX_PASSWORD'),
               pin_code=os.getenv('UPSTOX_PIN_CODE'),
               totp_secret=os.getenv('UPSTOX_TOTP_SECRET'),
               client_id=os.getenv('UPSTOX_CLIENT_ID'),
               client_secret=os.getenv('UPSTOX_CLIENT_SECRET'),
               redirect_uri=os.getenv('UPSTOX_REDIRECT_URI'),
               debug=os.getenv('UPSTOX_DEBUG', 'false').lower() == 'true',
               sleep_time=int(os.getenv('UPSTOX_SLEEP_TIME', '1000')),
               max_retries=int(os.getenv('UPSTOX_MAX_RETRIES', '3')),
               cache_enabled=os.getenv('UPSTOX_CACHE_ENABLED', 'true').lower() == 'true',
               cache_ttl_hours=int(os.getenv('UPSTOX_CACHE_TTL_HOURS', '24'))
           )

       @staticmethod
       def validate_config(config: UpstoxConfig) -> bool:
           """Validate configuration."""
           required_fields = [
               'username', 'password', 'pin_code', 'totp_secret',
               'client_id', 'client_secret', 'redirect_uri'
           ]
           
           for field in required_fields:
               if not getattr(config, field):
                   raise ValueError(f"Missing required field: {field}")
           
           return True

   # Usage
   config = ConfigManager.from_environment()
   ConfigManager.validate_config(config)

   upx = UpstoxTOTP(
       username=config.username,
       password=config.password,
       # ... other fields
   )

Performance Optimization
------------------------

Connection Pooling
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from requests.adapters import HTTPAdapter
   from urllib3.util.retry import Retry
   from urllib3 import PoolManager
   from upstox_totp import UpstoxTOTP

   class OptimizedUpstoxClient:
       def __init__(self):
           self.upx = UpstoxTOTP()
           self._setup_session()

       def _setup_session(self):
           """Set up optimized session configuration."""
           session = self.upx.session
           
           # Configure retry strategy
           retry_strategy = Retry(
               total=3,
               backoff_factor=1,
               status_forcelist=[429, 500, 502, 503, 504],
               allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
           )
           
           # Configure adapter with connection pooling
           adapter = HTTPAdapter(
               max_retries=retry_strategy,
               pool_connections=10,
               pool_maxsize=20,
               pool_block=False
           )
           
           session.mount("http://", adapter)
           session.mount("https://", adapter)
           
           # Set timeouts
           session.timeout = (10, 30)  # (connect, read)

   # Usage
   client = OptimizedUpstoxClient()

Next Steps
----------

Now that you've learned about advanced usage patterns:

1. **Explore integration examples**: See :doc:`examples/integration`
2. **Learn about token caching**: See :doc:`examples/token_caching`
3. **Check database storage patterns**: See :doc:`examples/database_storage`
4. **Review security best practices**: See :doc:`security`
5. **Read troubleshooting guide**: See :doc:`troubleshooting`
