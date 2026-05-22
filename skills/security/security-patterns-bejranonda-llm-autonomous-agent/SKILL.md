---
name: security-patterns
description: Comprehensive OWASP security guidelines, secure coding patterns, vulnerability prevention strategies, and remediation best practices for building secure applications
version: 1.0.0
---

## Security Patterns Skill

Provides comprehensive security knowledge based on OWASP Top 10, secure coding practices, common vulnerability patterns, and proven remediation strategies.

## Core Philosophy: Secure by Default

**Security is not optional**. Every line of code should be written with security in mind. This skill provides the knowledge to:
- Prevent vulnerabilities before they occur
- Detect security issues early
- Remediate problems effectively
- Build security into the development process

## OWASP Top 10 (2021) - Deep Dive

### A01: Broken Access Control

**What It Is**: Failures that allow users to act outside their intended permissions.

**Common Vulnerabilities**:
```python
# ❌ INSECURE: No authorization check
@app.route('/api/user/<int:user_id>/profile')
def get_profile(user_id):
    user = User.query.get(user_id)
    return jsonify(user.to_dict())

# ✅ SECURE: Proper authorization
@app.route('/api/user/<int:user_id>/profile')
@require_auth
def get_profile(user_id):
    # Check if current user can access this profile
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)  # Forbidden

    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())
```

**Prevention Strategies**:
1. **Deny by Default**: Require explicit permission grants
2. **Principle of Least Privilege**: Grant minimum necessary permissions
3. **Verify on Server**: Never trust client-side access control
4. **Use Mature Frameworks**: Leverage battle-tested authorization libraries
5. **Log Access Failures**: Monitor for unauthorized access attempts

**Testing**:
```python
def test_authorization():
    """Test that users can only access their own data."""
    # Create two users
    user1 = create_user()
    user2 = create_user()

    # User1 tries to access User2's data
    response = client.get(
        f'/api/user/{user2.id}/profile',
        headers={'Authorization': f'Bearer {user1.token}'}
    )

    assert response.status_code == 403  # Should be forbidden
```

### A02: Cryptographic Failures

**What It Is**: Failures related to cryptography that expose sensitive data.

**Secure Patterns**:

**Password Hashing**:
```python
# ❌ INSECURE: Weak hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ SECURE: Strong password hashing
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)  # Cost factor 12
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

**Encryption**:
```python
# ✅ SECURE: AES-256 encryption
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64

def generate_encryption_key(password: str, salt: bytes) -> bytes:
    """Generate encryption key from password."""
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_data(data: str, key: bytes) -> str:
    """Encrypt data using Fernet (AES-128-CBC + HMAC)."""
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted: str, key: bytes) -> str:
    """Decrypt data."""
    f = Fernet(key)
    return f.decrypt(encrypted.encode()).decode()
```

**Secure Random**:
```python
# ❌ INSECURE: Predictable random
import random
token = str(random.randint(100000, 999999))

# ✅ SECURE: Cryptographically secure random
import secrets

def generate_secure_token(length: int = 32) -> str:
    """Generate cryptographically secure token."""
    return secrets.token_urlsafe(length)

def generate_reset_token() -> str:
    """Generate password reset token."""
    return secrets.token_hex(32)  # 64 character hex string
```

**Secret Management**:
```python
# ❌ INSECURE: Hardcoded secrets
API_KEY = "sk_live_abcdef123456"
DB_PASSWORD = "mysecretpassword"

# ✅ SECURE: Environment variables
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

API_KEY = os.environ.get('API_KEY')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

### A03: Injection

**SQL Injection Prevention**:
```python
# ❌ INSECURE: String concatenation
def get_user_by_username(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# ✅ SECURE: Parameterized queries
def get_user_by_username(username):
    query = "SELECT * FROM users WHERE username = %s"
    return db.execute(query, (username,))

# ✅ SECURE: ORM usage
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
```

**Command Injection Prevention**:
```python
# ❌ INSECURE: Shell command with user input
import os
def ping_host(hostname):
    os.system(f"ping -c 4 {hostname}")

# ✅ SECURE: Subprocess with list arguments
import subprocess
def ping_host(hostname):
    # Validate hostname
    if not re.match(r'^[a-zA-Z0-9.-]+$', hostname):
        raise ValueError("Invalid hostname")

    result = subprocess.run(
        ['ping', '-c', '4', hostname],
        capture_output=True,
        text=True,
        timeout=10
    )
    return result.stdout
```

**NoSQL Injection Prevention**:
```python
# ❌ INSECURE: Direct query construction
def find_user(user_id):
    query = {"_id": user_id}  # If user_id is dict, can inject
    return db.users.find_one(query)

# ✅ SECURE: Type validation
def find_user(user_id):
    # Ensure user_id is a string
    if not isinstance(user_id, str):
        raise TypeError("user_id must be string")

    from bson.objectid import ObjectId
    try:
        query = {"_id": ObjectId(user_id)}
    except:
        return None

    return db.users.find_one(query)
```

**Template Injection Prevention**:
```python
# ❌ INSECURE: Rendering user input as template
from flask import render_template_string
def render_page(template_str):
    return render_template_string(template_str)

# ✅ SECURE: Render with automatic escaping
from flask import render_template
def render_page(data):
    return render_template('page.html', data=data)
# In template: {{ data|e }} or use autoescaping
```

### A04: Insecure Design

**Secure Design Patterns**:

**Rate Limiting**:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")  # Prevent brute force
def login():
    # Login logic
    pass
```

**Business Logic Protection**:
```python
# ✅ SECURE: Prevent business logic flaws
class EcommerceCart:
    def apply_discount(self, code: str) -> bool:
        """Apply discount code with proper validation."""
        # Validate discount hasn't been used
        if self.discount_used:
            raise ValueError("Discount already applied")

        # Validate discount code
        discount = DiscountCode.query.filter_by(
            code=code,
            active=True
        ).first()

        if not discount:
            return False

        # Check expiration
        if discount.expires_at < datetime.now():
            return False

        # Check usage limit
        if discount.usage_count >= discount.max_uses:
            return False

        # Check minimum purchase amount
        if self.total < discount.min_purchase:
            return False

        # Apply discount
        self.discount_amount = min(
            self.total * discount.percentage / 100,
            discount.max_discount_amount
        )
        self.discount_used = True
        discount.usage_count += 1

        return True
```

### A05: Security Misconfiguration

**Secure Configuration Checklist**:

**Security Headers**:
```python
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

# Force HTTPS and set security headers
Talisman(app,
    force_https=True,
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    content_security_policy={
        'default-src': "'self'",
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'img-src': ["'self'", "data:", "https:"],
    },
    content_security_policy_nonce_in=['script-src'],
    referrer_policy='strict-origin-when-cross-origin',
    feature_policy={
        'geolocation': "'none'",
        'microphone': "'none'",
        'camera': "'none'",
    }
)

@app.after_request
def set_security_headers(response):
    """Set additional security headers."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response
```

**CORS Configuration**:
```python
# ❌ INSECURE: Wildcard CORS
from flask_cors import CORS
CORS(app, origins="*")  # Allows any origin

# ✅ SECURE: Specific origins
CORS(app,
    origins=["https://yourdomain.com", "https://app.yourdomain.com"],
    methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
    supports_credentials=True
)
```

**Error Handling**:
```python
# ❌ INSECURE: Verbose error messages
@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        "error": str(error),
        "traceback": traceback.format_exc()
    }), 500

# ✅ SECURE: Generic error messages
@app.errorhandler(Exception)
def handle_error(error):
    # Log full error for debugging
    app.logger.error(f"Error: {error}", exc_info=True)

    # Return generic message to user
    return jsonify({
        "error": "An internal error occurred",
        "request_id": generate_request_id()
    }), 500
```

### A06: Vulnerable Components

**Dependency Management**:
```python
# requirements.txt - Pin versions
flask==2.3.0
requests==2.31.0
cryptography==41.0.0

# Use pip-audit or safety
$ pip-audit  # Check for vulnerabilities
$ safety check  # Alternative tool
```

**Automated Scanning**:
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run pip-audit
        run: |
          pip install pip-audit
          pip-audit -r requirements.txt
```

### A07: Authentication Failures

**Secure Authentication Pattern**:
```python
from werkzeug.security import check_password_hash
import secrets
from datetime import datetime, timedelta

class SecureAuth:
    # Password policy
    MIN_PASSWORD_LENGTH = 12
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL = True

    # Account lockout
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=15)

    # Session security
    SESSION_TIMEOUT = timedelta(hours=2)
    SESSION_ABSOLUTE_TIMEOUT = timedelta(hours=8)

    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        """Validate password meets security requirements."""
        if len(password) < SecureAuth.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {SecureAuth.MIN_PASSWORD_LENGTH} characters"

        if SecureAuth.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            return False, "Password must contain uppercase letter"

        if SecureAuth.REQUIRE_LOWERCASE and not any(c.islower() for c in password):
            return False, "Password must contain lowercase letter"

        if SecureAuth.REQUIRE_DIGIT and not any(c.isdigit() for c in password):
            return False, "Password must contain digit"

        if SecureAuth.REQUIRE_SPECIAL and not any(c in "!@#$%^&*" for c in password):
            return False, "Password must contain special character"

        return True, "Password meets requirements"

    @staticmethod
    def login(username: str, password: str) -> dict:
        """Secure login implementation."""
        user = User.query.filter_by(username=username).first()

        # Timing attack prevention: always hash even if user doesn't exist
        if not user:
            check_password_hash("$2b$12$dummy", password)
            return {"success": False, "message": "Invalid credentials"}

        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.now():
            return {"success": False, "message": "Account temporarily locked"}

        # Verify password
        if not check_password_hash(user.password_hash, password):
            user.failed_login_attempts += 1

            # Lock account after max attempts
            if user.failed_login_attempts >= SecureAuth.MAX_LOGIN_ATTEMPTS:
                user.locked_until = datetime.now() + SecureAuth.LOCKOUT_DURATION

            db.session.commit()
            return {"success": False, "message": "Invalid credentials"}

        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.last_login = datetime.now()
        db.session.commit()

        # Create session
        session_token = secrets.token_urlsafe(32)
        session = UserSession(
            user_id=user.id,
            token=session_token,
            expires_at=datetime.now() + SecureAuth.SESSION_TIMEOUT,
            absolute_expires_at=datetime.now() + SecureAuth.SESSION_ABSOLUTE_TIMEOUT
        )
        db.session.add(session)
        db.session.commit()

        return {
            "success": True,
            "token": session_token,
            "expires_in": int(SecureAuth.SESSION_TIMEOUT.total_seconds())
        }
```

**Multi-Factor Authentication**:
```python
import pyotp

class MFAManager:
    @staticmethod
    def generate_secret() -> str:
        """Generate TOTP secret for user."""
        return pyotp.random_base32()

    @staticmethod
    def get_totp_uri(secret: str, username: str, issuer: str) -> str:
        """Generate QR code URI for TOTP app."""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=username,
            issuer_name=issuer
        )

    @staticmethod
    def verify_totp(secret: str, token: str, window: int = 1) -> bool:
        """Verify TOTP token with tolerance window."""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=window)

    @staticmethod
    def generate_backup_codes(count: int = 10) -> List[str]:
        """Generate one-time backup codes."""
        return [secrets.token_hex(4) for _ in range(count)]
```

### A08: Software and Data Integrity Failures

**Secure Deserialization**:
```python
# ❌ INSECURE: pickle allows code execution
import pickle
def load_data(data):
    return pickle.loads(data)

# ✅ SECURE: Use JSON or safer formats
import json
def load_data(data):
    return json.loads(data)

# If you must use pickle, sign the data
import hmac
import hashlib

def secure_pickle_dumps(obj, secret_key):
    """Pickle with HMAC signature."""
    pickled = pickle.dumps(obj)
    signature = hmac.new(secret_key, pickled, hashlib.sha256).hexdigest()
    return signature.encode() + b':' + pickled

def secure_pickle_loads(data, secret_key):
    """Verify signature before unpickling."""
    signature, pickled = data.split(b':', 1)
    expected_signature = hmac.new(secret_key, pickled, hashlib.sha256).hexdigest().encode()

    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("Invalid signature")

    return pickle.loads(pickled)
```

### A09: Logging and Monitoring

**Secure Logging Pattern**:
```python
import logging
from logging.handlers import RotatingFileHandler
import json

# Configure security event logging
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    'logs/security.log',
    maxBytes=10485760,  # 10MB
    backupCount=10
)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
security_logger.addHandler(handler)

def log_security_event(event_type: str, user_id: str, details: dict):
    """Log security-relevant events."""
    event = {
        "event_type": event_type,
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "details": details,
        "ip_address": request.remote_addr if request else None
    }

    security_logger.info(json.dumps(event))

# Usage
log_security_event("LOGIN_SUCCESS", user.id, {"username": user.username})
log_security_event("ACCESS_DENIED", user.id, {"resource": "/admin/users"})
log_security_event("PASSWORD_CHANGE", user.id, {})
```

### A10: Server-Side Request Forgery (SSRF)

**SSRF Prevention**:
```python
import requests
from urllib.parse import urlparse

ALLOWED_PROTOCOLS = ['http', 'https']
BLOCKED_IPS = [
    '127.0.0.0/8',    # Loopback
    '10.0.0.0/8',     # Private
    '172.16.0.0/12',  # Private
    '192.168.0.0/16', # Private
    '169.254.0.0/16', # Link-local
]

def is_safe_url(url: str) -> bool:
    """Validate URL is safe from SSRF."""
    parsed = urlparse(url)

    # Check protocol
    if parsed.scheme not in ALLOWED_PROTOCOLS:
        return False

    # Check for localhost/internal IPs
    hostname = parsed.hostname
    if not hostname:
        return False

    if hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
        return False

    # Resolve and check IP
    import socket
    try:
        ip = socket.gethostbyname(hostname)

        import ipaddress
        ip_obj = ipaddress.ip_address(ip)

        # Check if private/internal
        if ip_obj.is_private or ip_obj.is_loopback:
            return False

    except:
        return False

    return True

def fetch_url(url: str) -> str:
    """Safely fetch URL content."""
    if not is_safe_url(url):
        raise ValueError("URL not allowed")

    response = requests.get(
        url,
        timeout=5,
        allow_redirects=False  # Prevent redirect to internal URLs
    )

    return response.text
```

## Secure Coding Checklist

### Input Validation
- [ ] All user input is validated
- [ ] Whitelist validation where possible
- [ ] Length limits enforced
- [ ] Type checking implemented
- [ ] Special characters handled

### Authentication
- [ ] Strong password policy enforced
- [ ] Multi-factor authentication available
- [ ] Account lockout after failed attempts
- [ ] Secure password reset process
- [ ] Session timeout configured

### Authorization
- [ ] All endpoints require authorization
- [ ] Principle of least privilege applied
- [ ] Authorization checked on server-side
- [ ] No IDOR vulnerabilities
- [ ] Admin functions protected

### Cryptography
- [ ] Strong algorithms used (AES-256, SHA-256)
- [ ] No hardcoded secrets
- [ ] Secure random for tokens
- [ ] TLS/HTTPS enforced
- [ ] Passwords hashed with bcrypt/argon2

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit
- [ ] PII properly handled
- [ ] Data retention policies implemented
- [ ] Secure deletion procedures

### Error Handling
- [ ] Generic error messages to users
- [ ] Detailed errors logged securely
- [ ] No stack traces exposed
- [ ] Sensitive data not in logs
- [ ] Error monitoring implemented

### Logging & Monitoring
- [ ] Security events logged
- [ ] Log tampering prevented
- [ ] Anomaly detection configured
- [ ] Alerting for critical events
- [ ] Regular log review

This skill provides the foundation for writing secure code and identifying vulnerabilities effectively.