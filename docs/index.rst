Upstox TOTP Python SDK
======================

.. image:: https://cdn.statically.io/gh/batpool/upstox-totp/master/assets/upstox-totp.png
   :alt: Upstox TOTP Logo
   :align: center
   :width: 100%

A modern, lightweight Python package that simplifies Upstox API authentication by handling TOTP-based login and token generation automatically. With this library, you can securely generate and refresh access tokens required to connect to the Upstox trading platform without manual intervention.

.. image:: https://img.shields.io/pypi/v/upstox-totp?logo=pypi&logoColor=white&label=PyPI&color=blue
   :target: https://pypi.org/project/upstox-totp/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/dm/upstox-totp?logo=pypi&logoColor=white&label=Downloads&color=green
   :target: https://pypi.org/project/upstox-totp/
   :alt: PyPI Downloads

.. image:: https://img.shields.io/pypi/pyversions/upstox-totp?logo=python&logoColor=white&label=Python
   :target: https://pypi.org/project/upstox-totp/
   :alt: Python Versions

.. image:: https://img.shields.io/pypi/l/upstox-totp?logo=opensource&logoColor=white&color=green
   :target: https://github.com/batpool/upstox-totp/blob/master/LICENSE
   :alt: License

Features
--------

🔐 **Automated TOTP Authentication** – Generate secure time-based one-time passwords (TOTP) for Upstox login

⚡ **Token Management** – Fetch, refresh, and store Upstox access tokens with ease

🛠️ **Simple API** – Minimal, developer-friendly methods for quick integration

📈 **Trading Ready** – Instantly plug into Upstox APIs for real-time market data, order placement, and portfolio management

🐍 **Pythonic Design** – Built with modern async/session handling for robust performance

🎯 **CLI Tool** – Command-line interface for quick token generation

🔧 **Environment Configuration** – Auto-configuration from environment variables

💡 **Helpful Error Messages** – Clear error messages with troubleshooting guidance

🔒 **Secure by Design** – Uses secure SecretStr for sensitive data handling

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   # Add as a dependency to your project
   uv add upstox-totp

   # Or install with pip
   pip install upstox-totp

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from upstox_totp import UpstoxTOTP

   # Initialize (auto-loads from environment variables or .env file)
   upx = UpstoxTOTP()

   # Generate access token
   try:
       response = upx.app_token.get_access_token()
       
       if response.success and response.data:
           print(f"✅ Access Token: {response.data.access_token}")
           print(f"👤 User: {response.data.user_name} ({response.data.user_id})")
           print(f"📧 Email: {response.data.email}")
           print(f"🏢 Broker: {response.data.broker}")
           
           # Use the token for Upstox API calls
           access_token = response.data.access_token
           
   except Exception as e:
       print(f"❌ Error: {e}")

CLI Usage
~~~~~~~~~

.. code-block:: bash

   # Check if environment is properly configured
   upstox_cli check-env

   # Generate access token
   upstox_cli generate-token

Documentation Contents
======================

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   configuration
   advanced_usage
   cli_reference

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/client
   api/models
   api/errors
   api/logging

.. toctree::
   :maxdepth: 2
   :caption: Examples & Tutorials

   examples/basic_usage
   examples/integration
   examples/token_caching
   examples/database_storage

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   security
   troubleshooting
   contributing
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Requirements
============

- Python 3.12 or higher
- Active Upstox trading account
- Upstox Developer App (for client credentials)
- TOTP app setup (Google Authenticator, Authy, etc.)

License
=======

MIT License - see :doc:`license` for details.

Important Notes
===============

.. warning::
   **📅 Access Token Expiry**: Upstox access tokens have a **24-hour expiration time**. For production applications, it's recommended to:
   
   - Store tokens securely in a database or cache (Redis, etc.)
   - Implement automatic token refresh logic
   - Monitor token expiry and regenerate proactively

.. note::
   This is an unofficial library for Upstox API authentication. Please ensure you comply with Upstox's terms of service and API usage guidelines. Use at your own risk.

Links
=====

- `GitHub Repository <https://github.com/batpool/upstox-totp>`_
- `PyPI Package <https://pypi.org/project/upstox-totp/>`_
- `Issue Tracker <https://github.com/batpool/upstox-totp/issues>`_
- `Reddit Community <https://www.reddit.com/user/iamdeadloop/>`_
