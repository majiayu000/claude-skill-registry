---
name: security-guardrails
description: Comprehensive security implementation standards. Use when security guardrails guidance is required.
---
## Purpose

Provide comprehensive security implementation standards covering credential management, secret rotation, input validation, and other guardrails that can be reused across services.

## IO Semantics

Input: Service configurations, deployment environments, and code paths that handle credentials or security-sensitive operations.

Output: Concrete policies, code templates, and operational procedures for secure storage, rotation, and validation of secrets.

Side Effects: Applying these guardrails may require changes to deployment pipelines, secret management systems, and runtime configuration.

## Deterministic Steps

### 1. Credential Management Security

Implement secure credential handling:
- Use environment variables for all configuration secrets
- Apply encrypted storage for sensitive environment variables
- Implement proper access controls for credential files
- Use secret management services for production environments

Apply secure credential patterns:
```python
# Secure credential access
import os
from cryptography.fernet import Fernet

class SecureConfig:
    def __init__(self):
        self.cipher_suite = Fernet(self._get_encryption_key())

    def get_database_config(self):
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5432')),
            'username': os.getenv('DB_USER'),
            'password': self._decrypt(os.getenv('DB_PASSWORD')),
            'database': os.getenv('DB_NAME')
        }

    def _get_encryption_key(self):
        key_file = os.getenv('ENCRYPTION_KEY_FILE', '/app/.encryption_key')
        with open(key_file, 'rb') as f:
            return f.read()

    def _decrypt(self, encrypted_value):
        if not encrypted_value:
            return None
        return self.cipher_suite.decrypt(encrypted_value.encode()).decode()
```

### 2. Secret Rotation Implementation

Automate secret lifecycle management:
```bash
#!/bin/bash
# secret-rotation.sh

rotate_database_credentials() {
    local service_name="$1"
    local max_age_days="${2:-90}"

    # Check credential age
    local credential_age=$(find /etc/secrets/ -name "${service_name}_db_*" -mtime +${max_age_days} | wc -l)

    if [ "$credential_age" -gt 0 ]; then
        echo "Rotating credentials for $service_name"

        # Generate new password
        new_password=$(openssl rand -base64 32)

        # Update database user password
        psql -h "$DB_HOST" -U "$DB_ADMIN" -c "ALTER USER ${service_name}_user WITH PASSWORD '$new_password';"

        # Store encrypted new password
        echo "$new_password" | gpg --encrypt --recipient "$GPG_RECIPIENT" > "/etc/secrets/${service_name}_db_password.gpg"

        # Update environment file
        sed -i "s/${service_name}_DB_PASSWORD=.*/${service_name}_DB_PASSWORD=$(echo "$new_password" | gpg --encrypt --armor --recipient "$GPG_RECIPIENT")/" /etc/environment

        echo "Credentials rotated successfully"
    fi
}
```

## Network Security Implementation

### TLS Configuration Standards

Implement comprehensive encryption:
```nginx
# TLS 1.3 only configuration
server {
    listen 443 ssl http2;
    server_name api.example.com;

    # Modern TLS configuration
    ssl_protocols TLSv1.3;
    ssl_prefer_server_ciphers on;

    # Forward secrecy cipher suites
    ssl_ciphers TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;

    # HSTS enforcement
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";

    # Certificate configuration
    ssl_certificate /etc/ssl/certs/api.crt;
    ssl_certificate_key /etc/ssl/private/api.key;
    ssl_trusted_certificate /etc/ssl/certs/chain.crt;
}
```

### CORS and Security Headers

Apply comprehensive web security:
```python
# Flask security configuration
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

app = Flask(__name__)

# Strict CORS configuration
CORS(app,
     resources={
         r"/api/*": {
             "origins": ["https://app.example.com"],
             "methods": ["GET", "POST", "PUT", "DELETE"],
             "allow_headers": ["Content-Type", "Authorization"],
             "max_age": 86400
         }
     })

# Security headers with Talisman
csp = {
    'default-src': "'self'",
    'script-src': [
        "'self'",
        "'nonce-${nonce}'",
        "https://trusted-cdn.example.com"
    ],
    'style-src': [
        "'self'",
        "'unsafe-inline'",
        "https://fonts.googleapis.com"
    ],
    'font-src': ["'self'", "https://fonts.gstatic.com"],
    'img-src': ["'self'", "data:", "https:"],
    'connect-src': ["'self'", "https://api.example.com"]
}

Talisman(app,
         force_https=True,
         strict_transport_security=True,
         content_security_policy=csp,
         referrer_policy='strict-origin-when-cross-origin',
         feature_policy={
             'geolocation': "'none'",
             'camera': "'none'",
             'microphone': "'none'"
         })
```

## Input Validation and Sanitization

### Comprehensive Input Security

Implement multi-layer validation:
```python
import re
import bleach
from typing import Any, Dict, List
from pydantic import BaseModel, validator, constr

class UserInputValidator:
    # Security patterns
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
        r"(--|#|\/\*|\*\/)",
        r"(;|\|||\|&)",
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
    def sanitize_input(cls, user_input: str) -> str:
        # Remove HTML tags
        clean_input = bleach.clean(user_input, tags=[], strip=True)

        # Normalize whitespace
        clean_input = ' '.join(clean_input.split())

        return clean_input

    @classmethod
    def detect_sql_injection(cls, input_string: str) -> bool:
        upper_input = input_string.upper()
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, upper_input, re.IGNORECASE):
                return True
        return False

    @classmethod
    def detect_xss(cls, input_string: str) -> bool:
        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, input_string, re.IGNORECASE | re.DOTALL):
                return True
        return False

# Pydantic model for validation
class SecureUserRegistration(BaseModel):
    username: constr(regex=r'^[a-zA-Z0-9_]{3,30}$')
    email: constr(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    password: constr(min_length=12, max_length=128)

    @validator('password')
    def validate_password_strength(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain special character')
        return v

    @validator('username')
    def validate_username_safe(cls, v):
        if UserInputValidator.detect_sql_injection(v):
            raise ValueError('Invalid characters in username')
        if UserInputValidator.detect_xss(v):
            raise ValueError('Invalid characters in username')
        return v
```

### File Upload Security

Implement secure file handling:
```python
import magic
import hashlib
from werkzeug.utils import secure_filename

class SecureFileUploader:
    ALLOWED_MIME_TYPES = {
        'image/jpeg', 'image/png', 'image/gif',
        'application/pdf', 'text/plain'
    }

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER = '/secure/uploads'

    @classmethod
    def validate_file(cls, file) -> Dict[str, Any]:
        result = {'valid': False, 'errors': []}

        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning

        if file_size > cls.MAX_FILE_SIZE:
            result['errors'].append('File too large')
            return result

        # Check file type
        file_content = file.read(1024)
        file.seek(0)

        mime_type = magic.from_buffer(file_content, mime=True)
        if mime_type not in cls.ALLOWED_MIME_TYPES:
            result['errors'].append(f'File type {mime_type} not allowed')
            return result

        # Generate secure filename
        original_filename = file.filename
        secure_name = secure_filename(original_filename)

        # Add hash to prevent filename collisions
        file_hash = hashlib.sha256(file_content).hexdigest()[:8]
        final_filename = f"{file_hash}_{secure_name}"

        result.update({
            'valid': True,
            'secure_filename': final_filename,
            'mime_type': mime_type,
            'size': file_size
        })

        return result

    @classmethod
    def save_file(cls, file, filename: str) -> str:
        file_path = os.path.join(cls.UPLOAD_FOLDER, filename)

        # Ensure directory exists
        os.makedirs(cls.UPLOAD_FOLDER, mode=0o700, exist_ok=True)

        # Save file with restricted permissions
        with open(file_path, 'wb') as f:
            file.save(file_path)

        # Set file permissions
        os.chmod(file_path, 0o600)

        return file_path
```

## Container and Deployment Security

### Container Hardening

Implement secure container practices:
```dockerfile
# Multi-stage secure build
FROM alpine:3.18 AS builder

# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Install build dependencies
RUN apk add --no-cache \
    ca-certificates \
    tzdata \
    && rm -rf /var/cache/apk/*

# Build application
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python -m compileall .

# Production stage
FROM alpine:3.18

# Import user from builder stage
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group

# Install runtime dependencies only
RUN apk add --no-cache \
    ca-certificates \
    tzdata \
    && rm -rf /var/cache/apk/* \
    && rm -rf /root/.cache

# Create app directory with proper permissions
WORKDIR /app
COPY --from=builder /app .

# Set ownership and permissions
RUN chown -R appuser:appgroup /app && \
    chmod -R 755 /app && \
    chmod -R 644 /app/*.py

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start application with security flags
CMD ["python", "-u", "app.py"]
```

### Security Scanning Integration

Automated security validation:
```yaml
# GitHub Actions security workflow
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Trivy vulnerability scanner
        run: |
          docker run --rm -v $PWD:/app aquasec/trivy:latest image --exit-code 0 --severity HIGH,CRITICAL myapp:latest

      - name: Run Bandit security linter
        run: |
          pip install bandit[toml]
          bandit -r src/ -f json -o bandit-report.json

      - name: Run Safety dependency check
        run: |
          pip install safety
          safety check --json --output safety-report.json

      - name: Run Semgrep security analysis
        run: |
          docker run --rm -v $PWD:/app returntocorp/semgrep:latest semgrep --config=auto --json --output=semgrep-report.json

      - name: Upload security reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            bandit-report.json
            safety-report.json
            semgrep-report.json
```

## Security Monitoring Implementation

### Intrusion Detection Setup

Implement comprehensive security monitoring:
```python
# Security event monitoring
import json
import logging
from datetime import datetime
from typing import Dict, List

class SecurityMonitor:
    def __init__(self):
        self.logger = logging.getLogger('security')
        self.security_events = []

    def log_security_event(self, event_type: str, severity: str, details: Dict[str, Any]):
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'severity': severity,
            'details': details,
            'source_ip': details.get('source_ip'),
            'user_agent': details.get('user_agent')
        }

        self.security_events.append(event)

        # Log structured security event
        log_entry = json.dumps(event)

        if severity == 'CRITICAL':
            self.logger.critical(log_entry)
            self._send_alert(event)
        elif severity == 'HIGH':
            self.logger.error(log_entry)
        elif severity == 'MEDIUM':
            self.logger.warning(log_entry)
        else:
            self.logger.info(log_entry)

    def detect_anomalous_login(self, user_id: str, ip_address: str, user_agent: str):
        # Check for login from new location
        recent_logins = [e for e in self.security_events
                        if e['event_type'] == 'login' and e['details']['user_id'] == user_id
                        and (datetime.utcnow() - datetime.fromisoformat(e['timestamp'])).seconds < 3600]

        known_ips = {e['details']['ip_address'] for e in recent_logins}

        if ip_address not in known_ips and len(known_ips) > 0:
            self.log_security_event(
                'suspicious_login_location',
                'HIGH',
                {
                    'user_id': user_id,
                    'new_ip': ip_address,
                    'known_ips': list(known_ips),
                    'source_ip': ip_address,
                    'user_agent': user_agent
                }
            )

    def detect_brute_force(self, ip_address: str):
        failed_attempts = len([e for e in self.security_events
                             if e['event_type'] == 'failed_login'
                             and e['details']['ip_address'] == ip_address
                             and (datetime.utcnow() - datetime.fromisoformat(e['timestamp'])).seconds < 300])

        if failed_attempts >= 5:
            self.log_security_event(
                'brute_force_detected',
                'CRITICAL',
                {
                    'ip_address': ip_address,
                    'failed_attempts': failed_attempts,
                    'timeframe': '5 minutes',
                    'source_ip': ip_address
                }
            )

    def _send_alert(self, event: Dict[str, Any]):
        # Integration with alerting system
        alert_message = f"Security Alert: {event['event_type']} - {event['details']}"

        # Send to monitoring system
        # send_to_slack(alert_message)
        # send_to_pagerduty(alert_message)
        # send_email(alert_message)
```
