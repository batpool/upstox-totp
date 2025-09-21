Installation Guide
==================

This guide will help you install the Upstox TOTP Python SDK in your environment.

Requirements
------------

Before installing, ensure you have:

- **Python 3.12 or higher**
- **Active Upstox trading account**
- **Upstox Developer App** (for client credentials)
- **TOTP app setup** (Google Authenticator, Authy, etc.)

Installation Methods
--------------------

Using uv (Recommended)
~~~~~~~~~~~~~~~~~~~~~~

If you're using `uv <https://github.com/astral-sh/uv>`_ as your Python package manager:

.. code-block:: bash

   # Add to your project
   uv add upstox-totp

   # Or install globally
   uv tool install upstox-totp

Using pip
~~~~~~~~~

.. code-block:: bash

   # Install from PyPI
   pip install upstox-totp

   # Install specific version
   pip install upstox-totp==1.0.3

   # Install with extra dependencies (if available)
   pip install upstox-totp[dev]

Using pipx (For CLI usage)
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you only want to use the CLI tool:

.. code-block:: bash

   # Install CLI tool globally
   pipx install upstox-totp

   # Use the CLI
   upstox_cli --help

Development Installation
------------------------

If you want to contribute or run the latest development version:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/batpool/upstox-totp.git
   cd upstox-totp

   # Install dependencies with uv
   uv sync

   # Install development dependencies
   uv sync --group dev

   # Install in editable mode
   uv pip install -e .

Virtual Environment Setup
--------------------------

It's recommended to use a virtual environment:

Using venv
~~~~~~~~~~

.. code-block:: bash

   # Create virtual environment
   python -m venv upstox-env

   # Activate (Linux/macOS)
   source upstox-env/bin/activate

   # Activate (Windows)
   upstox-env\Scripts\activate

   # Install package
   pip install upstox-totp

Using conda
~~~~~~~~~~~

.. code-block:: bash

   # Create conda environment
   conda create -n upstox-env python=3.12

   # Activate environment
   conda activate upstox-env

   # Install package
   pip install upstox-totp

Using Poetry
~~~~~~~~~~~~

.. code-block:: bash

   # Initialize project (if new)
   poetry init

   # Add dependency
   poetry add upstox-totp

   # Install dependencies
   poetry install

   # Run in poetry environment
   poetry run upstox_cli --help

Verification
------------

After installation, verify that everything is working:

.. code-block:: bash

   # Check CLI is available
   upstox_cli --help

   # Check Python package
   python -c "import upstox_totp; print(upstox_totp.__version__)"

Expected output:

.. code-block:: text

   Usage: upstox_cli [OPTIONS] COMMAND [ARGS]...

     Upstox TOTP CLI - Generate access tokens for Upstox API authentication.

   Options:
     --version  Show the version and exit.
     --help     Show this message and exit.

   Commands:
     check-env        Check if environment variables are properly configured.
     generate-token   Generate Upstox access token using TOTP authentication.

Docker Installation
-------------------

If you prefer using Docker:

.. code-block:: dockerfile

   FROM python:3.12-slim

   # Install upstox-totp
   RUN pip install upstox-totp

   # Set working directory
   WORKDIR /app

   # Copy your application
   COPY . .

   # Set environment variables
   ENV UPSTOX_USERNAME=your-username
   ENV UPSTOX_PASSWORD=your-password
   # ... other environment variables

   # Run your application
   CMD ["python", "your_app.py"]

Build and run:

.. code-block:: bash

   # Build image
   docker build -t my-upstox-app .

   # Run container
   docker run --env-file .env my-upstox-app

Troubleshooting Installation
----------------------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'upstox_totp'**

.. code-block:: bash

   # Ensure you're in the correct environment
   which python
   python -m pip list | grep upstox

   # Reinstall if necessary
   pip uninstall upstox-totp
   pip install upstox-totp

**Permission denied errors**

.. code-block:: bash

   # Use --user flag
   pip install --user upstox-totp

   # Or use virtual environment
   python -m venv venv
   source venv/bin/activate
   pip install upstox-totp

**SSL Certificate errors**

.. code-block:: bash

   # Install with trusted hosts
   pip install --trusted-host pypi.org --trusted-host pypi.python.org upstox-totp

   # Or upgrade certificates
   pip install --upgrade certifi

**Python version compatibility**

.. code-block:: bash

   # Check Python version
   python --version

   # Use specific Python version
   python3.12 -m pip install upstox-totp

Dependencies
------------

The package automatically installs these dependencies:

Core Dependencies
~~~~~~~~~~~~~~~~~

- **click>=8.3.0** - Command-line interface framework
- **curl-cffi>=0.13.0** - HTTP client with better performance
- **dotenv>=0.9.9** - Environment variable management
- **pydantic>=2.11.9** - Data validation and settings management
- **pyotp>=2.9.0** - TOTP (Time-based One-Time Password) generation

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

- **black>=25.9.0** - Code formatting
- **isort>=6.0.1** - Import sorting

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

For documentation building:

- **sphinx** - Documentation generator
- **sphinx-rtd-theme** - Read the Docs theme
- **myst-parser** - Markdown parser for Sphinx

Installation Verification Script
--------------------------------

Create a simple script to verify installation:

.. code-block:: python

   # verify_installation.py
   
   def verify_installation():
       """Verify that upstox-totp is properly installed."""
       try:
           import upstox_totp
           from upstox_totp import UpstoxTOTP
           
           print(f"✅ upstox-totp version: {upstox_totp.__version__}")
           print("✅ All imports successful")
           
           # Try to initialize (will fail without env vars, but import should work)
           try:
               upx = UpstoxTOTP()
               print("✅ UpstoxTOTP class can be instantiated")
           except Exception as e:
               print(f"⚠️  UpstoxTOTP instantiation failed (expected without env vars): {e}")
           
           print("\n🎉 Installation verified successfully!")
           
       except ImportError as e:
           print(f"❌ Import failed: {e}")
           print("💡 Try reinstalling: pip install upstox-totp")
           
       except Exception as e:
           print(f"❌ Unexpected error: {e}")

   if __name__ == "__main__":
       verify_installation()

Run the verification:

.. code-block:: bash

   python verify_installation.py

Next Steps
----------

After successful installation:

1. **Set up your credentials** - See :doc:`configuration`
2. **Try the quickstart** - See :doc:`quickstart`
3. **Read the API reference** - See :doc:`api/client`
4. **Check out examples** - See :doc:`examples/basic_usage`

Need Help?
----------

If you encounter any installation issues:

- Check our :doc:`troubleshooting` guide
- Search existing `GitHub Issues <https://github.com/batpool/upstox-totp/issues>`_
- Create a new issue with your installation details
- Join the discussion on `Reddit <https://www.reddit.com/user/iamdeadloop/>`_
