<p align="center">
  <img src="https://cdn.statically.io/gh/batpool/upstox-totp/master/assets/upstox-totp.png" alt="upstox-totp.png-logo" width="100%" />
</p>


<h1 align="center">Upstox TOTP Python SDK</h1>

A modern, lightweight Python package that simplifies Upstox API authentication by handling TOTP-based login and token generation automatically. With this library, you can securely generate and refresh access tokens required to connect to the Upstox trading platform without manual intervention.

<p align="center">
  <a href="https://pypi.org/project/upstox-totp/"><img src="https://img.shields.io/pypi/v/upstox-totp?logo=pypi&logoColor=white&label=PyPI&color=blue" alt="PyPI Version" /></a>
  <a href="https://pypi.org/project/upstox-totp/"><img src="https://img.shields.io/pypi/dm/upstox-totp?logo=pypi&logoColor=white&label=Downloads&color=green" alt="PyPI Downloads" /></a>
  <a href="https://pypi.org/project/upstox-totp/"><img src="https://img.shields.io/pypi/pyversions/upstox-totp?logo=python&logoColor=white&label=Python" alt="Python Versions" /></a>
  <a href="https://github.com/batpool/upstox-totp/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/upstox-totp?logo=opensource&logoColor=white&color=green" alt="License" /></a>
</p>

<p align="center">
  <a href="https://upstox-totp.readthedocs.io/en/latest/"><img src="https://img.shields.io/readthedocs/upstox-totp?logo=readthedocs&logoColor=white&label=Documentation" alt="Documentation Status" /></a>
  <a href="https://upstox-totp.readthedocs.io/en/latest/"><img src="https://img.shields.io/badge/docs-latest-brightgreen?logo=readthedocs&logoColor=white" alt="Documentation" /></a>
</p>

<p align="center">
  <a href="https://pypi.org/project/upstox-totp/"><img src="https://img.shields.io/badge/PyPI%20Trusted%20Publishing-✅%20Verified-brightgreen?logo=pypi&logoColor=white" alt="Trusted Publishing" /></a>
  <a href="https://github.com/batpool/upstox-totp/actions"><img src="https://img.shields.io/github/actions/workflow/status/batpool/upstox-totp/release.yml?branch=master&logo=github&logoColor=white&label=CI/CD" alt="Build Status" /></a>
  <a href="https://github.com/batpool/upstox-totp"><img src="https://img.shields.io/github/stars/batpool/upstox-totp?logo=github&logoColor=white&color=yellow" alt="GitHub Stars" /></a>
  <a href="https://github.com/batpool/upstox-totp/issues"><img src="https://img.shields.io/github/issues/batpool/upstox-totp?logo=github&logoColor=white" alt="GitHub Issues" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/pydantic-v2-blue?logo=pydantic&logoColor=white" />
  <img src="https://img.shields.io/badge/secure%20by%20design-🔒-brightgreen" />
  <img src="https://img.shields.io/badge/CLI%20tool-⚡-orange" />
  <img src="https://img.shields.io/badge/env%20config-📝-yellow" />
  <img src="https://img.shields.io/badge/TOTP%20auth-🔐-red" />
  <img src="https://img.shields.io/badge/trading%20ready-📈-success" />
</p>

<hr>

## 🚀 Features

- **🔐 Automated TOTP Authentication** – Generate secure time-based one-time passwords (TOTP) for Upstox login
- **⚡ Token Management** – Fetch, refresh, and store Upstox access tokens with ease
- **🛠️ Simple API** – Minimal, developer-friendly methods for quick integration
- **📈 Trading Ready** – Instantly plug into Upstox APIs for real-time market data, order placement, and portfolio management
- **🐍 Pythonic Design** – Built with modern async/session handling for robust performance
- **🎯 CLI Tool** – Command-line interface for quick token generation
- **🔧 Environment Configuration** – Auto-configuration from environment variables
- **💡 Helpful Error Messages** – Clear error messages with troubleshooting guidance
- **🔒 Secure by Design** – Uses secure SecretStr for sensitive data handling
- **📚 Comprehensive Documentation** – Detailed guides and API reference at [upstox-totp.readthedocs.io](https://upstox-totp.readthedocs.io/en/latest/)

## 📚 Table of Contents

- [🚀 Features](#-features)
- [📚 Table of Contents](#-table-of-contents)
- [🎯 Quick Start](#-quick-start)
  - [Installation](#installation)
  - [Python SDK Usage](#python-sdk-usage)
  - [CLI Tool Usage](#cli-tool-usage)
- [⚙️ Configuration](#️-configuration)
  - [Environment Variables](#environment-variables)
  - [Python Configuration](#python-configuration)
- [🔧 Advanced Usage](#-advanced-usage)
  - [Context Manager](#context-manager)
  - [Session Management](#session-management)
  - [TOTP Generation](#totp-generation)
  - [Error Handling](#error-handling)
- [📖 API Reference](#-api-reference)
  - [Main Classes](#main-classes)
  - [Response Models](#response-models)
  - [Access Token Data](#access-token-data)
- [📚 Documentation](#-documentation)
- [🛠️ CLI Commands](#️-cli-commands)
  - [Check Environment](#check-environment)
  - [Generate Token](#generate-token)
  - [Help](#help)
- [🔒 Security Best Practices](#-security-best-practices)
- [🚨 Troubleshooting](#-troubleshooting)
  - [Common Issues](#common-issues)
- [📊 Integration Examples](#-integration-examples)
  - [With Upstox API](#with-upstox-api)
  - [Automated Token Refresh with Caching](#automated-token-refresh-with-caching)
  - [Database Storage Example (SQLite)](#database-storage-example-sqlite)
- [🎓 Examples](#-examples)
- [🤝 Contributing](#-contributing)
  - [Development Setup](#development-setup)
- [📋 Requirements](#-requirements)
- [📝 License](#-license)
- [⚠️ Important Notes](#️-important-notes)
  - [Token Management](#token-management)
  - [Disclaimer](#disclaimer)
- [🙏 Acknowledgments](#-acknowledgments)

## 🎯 Quick Start

**Requires Python 3.12 or higher**

### Installation

```bash
# Add as a dependency to your project
uv add upstox-totp

# Or install with pip
pip install upstox-totp
```

### Python SDK Usage

```python
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
        print(f"📊 Products: {', '.join(response.data.products)}")
        print(f"🏛️ Exchanges: {', '.join(response.data.exchanges)}")
        
        # Use the token for Upstox API calls
        access_token = response.data.access_token
        
except Exception as e:
    print(f"❌ Error: {e}")
```

### CLI Tool Usage

```bash
# Check if environment is properly configured
upstox_cli check-env

# Generate access token
upstox_cli generate-token
```

**Example CLI output:**
```bash
❯ upstox_cli generate-token

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
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required - Your Upstox account credentials
UPSTOX_USERNAME=your-mobile-number      # 10-digit mobile number
UPSTOX_PASSWORD=your-password           # Your Upstox password
UPSTOX_PIN_CODE=your-pin                # Your Upstox PIN code

# Required - TOTP secret from your Upstox app setup
UPSTOX_TOTP_SECRET=your-totp-secret     # TOTP secret key

# Required - OAuth app credentials from Upstox Developer Console
UPSTOX_CLIENT_ID=your-client-id         # API key from app generation
UPSTOX_CLIENT_SECRET=your-client-secret # API secret from app generation
UPSTOX_REDIRECT_URI=your-redirect-uri   # Must match app settings

# Optional
UPSTOX_DEBUG=false                      # Enable debug logging
UPSTOX_SLEEP_TIME=1000                  # Request delay in milliseconds
```

### Python Configuration

```python
from upstox_totp import UpstoxTOTP
from pydantic import SecretStr

# Method 1: Auto-load from environment
upx = UpstoxTOTP()

# Method 2: Load from specific .env file
upx = UpstoxTOTP.from_env_file(".env.production")

# Method 3: Manual configuration
upx = UpstoxTOTP(
    username="9876543210",
    password=SecretStr("your-password"),
    pin_code=SecretStr("your-pin"),
    totp_secret=SecretStr("your-totp-secret"),
    client_id="your-client-id",
    client_secret=SecretStr("your-client-secret"),
    redirect_uri="https://your-app.com/callback",
    debug=True
)
```

## 🔧 Advanced Usage

### Context Manager

```python
from upstox_totp import UpstoxTOTP

# Use as context manager for automatic cleanup
with UpstoxTOTP() as upx:
    response = upx.app_token.get_access_token()
    if response.success:
        access_token = response.data.access_token
        # Use token for API calls
```

### Session Management

```python
# Access the underlying HTTP session
upx = UpstoxTOTP()
session = upx.session

# Reset session if needed (clears cookies, headers, etc.)
upx.reset_session()

# Generate new request ID
request_id = upx.generate_request_id()
```

### TOTP Generation

```python
# Generate TOTP manually
upx = UpstoxTOTP()
totp_code = upx.generate_totp_secret()
print(f"Current TOTP: {totp_code}")
```

### Error Handling

```python
from upstox_totp import UpstoxTOTP, UpstoxError, ConfigurationError

try:
    upx = UpstoxTOTP()
    response = upx.app_token.get_access_token()
    
except ConfigurationError as e:
    print(f"Configuration Error: {e}")
    print("💡 Check your environment variables in .env file")
    
except UpstoxError as e:
    print(f"Upstox API Error: {e}")
    # Error includes helpful troubleshooting tips
    
except Exception as e:
    print(f"Unexpected Error: {e}")
```

## 📖 API Reference

### Main Classes

- **`UpstoxTOTP`** - Main client class for TOTP authentication
- **`AccessTokenResponse`** - Response model for access token data
- **`UpstoxError`** - Custom exception with helpful error messages
- **`ConfigurationError`** - Raised when configuration is invalid

### Response Models

All API responses follow a consistent structure:

```python
class ResponseBase:
    success: bool           # Whether the request was successful
    data: T | None         # Response data (varies by endpoint)
    error: dict | None     # Error details if request failed
```

### Access Token Data

```python
class AccessTokenData:
    access_token: str      # Your Upstox access token
    user_id: str          # Your user ID
    user_name: str        # Your display name
    email: str            # Your email address
    broker: str           # Broker name (UPSTOX)
    user_type: str        # Account type
    products: list[str]   # Available product types
    exchanges: list[str]  # Available exchanges
    is_active: bool       # Account status
    # ... more fields
```

## 📚 Documentation

For comprehensive documentation, tutorials, and examples, visit our official documentation:

**🌐 [upstox-totp.readthedocs.io](https://upstox-totp.readthedocs.io/en/latest/)**

The documentation includes:

- **📖 User Guide**
  - [Installation Guide](https://upstox-totp.readthedocs.io/en/latest/installation.html)
  - [Quick Start Guide](https://upstox-totp.readthedocs.io/en/latest/quickstart.html)
  - [Configuration Guide](https://upstox-totp.readthedocs.io/en/latest/configuration.html)
  - [Advanced Usage Guide](https://upstox-totp.readthedocs.io/en/latest/advanced_usage.html)
  - [CLI Reference](https://upstox-totp.readthedocs.io/en/latest/cli_reference.html)

- **🔍 API Reference**
  - [Client API Reference](https://upstox-totp.readthedocs.io/en/latest/api/client.html)
  - [Data Models Reference](https://upstox-totp.readthedocs.io/en/latest/api/models.html)
  - [Error Handling Reference](https://upstox-totp.readthedocs.io/en/latest/api/errors.html)
  - [Logging Reference](https://upstox-totp.readthedocs.io/en/latest/api/logging.html)

- **💡 Examples & Tutorials**
  - [Basic Usage Examples](https://upstox-totp.readthedocs.io/en/latest/examples/basic_usage.html)
  - [Integration Examples](https://upstox-totp.readthedocs.io/en/latest/examples/integration.html)
  - [Token Caching Examples](https://upstox-totp.readthedocs.io/en/latest/examples/token_caching.html)
  - [Database Storage Examples](https://upstox-totp.readthedocs.io/en/latest/examples/database_storage.html)

- **🛡️ Additional Information**
  - [Security Best Practices](https://upstox-totp.readthedocs.io/en/latest/security.html)
  - [Troubleshooting Guide](https://upstox-totp.readthedocs.io/en/latest/troubleshooting.html)
  - [Contributing Guide](https://upstox-totp.readthedocs.io/en/latest/contributing.html)

## 🛠️ CLI Commands

### Check Environment

Validate your configuration before generating tokens:

```bash
upstox_cli check-env
```

### Generate Token

Generate access token for API usage:

```bash
upstox_cli generate-token
```

### Help

Get help for any command:

```bash
upstox_cli --help
upstox_cli generate-token --help
```

## 🔒 Security Best Practices

1. **Never commit secrets** - Use `.env` files and add them to `.gitignore`
2. **Use SecretStr** - Sensitive data is automatically protected from logs
3. **Environment variables** - Store credentials in environment variables, not code
4. **Token rotation** - Regenerate tokens regularly for security
5. **Debug mode** - Disable debug mode in production to prevent credential leaks

## 🚨 Troubleshooting

### Common Issues

**Configuration Error: Missing environment variables**
```bash
# Check what's missing
upstox_cli check-env

# Set required variables in .env file
echo "UPSTOX_USERNAME=9876543210" >> .env
echo "UPSTOX_PASSWORD=your-password" >> .env
# ... add other variables
```

**Invalid Credentials Error**
- Verify your username (should be 10-digit mobile number)
- Check password and PIN are correct
- Ensure TOTP secret is properly configured

**Client ID / Redirect URI Error**
- Verify client_id and client_secret in Upstox Developer Console
- Ensure redirect_uri exactly matches your app settings
- Check if your app is approved and active

**TOTP Validation Failed**
- Verify your TOTP secret is correct
- Check system time is synchronized
- Ensure TOTP secret format is valid (no spaces, correct encoding)

## 📊 Integration Examples

### With Upstox API

```python
import requests
from upstox_totp import UpstoxTOTP

# Get access token
upx = UpstoxTOTP()
token_response = upx.app_token.get_access_token()
access_token = token_response.data.access_token

# Use token with Upstox API
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Get user profile
response = requests.get(
    'https://api.upstox.com/v2/user/profile',
    headers=headers
)
print(response.json())

# Get positions
response = requests.get(
    'https://api.upstox.com/v2/portfolio/long-term-positions',
    headers=headers
)
print(response.json())
```

### Automated Token Refresh with Caching

```python
import time
import json
from datetime import datetime, timedelta
from upstox_totp import UpstoxTOTP

class UpstoxClient:
    def __init__(self, cache_file="upstox_token.json"):
        self.upx = UpstoxTOTP()
        self.cache_file = cache_file
        self.access_token = None
        self.token_expiry = None
        self.load_cached_token()
    
    def load_cached_token(self):
        """Load token from cache if still valid"""
        try:
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
                token_expiry = datetime.fromisoformat(data['expiry'])
                
                # Check if token is still valid (with 1-hour buffer)
                if token_expiry > datetime.now() + timedelta(hours=1):
                    self.access_token = data['token']
                    self.token_expiry = token_expiry
                    print("✅ Using cached token")
                    return
        except (FileNotFoundError, KeyError, ValueError):
            pass
        
        # Cache miss or expired token - refresh
        self.refresh_token()
    
    def refresh_token(self):
        """Refresh access token and cache it"""
        response = self.upx.app_token.get_access_token()
        if response.success:
            self.access_token = response.data.access_token
            self.token_expiry = datetime.now() + timedelta(hours=24)
            
            # Cache the token
            with open(self.cache_file, 'w') as f:
                json.dump({
                    'token': self.access_token,
                    'expiry': self.token_expiry.isoformat()
                }, f)
            
            print("✅ Token refreshed and cached successfully")
        else:
            raise Exception("Failed to refresh token")
    
    def api_call(self, endpoint, **kwargs):
        """Make authenticated API call with auto-refresh"""
        # Check if token needs refresh
        if (self.token_expiry and 
            self.token_expiry < datetime.now() + timedelta(hours=1)):
            print("🔄 Token expiring soon, refreshing...")
            self.refresh_token()
        
        headers = kwargs.setdefault('headers', {})
        headers['Authorization'] = f'Bearer {self.access_token}'
        
        # Make your API call here
        return requests.get(endpoint, **kwargs)

# Usage
client = UpstoxClient()
response = client.api_call('https://api.upstox.com/v2/user/profile')
```

### Database Storage Example (SQLite)

```python
import sqlite3
from datetime import datetime, timedelta
from upstox_totp import UpstoxTOTP

class UpstoxTokenManager:
    def __init__(self, db_path="upstox.db"):
        self.upx = UpstoxTOTP()
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database table"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tokens (
                id INTEGER PRIMARY KEY,
                access_token TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_valid_token(self):
        """Get valid token from DB or generate new one"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute('''
            SELECT access_token, expires_at FROM tokens 
            WHERE expires_at > datetime('now', '+1 hour')
            ORDER BY created_at DESC LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print("✅ Using cached token from database")
            return result[0]
        
        # Generate new token
        return self.refresh_and_store_token()
    
    def refresh_and_store_token(self):
        """Generate new token and store in database"""
        response = self.upx.app_token.get_access_token()
        if not response.success:
            raise Exception("Failed to generate token")
        
        token = response.data.access_token
        expires_at = datetime.now() + timedelta(hours=24)
        
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT INTO tokens (access_token, expires_at)
            VALUES (?, ?)
        ''', (token, expires_at))
        conn.commit()
        conn.close()
        
        print("✅ New token generated and stored in database")
        return token

# Usage
token_manager = UpstoxTokenManager()
access_token = token_manager.get_valid_token()
```

## 🎓 Examples

Check out the [`examples/`](https://github.com/batpool/upstox-totp/tree/master/examples/) directory for more comprehensive examples:

- [`quickstart.py`](https://github.com/batpool/upstox-totp/blob/master/examples/quickstart.py) - Basic token generation
- More examples coming soon!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/batpool/upstox-totp.git
cd upstox-totp

# Install dependencies with uv
uv sync

# Install development dependencies
uv sync --group dev

# Run tests
uv run pytest

# Format code
uv run black src/
uv run isort src/
```

## 📋 Requirements

- Python 3.12 or higher
- Active Upstox trading account
- Upstox Developer App (for client credentials)
- TOTP app setup (Google Authenticator, Authy, etc.)

## 📝 License

MIT License - see [LICENSE](https://github.com/batpool/upstox-totp/blob/master/LICENSE) file for details.

## ⚠️ Important Notes

### Token Management
> **📅 Access Token Expiry**: Upstox access tokens have a **24-hour expiration time**. For production applications, it's recommended to:
> - Store tokens securely in a database or cache (Redis, etc.)
> - Implement automatic token refresh logic
> - Monitor token expiry and regenerate proactively

### Disclaimer
This is an unofficial library for Upstox API authentication. Please ensure you comply with Upstox's terms of service and API usage guidelines. Use at your own risk.

## 🙏 Acknowledgments

- [Upstox](https://upstox.com/) for providing the trading platform and API
- [Pydantic](https://pydantic.dev/) for excellent data validation
- [pyOTP](https://pyotp.readthedocs.io/) for TOTP implementation
- [curl-cffi](https://github.com/yifeikong/curl_cffi) for HTTP client

---

**Happy Trading! 📈**

For questions or support, please [open an issue](https://github.com/batpool/upstox-totp/issues) on GitHub.