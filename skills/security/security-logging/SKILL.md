---
name: security-logging
description: Security controls and structured logging implementation. Use when security logging guidance is required.
allowed-tools:
  - Bash(shellcheck)
  - Bash(grep -E '^[[:space:]]*[^[:space:]]+[[:space:]]*=')
  - Bash(rg --pcre2 'password|secret|key|token')
---
## Purpose

Define security-focused logging and input validation standards so that services can detect, trace, and audit security-relevant events consistently.

## IO Semantics

Input: Application logs, inbound requests, and configuration surfaces that must be validated or monitored for security.

Output: Structured logging and validation patterns that flag suspicious input, support incident response, and integrate with monitoring systems.

Side Effects: When adopted, may increase log volume and require tuning of alerting rules and storage policies.

## Deterministic Steps

### 1. Input Validation Security

Execute input validation at all system boundaries:
```python
import re
import bleach
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, validator

class SecurityValidator:
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
        r"(--|#|\/\*|\*\/)",
        r"(;|\||\|\|&)",
        r"(\b(OR|AND)\s+\w+\s*=\s*\w+)"
    ]

    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>"
    ]

    @classmethod
    def validate_input(cls, user_input: str, max_length: int = 1000) -> str:
        # Length validation
        if len(user_input) > max_length:
            raise ValueError(f"Input too long: max {max_length} characters")

        # SQL injection detection
        upper_input = user_input.upper()
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, upper_input, re.IGNORECASE):
                raise ValueError("Potentially malicious SQL pattern detected")

        # XSS detection
        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE | re.DOTALL):
                raise ValueError("Potentially malicious XSS pattern detected")

        # Sanitize with bleach
        clean_input = bleach.clean(user_input, tags=[], strip=True)

        return clean_input.strip()

    @classmethod
    def validate_filename(cls, filename: str) -> str:
        # Remove directory traversal attempts
        safe_filename = re.sub(r'[\\/]', '_', filename)

        # Remove shell special characters
        safe_filename = re.sub(r'[;&|`$(){}[\]]', '', safe_filename)

        # Validate filename pattern
        if not re.match(r'^[a-zA-Z0-9._-]+$', safe_filename):
            raise ValueError("Invalid filename format")

        return safe_filename
```

### API Request Validation

Execute comprehensive API security:
```python
from flask import Flask, request, jsonify
from functools import wraps
import logging

class APISecurityMiddleware:
    def __init__(self, app: Flask):
        self.app = app
        self.logger = logging.getLogger('api_security')
        self._setup_middleware()

    def _setup_middleware(self):
        @self.app.before_request
        def validate_request():
            # Rate limiting check
            if not self._check_rate_limit(request):
                self.logger.warning(f"Rate limit exceeded: {request.remote_addr}")
                return jsonify({"error": "Rate limit exceeded"}), 429

            # Request size validation
            content_length = request.content_length or 0
            if content_length > 10 * 1024 * 1024:  # 10MB limit
                self.logger.warning(f"Request too large: {content_length} bytes")
                return jsonify({"error": "Request too large"}), 413

        @self.app.after_request
        def log_response(response):
            # Log security-relevant events
            if response.status_code >= 400:
                self.logger.warning(
                    f"HTTP {response.status_code}: {request.method} {request.path} "
                    f"from {request.remote_addr}"
                )
            return response

    def _check_rate_limit(self, request) -> bool:
        # Implement rate limiting logic
        return True  # Placeholder
```

## Credential Security Enforcement

### Secret Detection and Removal

Execute identification and elimination of hardcoded secrets:
```bash
#!/bin/bash
# secret-scanner.sh

scan_for_secrets() {
    local scan_dir="$1"

    echo "Scanning for hardcoded secrets in: $scan_dir"

    # Scan for common secret patterns
    echo "=== Password patterns ==="
    rg -i --line-number "password\s*=\s*['\"][^'\"]{8,}['\"]" "$scan_dir" || echo "No password patterns found"

    echo "=== API key patterns ==="
    rg -i --line-number "(api[_-]?key|apikey)\s*=\s*['\"][a-zA-Z0-9]{16,}['\"]" "$scan_dir" || echo "No API key patterns found"

    echo "=== Token patterns ==="
    rg -i --line-number "token\s*=\s*['\"][a-zA-Z0-9]{20,}['\"]" "$scan_dir" || echo "No token patterns found"

    echo "=== Secret key patterns ==="
    rg -i --line-number "secret[_-]?key\s*=\s*['\"][a-zA-Z0-9]{16,}['\"]" "$scan_dir" || echo "No secret key patterns found"

    echo "=== Database URL patterns ==="
    rg -i --line-number "(database[_-]?url|db[_-]?url)\s*=\s*['\"][^'\"]*://[^'\"]*:[^'\"]*@" "$scan_dir" || echo "No database URL patterns found"
}

# Function to replace secrets with environment variables
replace_secrets_with_env() {
    local file="$1"

    # Create backup
    cp "$file" "$file.backup"

    # Replace common secret patterns
    sed -i.tmp \
        -e "s/password\s*=\s*'.*'/password = os.getenv('DB_PASSWORD')/g" \
        -e "s/password\s*=\s*\".*\"/password = os.getenv('DB_PASSWORD')/g" \
        -e "s/api_key\s*=\s*'.*'/api_key = os.getenv('API_KEY')/g" \
        -e "s/api_key\s*=\s*\".*\"/api_key = os.getenv('API_KEY')/g" \
        "$file"

    # Add import if not present
    if ! grep -q "import os" "$file"; then
        sed -i.tmp "1i import os" "$file"
    fi

    rm "$file.tmp"
    echo "Secrets replaced in $file (backup saved as $file.backup)"
}
```

## Structured Logging Implementation

### Security Event Logging

Execute comprehensive security logging:
```python
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib
import hmac

class SecurityLogger:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(f'security.{service_name}')
        self.logger.setLevel(logging.INFO)

        # Structured formatter
        formatter = logging.Formatter('%(message)s')

        # File handler with rotation
        from logging.handlers import RotatingFileHandler
        handler = RotatingFileHandler(
            f'/var/log/security/{service_name}-security.log',
            maxBytes=100*1024*1024,  # 100MB
            backupCount=10
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_security_event(self, event_type: str, severity: str,
                          details: Dict[str, Any], user_id: Optional[str] = None):
        """Execute structured security event logging"""
        timestamp = datetime.utcnow().isoformat() + 'Z'

        # Create event hash for integrity
        event_data = {
            'timestamp': timestamp,
            'service': self.service_name,
            'event_type': event_type,
            'severity': severity,
            'user_id': user_id,
            'details': details
        }

        # Calculate integrity hash
        event_hash = hmac.new(
            key=self._get_hash_key(),
            msg=json.dumps(event_data, sort_keys=True).encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        event_data['integrity_hash'] = event_hash

        # Log structured event
        log_entry = json.dumps(event_data)

        if severity == 'CRITICAL':
            self.logger.critical(log_entry)
        elif severity == 'HIGH':
            self.logger.error(log_entry)
        elif severity == 'MEDIUM':
            self.logger.warning(log_entry)
        else:
            self.logger.info(log_entry)

    def log_authentication_event(self, success: bool, user_id: str,
                               ip_address: str, user_agent: str,
                               failure_reason: Optional[str] = None):
        """Execute authentication attempt logging"""
        event_type = 'login_success' if success else 'login_failure'
        severity = 'INFO' if success else 'HIGH'

        details = {
            'ip_address': ip_address,
            'user_agent': user_agent,
            'success': success
        }

        if not success and failure_reason:
            details['failure_reason'] = failure_reason

        self.log_security_event(event_type, severity, details, user_id)

    def log_authorization_event(self, user_id: str, resource: str,
                               action: str, success: bool,
                               ip_address: str):
        """Execute authorization attempt logging"""
        event_type = 'authorization_success' if success else 'authorization_failure'
        severity = 'INFO' if success else 'MEDIUM'

        details = {
            'resource': resource,
            'action': action,
            'ip_address': ip_address,
            'success': success
        }

        self.log_security_event(event_type, severity, details, user_id)

    def log_privilege_escalation(self, user_id: str, old_role: str,
                               new_role: str, ip_address: str):
        """Execute privilege escalation logging"""
        details = {
            'old_role': old_role,
            'new_role': new_role,
            'ip_address': ip_address
        }

        self.log_security_event('privilege_escalation', 'HIGH', details, user_id)

    def _get_hash_key(self) -> bytes:
        """Execute key retrieval for integrity hashing"""
        key_file = '/etc/security/log-integrity.key'
        try:
            with open(key_file, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            # Generate new key
            import os
            key = os.urandom(32)
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(key)
            os.chmod(key_file, 0o600)
            return key
```

### Log Integrity and Auditing

Execute tamper-evident logging implementation:
```python
import hashlib
import json
from typing import List, Dict
from pathlib import Path

class LogIntegrityMonitor:
    def __init__(self, log_directory: str):
        self.log_directory = Path(log_directory)
        self.chain_file = self.log_directory / '.log-chain'
        self.chain = self._load_chain()

    def _load_chain(self) -> List[str]:
        """Execute existing log chain loading"""
        if self.chain_file.exists():
            with open(self.chain_file, 'r') as f:
                return json.load(f)
        return []

    def _save_chain(self):
        """Execute log chain saving"""
        with open(self.chain_file, 'w') as f:
            json.dump(self.chain, f, indent=2)

    def add_log_entry(self, log_entry: Dict[str, Any]) -> str:
        """Execute entry addition to tamper-evident log chain"""
        entry_json = json.dumps(log_entry, sort_keys=True)

        # Create hash of entry with previous hash
        previous_hash = self.chain[-1] if self.chain else '0' * 64
        entry_with_hash = entry_json + previous_hash

        entry_hash = hashlib.sha256(entry_with_hash.encode()).hexdigest()

        # Update chain
        self.chain.append(entry_hash)
        self._save_chain()

        return entry_hash

    def verify_log_integrity(self) -> bool:
        """Execute log chain integrity verification"""
        log_files = sorted(self.log_directory.glob('*.log'))

        for i, log_file in enumerate(log_files):
            if i >= len(self.chain):
                return False

            # Verify file integrity
            file_hash = self._calculate_file_hash(log_file)
            if file_hash != self.chain[i]:
                return False

        return True

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Execute SHA256 hash calculation for file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
```

## Access Control Implementation

### Multi-Factor Authentication

Execute comprehensive access controls:
```python
import pyotp
import qrcode
from typing import Optional
from datetime import datetime, timedelta

class AuthenticationService:
    def __init__(self):
        self.failed_attempts = {}
        self.max_attempts = 5
        self.lockout_duration = timedelta(minutes=15)

    def enable_mfa(self, user_id: str) -> str:
        """Execute MFA enabling for user and return provisioning URI"""
        # Generate secret
        secret = pyotp.random_base32()

        # Store secret securely (in production, use encrypted storage)
        self._store_mfa_secret(user_id, secret)

        # Generate provisioning URI
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user_id,
            issuer_name="YourApp"
        )

        return provisioning_uri

    def verify_mfa(self, user_id: str, token: str) -> bool:
        """Execute MFA token verification"""
        secret = self._get_mfa_secret(user_id)
        if not secret:
            return False

        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)  # Allow 1 step tolerance

    def is_account_locked(self, user_id: str) -> bool:
        """Execute account lockout status check"""
        if user_id not in self.failed_attempts:
            return False

        attempts, lock_time = self.failed_attempts[user_id]

        if attempts >= self.max_attempts:
            if datetime.now() - lock_time < self.lockout_duration:
                return True
            else:
                # Lockout expired, reset attempts
                del self.failed_attempts[user_id]

        return False

    def record_failed_attempt(self, user_id: str):
        """Execute failed login attempt recording"""
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = [0, datetime.now()]

        attempts, _ = self.failed_attempts[user_id]
        self.failed_attempts[user_id] = [attempts + 1, datetime.now()]

    def reset_attempts(self, user_id: str):
        """Execute failed attempts reset after successful login"""
        if user_id in self.failed_attempts:
            del self.failed_attempts[user_id]

    def _store_mfa_secret(self, user_id: str, secret: str):
        """Execute MFA secret secure storage"""
        # In production, use encrypted database or key management service
        pass

    def _get_mfa_secret(self, user_id: str) -> Optional[str]:
        """Execute MFA secret secure retrieval"""
        # In production, retrieve from encrypted storage
        return None  # Placeholder
```
