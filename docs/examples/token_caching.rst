Token Caching Examples
======================

This guide shows various strategies for caching Upstox access tokens to improve performance and reduce API calls.

Why Cache Tokens?
-----------------

Upstox access tokens:

- **Expire after 24 hours** - Need periodic refresh
- **Take 2-5 seconds to generate** - Network overhead
- **Have rate limits** - Avoid unnecessary calls
- **Are reusable** - Same token works for multiple API calls

Caching tokens reduces latency and improves application performance.

Simple File-Based Caching
-------------------------

Basic File Cache
~~~~~~~~~~~~~~~~

.. code-block:: python

   import json
   import os
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP

   class SimpleTokenCache:
       def __init__(self, cache_file="upstox_token.json"):
           self.cache_file = cache_file
           self.upstox = UpstoxTOTP()

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
               if os.path.exists(self.cache_file):
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
           response = self.upstox.app_token.get_access_token()

           if response.success and response.data:
               token = response.data.access_token
               self.cache_token(token)
               return token
           else:
               raise Exception(f"Token generation failed: {response.error}")

   # Usage
   cache = SimpleTokenCache()
   token = cache.get_fresh_token()

Secure File Cache
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json
   import os
   import stat
   from datetime import datetime, timedelta
   from cryptography.fernet import Fernet
   from upstox_totp import UpstoxTOTP

   class SecureTokenCache:
       def __init__(self, cache_file="upstox_token.enc", key_file="token.key"):
           self.cache_file = cache_file
           self.key_file = key_file
           self.upstox = UpstoxTOTP()
           self.cipher = self._get_cipher()

       def _get_cipher(self):
           """Get or create encryption cipher."""
           if os.path.exists(self.key_file):
               with open(self.key_file, 'rb') as f:
                   key = f.read()
           else:
               key = Fernet.generate_key()
               with open(self.key_file, 'wb') as f:
                   f.write(key)
               # Set secure permissions
               os.chmod(self.key_file, stat.S_IRUSR | stat.S_IWUSR)  # 600

           return Fernet(key)

       def get_cached_token(self):
           """Get encrypted token from cache."""
           if not os.path.exists(self.cache_file):
               return None

           try:
               with open(self.cache_file, 'rb') as f:
                   encrypted_data = f.read()

               # Decrypt data
               decrypted_data = self.cipher.decrypt(encrypted_data)
               data = json.loads(decrypted_data.decode())

               # Check expiry
               expiry = datetime.fromisoformat(data['expiry'])
               if expiry > datetime.now() + timedelta(hours=1):
                   return data['token']
               else:
                   os.remove(self.cache_file)
                   return None

           except Exception:
               if os.path.exists(self.cache_file):
                   os.remove(self.cache_file)
               return None

       def cache_token(self, token):
           """Cache token with encryption."""
           expiry = datetime.now() + timedelta(hours=24)
           data = {
               'token': token,
               'expiry': expiry.isoformat(),
               'created': datetime.now().isoformat()
           }

           # Encrypt data
           json_data = json.dumps(data).encode()
           encrypted_data = self.cipher.encrypt(json_data)

           with open(self.cache_file, 'wb') as f:
               f.write(encrypted_data)

           # Set secure permissions
           os.chmod(self.cache_file, stat.S_IRUSR | stat.S_IWUSR)  # 600

       def get_fresh_token(self):
           """Get token from secure cache or generate new one."""
           token = self.get_cached_token()
           if token:
               return token

           response = self.upstox.app_token.get_access_token()
           if response.success and response.data:
               token = response.data.access_token
               self.cache_token(token)
               return token
           else:
               raise Exception(f"Token generation failed: {response.error}")

   # Usage
   secure_cache = SecureTokenCache()
   token = secure_cache.get_fresh_token()

Memory-Based Caching
--------------------

In-Memory Cache
~~~~~~~~~~~~~~~

.. code-block:: python

   import threading
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP

   class MemoryTokenCache:
       def __init__(self):
           self.upstox = UpstoxTOTP()
           self._token = None
           self._expiry = None
           self._lock = threading.Lock()

       def get_fresh_token(self):
           """Get token from memory cache or generate new one."""
           with self._lock:
               # Check if token is still valid
               if (self._token and self._expiry and 
                   self._expiry > datetime.now() + timedelta(hours=1)):
                   print("✅ Using cached token from memory")
                   return self._token

               # Generate new token
               print("🔄 Generating new token...")
               response = self.upstox.app_token.get_access_token()

               if response.success and response.data:
                   self._token = response.data.access_token
                   self._expiry = datetime.now() + timedelta(hours=24)
                   print("💾 Token cached in memory")
                   return self._token
               else:
                   raise Exception(f"Token generation failed: {response.error}")

       def invalidate_cache(self):
           """Manually invalidate cached token."""
           with self._lock:
               self._token = None
               self._expiry = None
               print("🗑️ Memory cache invalidated")

   # Usage
   memory_cache = MemoryTokenCache()
   token = memory_cache.get_fresh_token()

LRU Cache with TTL
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import threading
   from functools import wraps
   from upstox_totp import UpstoxTOTP

   class TTLCache:
       def __init__(self, ttl_seconds=3600):  # 1 hour default
           self.ttl_seconds = ttl_seconds
           self.cache = {}
           self.lock = threading.Lock()

       def get(self, key):
           with self.lock:
               if key in self.cache:
                   value, timestamp = self.cache[key]
                   if time.time() - timestamp < self.ttl_seconds:
                       return value
                   else:
                       del self.cache[key]
               return None

       def set(self, key, value):
           with self.lock:
               self.cache[key] = (value, time.time())

       def delete(self, key):
           with self.lock:
               if key in self.cache:
                   del self.cache[key]

   def cached_token(ttl_seconds=23*3600):  # 23 hours
       """Decorator for token caching."""
       cache = TTLCache(ttl_seconds)
       
       def decorator(func):
           @wraps(func)
           def wrapper(*args, **kwargs):
               # Create cache key from function args
               cache_key = f"{func.__name__}_{hash(str(args) + str(sorted(kwargs.items())))}"
               
               # Try cache first
               cached_result = cache.get(cache_key)
               if cached_result:
                   print("✅ Using cached token")
                   return cached_result
               
               # Generate new token
               print("🔄 Generating new token...")
               result = func(*args, **kwargs)
               
               # Cache result
               cache.set(cache_key, result)
               print("💾 Token cached")
               
               return result
           return wrapper
       return decorator

   class CachedUpstoxClient:
       def __init__(self):
           self.upstox = UpstoxTOTP()

       @cached_token(ttl_seconds=23*3600)  # 23 hours
       def get_access_token(self):
           response = self.upstox.app_token.get_access_token()
           if response.success and response.data:
               return response.data.access_token
           else:
               raise Exception(f"Token generation failed: {response.error}")

   # Usage
   client = CachedUpstoxClient()
   token = client.get_access_token()  # First call - generates token
   token = client.get_access_token()  # Second call - uses cache

Redis Caching
-------------

Basic Redis Cache
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import redis
   import json
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP

   class RedisTokenCache:
       def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
           self.redis_client = redis.Redis(
               host=redis_host,
               port=redis_port,
               db=redis_db,
               decode_responses=True
           )
           self.upstox = UpstoxTOTP()
           self.cache_key = 'upstox:access_token'

       def get_fresh_token(self):
           """Get token from Redis cache or generate new one."""
           # Try cache first
           cached_token = self.redis_client.get(self.cache_key)
           if cached_token:
               print("✅ Using cached token from Redis")
               return cached_token

           # Generate new token
           print("🔄 Generating new token...")
           response = self.upstox.app_token.get_access_token()

           if response.success and response.data:
               token = response.data.access_token
               
               # Cache with expiration (23 hours)
               self.redis_client.setex(
                   self.cache_key,
                   23 * 3600,  # 23 hours in seconds
                   token
               )
               
               print("💾 Token cached in Redis")
               return token
           else:
               raise Exception(f"Token generation failed: {response.error}")

       def invalidate_cache(self):
           """Manually invalidate cached token."""
           self.redis_client.delete(self.cache_key)
           print("🗑️ Redis cache invalidated")

   # Usage
   redis_cache = RedisTokenCache()
   token = redis_cache.get_fresh_token()

Redis with Metadata
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import redis
   import json
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP

   class AdvancedRedisTokenCache:
       def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
           self.redis_client = redis.Redis(
               host=redis_host,
               port=redis_port,
               db=redis_db,
               decode_responses=True
           )
           self.upstox = UpstoxTOTP()
           self.token_key = 'upstox:token'
           self.metadata_key = 'upstox:token:metadata'
           self.stats_key = 'upstox:token:stats'

       def get_fresh_token(self):
           """Get token with metadata tracking."""
           # Check cache
           cached_token = self.redis_client.get(self.token_key)
           if cached_token:
               # Update stats
               self._increment_cache_hits()
               print("✅ Using cached token from Redis")
               return cached_token

           # Generate new token
           print("🔄 Generating new token...")
           response = self.upstox.app_token.get_access_token()

           if response.success and response.data:
               token = response.data.access_token
               
               # Store token
               self.redis_client.setex(self.token_key, 23 * 3600, token)
               
               # Store metadata
               metadata = {
                   'user_id': response.data.user_id,
                   'user_name': response.data.user_name,
                   'email': response.data.email,
                   'generated_at': datetime.now().isoformat(),
                   'expires_at': (datetime.now() + timedelta(hours=24)).isoformat()
               }
               
               self.redis_client.setex(
                   self.metadata_key,
                   23 * 3600,
                   json.dumps(metadata)
               )
               
               # Update stats
               self._increment_cache_misses()
               self._increment_total_generations()
               
               print("💾 Token and metadata cached in Redis")
               return token
           else:
               raise Exception(f"Token generation failed: {response.error}")

       def get_token_metadata(self):
           """Get token metadata."""
           metadata_json = self.redis_client.get(self.metadata_key)
           if metadata_json:
               return json.loads(metadata_json)
           return None

       def get_cache_stats(self):
           """Get cache statistics."""
           stats = self.redis_client.hgetall(self.stats_key)
           return {
               'cache_hits': int(stats.get('hits', 0)),
               'cache_misses': int(stats.get('misses', 0)),
               'total_generations': int(stats.get('generations', 0)),
               'hit_ratio': self._calculate_hit_ratio(stats)
           }

       def _increment_cache_hits(self):
           self.redis_client.hincrby(self.stats_key, 'hits', 1)

       def _increment_cache_misses(self):
           self.redis_client.hincrby(self.stats_key, 'misses', 1)

       def _increment_total_generations(self):
           self.redis_client.hincrby(self.stats_key, 'generations', 1)

       def _calculate_hit_ratio(self, stats):
           hits = int(stats.get('hits', 0))
           misses = int(stats.get('misses', 0))
           total = hits + misses
           return (hits / total * 100) if total > 0 else 0

   # Usage
   advanced_cache = AdvancedRedisTokenCache()
   token = advanced_cache.get_fresh_token()
   
   # Get metadata and stats
   metadata = advanced_cache.get_token_metadata()
   stats = advanced_cache.get_cache_stats()
   print(f"Cache hit ratio: {stats['hit_ratio']:.1f}%")

Database Caching
----------------

SQLite Cache
~~~~~~~~~~~~

.. code-block:: python

   import sqlite3
   import json
   from datetime import datetime, timedelta
   from contextlib import contextmanager
   from upstox_totp import UpstoxTOTP

   class SQLiteTokenCache:
       def __init__(self, db_path="upstox_cache.db"):
           self.db_path = db_path
           self.upstox = UpstoxTOTP()
           self.init_database()

       def init_database(self):
           """Initialize SQLite database."""
           with self.get_connection() as conn:
               conn.execute('''
                   CREATE TABLE IF NOT EXISTS token_cache (
                       id INTEGER PRIMARY KEY,
                       token TEXT NOT NULL,
                       user_id TEXT,
                       user_name TEXT,
                       email TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       expires_at TIMESTAMP NOT NULL,
                       is_active BOOLEAN DEFAULT TRUE
                   )
               ''')
               
               conn.execute('''
                   CREATE TABLE IF NOT EXISTS cache_stats (
                       id INTEGER PRIMARY KEY,
                       cache_hits INTEGER DEFAULT 0,
                       cache_misses INTEGER DEFAULT 0,
                       total_generations INTEGER DEFAULT 0,
                       last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
               ''')
               
               # Initialize stats if not exists
               conn.execute('''
                   INSERT OR IGNORE INTO cache_stats (id, cache_hits, cache_misses, total_generations)
                   VALUES (1, 0, 0, 0)
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

       def get_fresh_token(self):
           """Get token from SQLite cache or generate new one."""
           with self.get_connection() as conn:
               # Check for valid token
               cursor = conn.execute('''
                   SELECT token FROM token_cache
                   WHERE is_active = TRUE
                     AND expires_at > datetime('now', '+1 hour')
                   ORDER BY created_at DESC
                   LIMIT 1
               ''')
               
               row = cursor.fetchone()
               if row:
                   self._update_cache_hits(conn)
                   print("✅ Using cached token from SQLite")
                   return row['token']

           # Generate new token
           print("🔄 Generating new token...")
           response = self.upstox.app_token.get_access_token()

           if response.success and response.data:
               token = response.data.access_token
               expires_at = datetime.now() + timedelta(hours=24)

               with self.get_connection() as conn:
                   # Deactivate old tokens
                   conn.execute('''
                       UPDATE token_cache
                       SET is_active = FALSE
                       WHERE is_active = TRUE
                   ''')

                   # Insert new token
                   conn.execute('''
                       INSERT INTO token_cache (token, user_id, user_name, email, expires_at)
                       VALUES (?, ?, ?, ?, ?)
                   ''', (
                       token,
                       response.data.user_id,
                       response.data.user_name,
                       response.data.email,
                       expires_at
                   ))

                   self._update_cache_misses(conn)
                   self._update_total_generations(conn)
                   conn.commit()

               print("💾 Token cached in SQLite")
               return token
           else:
               raise Exception(f"Token generation failed: {response.error}")

       def get_cache_stats(self):
           """Get cache statistics."""
           with self.get_connection() as conn:
               cursor = conn.execute('''
                   SELECT cache_hits, cache_misses, total_generations
                   FROM cache_stats WHERE id = 1
               ''')
               
               row = cursor.fetchone()
               if row:
                   hits = row['cache_hits']
                   misses = row['cache_misses']
                   total = hits + misses
                   hit_ratio = (hits / total * 100) if total > 0 else 0
                   
                   return {
                       'cache_hits': hits,
                       'cache_misses': misses,
                       'total_generations': row['total_generations'],
                       'hit_ratio': hit_ratio
                   }
               return {}

       def cleanup_expired_tokens(self):
           """Remove expired tokens."""
           with self.get_connection() as conn:
               cursor = conn.execute('''
                   DELETE FROM token_cache
                   WHERE expires_at < datetime('now')
               ''')
               deleted_count = cursor.rowcount
               conn.commit()
               return deleted_count

       def _update_cache_hits(self, conn):
           conn.execute('''
               UPDATE cache_stats
               SET cache_hits = cache_hits + 1,
                   last_updated = CURRENT_TIMESTAMP
               WHERE id = 1
           ''')

       def _update_cache_misses(self, conn):
           conn.execute('''
               UPDATE cache_stats
               SET cache_misses = cache_misses + 1,
                   last_updated = CURRENT_TIMESTAMP
               WHERE id = 1
           ''')

       def _update_total_generations(self, conn):
           conn.execute('''
               UPDATE cache_stats
               SET total_generations = total_generations + 1,
                   last_updated = CURRENT_TIMESTAMP
               WHERE id = 1
           ''')

   # Usage
   sqlite_cache = SQLiteTokenCache()
   token = sqlite_cache.get_fresh_token()
   
   # Get stats
   stats = sqlite_cache.get_cache_stats()
   print(f"Cache performance: {stats}")
   
   # Cleanup
   deleted = sqlite_cache.cleanup_expired_tokens()
   print(f"Cleaned up {deleted} expired tokens")

Multi-Level Caching
-------------------

Memory + Redis Cache
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import redis
   import threading
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP

   class MultiLevelTokenCache:
       def __init__(self, redis_host='localhost', redis_port=6379):
           self.upstox = UpstoxTOTP()
           
           # Level 1: Memory cache
           self._memory_token = None
           self._memory_expiry = None
           self._memory_lock = threading.Lock()
           
           # Level 2: Redis cache
           self.redis_client = redis.Redis(
               host=redis_host,
               port=redis_port,
               decode_responses=True
           )
           self.redis_key = 'upstox:token:multilevel'

       def get_fresh_token(self):
           """Get token from multi-level cache or generate new one."""
           
           # Level 1: Check memory cache
           with self._memory_lock:
               if (self._memory_token and self._memory_expiry and
                   self._memory_expiry > datetime.now() + timedelta(hours=1)):
                   print("✅ Using token from memory cache (L1)")
                   return self._memory_token

           # Level 2: Check Redis cache
           redis_token = self.redis_client.get(self.redis_key)
           if redis_token:
               # Store in memory cache
               with self._memory_lock:
                   self._memory_token = redis_token
                   self._memory_expiry = datetime.now() + timedelta(hours=24)
               
               print("✅ Using token from Redis cache (L2), cached in memory")
               return redis_token

           # Level 3: Generate new token
           print("🔄 Generating new token...")
           response = self.upstox.app_token.get_access_token()

           if response.success and response.data:
               token = response.data.access_token

               # Store in Redis (L2)
               self.redis_client.setex(self.redis_key, 23 * 3600, token)

               # Store in memory (L1)
               with self._memory_lock:
                   self._memory_token = token
                   self._memory_expiry = datetime.now() + timedelta(hours=24)

               print("💾 Token cached in memory (L1) and Redis (L2)")
               return token
           else:
               raise Exception(f"Token generation failed: {response.error}")

       def invalidate_cache(self, level='all'):
           """Invalidate cache at specified level."""
           if level in ('all', 'memory'):
               with self._memory_lock:
                   self._memory_token = None
                   self._memory_expiry = None
               print("🗑️ Memory cache (L1) invalidated")

           if level in ('all', 'redis'):
               self.redis_client.delete(self.redis_key)
               print("🗑️ Redis cache (L2) invalidated")

   # Usage
   multi_cache = MultiLevelTokenCache()
   
   token1 = multi_cache.get_fresh_token()  # Generates new token
   token2 = multi_cache.get_fresh_token()  # Uses memory cache
   
   # Invalidate memory cache only
   multi_cache.invalidate_cache('memory')
   token3 = multi_cache.get_fresh_token()  # Uses Redis cache

Advanced Caching Strategies
---------------------------

Write-Through Cache
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import threading
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP

   class WriteThroughTokenCache:
       def __init__(self):
           self.upstox = UpstoxTOTP()
           self.primary_cache = {}  # Memory
           self.secondary_cache = {}  # Persistent storage simulation
           self.lock = threading.Lock()

       def get_fresh_token(self):
           """Get token with write-through caching."""
           with self.lock:
               # Check primary cache
               if self._is_token_valid(self.primary_cache):
                   print("✅ Using token from primary cache")
                   return self.primary_cache['token']

               # Check secondary cache
               if self._is_token_valid(self.secondary_cache):
                   # Promote to primary cache
                   self.primary_cache = self.secondary_cache.copy()
                   print("✅ Using token from secondary cache, promoted to primary")
                   return self.secondary_cache['token']

               # Generate new token
               print("🔄 Generating new token...")
               response = self.upstox.app_token.get_access_token()

               if response.success and response.data:
                   token_data = {
                       'token': response.data.access_token,
                       'expiry': datetime.now() + timedelta(hours=24),
                       'user_id': response.data.user_id
                   }

                   # Write to both caches simultaneously
                   self.primary_cache = token_data.copy()
                   self.secondary_cache = token_data.copy()

                   print("💾 Token stored in both primary and secondary caches")
                   return token_data['token']
               else:
                   raise Exception(f"Token generation failed: {response.error}")

       def _is_token_valid(self, cache):
           return (cache and 'token' in cache and 'expiry' in cache and
                   cache['expiry'] > datetime.now() + timedelta(hours=1))

   # Usage
   write_through_cache = WriteThroughTokenCache()
   token = write_through_cache.get_fresh_token()

Cache with Background Refresh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import threading
   import time
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP

   class BackgroundRefreshCache:
       def __init__(self, refresh_threshold_hours=2):
           self.upstox = UpstoxTOTP()
           self.refresh_threshold = timedelta(hours=refresh_threshold_hours)
           self.token_data = None
           self.lock = threading.Lock()
           self.refresh_thread = None
           self.stop_refresh = threading.Event()

       def get_fresh_token(self):
           """Get token with background refresh."""
           with self.lock:
               # Check if we have a valid token
               if self._is_token_valid():
                   # Check if we need background refresh
                   if self._needs_refresh():
                       self._start_background_refresh()
                   
                   return self.token_data['token']

               # No valid token, generate immediately
               return self._generate_token()

       def _is_token_valid(self):
           return (self.token_data and 
                   self.token_data['expiry'] > datetime.now() + timedelta(hours=1))

       def _needs_refresh(self):
           return (self.token_data and 
                   self.token_data['expiry'] - datetime.now() < self.refresh_threshold)

       def _generate_token(self):
           """Generate new token synchronously."""
           print("🔄 Generating new token...")
           response = self.upstox.app_token.get_access_token()

           if response.success and response.data:
               self.token_data = {
                   'token': response.data.access_token,
                   'expiry': datetime.now() + timedelta(hours=24),
                   'generated_at': datetime.now()
               }
               print("💾 Token generated and cached")
               return self.token_data['token']
           else:
               raise Exception(f"Token generation failed: {response.error}")

       def _start_background_refresh(self):
           """Start background token refresh if not already running."""
           if self.refresh_thread and self.refresh_thread.is_alive():
               return  # Already refreshing

           self.refresh_thread = threading.Thread(target=self._background_refresh)
           self.refresh_thread.daemon = True
           self.refresh_thread.start()
           print("🔄 Background token refresh started")

       def _background_refresh(self):
           """Background thread to refresh token."""
           try:
               time.sleep(1)  # Small delay to avoid immediate refresh
               
               with self.lock:
                   if not self._needs_refresh():
                       return  # No longer needs refresh
                   
                   print("🔄 Background: Refreshing token...")
                   self._generate_token()
                   print("✅ Background: Token refreshed successfully")
                   
           except Exception as e:
               print(f"❌ Background refresh failed: {e}")

       def stop_background_refresh(self):
           """Stop background refresh thread."""
           self.stop_refresh.set()
           if self.refresh_thread:
               self.refresh_thread.join(timeout=5)

   # Usage
   bg_cache = BackgroundRefreshCache(refresh_threshold_hours=2)

   # This will generate a token
   token1 = bg_cache.get_fresh_token()

   # Later calls will use cached token and start background refresh if needed
   token2 = bg_cache.get_fresh_token()

   # Clean shutdown
   bg_cache.stop_background_refresh()

Cache Monitoring and Metrics
----------------------------

Comprehensive Cache Monitor
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import time
   import threading
   from datetime import datetime, timedelta
   from collections import defaultdict
   from upstox_totp import UpstoxTOTP

   class MonitoredTokenCache:
       def __init__(self):
           self.upstox = UpstoxTOTP()
           self.cache = {}
           self.lock = threading.Lock()
           
           # Metrics
           self.metrics = {
               'cache_hits': 0,
               'cache_misses': 0,
               'token_generations': 0,
               'total_requests': 0,
               'average_generation_time': 0,
               'last_generation_time': None,
               'generation_times': [],
               'errors': 0
           }
           
           self.request_history = []

       def get_fresh_token(self):
           """Get token with comprehensive monitoring."""
           start_time = time.time()
           request_id = f"req_{int(time.time() * 1000)}"
           
           self.metrics['total_requests'] += 1
           
           with self.lock:
               # Check cache
               if self._is_token_valid():
                   self.metrics['cache_hits'] += 1
                   self._log_request(request_id, 'cache_hit', time.time() - start_time)
                   return self.cache['token']

               # Cache miss - generate new token
               self.metrics['cache_misses'] += 1
               
               try:
                   generation_start = time.time()
                   response = self.upstox.app_token.get_access_token()
                   generation_time = time.time() - generation_start

                   if response.success and response.data:
                       self.cache = {
                           'token': response.data.access_token,
                           'expiry': datetime.now() + timedelta(hours=24),
                           'generated_at': datetime.now(),
                           'generation_time': generation_time
                       }

                       # Update metrics
                       self.metrics['token_generations'] += 1
                       self.metrics['generation_times'].append(generation_time)
                       self.metrics['average_generation_time'] = (
                           sum(self.metrics['generation_times']) / 
                           len(self.metrics['generation_times'])
                       )
                       self.metrics['last_generation_time'] = datetime.now()

                       total_time = time.time() - start_time
                       self._log_request(request_id, 'cache_miss_generated', total_time, generation_time)
                       
                       return self.cache['token']
                   else:
                       self.metrics['errors'] += 1
                       self._log_request(request_id, 'error', time.time() - start_time)
                       raise Exception(f"Token generation failed: {response.error}")
                       
               except Exception as e:
                   self.metrics['errors'] += 1
                   self._log_request(request_id, 'exception', time.time() - start_time)
                   raise

       def _is_token_valid(self):
           return (self.cache and 'expiry' in self.cache and
                   self.cache['expiry'] > datetime.now() + timedelta(hours=1))

       def _log_request(self, request_id, result_type, total_time, generation_time=None):
           log_entry = {
               'request_id': request_id,
               'timestamp': datetime.now(),
               'result_type': result_type,
               'total_time': total_time,
               'generation_time': generation_time
           }
           
           self.request_history.append(log_entry)
           
           # Keep only last 1000 requests
           if len(self.request_history) > 1000:
               self.request_history.pop(0)

       def get_metrics(self):
           """Get comprehensive cache metrics."""
           with self.lock:
               total_requests = self.metrics['total_requests']
               cache_hits = self.metrics['cache_hits']
               
               hit_ratio = (cache_hits / total_requests * 100) if total_requests > 0 else 0
               
               recent_requests = [
                   req for req in self.request_history 
                   if req['timestamp'] > datetime.now() - timedelta(minutes=5)
               ]
               
               return {
                   'cache_hits': cache_hits,
                   'cache_misses': self.metrics['cache_misses'],
                   'hit_ratio': hit_ratio,
                   'token_generations': self.metrics['token_generations'],
                   'total_requests': total_requests,
                   'average_generation_time': self.metrics['average_generation_time'],
                   'last_generation_time': self.metrics['last_generation_time'],
                   'errors': self.metrics['errors'],
                   'recent_requests_5min': len(recent_requests),
                   'cache_status': 'valid' if self._is_token_valid() else 'invalid'
               }

       def get_performance_report(self):
           """Get detailed performance report."""
           metrics = self.get_metrics()
           generation_times = self.metrics['generation_times']
           
           if generation_times:
               report = {
                   **metrics,
                   'min_generation_time': min(generation_times),
                   'max_generation_time': max(generation_times),
                   'median_generation_time': sorted(generation_times)[len(generation_times)//2],
                   'p95_generation_time': sorted(generation_times)[int(len(generation_times)*0.95)],
                   'generation_time_samples': len(generation_times)
               }
           else:
               report = metrics
           
           return report

   # Usage
   monitored_cache = MonitoredTokenCache()

   # Generate some requests
   for i in range(10):
       token = monitored_cache.get_fresh_token()
       time.sleep(0.1)  # Simulate some delay

   # Get metrics
   metrics = monitored_cache.get_metrics()
   print(f"Cache hit ratio: {metrics['hit_ratio']:.1f}%")
   print(f"Average generation time: {metrics['average_generation_time']:.2f}s")

   # Get detailed report
   report = monitored_cache.get_performance_report()
   print(f"Performance report: {report}")

Best Practices
--------------

1. **Choose Appropriate TTL**: Use 23 hours for tokens (1-hour safety buffer)
2. **Implement Proper Locking**: Use threading locks for thread-safe caching
3. **Handle Cache Failures**: Always have fallback to token generation
4. **Monitor Cache Performance**: Track hit ratios and generation times
5. **Secure Sensitive Data**: Encrypt cached tokens when possible
6. **Clean Up Expired Entries**: Regularly remove old cache entries
7. **Use Multi-Level Caching**: Combine memory and persistent caching
8. **Implement Background Refresh**: Refresh tokens before they expire
9. **Add Proper Logging**: Log cache operations for debugging
10. **Test Cache Logic**: Thoroughly test cache expiry and refresh logic

See Also
--------

- :doc:`basic_usage` - Basic usage examples
- :doc:`integration` - Framework integration examples
- :doc:`../security` - Security considerations for token storage
- :doc:`../advanced_usage` - Advanced usage patterns
