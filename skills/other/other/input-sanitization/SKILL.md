---
name: input-sanitization
description: Эксперт по санитизации ввода. Используй для XSS prevention, encoding, validation и security headers.
---

# Input Sanitization Expert

Expert in input validation, sanitization, and encoding for secure applications.

## Core Principles

### Validation vs Sanitization vs Encoding

- **Validation**: Reject invalid input entirely (preferred)
- **Sanitization**: Clean/modify input to make it safe
- **Encoding**: Transform input for safe use in specific contexts
- Apply in order: Validate first, sanitize if needed, encode for output context

### Defense in Depth

- Never rely on client-side validation alone
- Implement validation at multiple layers (input, business logic, data access)
- Use allowlists over denylists when possible
- Fail securely - reject invalid input rather than attempting to fix it

## Input Validation Strategies

### Strict Validation Patterns (Python)

```python
import re
from typing import Optional

class InputValidator:
    """Strict input validation using allowlist patterns."""

    PATTERNS = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'username': r'^[a-zA-Z0-9_]{3,20}$',
        'phone': r'^\+?1?[0-9]{10,14}$',
        'alphanumeric': r'^[a-zA-Z0-9]+$',
        'safe_filename': r'^[a-zA-Z0-9._-]+$',
        'uuid': r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$',
        'slug': r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
    }

    @staticmethod
    def validate_input(value: str, pattern_type: str, max_length: int = 255) -> Optional[str]:
        """Validate input against allowlist pattern."""
        if not value or len(value) > max_length:
            return None

        pattern = InputValidator.PATTERNS.get(pattern_type)
        if pattern and re.match(pattern, value):
            return value.strip()
        return None

    @staticmethod
    def validate_integer(value: str, min_val: int = None, max_val: int = None) -> Optional[int]:
        """Validate and convert string to integer with bounds checking."""
        try:
            num = int(value)
            if min_val is not None and num < min_val:
                return None
            if max_val is not None and num > max_val:
                return None
            return num
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_enum(value: str, allowed_values: set) -> Optional[str]:
        """Validate value against allowed set."""
        if value in allowed_values:
            return value
        return None
```

### JavaScript/TypeScript Validation

```typescript
class InputValidator {
  private static readonly PATTERNS: Record<string, RegExp> = {
    email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    username: /^[a-zA-Z0-9_]{3,20}$/,
    phone: /^\+?1?[0-9]{10,14}$/,
    alphanumeric: /^[a-zA-Z0-9]+$/,
    uuid: /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/
  };

  static validate(value: string, type: string, maxLength = 255): string | null {
    if (!value || value.length > maxLength) {
      return null;
    }

    const pattern = this.PATTERNS[type];
    if (pattern && pattern.test(value)) {
      return value.trim();
    }
    return null;
  }

  static validateInteger(value: string, min?: number, max?: number): number | null {
    const num = parseInt(value, 10);
    if (isNaN(num)) return null;
    if (min !== undefined && num < min) return null;
    if (max !== undefined && num > max) return null;
    return num;
  }

  static sanitizeHtml(input: string): string {
    const map: Record<string, string> = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#x27;',
      '/': '&#x2F;'
    };
    return input.replace(/[&<>"'/]/g, char => map[char]);
  }
}
```

## Context-Specific Encoding

### HTML Output Encoding

```python
import html
from markupsafe import escape

def safe_html_output(user_input: str) -> str:
    """Encode for HTML context."""
    return html.escape(user_input, quote=True)

def safe_html_attribute(user_input: str) -> str:
    """Encode for HTML attribute context - more restrictive."""
    encoded = html.escape(user_input, quote=True)
    # Additional encoding for attribute-specific risks
    encoded = encoded.replace("'", "&#x27;").replace("`", "&#x60;")
    return encoded

def safe_html_url(user_input: str) -> str:
    """Encode URL for use in href/src attributes."""
    from urllib.parse import quote
    # Only allow safe URL schemes
    if not user_input.lower().startswith(('http://', 'https://', '/')):
        return '#'
    return quote(user_input, safe=':/?&=#')
```

### JavaScript Context Encoding

```javascript
class JSEncoder {
    static encodeForJS(input) {
        if (typeof input !== 'string') {
            input = String(input);
        }

        return input
            .replace(/\\/g, '\\\\')
            .replace(/'/g, "\\'")
            .replace(/"/g, '\\"')
            .replace(/\n/g, '\\n')
            .replace(/\r/g, '\\r')
            .replace(/\t/g, '\\t')
            .replace(/</g, '\\u003c')
            .replace(/>/g, '\\u003e');
    }

    static safeJSONStringify(obj) {
        return JSON.stringify(obj)
            .replace(/</g, '\\u003c')
            .replace(/>/g, '\\u003e')
            .replace(/&/g, '\\u0026');
    }

    static encodeForHTMLAttribute(input) {
        return input
            .replace(/&/g, '&amp;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#x27;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }
}
```

### SQL Context - Parameterized Queries

```python
import sqlite3
from typing import List, Any, Optional

class SafeDatabaseAccess:
    """Always use parameterized queries - never string concatenation."""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def safe_query(self, query: str, params: tuple = ()) -> List[Any]:
        """Execute query with parameters - prevents SQL injection."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Parameters are automatically escaped
            cursor.execute(query, params)
            return cursor.fetchall()

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Example: safe parameterized query."""
        # Validate email first
        if not InputValidator.validate_input(email, 'email'):
            return None

        # Use ? placeholder - NEVER f-string or .format()
        query = "SELECT id, username, email FROM users WHERE email = ?"
        results = self.safe_query(query, (email,))

        if results:
            return dict(zip(['id', 'username', 'email'], results[0]))
        return None

    # WRONG - SQL Injection vulnerable:
    # query = f"SELECT * FROM users WHERE email = '{email}'"
    # query = "SELECT * FROM users WHERE email = '%s'" % email
```

## File Upload Sanitization

```python
import os
import hashlib
import magic
from pathlib import Path
from typing import Optional

class FileUploadSanitizer:
    """Secure file upload handling."""

    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.docx'}
    ALLOWED_MIME_TYPES = {
        'image/jpeg', 'image/png', 'image/gif',
        'application/pdf', 'text/plain',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Generate safe filename."""
        # Remove path components (directory traversal prevention)
        filename = os.path.basename(filename)

        # Remove dangerous characters - allowlist approach
        safe_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        filename = ''.join(c for c in filename if c in safe_chars)

        # Limit length
        if len(filename) > 100:
            name, ext = os.path.splitext(filename)
            filename = name[:95] + ext

        return filename or "unnamed_file"

    @classmethod
    def validate_upload(cls, file_data: bytes, filename: str, content_type: str) -> dict:
        """Comprehensive file upload validation."""
        result = {'valid': False, 'errors': [], 'safe_filename': None}

        # Check file size
        if len(file_data) > cls.MAX_FILE_SIZE:
            result['errors'].append(f"File too large: {len(file_data)} bytes (max: {cls.MAX_FILE_SIZE})")

        # Check extension
        ext = Path(filename).suffix.lower()
        if ext not in cls.ALLOWED_EXTENSIONS:
            result['errors'].append(f"Extension not allowed: {ext}")

        # Check declared MIME type
        if content_type not in cls.ALLOWED_MIME_TYPES:
            result['errors'].append(f"MIME type not allowed: {content_type}")

        # Verify actual content type matches (magic bytes)
        try:
            detected_mime = magic.from_buffer(file_data, mime=True)
            if detected_mime != content_type:
                result['errors'].append(f"MIME type mismatch: declared={content_type}, detected={detected_mime}")
        except Exception:
            result['errors'].append("Could not verify file content type")

        result['valid'] = len(result['errors']) == 0
        result['safe_filename'] = cls.sanitize_filename(filename)

        return result

    @staticmethod
    def generate_safe_path(base_dir: str, filename: str) -> str:
        """Generate unique, safe file path."""
        safe_name = FileUploadSanitizer.sanitize_filename(filename)
        # Add hash to prevent overwriting
        hash_prefix = hashlib.md5(os.urandom(16)).hexdigest()[:8]
        name, ext = os.path.splitext(safe_name)
        return os.path.join(base_dir, f"{name}_{hash_prefix}{ext}")
```

## URL and Path Sanitization

```python
from urllib.parse import urlparse, quote
import os.path

class URLSanitizer:
    @staticmethod
    def validate_redirect_url(url: str, allowed_hosts: set) -> Optional[str]:
        """Validate redirect URLs to prevent open redirects."""
        try:
            parsed = urlparse(url)

            # Only allow specific schemes
            if parsed.scheme not in ('http', 'https', ''):
                return None

            # For relative URLs
            if not parsed.netloc:
                # Prevent protocol-relative URLs (//evil.com)
                if url.startswith('//'):
                    return None
                return url

            # Check against allowlist of hosts
            if parsed.netloc not in allowed_hosts:
                return None

            return url
        except Exception:
            return None

    @staticmethod
    def sanitize_path_parameter(path: str, base_dir: str) -> Optional[str]:
        """Prevent directory traversal attacks."""
        # Normalize the path
        normalized = os.path.normpath(path)

        # Check for directory traversal attempts
        if '..' in normalized or normalized.startswith('/') or normalized.startswith('\\'):
            return None

        # Ensure path stays within base directory
        full_path = os.path.abspath(os.path.join(base_dir, normalized))
        base_abs = os.path.abspath(base_dir)

        if not full_path.startswith(base_abs + os.sep):
            return None

        return normalized
```

## Content Security Policy Headers

```python
from flask import Flask, Response

def apply_security_headers(response: Response) -> Response:
    """Apply comprehensive security headers."""

    response.headers.update({
        # Content Security Policy - prevent XSS
        'Content-Security-Policy': '; '.join([
            "default-src 'self'",
            "script-src 'self' https://trusted-cdn.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "img-src 'self' data: https:",
            "font-src 'self' https://fonts.gstatic.com",
            "connect-src 'self' https://api.example.com",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ]),

        # Prevent MIME type sniffing
        'X-Content-Type-Options': 'nosniff',

        # Clickjacking protection
        'X-Frame-Options': 'DENY',

        # XSS filter (legacy browsers)
        'X-XSS-Protection': '1; mode=block',

        # Force HTTPS
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',

        # Referrer policy
        'Referrer-Policy': 'strict-origin-when-cross-origin',

        # Permissions policy
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
    })

    return response


# Express.js equivalent
'''
const helmet = require('helmet');

app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "https://trusted-cdn.com"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", "data:", "https:"],
            frameAncestors: ["'none'"]
        }
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    }
}));
'''
```

## XSS Prevention Checklist

```yaml
Output Encoding:
  - HTML body: Use HTML entity encoding
  - HTML attributes: Use attribute encoding, always quote values
  - JavaScript: Use JavaScript encoding, prefer JSON.stringify
  - CSS: Use CSS encoding
  - URLs: Use URL encoding

Input Validation:
  - Validate type, length, format, range
  - Use allowlists over denylists
  - Reject invalid input, don't sanitize

Security Headers:
  - Implement Content Security Policy
  - Set X-Content-Type-Options: nosniff
  - Set X-Frame-Options: DENY
  - Enable HSTS

Framework Protections:
  - Use auto-escaping template engines
  - Enable CSRF protection
  - Use HttpOnly and Secure cookie flags
  - Implement SameSite cookie attribute
```

## Лучшие практики

1. **Validate at server** — никогда не доверяйте client-side валидации
2. **Allowlist approach** — определяйте допустимое, не запрещённое
3. **Context-aware encoding** — разные контексты требуют разного encoding
4. **Parameterized queries** — никогда не конкатенируйте SQL
5. **Defense in depth** — валидация на каждом уровне
6. **Fail securely** — отклоняйте invalid input, не пытайтесь исправить
