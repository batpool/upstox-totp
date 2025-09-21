License
=======

The Upstox TOTP Python SDK is licensed under the MIT License.

MIT License
-----------

.. code-block:: text

   MIT License

   Copyright (c) 2025 batpool

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.

What This Means
---------------

The MIT License is a permissive license that allows you to:

✅ **Use** the software for any purpose
✅ **Copy** and distribute the software
✅ **Modify** the software to meet your needs
✅ **Distribute modified versions** of the software
✅ **Use the software in commercial projects**
✅ **Use the software in proprietary projects**

With these conditions:

📋 **Include the license notice** in all copies
📋 **Include the copyright notice** in all copies

And these limitations:

❌ **No warranty** - The software is provided "as is"
❌ **No liability** - Authors are not liable for any damages
❌ **No trademark rights** - License doesn't grant trademark rights

Dependencies
------------

This project uses several third-party libraries, each with their own licenses:

Core Dependencies
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Package
     - License
     - Purpose
   * - `click <https://click.palletsprojects.com/>`_
     - BSD-3-Clause
     - Command-line interface framework
   * - `curl-cffi <https://github.com/yifeikong/curl_cffi>`_
     - MIT
     - HTTP client with better performance
   * - `python-dotenv <https://github.com/theskumar/python-dotenv>`_
     - BSD-3-Clause
     - Environment variable management
   * - `pydantic <https://pydantic.dev/>`_
     - MIT
     - Data validation and settings management
   * - `pyotp <https://pyotp.readthedocs.io/>`_
     - MIT
     - TOTP (Time-based One-Time Password) generation

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Package
     - License
     - Purpose
   * - `black <https://black.readthedocs.io/>`_
     - MIT
     - Code formatting
   * - `isort <https://isort.readthedocs.io/>`_
     - MIT
     - Import sorting

Documentation Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Package
     - License
     - Purpose
   * - `sphinx <https://www.sphinx-doc.org/>`_
     - BSD-2-Clause
     - Documentation generator
   * - `sphinx-rtd-theme <https://sphinx-rtd-theme.readthedocs.io/>`_
     - MIT
     - Read the Docs theme
   * - `myst-parser <https://myst-parser.readthedocs.io/>`_
     - MIT
     - Markdown parser for Sphinx

License Compatibility
---------------------

All dependencies use licenses that are compatible with the MIT License:

- **MIT License**: Fully compatible ✅
- **BSD License**: Fully compatible ✅
- **Apache License 2.0**: Fully compatible ✅

This means you can use this project in both open-source and commercial applications without license conflicts.

Third-Party Services
--------------------

This SDK integrates with external services:

Upstox API
~~~~~~~~~~

- **Service**: Upstox Trading Platform API
- **Terms**: Subject to Upstox Terms of Service
- **Documentation**: https://upstox.com/developer/api-documentation
- **Privacy**: Subject to Upstox Privacy Policy

**Important**: Using this SDK requires compliance with Upstox's terms of service and API usage guidelines.

Contributing
------------

By contributing to this project, you agree that your contributions will be licensed under the same MIT License.

When you submit a pull request, you are agreeing to license your contribution under the MIT License and confirming that you have the right to do so.

Attribution
-----------

If you use this project, attribution is not required but is appreciated. You can include:

.. code-block:: text

   This project uses the Upstox TOTP Python SDK (https://github.com/batpool/upstox-totp)

Commercial Use
--------------

The MIT License explicitly allows commercial use. You can:

- Use this SDK in commercial trading applications
- Include it in proprietary software
- Sell applications that use this SDK
- Use it in enterprise environments

No additional permissions or fees are required.

Warranty Disclaimer
-------------------

.. warning::
   **Important Disclaimer**

   This software is provided "as is" without warranty of any kind. The authors and contributors are not responsible for:

   - Trading losses or financial damages
   - API failures or service interruptions  
   - Data breaches or security issues
   - Any other damages arising from use of this software

   **Use at your own risk** and ensure you understand the implications of automated trading.

License Text in Code
--------------------

When redistributing this software, include the license text. You can find it in:

- The `LICENSE` file in the repository root
- The package metadata
- This documentation page

For convenience, here's a short form you can include in your source files:

.. code-block:: python

   # This file is part of upstox-totp
   # Licensed under the MIT License
   # See LICENSE file for details

SPDX License Identifier
-----------------------

For automated license detection, this project uses:

.. code-block:: text

   SPDX-License-Identifier: MIT

Questions About Licensing
-------------------------

If you have questions about licensing:

1. **Review the license text** above carefully
2. **Check dependency licenses** if you're concerned about compatibility  
3. **Consult with a lawyer** for legal advice (we cannot provide legal advice)
4. **Open an issue** on GitHub for clarification about project-specific questions

Related Resources
-----------------

- **MIT License Official Text**: https://opensource.org/licenses/MIT
- **Choose a License Guide**: https://choosealicense.com/licenses/mit/
- **SPDX License List**: https://spdx.org/licenses/
- **Open Source Initiative**: https://opensource.org/

Copyright Notice
----------------

.. code-block:: text

   Copyright (c) 2025 batpool

   All rights reserved under the MIT License.
