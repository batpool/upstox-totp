Integration Examples
====================

This guide shows how to integrate the Upstox TOTP SDK with various frameworks and services.

Web Framework Integration
-------------------------

Flask Integration
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from flask import Flask, jsonify, request
   from upstox_totp import UpstoxTOTP, UpstoxError
   import logging

   app = Flask(__name__)
   logging.basicConfig(level=logging.INFO)

   class UpstoxService:
       def __init__(self):
           self.client = UpstoxTOTP()

       def get_access_token(self):
           try:
               response = self.client.app_token.get_access_token()
               if response.success:
                   return {
                       'success': True,
                       'token': response.data.access_token,
                       'user_id': response.data.user_id,
                       'user_name': response.data.user_name
                   }
               else:
                   return {
                       'success': False,
                       'error': str(response.error)
                   }
           except Exception as e:
               return {
                   'success': False,
                   'error': str(e)
               }

   upstox_service = UpstoxService()

   @app.route('/health')
   def health_check():
       return jsonify({'status': 'healthy', 'service': 'upstox-totp'})

   @app.route('/api/token', methods=['POST'])
   def generate_token():
       try:
           result = upstox_service.get_access_token()
           status_code = 200 if result['success'] else 400
           return jsonify(result), status_code
       except Exception as e:
           app.logger.error(f"Token generation failed: {e}")
           return jsonify({'success': False, 'error': 'Internal server error'}), 500

   @app.route('/api/user/profile')
   def get_user_profile():
       # Generate token first
       token_result = upstox_service.get_access_token()
       if not token_result['success']:
           return jsonify(token_result), 400

       # Use token to fetch profile
       import requests
       headers = {
           'Authorization': f"Bearer {token_result['token']}",
           'Content-Type': 'application/json'
       }

       try:
           response = requests.get(
               'https://api.upstox.com/v2/user/profile',
               headers=headers
           )
           return jsonify(response.json())
       except Exception as e:
           return jsonify({'error': str(e)}), 500

   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0', port=5000)

FastAPI Integration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fastapi import FastAPI, HTTPException, Depends
   from pydantic import BaseModel
   from upstox_totp import UpstoxTOTP, UpstoxError
   import logging
   from typing import Optional

   app = FastAPI(title="Upstox TOTP API", version="1.0.0")
   logging.basicConfig(level=logging.INFO)

   class TokenResponse(BaseModel):
       success: bool
       token: Optional[str] = None
       user_id: Optional[str] = None
       user_name: Optional[str] = None
       error: Optional[str] = None

   class UpstoxService:
       def __init__(self):
           self._client = None

       @property
       def client(self):
           if self._client is None:
               self._client = UpstoxTOTP()
           return self._client

       async def get_token(self) -> TokenResponse:
           try:
               response = self.client.app_token.get_access_token()
               if response.success:
                   return TokenResponse(
                       success=True,
                       token=response.data.access_token,
                       user_id=response.data.user_id,
                       user_name=response.data.user_name
                   )
               else:
                   return TokenResponse(
                       success=False,
                       error=str(response.error)
                   )
           except Exception as e:
               return TokenResponse(
                   success=False,
                   error=str(e)
               )

   # Dependency injection
   def get_upstox_service() -> UpstoxService:
       return UpstoxService()

   @app.get("/health")
   async def health_check():
       return {"status": "healthy", "service": "upstox-totp"}

   @app.post("/api/token", response_model=TokenResponse)
   async def generate_token(service: UpstoxService = Depends(get_upstox_service)):
       result = await service.get_token()
       if not result.success:
           raise HTTPException(status_code=400, detail=result.error)
       return result

   @app.get("/api/user/profile")
   async def get_user_profile(service: UpstoxService = Depends(get_upstox_service)):
       # Generate token
       token_result = await service.get_token()
       if not token_result.success:
           raise HTTPException(status_code=400, detail=token_result.error)

       # Fetch profile
       import httpx
       headers = {
           'Authorization': f'Bearer {token_result.token}',
           'Content-Type': 'application/json'
       }

       async with httpx.AsyncClient() as client:
           response = await client.get(
               'https://api.upstox.com/v2/user/profile',
               headers=headers
           )
           return response.json()

   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)

Django Integration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # views.py
   from django.http import JsonResponse
   from django.views import View
   from django.utils.decorators import method_decorator
   from django.views.decorators.csrf import csrf_exempt
   from upstox_totp import UpstoxTOTP, UpstoxError
   import json
   import logging

   logger = logging.getLogger(__name__)

   class UpstoxTokenView(View):
       def __init__(self):
           super().__init__()
           self.upstox_client = UpstoxTOTP()

       @method_decorator(csrf_exempt)
       def dispatch(self, request, *args, **kwargs):
           return super().dispatch(request, *args, **kwargs)

       def post(self, request):
           try:
               response = self.upstox_client.app_token.get_access_token()
               
               if response.success:
                   return JsonResponse({
                       'success': True,
                       'data': {
                           'access_token': response.data.access_token,
                           'user_id': response.data.user_id,
                           'user_name': response.data.user_name,
                           'email': response.data.email
                       }
                   })
               else:
                   return JsonResponse({
                       'success': False,
                       'error': str(response.error)
                   }, status=400)
                   
           except Exception as e:
               logger.error(f"Token generation failed: {e}")
               return JsonResponse({
                   'success': False,
                   'error': 'Internal server error'
               }, status=500)

   # urls.py
   from django.urls import path
   from .views import UpstoxTokenView

   urlpatterns = [
       path('api/token/', UpstoxTokenView.as_view(), name='upstox_token'),
   ]

   # settings.py addition
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'file': {
               'level': 'INFO',
               'class': 'logging.FileHandler',
               'filename': 'upstox.log',
           },
       },
       'loggers': {
           'upstox_totp': {
               'handlers': ['file'],
               'level': 'INFO',
               'propagate': True,
           },
       },
   }

Database Integration
--------------------

SQLAlchemy Integration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP
   import json

   Base = declarative_base()

   class UpstoxToken(Base):
       __tablename__ = 'upstox_tokens'

       id = Column(Integer, primary_key=True)
       user_id = Column(String(50), nullable=False)
       access_token = Column(Text, nullable=False)
       user_name = Column(String(100))
       email = Column(String(100))
       created_at = Column(DateTime, default=datetime.utcnow)
       expires_at = Column(DateTime, nullable=False)
       is_active = Column(Boolean, default=True)

   class UpstoxTokenManager:
       def __init__(self, database_url):
           self.engine = create_engine(database_url)
           Base.metadata.create_all(self.engine)
           self.Session = sessionmaker(bind=self.engine)
           self.upstox = UpstoxTOTP()

       def get_valid_token(self, user_identifier=None):
           """Get valid token from database or generate new one."""
           session = self.Session()
           
           try:
               # Try to find valid token
               now = datetime.utcnow()
               token_record = session.query(UpstoxToken).filter(
                   UpstoxToken.is_active == True,
                   UpstoxToken.expires_at > now + timedelta(hours=1)  # 1 hour buffer
               ).first()

               if token_record:
                   return token_record.access_token

               # Generate new token
               response = self.upstox.app_token.get_access_token()
               
               if response.success:
                   # Deactivate old tokens
                   session.query(UpstoxToken).filter(
                       UpstoxToken.is_active == True
                   ).update({'is_active': False})

                   # Store new token
                   new_token = UpstoxToken(
                       user_id=response.data.user_id,
                       access_token=response.data.access_token,
                       user_name=response.data.user_name,
                       email=response.data.email,
                       expires_at=datetime.utcnow() + timedelta(hours=24)
                   )
                   
                   session.add(new_token)
                   session.commit()
                   
                   return response.data.access_token
               else:
                   raise Exception(f"Token generation failed: {response.error}")
                   
           finally:
               session.close()

       def cleanup_expired_tokens(self):
           """Remove expired tokens from database."""
           session = self.Session()
           try:
               deleted = session.query(UpstoxToken).filter(
                   UpstoxToken.expires_at < datetime.utcnow()
               ).delete()
               session.commit()
               return deleted
           finally:
               session.close()

   # Usage
   token_manager = UpstoxTokenManager('sqlite:///upstox_tokens.db')
   token = token_manager.get_valid_token()

MongoDB Integration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pymongo import MongoClient
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP
   import logging

   class MongoUpstoxTokenManager:
       def __init__(self, connection_string, database_name='upstox_db'):
           self.client = MongoClient(connection_string)
           self.db = self.client[database_name]
           self.tokens = self.db.tokens
           self.upstox = UpstoxTOTP()
           self.logger = logging.getLogger(__name__)

       def get_valid_token(self):
           """Get valid token from MongoDB or generate new one."""
           # Check for valid token
           now = datetime.utcnow()
           buffer_time = now + timedelta(hours=1)
           
           token_doc = self.tokens.find_one({
               'is_active': True,
               'expires_at': {'$gt': buffer_time}
           })

           if token_doc:
               self.logger.info("Using cached token from MongoDB")
               return token_doc['access_token']

           # Generate new token
           self.logger.info("Generating new token")
           response = self.upstox.app_token.get_access_token()
           
           if response.success:
               # Deactivate old tokens
               self.tokens.update_many(
                   {'is_active': True},
                   {'$set': {'is_active': False}}
               )

               # Insert new token
               token_doc = {
                   'user_id': response.data.user_id,
                   'access_token': response.data.access_token,
                   'user_name': response.data.user_name,
                   'email': response.data.email,
                   'created_at': now,
                   'expires_at': now + timedelta(hours=24),
                   'is_active': True,
                   'metadata': {
                       'broker': response.data.broker,
                       'products': response.data.products,
                       'exchanges': response.data.exchanges
                   }
               }
               
               self.tokens.insert_one(token_doc)
               self.logger.info("New token stored in MongoDB")
               
               return response.data.access_token
           else:
               raise Exception(f"Token generation failed: {response.error}")

       def get_token_history(self, limit=10):
           """Get token generation history."""
           return list(self.tokens.find(
               {},
               {'access_token': 0}  # Exclude sensitive token data
           ).sort('created_at', -1).limit(limit))

   # Usage
   mongo_manager = MongoUpstoxTokenManager('mongodb://localhost:27017/')
   token = mongo_manager.get_valid_token()

Redis Integration
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import redis
   import json
   from datetime import datetime, timedelta
   from upstox_totp import UpstoxTOTP

   class RedisUpstoxTokenManager:
       def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
           self.redis_client = redis.Redis(
               host=redis_host,
               port=redis_port,
               db=redis_db,
               decode_responses=True
           )
           self.upstox = UpstoxTOTP()
           self.token_key = 'upstox:token'
           self.metadata_key = 'upstox:metadata'

       def get_valid_token(self):
           """Get valid token from Redis cache or generate new one."""
           # Check cache
           cached_token = self.redis_client.get(self.token_key)
           
           if cached_token:
               return cached_token

           # Generate new token
           response = self.upstox.app_token.get_access_token()
           
           if response.success:
               token = response.data.access_token
               
               # Cache token with expiration (23 hours to be safe)
               self.redis_client.setex(
                   self.token_key,
                   timedelta(hours=23),
                   token
               )
               
               # Store metadata separately
               metadata = {
                   'user_id': response.data.user_id,
                   'user_name': response.data.user_name,
                   'email': response.data.email,
                   'generated_at': datetime.utcnow().isoformat()
               }
               
               self.redis_client.setex(
                   self.metadata_key,
                   timedelta(hours=23),
                   json.dumps(metadata)
               )
               
               return token
           else:
               raise Exception(f"Token generation failed: {response.error}")

       def get_token_metadata(self):
           """Get token metadata from cache."""
           metadata_json = self.redis_client.get(self.metadata_key)
           if metadata_json:
               return json.loads(metadata_json)
           return None

       def invalidate_token(self):
           """Manually invalidate cached token."""
           self.redis_client.delete(self.token_key, self.metadata_key)

   # Usage
   redis_manager = RedisUpstoxTokenManager()
   token = redis_manager.get_valid_token()

Background Job Integration
--------------------------

Celery Integration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from celery import Celery
   from upstox_totp import UpstoxTOTP, UpstoxError
   import logging
   from datetime import datetime

   # Configure Celery
   app = Celery('upstox_tasks', broker='redis://localhost:6379/0')

   # Configure logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   @app.task(bind=True, max_retries=3)
   def generate_upstox_token(self):
       """Background task to generate Upstox token."""
       try:
           upstox = UpstoxTOTP()
           response = upstox.app_token.get_access_token()
           
           if response.success:
               result = {
                   'success': True,
                   'token': response.data.access_token,
                   'user_id': response.data.user_id,
                   'generated_at': datetime.utcnow().isoformat()
               }
               logger.info(f"Token generated successfully: {result['user_id']}")
               return result
           else:
               raise Exception(f"Token generation failed: {response.error}")
               
       except Exception as e:
           logger.error(f"Token generation task failed: {e}")
           
           # Retry with exponential backoff
           countdown = 2 ** self.request.retries
           raise self.retry(exc=e, countdown=countdown)

   @app.task
   def refresh_all_user_tokens():
       """Background task to refresh tokens for all users."""
       # This would integrate with your user management system
       results = []
       
       # Example: get all users who need token refresh
       users_needing_refresh = get_users_needing_refresh()  # Implement this
       
       for user in users_needing_refresh:
           try:
               # Generate token for each user
               result = generate_upstox_token.delay()
               results.append({
                   'user_id': user['id'],
                   'task_id': result.id,
                   'status': 'pending'
               })
           except Exception as e:
               logger.error(f"Failed to queue token refresh for user {user['id']}: {e}")
               
       return results

   # Periodic task
   from celery.schedules import crontab

   app.conf.beat_schedule = {
       'refresh-tokens-daily': {
           'task': 'refresh_all_user_tokens',
           'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
       },
   }

APScheduler Integration
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from apscheduler.schedulers.blocking import BlockingScheduler
   from apscheduler.schedulers.background import BackgroundScheduler
   from upstox_totp import UpstoxTOTP
   import logging
   from datetime import datetime

   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   class UpstoxTokenScheduler:
       def __init__(self):
           self.scheduler = BackgroundScheduler()
           self.upstox = UpstoxTOTP()
           self.current_token = None
           
       def generate_token(self):
           """Job function to generate token."""
           try:
               logger.info("Starting scheduled token generation")
               response = self.upstox.app_token.get_access_token()
               
               if response.success:
                   self.current_token = response.data.access_token
                   logger.info(f"Token generated successfully at {datetime.now()}")
               else:
                   logger.error(f"Token generation failed: {response.error}")
                   
           except Exception as e:
               logger.error(f"Token generation exception: {e}")

       def start_scheduler(self):
           """Start the token refresh scheduler."""
           # Generate token immediately
           self.generate_token()
           
           # Schedule token refresh every 23 hours
           self.scheduler.add_job(
               self.generate_token,
               'interval',
               hours=23,
               id='token_refresh',
               replace_existing=True
           )
           
           self.scheduler.start()
           logger.info("Token refresh scheduler started")

       def stop_scheduler(self):
           """Stop the scheduler."""
           self.scheduler.shutdown()
           logger.info("Token refresh scheduler stopped")

       def get_current_token(self):
           """Get the current valid token."""
           if not self.current_token:
               self.generate_token()
           return self.current_token

   # Usage
   token_scheduler = UpstoxTokenScheduler()
   token_scheduler.start_scheduler()

   # Get token when needed
   token = token_scheduler.get_current_token()

Cloud Service Integration
-------------------------

AWS Lambda Integration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import json
   import boto3
   from upstox_totp import UpstoxTOTP, UpstoxError
   import logging

   # Configure logging for Lambda
   logger = logging.getLogger()
   logger.setLevel(logging.INFO)

   def lambda_handler(event, context):
       """AWS Lambda function to generate Upstox token."""
       
       try:
           # Initialize Upstox client
           upstox = UpstoxTOTP()
           
           # Generate token
           response = upstox.app_token.get_access_token()
           
           if response.success:
               # Store token in Parameter Store
               ssm = boto3.client('ssm')
               ssm.put_parameter(
                   Name='/upstox/access_token',
                   Value=response.data.access_token,
                   Type='SecureString',
                   Overwrite=True
               )
               
               # Return success response
               return {
                   'statusCode': 200,
                   'body': json.dumps({
                       'success': True,
                       'user_id': response.data.user_id,
                       'message': 'Token generated and stored successfully'
                   })
               }
           else:
               logger.error(f"Token generation failed: {response.error}")
               return {
                   'statusCode': 400,
                   'body': json.dumps({
                       'success': False,
                       'error': str(response.error)
                   })
               }
               
       except Exception as e:
           logger.error(f"Lambda function error: {e}")
           return {
               'statusCode': 500,
               'body': json.dumps({
                   'success': False,
                   'error': 'Internal server error'
               })
           }

   # CloudWatch Events integration
   def scheduled_lambda_handler(event, context):
       """Lambda function triggered by CloudWatch Events for periodic token refresh."""
       
       logger.info("Scheduled token refresh triggered")
       
       try:
           upstox = UpstoxTOTP()
           response = upstox.app_token.get_access_token()
           
           if response.success:
               # Store in Parameter Store
               ssm = boto3.client('ssm')
               ssm.put_parameter(
                   Name='/upstox/access_token',
                   Value=response.data.access_token,
                   Type='SecureString',
                   Overwrite=True
               )
               
               # Send notification
               sns = boto3.client('sns')
               sns.publish(
                   TopicArn='arn:aws:sns:region:account:upstox-notifications',
                   Message=f'Token refreshed successfully for user {response.data.user_id}',
                   Subject='Upstox Token Refresh Success'
               )
               
               logger.info("Scheduled token refresh completed successfully")
               
           else:
               # Send error notification
               sns = boto3.client('sns')
               sns.publish(
                   TopicArn='arn:aws:sns:region:account:upstox-notifications',
                   Message=f'Token refresh failed: {response.error}',
                   Subject='Upstox Token Refresh Failed'
               )
               
               logger.error(f"Scheduled token refresh failed: {response.error}")
               
       except Exception as e:
           logger.error(f"Scheduled token refresh error: {e}")
           
           # Send error notification
           sns = boto3.client('sns')
           sns.publish(
               TopicArn='arn:aws:sns:region:account:upstox-notifications',
               Message=f'Token refresh error: {str(e)}',
               Subject='Upstox Token Refresh Error'
           )

Google Cloud Functions Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import functions_framework
   from google.cloud import secretmanager
   from upstox_totp import UpstoxTOTP, UpstoxError
   import json
   import logging

   @functions_framework.http
   def generate_upstox_token(request):
       """HTTP Cloud Function to generate Upstox token."""
       
       # Set CORS headers
       headers = {
           'Access-Control-Allow-Origin': '*',
           'Access-Control-Allow-Methods': 'POST',
           'Access-Control-Allow-Headers': 'Content-Type'
       }
       
       if request.method == 'OPTIONS':
           return ('', 204, headers)
       
       try:
           # Initialize Upstox client
           upstox = UpstoxTOTP()
           
           # Generate token
           response = upstox.app_token.get_access_token()
           
           if response.success:
               # Store token in Secret Manager
               client = secretmanager.SecretManagerServiceClient()
               project_id = "your-project-id"
               secret_id = "upstox-access-token"
               
               # Create or update secret
               parent = f"projects/{project_id}"
               secret_path = f"{parent}/secrets/{secret_id}"
               
               try:
                   # Add secret version
                   client.add_secret_version(
                       parent=secret_path,
                       payload={'data': response.data.access_token.encode('utf-8')}
                   )
               except Exception:
                   # Secret might not exist, create it
                   client.create_secret(
                       parent=parent,
                       secret_id=secret_id,
                       secret={'replication': {'automatic': {}}}
                   )
                   client.add_secret_version(
                       parent=secret_path,
                       payload={'data': response.data.access_token.encode('utf-8')}
                   )
               
               return (json.dumps({
                   'success': True,
                   'user_id': response.data.user_id,
                   'message': 'Token generated successfully'
               }), 200, headers)
           else:
               return (json.dumps({
                   'success': False,
                   'error': str(response.error)
               }), 400, headers)
               
       except Exception as e:
           logging.error(f"Cloud Function error: {e}")
           return (json.dumps({
               'success': False,
               'error': 'Internal server error'
           }), 500, headers)

Docker Integration
------------------

Production Docker Setup
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: dockerfile

   # Dockerfile
   FROM python:3.12-slim

   # Set working directory
   WORKDIR /app

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       curl \
       && rm -rf /var/lib/apt/lists/*

   # Install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application code
   COPY . .

   # Create non-root user
   RUN useradd --create-home --shell /bin/bash upstox
   RUN chown -R upstox:upstox /app
   USER upstox

   # Health check
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
       CMD curl -f http://localhost:8000/health || exit 1

   # Run application
   CMD ["python", "app.py"]

.. code-block:: yaml

   # docker-compose.yml
   version: '3.8'

   services:
     upstox-api:
       build: .
       ports:
         - "8000:8000"
       environment:
         - UPSTOX_USERNAME=${UPSTOX_USERNAME}
         - UPSTOX_PASSWORD=${UPSTOX_PASSWORD}
         - UPSTOX_PIN_CODE=${UPSTOX_PIN_CODE}
         - UPSTOX_TOTP_SECRET=${UPSTOX_TOTP_SECRET}
         - UPSTOX_CLIENT_ID=${UPSTOX_CLIENT_ID}
         - UPSTOX_CLIENT_SECRET=${UPSTOX_CLIENT_SECRET}
         - UPSTOX_REDIRECT_URI=${UPSTOX_REDIRECT_URI}
         - REDIS_URL=redis://redis:6379/0
       depends_on:
         - redis
       restart: unless-stopped
       volumes:
         - ./logs:/app/logs

     redis:
       image: redis:7-alpine
       ports:
         - "6379:6379"
       restart: unless-stopped
       volumes:
         - redis_data:/data

     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
         - ./ssl:/etc/nginx/ssl
       depends_on:
         - upstox-api
       restart: unless-stopped

   volumes:
     redis_data:

Kubernetes Integration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # k8s-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: upstox-totp-api
     labels:
       app: upstox-totp-api
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: upstox-totp-api
     template:
       metadata:
         labels:
           app: upstox-totp-api
       spec:
         containers:
         - name: upstox-api
           image: your-registry/upstox-totp-api:latest
           ports:
           - containerPort: 8000
           env:
           - name: UPSTOX_USERNAME
             valueFrom:
               secretKeyRef:
                 name: upstox-credentials
                 key: username
           - name: UPSTOX_PASSWORD
             valueFrom:
               secretKeyRef:
                 name: upstox-credentials
                 key: password
           # ... other environment variables
           livenessProbe:
             httpGet:
               path: /health
               port: 8000
             initialDelaySeconds: 30
             periodSeconds: 10
           readinessProbe:
             httpGet:
               path: /health
               port: 8000
             initialDelaySeconds: 5
             periodSeconds: 5
           resources:
             requests:
               memory: "128Mi"
               cpu: "100m"
             limits:
               memory: "512Mi"
               cpu: "500m"

   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: upstox-totp-service
   spec:
     selector:
       app: upstox-totp-api
     ports:
     - protocol: TCP
       port: 80
       targetPort: 8000
     type: LoadBalancer

   ---
   apiVersion: v1
   kind: Secret
   metadata:
     name: upstox-credentials
   type: Opaque
   data:
     username: <base64-encoded-username>
     password: <base64-encoded-password>
     # ... other credentials

Testing Integration
-------------------

pytest Integration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # test_integration.py
   import pytest
   from unittest.mock import patch, Mock
   from your_app import app, UpstoxService
   from upstox_totp.models import AccessTokenResponse, AccessTokenData

   @pytest.fixture
   def client():
       app.config['TESTING'] = True
       with app.test_client() as client:
           yield client

   @pytest.fixture
   def mock_upstox_response():
       return AccessTokenResponse(
           success=True,
           data=AccessTokenData(
               access_token="test-token-123",
               user_id="TEST123",
               user_name="Test User",
               email="test@example.com",
               broker="UPSTOX",
               user_type="individual",
               products=["D", "I"],
               exchanges=["NSE_EQ", "BSE_EQ"],
               is_active=True
           ),
           error=None
       )

   @patch('your_app.UpstoxTOTP')
   def test_token_generation_success(mock_upstox_class, client, mock_upstox_response):
       # Setup mock
       mock_upstox_instance = Mock()
       mock_upstox_instance.app_token.get_access_token.return_value = mock_upstox_response
       mock_upstox_class.return_value = mock_upstox_instance

       # Make request
       response = client.post('/api/token')
       
       # Assert response
       assert response.status_code == 200
       data = response.get_json()
       assert data['success'] is True
       assert data['token'] == "test-token-123"

   @patch('your_app.UpstoxTOTP')
   def test_token_generation_failure(mock_upstox_class, client):
       # Setup mock for failure
       mock_upstox_instance = Mock()
       mock_upstox_instance.app_token.get_access_token.return_value = AccessTokenResponse(
           success=False,
           data=None,
           error={'message': 'Invalid credentials'}
       )
       mock_upstox_class.return_value = mock_upstox_instance

       # Make request
       response = client.post('/api/token')
       
       # Assert response
       assert response.status_code == 400
       data = response.get_json()
       assert data['success'] is False

Monitoring Integration
----------------------

Prometheus Integration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from prometheus_client import Counter, Histogram, Gauge, start_http_server
   from upstox_totp import UpstoxTOTP
   import time

   # Metrics
   token_requests_total = Counter('upstox_token_requests_total', 'Total token requests')
   token_requests_duration = Histogram('upstox_token_requests_duration_seconds', 'Token request duration')
   token_generation_failures = Counter('upstox_token_generation_failures_total', 'Token generation failures')
   active_tokens = Gauge('upstox_active_tokens', 'Number of active tokens')

   class MonitoredUpstoxClient:
       def __init__(self):
           self.upstox = UpstoxTOTP()

       @token_requests_duration.time()
       def get_token(self):
           token_requests_total.inc()
           
           try:
               response = self.upstox.app_token.get_access_token()
               
               if response.success:
                   active_tokens.inc()
                   return response.data.access_token
               else:
                   token_generation_failures.inc()
                   raise Exception(f"Token generation failed: {response.error}")
                   
           except Exception as e:
               token_generation_failures.inc()
               raise

   # Start metrics server
   start_http_server(8001)

   # Usage
   client = MonitoredUpstoxClient()

Best Practices
--------------

1. **Environment Configuration**: Use environment variables for all sensitive data
2. **Error Handling**: Implement comprehensive error handling and logging
3. **Token Caching**: Cache tokens appropriately to avoid unnecessary API calls
4. **Security**: Follow security best practices for token storage and transmission
5. **Monitoring**: Implement monitoring and alerting for production deployments
6. **Testing**: Write comprehensive tests for all integration points
7. **Documentation**: Document your integration for future maintenance

See Also
--------

- :doc:`basic_usage` - Basic usage examples
- :doc:`token_caching` - Token caching strategies
- :doc:`../security` - Security best practices
- :doc:`../configuration` - Configuration guide
