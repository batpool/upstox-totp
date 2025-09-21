Contributing Guide
==================

Thank you for your interest in contributing to the Upstox TOTP Python SDK! This guide will help you get started with contributing to the project.

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   .. code-block:: bash

      git clone https://github.com/your-username/upstox-totp.git
      cd upstox-totp

3. **Install dependencies** with uv:

   .. code-block:: bash

      # Install the package in development mode
      uv sync

      # Install development dependencies
      uv sync --group dev

      # Install documentation dependencies
      uv sync --group docs

4. **Set up environment** for testing:

   .. code-block:: bash

      # Copy example environment file
      cp example.env .env

      # Edit .env with your test credentials
      # (Use test/sandbox credentials, never production)

Project Structure
~~~~~~~~~~~~~~~~~

.. code-block:: text

   upstox-totp/
   ├── src/upstox_totp/        # Main package code
   │   ├── __init__.py         # Package initialization
   │   ├── client.py          # Main client class
   │   ├── models.py          # Data models
   │   ├── errors.py          # Exception classes
   │   ├── cli.py             # CLI implementation
   │   └── _api/              # API modules
   ├── docs/                  # Documentation
   ├── examples/              # Usage examples
   ├── tests/                 # Test suite (to be added)
   ├── pyproject.toml         # Project configuration
   └── README.md              # Main documentation

Contributing Guidelines
-----------------------

Code Style
~~~~~~~~~~

We use strict coding standards to ensure consistency:

**Formatting:**

.. code-block:: bash

   # Format code with black
   uv run black src/

   # Sort imports with isort
   uv run isort src/

   # Run both before committing
   uv run black src/ && uv run isort src/

**Type Hints:**

.. code-block:: python

   # Always use type hints
   def get_token(self, username: str) -> AccessTokenResponse:
       """Get access token for user."""
       pass

   # Use proper return types
   from typing import Optional, List, Dict, Any

**Docstrings:**

.. code-block:: python

   def example_function(param1: str, param2: int = 10) -> bool:
       """Brief description of the function.

       Args:
           param1: Description of param1
           param2: Description of param2, defaults to 10

       Returns:
           Description of return value

       Raises:
           ValueError: When param1 is invalid
           ConfigurationError: When configuration is missing

       Example:
           >>> result = example_function("test", 5)
           >>> print(result)
           True
       """
       pass

Pydantic Models
~~~~~~~~~~~~~~~

Follow Pydantic v2 best practices:

.. code-block:: python

   from pydantic import BaseModel, Field, ConfigDict
   from typing import Optional

   class ExampleModel(BaseModel):
       """Example model with proper configuration."""
       
       model_config = ConfigDict(
           strict=True,          # Enable strict mode
           extra='forbid',       # Forbid extra fields
           validate_assignment=True,  # Validate on assignment
       )

       # Required field with validation
       id: int = Field(gt=0, description="Unique identifier")
       
       # Optional field with default
       name: Optional[str] = Field(None, max_length=100)
       
       # Custom validation
       @field_validator('name')
       @classmethod
       def validate_name(cls, v: Optional[str]) -> Optional[str]:
           if v is not None and not v.strip():
               raise ValueError('Name cannot be empty')
           return v

Error Handling
~~~~~~~~~~~~~~

Use custom exception classes:

.. code-block:: python

   from upstox_totp.errors import UpstoxError

   class NewFeatureError(UpstoxError):
       """Raised when new feature encounters an error."""
       pass

   def new_feature():
       try:
           # Implementation
           pass
       except SomeException as e:
           raise NewFeatureError(f"Feature failed: {e}") from e

Testing
-------

Writing Tests
~~~~~~~~~~~~~

We use pytest for testing. Create tests in the `tests/` directory:

.. code-block:: python

   # tests/test_client.py
   
   import pytest
   from unittest.mock import patch, Mock
   from upstox_totp import UpstoxTOTP, ConfigurationError

   class TestUpstoxTOTP:
       def test_initialization_success(self):
           """Test successful client initialization."""
           with patch.dict('os.environ', {
               'UPSTOX_USERNAME': '9876543210',
               'UPSTOX_PASSWORD': 'password',
               # ... other env vars
           }):
               client = UpstoxTOTP()
               assert client.username == '9876543210'

       def test_initialization_missing_env(self):
           """Test initialization with missing environment variables."""
           with patch.dict('os.environ', {}, clear=True):
               with pytest.raises(ConfigurationError):
                   UpstoxTOTP()

       @patch('requests.Session.post')
       def test_token_generation_success(self, mock_post):
           """Test successful token generation."""
           # Mock response
           mock_response = Mock()
           mock_response.status_code = 200
           mock_response.json.return_value = {
               'status': 'success',
               'data': {
                   'access_token': 'test-token'
               }
           }
           mock_post.return_value = mock_response

           client = UpstoxTOTP()
           response = client.app_token.get_access_token()
           
           assert response.success
           assert response.data.access_token == 'test-token'

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   uv run pytest

   # Run with coverage
   uv run pytest --cov=upstox_totp

   # Run specific test file
   uv run pytest tests/test_client.py

   # Run with verbose output
   uv run pytest -v

Test Configuration
~~~~~~~~~~~~~~~~~~

Create test fixtures:

.. code-block:: python

   # tests/conftest.py
   
   import pytest
   from unittest.mock import patch
   from upstox_totp import UpstoxTOTP

   @pytest.fixture
   def mock_env():
       """Mock environment variables for testing."""
       env_vars = {
           'UPSTOX_USERNAME': '9876543210',
           'UPSTOX_PASSWORD': 'test-password',
           'UPSTOX_PIN_CODE': '1234',
           'UPSTOX_TOTP_SECRET': 'JBSWY3DPEHPK3PXP',
           'UPSTOX_CLIENT_ID': 'test-client-id',
           'UPSTOX_CLIENT_SECRET': 'test-client-secret',
           'UPSTOX_REDIRECT_URI': 'https://test.com/callback'
       }
       
       with patch.dict('os.environ', env_vars):
           yield env_vars

   @pytest.fixture
   def upstox_client(mock_env):
       """Create UpstoxTOTP client for testing."""
       return UpstoxTOTP()

Documentation
-------------

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Install documentation dependencies
   uv sync --group docs

   # Build documentation
   cd docs
   make html

   # View documentation
   open _build/html/index.html

   # Clean build
   make clean

Writing Documentation
~~~~~~~~~~~~~~~~~~~~~

Follow these guidelines:

1. **Use reStructuredText** for documentation files
2. **Include code examples** for all features
3. **Add docstrings** to all public functions/classes
4. **Update the changelog** for user-facing changes

**Example documentation:**

.. code-block:: rst

   New Feature
   -----------

   Description of the new feature and why it's useful.

   Usage
   ~~~~~

   .. code-block:: python

      from upstox_totp import UpstoxTOTP

      # Example usage
      upx = UpstoxTOTP()
      result = upx.new_feature()

   Parameters
   ~~~~~~~~~~

   .. list-table::
      :header-rows: 1

      * - Parameter
        - Type
        - Description
      * - param1
        - str
        - Description of param1

Pull Request Process
--------------------

Before Submitting
~~~~~~~~~~~~~~~~~

1. **Ensure tests pass:**

   .. code-block:: bash

      uv run pytest

2. **Format code:**

   .. code-block:: bash

      uv run black src/
      uv run isort src/

3. **Check type hints:**

   .. code-block:: bash

      uv run mypy src/

4. **Update documentation** if needed

5. **Add/update tests** for new features

Pull Request Template
~~~~~~~~~~~~~~~~~~~~~

Use this template for pull requests:

.. code-block:: text

   ## Description
   Brief description of changes made.

   ## Type of Change
   - [ ] Bug fix (non-breaking change which fixes an issue)
   - [ ] New feature (non-breaking change which adds functionality)
   - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
   - [ ] Documentation update

   ## Testing
   - [ ] Tests pass locally
   - [ ] Added tests for new functionality
   - [ ] Manual testing completed

   ## Documentation
   - [ ] Documentation updated
   - [ ] Docstrings added/updated
   - [ ] Examples provided

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Code is commented where necessary
   - [ ] Breaking changes are documented

Review Process
~~~~~~~~~~~~~~

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Testing** on different platforms if needed
4. **Documentation review**
5. **Approval** and merge

Types of Contributions
----------------------

Bug Fixes
~~~~~~~~~

1. **Create an issue** first (unless it's trivial)
2. **Include reproduction steps**
3. **Add tests** that fail before the fix
4. **Ensure tests pass** after the fix

New Features
~~~~~~~~~~~~

1. **Discuss the feature** in an issue first
2. **Follow existing patterns** in the codebase
3. **Add comprehensive tests**
4. **Include documentation**
5. **Consider backward compatibility**

Documentation
~~~~~~~~~~~~~

- Fix typos and grammar
- Improve existing examples
- Add new examples
- Translate documentation
- Improve API documentation

Performance Improvements
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Benchmark before and after**
2. **Include performance tests**
3. **Document the improvement**
4. **Ensure no breaking changes**

Code Review Guidelines
----------------------

For Reviewers
~~~~~~~~~~~~~

1. **Be constructive** and helpful
2. **Explain the "why"** behind suggestions
3. **Test the changes** locally if possible
4. **Check documentation** is updated
5. **Verify tests are adequate**

For Contributors
~~~~~~~~~~~~~~~~

1. **Respond to feedback** promptly
2. **Ask questions** if feedback is unclear
3. **Make requested changes** or explain why not
4. **Keep discussions** focused on the code
5. **Be patient** with the review process

Development Workflow
--------------------

Git Workflow
~~~~~~~~~~~~

.. code-block:: bash

   # 1. Create feature branch
   git checkout -b feature/new-feature

   # 2. Make changes and commit
   git add .
   git commit -m "Add new feature: description"

   # 3. Keep branch updated
   git fetch origin
   git rebase origin/master

   # 4. Push branch
   git push origin feature/new-feature

   # 5. Create pull request on GitHub

Commit Messages
~~~~~~~~~~~~~~~

Follow conventional commits:

.. code-block:: text

   feat: add new token caching mechanism
   fix: resolve TOTP timing issue
   docs: update installation guide
   test: add unit tests for client
   refactor: improve error handling
   style: format code with black
   chore: update dependencies

Branch Naming
~~~~~~~~~~~~~

Use descriptive branch names:

- `feature/token-caching`
- `fix/totp-timing-issue`
- `docs/api-reference`
- `refactor/error-handling`

Release Process
---------------

Version Numbering
~~~~~~~~~~~~~~~~~

We follow semantic versioning (SemVer):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Changelog
~~~~~~~~~

Update `CHANGELOG.md` for all releases:

.. code-block:: markdown

   ## [1.1.0] - 2025-01-15

   ### Added
   - New token caching mechanism
   - Support for custom timeout values

   ### Fixed
   - TOTP timing synchronization issue
   - Memory leak in session management

   ### Changed
   - Improved error messages
   - Updated dependencies

   ### Deprecated
   - Old configuration method (use new method)

Communication
-------------

GitHub Issues
~~~~~~~~~~~~~

Use GitHub issues for:

- **Bug reports** with reproduction steps
- **Feature requests** with use cases
- **Questions** about usage
- **Documentation** improvements

Discussions
~~~~~~~~~~~

Use GitHub Discussions for:

- **General questions** about the project
- **Ideas** for new features
- **Show and tell** your projects using the SDK
- **Community support**

Getting Help
------------

If you need help contributing:

1. **Check existing issues** and documentation
2. **Create a GitHub issue** with your question
3. **Join discussions** for community help
4. **Contact maintainers** for complex issues

Resources
---------

Useful links for contributors:

- **GitHub Repository**: https://github.com/batpool/upstox-totp
- **Documentation**: https://upstox-totp.readthedocs.io/
- **PyPI Package**: https://pypi.org/project/upstox-totp/
- **Upstox API Docs**: https://upstox.com/developer/api-documentation
- **Python Packaging**: https://packaging.python.org/
- **pytest Documentation**: https://docs.pytest.org/
- **Sphinx Documentation**: https://www.sphinx-doc.org/

Code of Conduct
---------------

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. See `CODE_OF_CONDUCT.md` for details.

License
-------

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank You!
----------

Thank you for contributing to the Upstox TOTP Python SDK! Your contributions help make this project better for everyone. 🎉
