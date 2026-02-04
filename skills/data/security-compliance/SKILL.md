---
name: security-compliance
description: Skill for ensuring security best practices and regulatory compliance. Use when implementing authentication, handling sensitive data, securing APIs, or meeting compliance requirements (PCI-DSS, GDPR). Provides OWASP Top 10 prevention patterns, security headers, encryption strategies, and data protection guidelines.
---

# Security Compliance

Skill for implementing security best practices and meeting compliance requirements.

## Overview

This skill provides guidance for:
1. **OWASP Top 10** - Prevention of common vulnerabilities
2. **Authentication** - Secure auth implementation patterns
3. **Data Protection** - Encryption and handling of sensitive data
4. **Compliance** - PCI-DSS, GDPR requirements
5. **Security Headers** - CSP, HSTS, and other protective headers

## OWASP Top 10 Prevention

### A01: Broken Access Control

**Vulnerability:** Users can act outside intended permissions.

**Prevention:**

```python
# FastAPI dependency for authorization
from fastapi import Depends, HTTPException, status

async def require_permission(permission: str):
    async def checker(user: User = Depends(get_current_user)):
        if not user.has_permission(permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return checker

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_permission("admin:delete_users"))
):
    # Only executes if user has permission
    await user_service.delete(user_id)
```

```typescript
// Next.js middleware for route protection
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value;

  // Protect admin routes
  if (request.nextUrl.pathname.startsWith('/admin')) {
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url));
    }

    // Verify admin role in token
    const payload = verifyToken(token);
    if (payload.role !== 'admin') {
      return NextResponse.redirect(new URL('/unauthorized', request.url));
    }
  }

  return NextResponse.next();
}
```

### A02: Cryptographic Failures

**Vulnerability:** Sensitive data exposed due to weak/missing encryption.

**Prevention:**

```python
# Password hashing with bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)
```

```python
# Field-level encryption for sensitive data
from cryptography.fernet import Fernet
import base64
import os

class FieldEncryption:
    def __init__(self):
        key = os.environ.get("ENCRYPTION_KEY")
        self.cipher = Fernet(key.encode())

    def encrypt(self, value: str) -> str:
        return self.cipher.encrypt(value.encode()).decode()

    def decrypt(self, encrypted: str) -> str:
        return self.cipher.decrypt(encrypted.encode()).decode()

# Usage in model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    _ssn_encrypted = Column("ssn", String)  # Stored encrypted

    @property
    def ssn(self):
        if self._ssn_encrypted:
            return encryption.decrypt(self._ssn_encrypted)
        return None

    @ssn.setter
    def ssn(self, value: str):
        self._ssn_encrypted = encryption.encrypt(value)
```

### A03: Injection

**Vulnerability:** SQL, NoSQL, OS command injection.

**Prevention:**

```python
# ALWAYS use parameterized queries
from sqlalchemy import text

# BAD - SQL injection vulnerable
query = f"SELECT * FROM users WHERE email = '{email}'"

# GOOD - Parameterized query
result = session.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {"email": email}
)

# GOOD - ORM queries (automatically parameterized)
user = session.query(User).filter(User.email == email).first()
```

```python
# Input validation with Pydantic
from pydantic import BaseModel, EmailStr, constr, validator
import re

class UserCreate(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')
    bio: str

    @validator('bio')
    def sanitize_bio(cls, v):
        # Remove potential script tags
        return re.sub(r'<script[^>]*>.*?</script>', '', v, flags=re.IGNORECASE)
```

### A04: Insecure Design

**Vulnerability:** Missing security controls in design phase.

**Prevention Checklist:**

- [ ] Threat modeling completed
- [ ] Security requirements documented
- [ ] Rate limiting designed
- [ ] Input validation at all boundaries
- [ ] Audit logging planned
- [ ] Failure modes considered

### A05: Security Misconfiguration

**Vulnerability:** Default configs, unnecessary features, missing patches.

**Prevention:**

```python
# Production configuration checklist
# config/production.py

# Disable debug mode
DEBUG = False

# Restrict CORS
CORS_ORIGINS = ["https://yourdomain.com"]

# Secure cookies
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"

# Disable unnecessary endpoints
DOCS_URL = None  # Disable /docs in production
REDOC_URL = None  # Disable /redoc in production
```

```typescript
// next.config.js security settings
module.exports = {
  poweredBy: false,  // Remove X-Powered-By header
  reactStrictMode: true,

  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

### A06: Vulnerable and Outdated Components

**Prevention:**

```bash
# Regular dependency audits
npm audit
pip-audit

# Automated updates
npm outdated
pip list --outdated

# Lock file for reproducible builds
npm ci  # Instead of npm install
pip install -r requirements.txt --require-hashes
```

### A07: Identification and Authentication Failures

**Prevention:**

```python
# Secure session management
from fastapi import FastAPI, Response
from datetime import timedelta

SESSION_SETTINGS = {
    "secret_key": os.environ["SESSION_SECRET"],
    "expire_after": timedelta(hours=8),
    "secure": True,  # HTTPS only
    "httponly": True,  # No JavaScript access
    "samesite": "strict",  # CSRF protection
}

# Account lockout after failed attempts
class LoginService:
    MAX_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=15)

    async def login(self, email: str, password: str) -> User:
        attempts = await self.get_failed_attempts(email)

        if attempts >= self.MAX_ATTEMPTS:
            lockout_expires = await self.get_lockout_expiry(email)
            if datetime.utcnow() < lockout_expires:
                raise HTTPException(
                    status_code=429,
                    detail=f"Account locked. Try again in {lockout_expires - datetime.utcnow()}"
                )

        user = await self.verify_credentials(email, password)
        if not user:
            await self.record_failed_attempt(email)
            raise HTTPException(status_code=401, detail="Invalid credentials")

        await self.clear_failed_attempts(email)
        return user
```

### A08: Software and Data Integrity Failures

**Prevention:**

```python
# Verify webhook signatures
import hmac
import hashlib

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(f"sha256={expected}", signature)

@router.post("/webhooks/payment")
async def handle_payment_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-Signature")

    if not verify_webhook_signature(payload, signature, WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Process webhook...
```

### A09: Security Logging and Monitoring Failures

**Prevention:**

```python
# Structured security logging
import structlog
from datetime import datetime

logger = structlog.get_logger()

class SecurityAuditLogger:
    async def log_auth_event(
        self,
        event_type: str,
        user_id: str | None,
        ip_address: str,
        success: bool,
        details: dict = None
    ):
        await logger.ainfo(
            "security_event",
            event_type=event_type,
            user_id=user_id,
            ip_address=ip_address,
            success=success,
            timestamp=datetime.utcnow().isoformat(),
            details=details or {}
        )

# Usage
audit = SecurityAuditLogger()

@router.post("/login")
async def login(request: Request, credentials: LoginRequest):
    ip = request.client.host

    try:
        user = await auth_service.login(credentials)
        await audit.log_auth_event("login", user.id, ip, success=True)
        return {"token": create_token(user)}
    except AuthenticationError:
        await audit.log_auth_event(
            "login",
            None,
            ip,
            success=False,
            details={"email": credentials.email}
        )
        raise
```

### A10: Server-Side Request Forgery (SSRF)

**Prevention:**

```python
# Validate and sanitize URLs
from urllib.parse import urlparse
import ipaddress

ALLOWED_HOSTS = ["api.example.com", "cdn.example.com"]

def validate_url(url: str) -> bool:
    parsed = urlparse(url)

    # Only allow HTTPS
    if parsed.scheme != "https":
        return False

    # Check against allowlist
    if parsed.hostname not in ALLOWED_HOSTS:
        return False

    # Block internal IPs
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback:
            return False
    except ValueError:
        pass  # Not an IP, hostname already checked

    return True

@router.post("/fetch-preview")
async def fetch_url_preview(url: str):
    if not validate_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Safe to fetch
    response = await httpx.get(url, timeout=5.0)
    return parse_preview(response)
```

## Security Headers

### Implementation

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload'
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block'
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin'
  },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()'
  },
  {
    key: 'Content-Security-Policy',
    value: ContentSecurityPolicy.replace(/\s{2,}/g, ' ').trim()
  }
];

const ContentSecurityPolicy = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data: https:;
  font-src 'self';
  connect-src 'self' https://api.yourdomain.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
`;
```

### Header Reference

| Header | Purpose | Value |
|--------|---------|-------|
| Strict-Transport-Security | Force HTTPS | max-age=31536000; includeSubDomains |
| X-Frame-Options | Prevent clickjacking | DENY or SAMEORIGIN |
| X-Content-Type-Options | Prevent MIME sniffing | nosniff |
| Content-Security-Policy | Control resource loading | See CSP guide |
| X-XSS-Protection | Legacy XSS filter | 1; mode=block |
| Referrer-Policy | Control referrer info | strict-origin-when-cross-origin |
| Permissions-Policy | Disable browser features | camera=(), microphone=() |

## PCI-DSS Compliance

### Requirements Overview

| Requirement | Implementation |
|-------------|----------------|
| Protect cardholder data | Encryption at rest and in transit |
| Maintain vulnerability management | Regular patching, security scanning |
| Implement strong access control | RBAC, MFA, audit logging |
| Monitor and test networks | IDS/IPS, penetration testing |
| Maintain security policy | Documented procedures |

### Payment Data Handling

```python
# NEVER store full card numbers - use tokenization
class PaymentService:
    def __init__(self, payment_provider):
        self.provider = payment_provider  # Stripe, etc.

    async def process_payment(
        self,
        amount: int,
        card_token: str,  # Token from client-side SDK
        user_id: str
    ) -> PaymentResult:
        # Card data never touches our server
        result = await self.provider.charge(
            amount=amount,
            source=card_token,
            metadata={"user_id": user_id}
        )

        # Store only safe references
        await self.store_transaction(
            user_id=user_id,
            provider_id=result.id,
            last_four=result.card.last4,  # Safe to store
            amount=amount,
            status=result.status
        )

        return result
```

```typescript
// Client-side card collection with Stripe Elements
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe } from '@stripe/react-stripe-js';

function PaymentForm() {
  const stripe = useStripe();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    // Card data goes directly to Stripe, not our server
    const { token, error } = await stripe.createToken(cardElement);

    if (token) {
      // Send only the token to our backend
      await api.processPayment({ token: token.id, amount });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <CardElement />
      <button type="submit">Pay</button>
    </form>
  );
}
```

## GDPR Compliance

### Data Subject Rights

| Right | Implementation |
|-------|----------------|
| Access | Export user data endpoint |
| Rectification | Update profile endpoint |
| Erasure | Delete account endpoint |
| Portability | JSON/CSV export |
| Object | Opt-out mechanisms |

### Implementation

```python
# GDPR data export
class GDPRService:
    async def export_user_data(self, user_id: str) -> dict:
        """Export all user data for GDPR access request."""
        user = await user_repo.get(user_id)

        return {
            "profile": {
                "email": user.email,
                "name": user.name,
                "created_at": user.created_at.isoformat(),
            },
            "orders": await order_repo.get_by_user(user_id),
            "activity_log": await activity_repo.get_by_user(user_id),
            "preferences": await preference_repo.get_by_user(user_id),
        }

    async def delete_user_data(self, user_id: str) -> None:
        """Delete all user data for GDPR erasure request."""
        # Anonymize rather than delete for audit trail
        await user_repo.anonymize(user_id)
        await order_repo.anonymize_user(user_id)
        await activity_repo.delete_by_user(user_id)

        # Log the deletion request
        await audit_log.record(
            event="gdpr_erasure",
            user_id=user_id,
            timestamp=datetime.utcnow()
        )
```

### Consent Management

```typescript
// Cookie consent banner
interface ConsentState {
  necessary: true;  // Always required
  analytics: boolean;
  marketing: boolean;
}

function CookieConsent() {
  const [consent, setConsent] = useState<ConsentState | null>(null);

  const handleAccept = (options: Partial<ConsentState>) => {
    const newConsent = { necessary: true, ...options };
    setConsent(newConsent);
    setCookie('consent', JSON.stringify(newConsent), { maxAge: 365 * 24 * 60 * 60 });

    // Initialize only consented trackers
    if (newConsent.analytics) {
      initAnalytics();
    }
  };

  return (
    <div className="cookie-banner">
      <p>We use cookies to improve your experience.</p>
      <button onClick={() => handleAccept({ analytics: true, marketing: true })}>
        Accept All
      </button>
      <button onClick={() => handleAccept({ analytics: false, marketing: false })}>
        Essential Only
      </button>
    </div>
  );
}
```

## Encryption Best Practices

### At Rest

```python
# Database column encryption
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

class SensitiveData(Base):
    __tablename__ = "sensitive_data"

    id = Column(Integer, primary_key=True)
    # Encrypted at database level
    ssn = Column(EncryptedType(
        String,
        os.environ["DB_ENCRYPTION_KEY"],
        AesEngine,
        "pkcs5"
    ))
```

### In Transit

```python
# Force HTTPS in FastAPI
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)

# TLS configuration for database
DATABASE_URL = (
    "postgresql://user:pass@host/db"
    "?sslmode=require"
    "&sslrootcert=/path/to/ca.pem"
)
```

## Security Checklist

### Authentication

- [ ] Passwords hashed with bcrypt/argon2
- [ ] MFA available for sensitive accounts
- [ ] Account lockout after failed attempts
- [ ] Secure session management
- [ ] Password complexity requirements
- [ ] Secure password reset flow

### Data Protection

- [ ] Sensitive data encrypted at rest
- [ ] TLS/HTTPS enforced
- [ ] No sensitive data in logs
- [ ] No sensitive data in URLs
- [ ] Proper data retention policies
- [ ] Data anonymization for analytics

### API Security

- [ ] Authentication required for all endpoints
- [ ] Authorization checks on resources
- [ ] Rate limiting implemented
- [ ] Input validation on all inputs
- [ ] Output encoding for responses
- [ ] CORS properly configured

### Infrastructure

- [ ] Security headers configured
- [ ] Dependencies regularly audited
- [ ] Secrets in environment variables
- [ ] Debug mode disabled in production
- [ ] Error messages don't leak info
- [ ] Audit logging enabled

### Compliance

- [ ] GDPR consent mechanisms
- [ ] Data export capability
- [ ] Data deletion capability
- [ ] Privacy policy updated
- [ ] PCI tokenization (if payments)
- [ ] Audit trail maintained

## References

For detailed guidance, see:
- `references/owasp-prevention.md` - Detailed OWASP prevention strategies
- `references/compliance-checklist.md` - Comprehensive compliance requirements
