Logging Reference
=================

The Upstox TOTP SDK provides comprehensive logging capabilities to help with debugging and monitoring.

Overview
--------

The SDK uses Python's standard logging module and provides several logging levels and categories to help you understand what's happening during execution.

Logging Configuration
---------------------

Basic Setup
~~~~~~~~~~~

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP

   # Configure basic logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )

   # Enable debug mode
   upx = UpstoxTOTP(debug=True)

Advanced Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP

   # Create custom logger
   logger = logging.getLogger('upstox_totp')
   logger.setLevel(logging.DEBUG)

   # Create file handler
   file_handler = logging.FileHandler('upstox.log')
   file_handler.setLevel(logging.DEBUG)

   # Create console handler
   console_handler = logging.StreamHandler()
   console_handler.setLevel(logging.INFO)

   # Create formatter
   formatter = logging.Formatter(
       '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
   )

   file_handler.setFormatter(formatter)
   console_handler.setFormatter(formatter)

   # Add handlers
   logger.addHandler(file_handler)
   logger.addHandler(console_handler)

   # Use with SDK
   upx = UpstoxTOTP(debug=True)

Logging Levels
--------------

The SDK uses standard Python logging levels:

DEBUG
~~~~~

Most detailed logging, includes:

- Request/response details
- TOTP generation steps  
- Session state changes
- Internal method calls

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP

   logging.basicConfig(level=logging.DEBUG)
   upx = UpstoxTOTP(debug=True)

INFO
~~~~

General information about operations:

- Token generation start/completion
- Configuration loading
- Major operation milestones

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP

   logging.basicConfig(level=logging.INFO)
   upx = UpstoxTOTP()

WARNING
~~~~~~~

Issues that don't prevent operation:

- Deprecated feature usage
- Unusual response codes
- Performance concerns

ERROR
~~~~~

Errors that prevent normal operation:

- Authentication failures
- Network errors
- Configuration problems

CRITICAL
~~~~~~~~

Serious errors requiring immediate attention:

- Security issues
- Data corruption
- System failures

Logging Categories
------------------

The SDK logs messages under different categories:

Core Logging
~~~~~~~~~~~~

**Logger Name**: ``upstox_totp.client``

Main client operations and high-level flows.

.. code-block:: python

   # Enable specific logger
   logging.getLogger('upstox_totp.client').setLevel(logging.DEBUG)

API Logging
~~~~~~~~~~~

**Logger Name**: ``upstox_totp.api``

API communication and response handling.

.. code-block:: python

   # Enable API logging
   logging.getLogger('upstox_totp.api').setLevel(logging.DEBUG)

Network Logging
~~~~~~~~~~~~~~~

**Logger Name**: ``urllib3``

HTTP request/response details (external library).

.. code-block:: python

   # Enable network logging
   logging.getLogger('urllib3.connectionpool').setLevel(logging.DEBUG)

Configuration Logging
~~~~~~~~~~~~~~~~~~~~~

**Logger Name**: ``upstox_totp.config``

Configuration loading and validation.

Debug Mode
----------

Enable Enhanced Logging
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Enable debug mode
   upx = UpstoxTOTP(debug=True)

Or via environment variable:

.. code-block:: bash

   export UPSTOX_DEBUG=true

Debug Output Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   2025-01-15 10:30:15,123 - upstox_totp.client - DEBUG - Initializing UpstoxTOTP client
   2025-01-15 10:30:15,124 - upstox_totp.config - DEBUG - Loading configuration from environment
   2025-01-15 10:30:15,125 - upstox_totp.client - DEBUG - Configuration validated successfully
   2025-01-15 10:30:15,126 - upstox_totp.client - INFO - Starting token generation
   2025-01-15 10:30:15,127 - upstox_totp.api - DEBUG - Generating TOTP code
   2025-01-15 10:30:15,128 - upstox_totp.api - DEBUG - TOTP generated: 123456
   2025-01-15 10:30:15,129 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection
   2025-01-15 10:30:16,234 - upstox_totp.api - DEBUG - Received response: 200
   2025-01-15 10:30:16,235 - upstox_totp.client - INFO - Token generated successfully

Custom Logging
--------------

Logger Creation
~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP

   class CustomUpstoxClient:
       def __init__(self):
           self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
           self.upx = UpstoxTOTP()

       def get_token_with_logging(self):
           self.logger.info("Starting token generation process")
           
           try:
               response = self.upx.app_token.get_access_token()
               
               if response.success:
                   self.logger.info("Token generated successfully")
                   self.logger.debug(f"Token length: {len(response.data.access_token)}")
                   return response.data.access_token
               else:
                   self.logger.error(f"Token generation failed: {response.error}")
                   return None
                   
           except Exception as e:
               self.logger.exception("Unexpected error during token generation")
               raise

Structured Logging
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import json
   from datetime import datetime
   from upstox_totp import UpstoxTOTP

   class StructuredLogger:
       def __init__(self):
           self.logger = logging.getLogger('structured')
           handler = logging.StreamHandler()
           handler.setFormatter(logging.Formatter('%(message)s'))
           self.logger.addHandler(handler)
           self.logger.setLevel(logging.INFO)

       def log_event(self, event_type, **kwargs):
           log_entry = {
               'timestamp': datetime.now().isoformat(),
               'event_type': event_type,
               'level': 'INFO',
               **kwargs
           }
           self.logger.info(json.dumps(log_entry))

   # Usage
   structured = StructuredLogger()

   upx = UpstoxTOTP()
   structured.log_event('token_generation_start', user_id='user123')

   response = upx.app_token.get_access_token()

   if response.success:
       structured.log_event(
           'token_generation_success',
           user_id='user123',
           token_length=len(response.data.access_token)
       )

Filtering Sensitive Data
------------------------

Security Considerations
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import re

   class SensitiveDataFilter(logging.Filter):
       """Filter to remove sensitive data from logs."""
       
       SENSITIVE_PATTERNS = [
           r'password["\s]*[:=]["\s]*[^"\s,}]+',
           r'token["\s]*[:=]["\s]*[^"\s,}]+',
           r'secret["\s]*[:=]["\s]*[^"\s,}]+',
           r'access_token["\s]*[:=]["\s]*[^"\s,}]+',
       ]

       def filter(self, record):
           if record.msg:
               message = str(record.msg)
               for pattern in self.SENSITIVE_PATTERNS:
                   message = re.sub(pattern, 'REDACTED', message, flags=re.IGNORECASE)
               record.msg = message
           return True

   # Apply filter
   logger = logging.getLogger('upstox_totp')
   logger.addFilter(SensitiveDataFilter())

Logging Best Practices
----------------------

Production Logging
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import logging.handlers
   from upstox_totp import UpstoxTOTP

   def setup_production_logging():
       """Set up logging for production environment."""
       
       # Create logger
       logger = logging.getLogger('upstox_totp')
       logger.setLevel(logging.INFO)  # INFO level for production

       # Create rotating file handler
       file_handler = logging.handlers.RotatingFileHandler(
           'upstox.log',
           maxBytes=10*1024*1024,  # 10MB
           backupCount=5
       )
       
       # Create console handler for errors only
       console_handler = logging.StreamHandler()
       console_handler.setLevel(logging.ERROR)

       # Create formatter
       formatter = logging.Formatter(
           '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
       )

       file_handler.setFormatter(formatter)
       console_handler.setFormatter(formatter)

       # Add handlers
       logger.addHandler(file_handler)
       logger.addHandler(console_handler)

       return logger

   # Usage
   setup_production_logging()
   upx = UpstoxTOTP()

Development Logging
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP

   def setup_development_logging():
       """Set up logging for development environment."""
       
       # Enable all logging
       logging.basicConfig(
           level=logging.DEBUG,
           format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
           handlers=[
               logging.FileHandler('debug.log'),
               logging.StreamHandler()
           ]
       )

       # Enable HTTP debugging
       import http.client as http_client
       http_client.HTTPConnection.debuglevel = 1

       # Enable urllib3 debugging
       logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)

   # Usage
   setup_development_logging()
   upx = UpstoxTOTP(debug=True)

Log Analysis
------------

Parsing Log Files
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import re
   from datetime import datetime
   from collections import defaultdict

   def analyze_logs(log_file):
       """Analyze upstox logs for patterns and issues."""
       
       stats = {
           'total_requests': 0,
           'successful_tokens': 0,
           'failed_tokens': 0,
           'errors_by_type': defaultdict(int),
           'response_times': []
       }

       with open(log_file, 'r') as f:
           for line in f:
               # Parse timestamp
               timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
               
               if 'Starting token generation' in line:
                   stats['total_requests'] += 1
               elif 'Token generated successfully' in line:
                   stats['successful_tokens'] += 1
               elif 'Token generation failed' in line:
                   stats['failed_tokens'] += 1
               elif 'ERROR' in line:
                   # Extract error type
                   error_match = re.search(r'ERROR.*?([A-Za-z]+Error)', line)
                   if error_match:
                       stats['errors_by_type'][error_match.group(1)] += 1

       return stats

   # Usage
   stats = analyze_logs('upstox.log')
   print(f"Success rate: {stats['successful_tokens']}/{stats['total_requests']}")

Monitoring and Alerting
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import smtplib
   from email.mime.text import MimeText

   class AlertHandler(logging.Handler):
       """Custom handler that sends alerts for critical errors."""
       
       def __init__(self, smtp_host, smtp_port, username, password, recipients):
           super().__init__()
           self.smtp_host = smtp_host
           self.smtp_port = smtp_port
           self.username = username
           self.password = password
           self.recipients = recipients
           self.setLevel(logging.ERROR)

       def emit(self, record):
           if record.levelno >= logging.ERROR:
               self.send_alert(record)

       def send_alert(self, record):
           try:
               msg = MimeText(f"Upstox TOTP Error: {record.getMessage()}")
               msg['Subject'] = 'Upstox TOTP Alert'
               msg['From'] = self.username
               msg['To'] = ', '.join(self.recipients)

               with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                   server.starttls()
                   server.login(self.username, self.password)
                   server.send_message(msg)
                   
           except Exception:
               # Don't let alert failures break the application
               pass

   # Usage (configure with your SMTP settings)
   # alert_handler = AlertHandler(
   #     smtp_host='smtp.gmail.com',
   #     smtp_port=587,
   #     username='your-email@gmail.com',
   #     password='your-password',
   #     recipients=['admin@company.com']
   # )
   # 
   # logger = logging.getLogger('upstox_totp')
   # logger.addHandler(alert_handler)

Performance Logging
-------------------

Timing Operations
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import time
   import functools
   from upstox_totp import UpstoxTOTP

   def log_performance(func):
       """Decorator to log function performance."""
       
       @functools.wraps(func)
       def wrapper(*args, **kwargs):
           logger = logging.getLogger(f'performance.{func.__name__}')
           start_time = time.time()
           
           try:
               result = func(*args, **kwargs)
               duration = time.time() - start_time
               logger.info(f"Completed in {duration:.2f}s")
               return result
               
           except Exception as e:
               duration = time.time() - start_time
               logger.error(f"Failed after {duration:.2f}s: {e}")
               raise
               
       return wrapper

   # Usage
   class PerformanceTrackedClient:
       def __init__(self):
           self.upx = UpstoxTOTP()

       @log_performance
       def get_token(self):
           return self.upx.app_token.get_access_token()

Memory Usage Tracking
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import psutil
   import os
   from upstox_totp import UpstoxTOTP

   def log_memory_usage():
       """Log current memory usage."""
       process = psutil.Process(os.getpid())
       memory_info = process.memory_info()
       
       logger = logging.getLogger('memory')
       logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.1f} MB")

   # Usage
   logging.basicConfig(level=logging.INFO)

   log_memory_usage()  # Before
   upx = UpstoxTOTP()
   response = upx.app_token.get_access_token()
   log_memory_usage()  # After

Common Logging Patterns
-----------------------

Error Context
~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from upstox_totp import UpstoxTOTP, UpstoxError

   logger = logging.getLogger(__name__)

   def get_token_with_context():
       context = {
           'operation': 'token_generation',
           'timestamp': datetime.now().isoformat(),
           'user_agent': 'MyApp/1.0'
       }
       
       try:
           logger.info("Token generation started", extra=context)
           
           upx = UpstoxTOTP()
           response = upx.app_token.get_access_token()
           
           if response.success:
               context['success'] = True
               context['token_length'] = len(response.data.access_token)
               logger.info("Token generation completed", extra=context)
               return response.data.access_token
           else:
               context['success'] = False
               context['error'] = str(response.error)
               logger.error("Token generation failed", extra=context)
               return None
               
       except Exception as e:
           context['success'] = False
           context['exception'] = str(e)
           logger.exception("Token generation exception", extra=context)
           raise

Request Tracing
~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import uuid
   from upstox_totp import UpstoxTOTP

   class TrackedUpstoxClient:
       def __init__(self):
           self.upx = UpstoxTOTP()
           self.logger = logging.getLogger(self.__class__.__name__)

       def get_token(self):
           trace_id = str(uuid.uuid4())[:8]
           
           self.logger.info(f"[{trace_id}] Token generation started")
           
           try:
               response = self.upx.app_token.get_access_token()
               
               if response.success:
                   self.logger.info(f"[{trace_id}] Token generation successful")
                   return response.data.access_token
               else:
                   self.logger.error(f"[{trace_id}] Token generation failed: {response.error}")
                   return None
                   
           except Exception as e:
               self.logger.exception(f"[{trace_id}] Token generation exception")
               raise

Configuration Examples
----------------------

JSON Logging
~~~~~~~~~~~~

.. code-block:: python

   import logging
   import json
   from datetime import datetime

   class JSONFormatter(logging.Formatter):
       def format(self, record):
           log_entry = {
               'timestamp': datetime.utcnow().isoformat(),
               'level': record.levelname,
               'logger': record.name,
               'message': record.getMessage(),
               'module': record.module,
               'function': record.funcName,
               'line': record.lineno
           }
           
           if record.exc_info:
               log_entry['exception'] = self.formatException(record.exc_info)
               
           return json.dumps(log_entry)

   # Configure JSON logging
   logger = logging.getLogger('upstox_totp')
   handler = logging.StreamHandler()
   handler.setFormatter(JSONFormatter())
   logger.addHandler(handler)

Syslog Integration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   import logging.handlers

   def setup_syslog():
       logger = logging.getLogger('upstox_totp')
       
       # Syslog handler
       syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
       
       formatter = logging.Formatter(
           'upstox-totp[%(process)d]: %(levelname)s - %(message)s'
       )
       
       syslog_handler.setFormatter(formatter)
       logger.addHandler(syslog_handler)

Troubleshooting Logging
-----------------------

Common Issues
~~~~~~~~~~~~~

**No log output:**

.. code-block:: python

   # Check logger level
   import logging
   logger = logging.getLogger('upstox_totp')
   print(f"Logger level: {logger.level}")
   print(f"Effective level: {logger.getEffectiveLevel()}")

**Too much output:**

.. code-block:: python

   # Reduce urllib3 logging
   logging.getLogger('urllib3').setLevel(logging.WARNING)

**Missing context:**

.. code-block:: python

   # Add more context to log messages
   logger.info("Token generation", extra={
       'user_id': 'user123',
       'client_version': '1.0.0',
       'environment': 'production'
   })

See Also
--------

- :doc:`../troubleshooting` - Troubleshooting guide
- :doc:`client` - Client API reference
- :doc:`errors` - Error handling
- :doc:`../security` - Security considerations
