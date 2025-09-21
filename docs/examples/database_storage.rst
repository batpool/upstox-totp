Database Storage Examples
=========================

This guide shows how to integrate the Upstox TOTP SDK with various databases for persistent token storage and management.

Why Use Database Storage?
-------------------------

Database storage provides:

- **Persistence** - Tokens survive application restarts
- **Scalability** - Support multiple users and applications
- **History** - Track token generation and usage
- **Security** - Encrypted storage and access control
- **Reliability** - ACID properties and backup capabilities

SQLite Integration
------------------

Simple SQLite Storage
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import sqlite3
   import json
   from datetime import datetime, timedelta
   from contextlib import contextmanager
   from upstox_totp import UpstoxTOTP

   class SQLiteUpstoxStorage:
       def __init__(self, db_path="upstox.db"):
           self.db_path = db_path
           self.upstox = UpstoxTOTP()
           self.init_database()

       def init_database(self):
           """Initialize SQLite database schema."""
           with self.get_connection() as conn:
               conn.execute('''
                   CREATE TABLE IF NOT EXISTS upstox_tokens (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id TEXT NOT NULL,
                       access_token TEXT NOT NULL,
                       user_name TEXT,
                       email TEXT,
                       broker TEXT,
                       user_type TEXT,
                       products TEXT,  -- JSON array
                       exchanges TEXT, -- JSON array
                       is_active BOOLEAN DEFAULT TRUE,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       expires_at TIMESTAMP NOT NULL,
                       metadata TEXT   -- JSON for additional data
                   )
               ''')
               
               conn.execute('''
                   CREATE INDEX IF NOT EXISTS idx_user_id_active 
                   ON upstox_tokens(user_id, is_active)
               ''')
               
               conn.execute('''
                   CREATE INDEX IF NOT EXISTS idx_expires_at 
                   ON upstox_tokens(expires_at)
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

       def store_token(self, user_identifier=None):
           """Generate and store new token."""
           response = self.upstox.app_token.get_access_token()
           
           if not response.success:
               raise Exception(f"Token generation failed: {response.error}")
           
           data = response.data
           expires_at = datetime.now() + timedelta(hours=24)
           
           with self.get_connection() as conn:
               # Deactivate old tokens for this user
               conn.execute('''
                   UPDATE upstox_tokens 
                   SET is_active = FALSE 
                   WHERE user_id = ? AND is_active = TRUE
               ''', (data.user_id,))
               
               # Insert new token
               conn.execute('''
                   INSERT INTO upstox_tokens (
                       user_id, access_token, user_name, email, broker,
                       user_type, products, exchanges, expires_at, metadata
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ''', (
                   data.user_id,
                   data.access_token,
                   data.user_name,
                   data.email,
                   data.broker,
                   data.user_type,
                   json.dumps(data.products),
                   json.dumps(data.exchanges),
                   expires_at,
                   json.dumps({
                       'is_active_user': data.is_active,
                       'generation_method': 'upstox_totp_sdk'
                   })
               ))
               
               conn.commit()
               
           return {
               'token': data.access_token,
               'user_id': data.user_id,
               'expires_at': expires_at.isoformat()
           }

       def get_valid_token(self, user_id):
           """Get valid token for user."""
           with self.get_connection() as conn:
               cursor = conn.execute('''
                   SELECT access_token, expires_at, user_name
                   FROM upstox_tokens
                   WHERE user_id = ? 
                     AND is_active = TRUE
                     AND expires_at > datetime('now', '+1 hour')
                   ORDER BY created_at DESC
                   LIMIT 1
               ''', (user_id,))
               
               row = cursor.fetchone()
               if row:
                   return {
                       'token': row['access_token'],
                       'user_name': row['user_name'],
                       'expires_at': row['expires_at']
                   }
               
               return None

       def get_or_create_token(self, user_id=None):
           """Get existing valid token or create new one."""
           # Try to get existing token
           if user_id:
               existing = self.get_valid_token(user_id)
               if existing:
                   return existing
           
           # Generate new token
           return self.store_token(user_id)

       def get_token_history(self, user_id, limit=10):
           """Get token generation history for user."""
           with self.get_connection() as conn:
               cursor = conn.execute('''
                   SELECT 
                       created_at, expires_at, is_active,
                       user_name, email, broker
                   FROM upstox_tokens
                   WHERE user_id = ?
                   ORDER BY created_at DESC
                   LIMIT ?
               ''', (user_id, limit))
               
               return [dict(row) for row in cursor.fetchall()]

       def cleanup_expired_tokens(self):
           """Remove expired tokens."""
           with self.get_connection() as conn:
               cursor = conn.execute('''
                   DELETE FROM upstox_tokens
                   WHERE expires_at < datetime('now')
               ''')
               deleted_count = cursor.rowcount
               conn.commit()
               return deleted_count

   # Usage
   storage = SQLiteUpstoxStorage()

   # Store new token
   result = storage.store_token()
   print(f"Stored token for user: {result['user_id']}")

   # Get valid token
   token_info = storage.get_valid_token(result['user_id'])
   if token_info:
       print(f"Valid token found: {token_info['token'][:20]}...")

   # Get history
   history = storage.get_token_history(result['user_id'])
   print(f"Token history: {len(history)} entries")

PostgreSQL Integration
----------------------

Advanced PostgreSQL Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import psycopg2
   import psycopg2.extras
   import json
   from datetime import datetime, timedelta
   from contextlib import contextmanager
   from upstox_totp import UpstoxTOTP

   class PostgreSQLUpstoxStorage:
       def __init__(self, connection_string):
           self.connection_string = connection_string
           self.upstox = UpstoxTOTP()
           self.init_database()

       def init_database(self):
           """Initialize PostgreSQL database schema."""
           with self.get_connection() as conn:
               with conn.cursor() as cursor:
                   # Create enum types
                   cursor.execute('''
                       DO $$ BEGIN
                           CREATE TYPE user_type_enum AS ENUM ('individual', 'corporate');
                       EXCEPTION
                           WHEN duplicate_object THEN null;
                       END $$;
                   ''')
                   
                   # Create main table
                   cursor.execute('''
                       CREATE TABLE IF NOT EXISTS upstox_tokens (
                           id SERIAL PRIMARY KEY,
                           user_id VARCHAR(50) NOT NULL,
                           access_token TEXT NOT NULL,
                           user_name VARCHAR(100),
                           email VARCHAR(100),
                           broker VARCHAR(20),
                           user_type user_type_enum,
                           products JSONB,
                           exchanges JSONB,
                           is_active BOOLEAN DEFAULT TRUE,
                           created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                           expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                           metadata JSONB DEFAULT '{}'::jsonb,
                           last_used_at TIMESTAMP WITH TIME ZONE,
                           usage_count INTEGER DEFAULT 0
                       )
                   ''')
                   
                   # Create indexes
                   cursor.execute('''
                       CREATE INDEX IF NOT EXISTS idx_upstox_tokens_user_active
                       ON upstox_tokens(user_id, is_active)
                       WHERE is_active = TRUE
                   ''')
                   
                   cursor.execute('''
                       CREATE INDEX IF NOT EXISTS idx_upstox_tokens_expires
                       ON upstox_tokens(expires_at)
                   ''')
                   
                   cursor.execute('''
                       CREATE INDEX IF NOT EXISTS idx_upstox_tokens_created
                       ON upstox_tokens(created_at)
                   ''')
                   
                   # Create audit table
                   cursor.execute('''
                       CREATE TABLE IF NOT EXISTS upstox_token_audit (
                           id SERIAL PRIMARY KEY,
                           token_id INTEGER REFERENCES upstox_tokens(id),
                           action VARCHAR(20) NOT NULL,
                           performed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                           metadata JSONB DEFAULT '{}'::jsonb
                       )
                   ''')
                   
               conn.commit()

       @contextmanager
       def get_connection(self):
           """Get database connection with context management."""
           conn = psycopg2.connect(self.connection_string)
           try:
               yield conn
           finally:
               conn.close()

       def store_token(self, user_identifier=None):
           """Generate and store new token with audit trail."""
           response = self.upstox.app_token.get_access_token()
           
           if not response.success:
               raise Exception(f"Token generation failed: {response.error}")
           
           data = response.data
           expires_at = datetime.now() + timedelta(hours=24)
           
           with self.get_connection() as conn:
               with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                   # Deactivate old tokens
                   cursor.execute('''
                       UPDATE upstox_tokens 
                       SET is_active = FALSE,
                           metadata = metadata || '{"deactivated_at": "%s"}'::jsonb
                       WHERE user_id = %s AND is_active = TRUE
                       RETURNING id
                   ''', (datetime.now().isoformat(), data.user_id))
                   
                   deactivated_ids = [row['id'] for row in cursor.fetchall()]
                   
                   # Insert new token
                   cursor.execute('''
                       INSERT INTO upstox_tokens (
                           user_id, access_token, user_name, email, broker,
                           user_type, products, exchanges, expires_at, metadata
                       ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                       RETURNING id
                   ''', (
                       data.user_id,
                       data.access_token,
                       data.user_name,
                       data.email,
                       data.broker,
                       data.user_type,
                       json.dumps(data.products),
                       json.dumps(data.exchanges),
                       expires_at,
                       json.dumps({
                           'is_active_user': data.is_active,
                           'generation_method': 'upstox_totp_sdk',
                           'sdk_version': '1.0.3'
                       })
                   ))
                   
                   new_token_id = cursor.fetchone()['id']
                   
                   # Add audit entries
                   for old_id in deactivated_ids:
                       cursor.execute('''
                           INSERT INTO upstox_token_audit (token_id, action, metadata)
                           VALUES (%s, %s, %s)
                       ''', (old_id, 'deactivated', json.dumps({'reason': 'new_token_generated'})))
                   
                   cursor.execute('''
                       INSERT INTO upstox_token_audit (token_id, action, metadata)
                       VALUES (%s, %s, %s)
                   ''', (new_token_id, 'created', json.dumps({'generation_time': datetime.now().isoformat()})))
                   
               conn.commit()
               
           return {
               'token': data.access_token,
               'user_id': data.user_id,
               'token_id': new_token_id,
               'expires_at': expires_at.isoformat()
           }

       def get_valid_token(self, user_id):
           """Get valid token for user with usage tracking."""
           with self.get_connection() as conn:
               with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                   cursor.execute('''
                       SELECT id, access_token, expires_at, user_name, usage_count
                       FROM upstox_tokens
                       WHERE user_id = %s 
                         AND is_active = TRUE
                         AND expires_at > NOW() + INTERVAL '1 hour'
                       ORDER BY created_at DESC
                       LIMIT 1
                   ''', (user_id,))
                   
                   row = cursor.fetchone()
                   if row:
                       # Update usage tracking
                       cursor.execute('''
                           UPDATE upstox_tokens
                           SET usage_count = usage_count + 1,
                               last_used_at = NOW()
                           WHERE id = %s
                       ''', (row['id'],))
                       
                       cursor.execute('''
                           INSERT INTO upstox_token_audit (token_id, action, metadata)
                           VALUES (%s, %s, %s)
                       ''', (row['id'], 'used', json.dumps({'usage_count': row['usage_count'] + 1})))
                       
                       conn.commit()
                       
                       return {
                           'token': row['access_token'],
                           'user_name': row['user_name'],
                           'expires_at': row['expires_at'].isoformat(),
                           'usage_count': row['usage_count'] + 1
                       }
                   
                   return None

       def get_user_statistics(self, user_id):
           """Get comprehensive user statistics."""
           with self.get_connection() as conn:
               with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                   cursor.execute('''
                       SELECT 
                           COUNT(*) as total_tokens,
                           COUNT(*) FILTER (WHERE is_active = TRUE) as active_tokens,
                           SUM(usage_count) as total_usage,
                           MAX(created_at) as last_generation,
                           MAX(last_used_at) as last_usage,
                           AVG(usage_count) as avg_usage_per_token
                       FROM upstox_tokens
                       WHERE user_id = %s
                   ''', (user_id,))
                   
                   return dict(cursor.fetchone())

       def get_audit_trail(self, user_id, limit=50):
           """Get audit trail for user."""
           with self.get_connection() as conn:
               with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                   cursor.execute('''
                       SELECT 
                           a.action, a.performed_at, a.metadata,
                           t.user_id, t.created_at as token_created
                       FROM upstox_token_audit a
                       JOIN upstox_tokens t ON a.token_id = t.id
                       WHERE t.user_id = %s
                       ORDER BY a.performed_at DESC
                       LIMIT %s
                   ''', (user_id, limit))
                   
                   return [dict(row) for row in cursor.fetchall()]

   # Usage
   storage = PostgreSQLUpstoxStorage("postgresql://user:password@localhost/upstox_db")

   # Store token
   result = storage.store_token()
   print(f"Token stored with ID: {result['token_id']}")

   # Get statistics
   stats = storage.get_user_statistics(result['user_id'])
   print(f"User statistics: {stats}")

MongoDB Integration
-------------------

Document-Based Storage
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pymongo import MongoClient, ASCENDING, DESCENDING
   from datetime import datetime, timedelta
   from bson import ObjectId
   from upstox_totp import UpstoxTOTP

   class MongoUpstoxStorage:
       def __init__(self, connection_string, database_name='upstox_db'):
           self.client = MongoClient(connection_string)
           self.db = self.client[database_name]
           self.tokens = self.db.tokens
           self.audit = self.db.token_audit
           self.upstox = UpstoxTOTP()
           self.init_database()

       def init_database(self):
           """Initialize MongoDB collections and indexes."""
           # Create indexes for tokens collection
           self.tokens.create_index([
               ("user_id", ASCENDING),
               ("is_active", ASCENDING),
               ("expires_at", DESCENDING)
           ])
           
           self.tokens.create_index([("expires_at", ASCENDING)])
           self.tokens.create_index([("created_at", DESCENDING)])
           
           # Create indexes for audit collection
           self.audit.create_index([
               ("user_id", ASCENDING),
               ("performed_at", DESCENDING)
           ])
           
           # Create TTL index for automatic cleanup of expired tokens
           self.tokens.create_index([("expires_at", ASCENDING)], expireAfterSeconds=0)

       def store_token(self, user_identifier=None):
           """Generate and store new token."""
           response = self.upstox.app_token.get_access_token()
           
           if not response.success:
               raise Exception(f"Token generation failed: {response.error}")
           
           data = response.data
           now = datetime.utcnow()
           expires_at = now + timedelta(hours=24)
           
           # Deactivate old tokens
           old_tokens = self.tokens.update_many(
               {"user_id": data.user_id, "is_active": True},
               {
                   "$set": {
                       "is_active": False,
                       "deactivated_at": now,
                       "deactivation_reason": "new_token_generated"
                   }
               }
           )
           
           # Insert new token
           token_doc = {
               "user_id": data.user_id,
               "access_token": data.access_token,
               "user_name": data.user_name,
               "email": data.email,
               "broker": data.broker,
               "user_type": data.user_type,
               "products": data.products,
               "exchanges": data.exchanges,
               "is_active": True,
               "created_at": now,
               "expires_at": expires_at,
               "usage_count": 0,
               "last_used_at": None,
               "metadata": {
                   "is_active_user": data.is_active,
                   "generation_method": "upstox_totp_sdk",
                   "sdk_version": "1.0.3",
                   "generation_timestamp": now.isoformat()
               }
           }
           
           result = self.tokens.insert_one(token_doc)
           
           # Add audit entry
           self.audit.insert_one({
               "token_id": result.inserted_id,
               "user_id": data.user_id,
               "action": "token_created",
               "performed_at": now,
               "metadata": {
                   "old_tokens_deactivated": old_tokens.modified_count,
                   "generation_method": "upstox_totp_sdk"
               }
           })
           
           return {
               "token": data.access_token,
               "user_id": data.user_id,
               "token_id": str(result.inserted_id),
               "expires_at": expires_at.isoformat()
           }

       def get_valid_token(self, user_id):
           """Get valid token for user."""
           now = datetime.utcnow()
           buffer_time = now + timedelta(hours=1)
           
           token_doc = self.tokens.find_one({
               "user_id": user_id,
               "is_active": True,
               "expires_at": {"$gt": buffer_time}
           }, sort=[("created_at", DESCENDING)])
           
           if token_doc:
               # Update usage tracking
               self.tokens.update_one(
                   {"_id": token_doc["_id"]},
                   {
                       "$inc": {"usage_count": 1},
                       "$set": {"last_used_at": now}
                   }
               )
               
               # Add audit entry
               self.audit.insert_one({
                   "token_id": token_doc["_id"],
                   "user_id": user_id,
                   "action": "token_used",
                   "performed_at": now,
                   "metadata": {
                       "usage_count": token_doc["usage_count"] + 1
                   }
               })
               
               return {
                   "token": token_doc["access_token"],
                   "user_name": token_doc["user_name"],
                   "expires_at": token_doc["expires_at"].isoformat(),
                   "usage_count": token_doc["usage_count"] + 1
               }
           
           return None

       def get_user_dashboard(self, user_id):
           """Get comprehensive user dashboard data."""
           # User statistics
           pipeline = [
               {"$match": {"user_id": user_id}},
               {"$group": {
                   "_id": None,
                   "total_tokens": {"$sum": 1},
                   "active_tokens": {"$sum": {"$cond": ["$is_active", 1, 0]}},
                   "total_usage": {"$sum": "$usage_count"},
                   "avg_usage": {"$avg": "$usage_count"},
                   "last_generation": {"$max": "$created_at"},
                   "last_usage": {"$max": "$last_used_at"}
               }}
           ]
           
           stats = list(self.tokens.aggregate(pipeline))
           user_stats = stats[0] if stats else {}
           
           # Recent activity
           recent_audit = list(self.audit.find(
               {"user_id": user_id},
               sort=[("performed_at", DESCENDING)],
               limit=10
           ))
           
           # Current active token
           active_token = self.tokens.find_one({
               "user_id": user_id,
               "is_active": True
           }, sort=[("created_at", DESCENDING)])
           
           return {
               "user_id": user_id,
               "statistics": user_stats,
               "recent_activity": recent_audit,
               "active_token": {
                   "exists": active_token is not None,
                   "expires_at": active_token["expires_at"].isoformat() if active_token else None,
                   "usage_count": active_token.get("usage_count", 0) if active_token else 0
               }
           }

       def get_tokens_by_timeframe(self, start_date, end_date):
           """Get tokens generated within timeframe."""
           return list(self.tokens.find({
               "created_at": {
                   "$gte": start_date,
                   "$lte": end_date
               }
           }, {
               "access_token": 0  # Exclude sensitive token data
           }).sort("created_at", DESCENDING))

       def cleanup_old_audit_entries(self, days_to_keep=90):
           """Clean up old audit entries."""
           cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
           
           result = self.audit.delete_many({
               "performed_at": {"$lt": cutoff_date}
           })
           
           return result.deleted_count

   # Usage
   storage = MongoUpstoxStorage("mongodb://localhost:27017/")

   # Store token
   result = storage.store_token()
   print(f"Token stored: {result}")

   # Get user dashboard
   dashboard = storage.get_user_dashboard(result['user_id'])
   print(f"User dashboard: {dashboard}")

Redis with Backup Storage
-------------------------

Hybrid Redis + PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import redis
   import psycopg2
   import json
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP

   class HybridUpstoxStorage:
       def __init__(self, redis_config, postgres_config):
           # Redis for fast access
           self.redis_client = redis.Redis(**redis_config, decode_responses=True)
           
           # PostgreSQL for persistence
           self.postgres_conn_string = postgres_config
           
           self.upstox = UpstoxTOTP()
           self.redis_key_prefix = "upstox:token:"
           
           self.init_postgres()

       def init_postgres(self):
           """Initialize PostgreSQL backup storage."""
           with psycopg2.connect(self.postgres_conn_string) as conn:
               with conn.cursor() as cursor:
                   cursor.execute('''
                       CREATE TABLE IF NOT EXISTS upstox_token_backup (
                           id SERIAL PRIMARY KEY,
                           user_id VARCHAR(50) NOT NULL,
                           access_token TEXT NOT NULL,
                           user_data JSONB,
                           created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                           expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                           is_active BOOLEAN DEFAULT TRUE
                       )
                   ''')
                   
                   cursor.execute('''
                       CREATE INDEX IF NOT EXISTS idx_backup_user_active
                       ON upstox_token_backup(user_id, is_active, expires_at)
                   ''')
               
               conn.commit()

       def store_token(self, user_id=None):
           """Store token in both Redis and PostgreSQL."""
           response = self.upstox.app_token.get_access_token()
           
           if not response.success:
               raise Exception(f"Token generation failed: {response.error}")
           
           data = response.data
           now = datetime.now()
           expires_at = now + timedelta(hours=24)
           
           token_data = {
               "token": data.access_token,
               "user_id": data.user_id,
               "user_name": data.user_name,
               "email": data.email,
               "created_at": now.isoformat(),
               "expires_at": expires_at.isoformat(),
               "usage_count": 0
           }
           
           user_data = {
               "user_name": data.user_name,
               "email": data.email,
               "broker": data.broker,
               "user_type": data.user_type,
               "products": data.products,
               "exchanges": data.exchanges,
               "is_active": data.is_active
           }
           
           # Store in Redis with expiration
           redis_key = f"{self.redis_key_prefix}{data.user_id}"
           self.redis_client.setex(
               redis_key,
               23 * 3600,  # 23 hours
               json.dumps(token_data)
           )
           
           # Store in PostgreSQL for persistence
           with psycopg2.connect(self.postgres_conn_string) as conn:
               with conn.cursor() as cursor:
                   # Deactivate old tokens
                   cursor.execute('''
                       UPDATE upstox_token_backup
                       SET is_active = FALSE
                       WHERE user_id = %s AND is_active = TRUE
                   ''', (data.user_id,))
                   
                   # Insert new token
                   cursor.execute('''
                       INSERT INTO upstox_token_backup 
                       (user_id, access_token, user_data, expires_at)
                       VALUES (%s, %s, %s, %s)
                   ''', (
                       data.user_id,
                       data.access_token,
                       json.dumps(user_data),
                       expires_at
                   ))
               
               conn.commit()
           
           return token_data

       def get_valid_token(self, user_id):
           """Get token from Redis, fallback to PostgreSQL."""
           # Try Redis first (fast path)
           redis_key = f"{self.redis_key_prefix}{user_id}"
           cached_data = self.redis_client.get(redis_key)
           
           if cached_data:
               token_data = json.loads(cached_data)
               expires_at = datetime.fromisoformat(token_data["expires_at"])
               
               if expires_at > datetime.now() + timedelta(hours=1):
                   # Update usage count
                   token_data["usage_count"] += 1
                   self.redis_client.setex(
                       redis_key,
                       int((expires_at - datetime.now()).total_seconds()),
                       json.dumps(token_data)
                   )
                   
                   return token_data
           
           # Fallback to PostgreSQL (slow path)
           with psycopg2.connect(self.postgres_conn_string) as conn:
               with conn.cursor() as cursor:
                   cursor.execute('''
                       SELECT access_token, user_data, expires_at
                       FROM upstox_token_backup
                       WHERE user_id = %s 
                         AND is_active = TRUE
                         AND expires_at > NOW() + INTERVAL '1 hour'
                       ORDER BY created_at DESC
                       LIMIT 1
                   ''', (user_id,))
                   
                   row = cursor.fetchone()
                   if row:
                       user_data = json.loads(row[1])
                       token_data = {
                           "token": row[0],
                           "user_id": user_id,
                           "user_name": user_data.get("user_name"),
                           "email": user_data.get("email"),
                           "expires_at": row[2].isoformat(),
                           "usage_count": 1
                       }
                       
                       # Restore to Redis
                       expires_at = row[2]
                       ttl = int((expires_at - datetime.now()).total_seconds())
                       if ttl > 0:
                           self.redis_client.setex(
                               redis_key,
                               ttl,
                               json.dumps(token_data)
                           )
                       
                       return token_data
           
           return None

       def get_storage_status(self):
           """Get status of both storage systems."""
           try:
               # Test Redis
               redis_info = self.redis_client.info()
               redis_status = "healthy"
           except Exception as e:
               redis_status = f"error: {e}"
           
           try:
               # Test PostgreSQL
               with psycopg2.connect(self.postgres_conn_string) as conn:
                   with conn.cursor() as cursor:
                       cursor.execute("SELECT 1")
               postgres_status = "healthy"
           except Exception as e:
               postgres_status = f"error: {e}"
           
           return {
               "redis": redis_status,
               "postgresql": postgres_status,
               "timestamp": datetime.now().isoformat()
           }

   # Usage
   storage = HybridUpstoxStorage(
       redis_config={"host": "localhost", "port": 6379, "db": 0},
       postgres_config="postgresql://user:password@localhost/upstox_db"
   )

   # Store token
   result = storage.store_token()
   print(f"Token stored in hybrid storage: {result}")

   # Get storage status
   status = storage.get_storage_status()
   print(f"Storage status: {status}")

Performance Optimization
------------------------

Connection Pooling
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import sqlite3
   import threading
   from queue import Queue
   from contextlib import contextmanager
   from upstox_totp import UpstoxTOTP

   class PooledUpstoxStorage:
       def __init__(self, db_path, pool_size=5):
           self.db_path = db_path
           self.pool_size = pool_size
           self.pool = Queue(maxsize=pool_size)
           self.upstox = UpstoxTOTP()
           
           # Initialize connection pool
           for _ in range(pool_size):
               conn = sqlite3.connect(db_path, check_same_thread=False)
               conn.row_factory = sqlite3.Row
               self.pool.put(conn)
           
           self.init_database()

       @contextmanager
       def get_connection(self):
           """Get connection from pool."""
           conn = self.pool.get()
           try:
               yield conn
           finally:
               self.pool.put(conn)

       def init_database(self):
           """Initialize database schema."""
           with self.get_connection() as conn:
               conn.execute('''
                   CREATE TABLE IF NOT EXISTS upstox_tokens (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id TEXT NOT NULL,
                       access_token TEXT NOT NULL,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       expires_at TIMESTAMP NOT NULL,
                       is_active BOOLEAN DEFAULT TRUE
                   )
               ''')
               conn.commit()

       def store_token_batch(self, user_ids):
           """Store tokens for multiple users efficiently."""
           results = []
           
           with self.get_connection() as conn:
               for user_id in user_ids:
                   try:
                       response = self.upstox.app_token.get_access_token()
                       
                       if response.success:
                           data = response.data
                           expires_at = datetime.now() + timedelta(hours=24)
                           
                           # Deactivate old tokens
                           conn.execute('''
                               UPDATE upstox_tokens 
                               SET is_active = FALSE 
                               WHERE user_id = ? AND is_active = TRUE
                           ''', (data.user_id,))
                           
                           # Insert new token
                           cursor = conn.execute('''
                               INSERT INTO upstox_tokens (user_id, access_token, expires_at)
                               VALUES (?, ?, ?)
                               RETURNING id
                           ''', (data.user_id, data.access_token, expires_at))
                           
                           token_id = cursor.fetchone()[0]
                           
                           results.append({
                               'user_id': data.user_id,
                               'token_id': token_id,
                               'success': True
                           })
                       else:
                           results.append({
                               'user_id': user_id,
                               'success': False,
                               'error': str(response.error)
                           })
                           
                   except Exception as e:
                       results.append({
                           'user_id': user_id,
                           'success': False,
                           'error': str(e)
                       })
               
               conn.commit()
           
           return results

   # Usage
   pooled_storage = PooledUpstoxStorage("upstox_pooled.db", pool_size=10)

   # Batch token generation
   user_ids = ["user1", "user2", "user3"]
   results = pooled_storage.store_token_batch(user_ids)
   print(f"Batch results: {results}")

Best Practices
--------------

1. **Use Appropriate Database**: Choose based on your scaling needs
2. **Implement Connection Pooling**: For high-traffic applications
3. **Create Proper Indexes**: On frequently queried columns
4. **Store Audit Trails**: Track token usage and generation
5. **Handle Expired Tokens**: Implement cleanup routines
6. **Secure Sensitive Data**: Use encryption for tokens at rest
7. **Monitor Performance**: Track query performance and optimize
8. **Backup Regularly**: Ensure data persistence and recovery
9. **Use Transactions**: Ensure data consistency
10. **Test Failover**: Implement and test fallback mechanisms

Security Considerations
-----------------------

1. **Encrypt Tokens**: Use database-level encryption
2. **Limit Access**: Use proper database permissions
3. **Audit Access**: Log all token access and modifications
4. **Regular Rotation**: Implement token rotation policies
5. **Secure Connections**: Use SSL/TLS for database connections

See Also
--------

- :doc:`basic_usage` - Basic usage examples
- :doc:`token_caching` - Caching strategies
- :doc:`integration` - Framework integration
- :doc:`../security` - Security best practices
