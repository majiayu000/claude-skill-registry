---
name: authentication
description: Authentication and authorization including JWT, OAuth2, OIDC, sessions, RBAC, and security analysis. Activate for login, auth flows, security audits, threat modeling, access control, and identity management.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
dependencies:
  - extended-thinking
  - deep-analysis
  - complex-reasoning
triggers:
  - authentication
  - authorization
  - auth flow
  - security audit
  - threat model
  - JWT
  - OAuth
  - OIDC
  - session
  - RBAC
  - access control
---

# Authentication Skill

Provides comprehensive authentication and authorization capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- User authentication flows
- JWT token management
- OAuth2 integration
- Session management
- Role-based access control (RBAC)

## JWT Authentication

### Token Generation
\`\`\`python
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user_id: str, roles: list[str]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "roles": roles,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": user_id,
        "exp": expire,
        "type": "refresh"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
\`\`\`

### Password Hashing
\`\`\`python
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Usage
async def authenticate_user(email: str, password: str) -> User | None:
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
\`\`\`

## FastAPI Auth Dependencies

\`\`\`python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = verify_token(token)
    user = await get_user(payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

# Role-based access
def require_roles(*roles: str):
    async def role_checker(user: User = Depends(get_current_user)):
        if not any(role in user.roles for role in roles):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

# Usage
@app.get("/admin")
async def admin_route(user: User = Depends(require_roles("admin"))):
    return {"message": "Admin access granted"}
\`\`\`

## OAuth2 Integration

### Google OAuth2
\`\`\`python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get('/auth/google')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth/google/callback')
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')

    # Find or create user
    user = await get_or_create_user(
        email=user_info['email'],
        name=user_info['name'],
        provider='google'
    )

    # Generate JWT
    access_token = create_access_token(user.id, user.roles)
    return {"access_token": access_token, "token_type": "bearer"}
\`\`\`

### GitHub OAuth2
\`\`\`python
oauth.register(
    name='github',
    client_id=os.environ['GITHUB_CLIENT_ID'],
    client_secret=os.environ['GITHUB_CLIENT_SECRET'],
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'}
)
\`\`\`

## Session Management

\`\`\`python
from fastapi import Request, Response
import secrets

async def create_session(user_id: str, response: Response) -> str:
    session_id = secrets.token_urlsafe(32)

    # Store in Redis
    await redis.hset(f"session:{session_id}", mapping={
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat()
    })
    await redis.expire(f"session:{session_id}", 86400)  # 24 hours

    # Set cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=86400
    )

    return session_id

async def get_session(request: Request) -> dict | None:
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None

    session = await redis.hgetall(f"session:{session_id}")
    if not session:
        return None

    # Refresh TTL
    await redis.expire(f"session:{session_id}", 86400)
    return session

async def destroy_session(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if session_id:
        await redis.delete(f"session:{session_id}")
    response.delete_cookie("session_id")
\`\`\`

## RBAC Implementation

\`\`\`python
from enum import Enum
from typing import Set

class Permission(str, Enum):
    READ_AGENTS = "read:agents"
    WRITE_AGENTS = "write:agents"
    DELETE_AGENTS = "delete:agents"
    ADMIN = "admin"

ROLE_PERMISSIONS: dict[str, Set[Permission]] = {
    "viewer": {Permission.READ_AGENTS},
    "operator": {Permission.READ_AGENTS, Permission.WRITE_AGENTS},
    "admin": {Permission.READ_AGENTS, Permission.WRITE_AGENTS, Permission.DELETE_AGENTS, Permission.ADMIN},
}

def has_permission(user_roles: list[str], required: Permission) -> bool:
    for role in user_roles:
        if role in ROLE_PERMISSIONS and required in ROLE_PERMISSIONS[role]:
            return True
    return False

def require_permission(permission: Permission):
    async def permission_checker(user: User = Depends(get_current_user)):
        if not has_permission(user.roles, permission):
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return permission_checker

# Usage
@app.delete("/agents/{id}")
async def delete_agent(
    id: str,
    user: User = Depends(require_permission(Permission.DELETE_AGENTS))
):
    await agent_service.delete(id)
    return {"status": "deleted"}
\`\`\`

## Security Best Practices

1. **Use HTTPS** always in production
2. **Hash passwords** with bcrypt or argon2
3. **Short-lived access tokens** (15-30 minutes)
4. **Refresh token rotation** on each use
5. **HttpOnly, Secure cookies** for tokens
6. **Rate limit** authentication endpoints
7. **Log authentication events** for auditing
8. **Implement account lockout** after failed attempts

## OAuth 2.0 & OIDC Best Practices

### OAuth 2.0 Grant Types

#### Authorization Code Flow (Recommended for Web Apps)
```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='custom_provider',
    client_id=os.environ['OAUTH_CLIENT_ID'],
    client_secret=os.environ['OAUTH_CLIENT_SECRET'],
    authorize_url='https://provider.com/oauth/authorize',
    authorize_params=None,
    access_token_url='https://provider.com/oauth/token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'openid profile email'}
)

@app.get('/auth/login')
async def login(request: Request):
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    await redis.set(f"oauth_state:{state}", "1", ex=600)

    redirect_uri = request.url_for('auth_callback')
    return await oauth.custom_provider.authorize_redirect(
        request,
        redirect_uri,
        state=state
    )

@app.get('/auth/callback')
async def auth_callback(request: Request):
    # Verify state (CSRF protection)
    state = request.query_params.get('state')
    if not await redis.get(f"oauth_state:{state}"):
        raise HTTPException(status_code=400, detail="Invalid state")

    await redis.delete(f"oauth_state:{state}")

    # Exchange authorization code for tokens
    token = await oauth.custom_provider.authorize_access_token(request)
    user_info = token.get('userinfo')

    # Create or update user
    user = await upsert_user(user_info)

    # Issue application tokens
    access_token = create_access_token(user.id, user.roles)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
```

#### PKCE (Proof Key for Code Exchange) for SPAs
```python
# Frontend (JavaScript/TypeScript)
import { generateCodeVerifier, generateCodeChallenge } from 'oauth-pkce'

// Generate PKCE parameters
const codeVerifier = generateCodeVerifier()
const codeChallenge = await generateCodeChallenge(codeVerifier)

// Store verifier for later use
sessionStorage.setItem('code_verifier', codeVerifier)

// Redirect to authorization endpoint
const authUrl = new URL('https://provider.com/oauth/authorize')
authUrl.searchParams.set('client_id', CLIENT_ID)
authUrl.searchParams.set('redirect_uri', REDIRECT_URI)
authUrl.searchParams.set('response_type', 'code')
authUrl.searchParams.set('scope', 'openid profile email')
authUrl.searchParams.set('code_challenge', codeChallenge)
authUrl.searchParams.set('code_challenge_method', 'S256')
authUrl.searchParams.set('state', generateState())

window.location.href = authUrl.toString()

// In callback handler
const code = new URLSearchParams(window.location.search).get('code')
const codeVerifier = sessionStorage.getItem('code_verifier')

const tokenResponse = await fetch('https://provider.com/oauth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: code,
    redirect_uri: REDIRECT_URI,
    client_id: CLIENT_ID,
    code_verifier: codeVerifier
  })
})
```

#### Client Credentials Flow (Service-to-Service)
```python
import httpx
from datetime import datetime, timedelta

class ServiceAuthClient:
    def __init__(self):
        self.token = None
        self.expires_at = None

    async def get_token(self) -> str:
        # Return cached token if still valid
        if self.token and self.expires_at > datetime.utcnow():
            return self.token

        # Request new token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://provider.com/oauth/token',
                data={
                    'grant_type': 'client_credentials',
                    'client_id': os.environ['SERVICE_CLIENT_ID'],
                    'client_secret': os.environ['SERVICE_CLIENT_SECRET'],
                    'scope': 'api.read api.write'
                }
            )
            response.raise_for_status()
            data = response.json()

            self.token = data['access_token']
            self.expires_at = datetime.utcnow() + timedelta(seconds=data['expires_in'] - 60)

            return self.token

# Usage
auth_client = ServiceAuthClient()

async def call_protected_api():
    token = await auth_client.get_token()
    async with httpx.AsyncClient() as client:
        response = await client.get(
            'https://api.service.com/resource',
            headers={'Authorization': f'Bearer {token}'}
        )
        return response.json()
```

### OpenID Connect (OIDC)

#### ID Token Validation
```python
from jose import jwt, jwk
from jose.utils import base64url_decode
import httpx

class OIDCValidator:
    def __init__(self, issuer: str, client_id: str):
        self.issuer = issuer
        self.client_id = client_id
        self.jwks = None
        self.jwks_updated_at = None

    async def get_jwks(self) -> dict:
        # Refresh JWKS if stale (cache for 24 hours)
        if not self.jwks or (datetime.utcnow() - self.jwks_updated_at).seconds > 86400:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.issuer}/.well-known/jwks.json")
                response.raise_for_status()
                self.jwks = response.json()
                self.jwks_updated_at = datetime.utcnow()

        return self.jwks

    async def validate_id_token(self, id_token: str) -> dict:
        # Decode header to get key ID
        header = jwt.get_unverified_header(id_token)
        kid = header['kid']

        # Get JWKS and find matching key
        jwks = await self.get_jwks()
        key = next((k for k in jwks['keys'] if k['kid'] == kid), None)

        if not key:
            raise ValueError("Public key not found in JWKS")

        # Convert JWK to PEM
        public_key = jwk.construct(key)

        # Validate and decode ID token
        try:
            claims = jwt.decode(
                id_token,
                public_key.to_pem().decode('utf-8'),
                algorithms=['RS256'],
                audience=self.client_id,
                issuer=self.issuer,
                options={
                    'verify_exp': True,
                    'verify_iat': True,
                    'verify_aud': True,
                    'verify_iss': True
                }
            )

            # Additional validations
            if claims.get('nonce'):
                # Verify nonce matches what was sent in auth request
                pass

            return claims

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="ID token expired")
        except jwt.JWTClaimsError as e:
            raise HTTPException(status_code=401, detail=f"Invalid ID token claims: {e}")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"ID token validation failed: {e}")

# Usage
validator = OIDCValidator(
    issuer="https://provider.com",
    client_id=os.environ['OIDC_CLIENT_ID']
)

@app.post("/auth/oidc/callback")
async def oidc_callback(id_token: str):
    claims = await validator.validate_id_token(id_token)

    # Extract user information
    user = await get_or_create_user(
        email=claims['email'],
        name=claims['name'],
        sub=claims['sub']
    )

    return {"user": user, "claims": claims}
```

### JWT Security Best Practices

#### Secure Token Generation
```python
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

# Use RS256 (asymmetric) instead of HS256 for public verification
PRIVATE_KEY_PATH = os.environ.get('JWT_PRIVATE_KEY_PATH')
PUBLIC_KEY_PATH = os.environ.get('JWT_PUBLIC_KEY_PATH')

def load_keys():
    with open(PRIVATE_KEY_PATH, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

    with open(PUBLIC_KEY_PATH, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )

    return private_key, public_key

PRIVATE_KEY, PUBLIC_KEY = load_keys()

def create_secure_access_token(
    user_id: str,
    roles: list[str],
    tenant_id: str = None,
    custom_claims: dict = None
) -> str:
    now = datetime.utcnow()

    payload = {
        # Standard claims (RFC 7519)
        "iss": "https://api.yourdomain.com",  # Issuer
        "sub": user_id,                        # Subject (user ID)
        "aud": ["https://api.yourdomain.com"], # Audience
        "exp": now + timedelta(minutes=15),    # Expiration (short-lived)
        "nbf": now,                             # Not before
        "iat": now,                             # Issued at
        "jti": secrets.token_urlsafe(16),      # JWT ID (unique token identifier)

        # Custom claims
        "roles": roles,
        "type": "access",
    }

    # Add tenant context for multi-tenant applications
    if tenant_id:
        payload["tenant_id"] = tenant_id

    # Add any custom claims
    if custom_claims:
        payload.update(custom_claims)

    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

def verify_secure_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience=["https://api.yourdomain.com"],
            issuer="https://api.yourdomain.com",
            options={
                'verify_exp': True,
                'verify_nbf': True,
                'verify_iat': True,
                'verify_aud': True,
                'verify_iss': True,
                'require_exp': True,
                'require_iat': True,
                'require_nbf': True
            }
        )

        # Validate token type
        if payload.get('type') != 'access':
            raise HTTPException(status_code=401, detail="Invalid token type")

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
```

#### Token Revocation with Blacklist
```python
class TokenBlacklist:
    """Redis-based token blacklist for revoked tokens"""

    def __init__(self, redis_client):
        self.redis = redis_client

    async def revoke_token(self, jti: str, exp: int):
        """Add token to blacklist until expiration"""
        ttl = exp - int(datetime.utcnow().timestamp())
        if ttl > 0:
            await self.redis.set(f"blacklist:{jti}", "1", ex=ttl)

    async def is_revoked(self, jti: str) -> bool:
        """Check if token is blacklisted"""
        return await self.redis.exists(f"blacklist:{jti}")

# Global blacklist instance
token_blacklist = TokenBlacklist(redis)

async def get_current_user_with_revocation_check(
    token: str = Depends(oauth2_scheme)
) -> User:
    payload = verify_secure_token(token)

    # Check if token has been revoked
    if await token_blacklist.is_revoked(payload['jti']):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    user = await get_user(payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

@app.post("/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    payload = verify_secure_token(token)
    await token_blacklist.revoke_token(payload['jti'], payload['exp'])
    return {"message": "Logged out successfully"}
```

## Security Analysis with Extended Thinking

When reviewing authentication flows, use extended thinking for comprehensive security analysis.

### Authentication Flow Security Review Template

```markdown
## Authentication Flow Security Review

**Flow**: [Login/OAuth/SSO/API Authentication]
**Date**: [YYYY-MM-DD]
**Reviewer**: [Name/Agent]

### Flow Diagram
[Document the authentication flow step-by-step]

### Security Analysis Checklist

#### Confidentiality
- [ ] Credentials transmitted over HTTPS only
- [ ] Passwords hashed with strong algorithm (bcrypt/argon2)
- [ ] Tokens encrypted in transit
- [ ] Sensitive data not logged
- [ ] Secrets stored securely (env vars, secrets manager)

#### Integrity
- [ ] CSRF protection implemented
- [ ] Request tampering prevented
- [ ] Token signature validation
- [ ] State parameter validated (OAuth)
- [ ] Nonce validated (OIDC)

#### Availability
- [ ] Rate limiting on auth endpoints
- [ ] Account lockout after failed attempts
- [ ] DDoS protection in place
- [ ] Graceful degradation strategy
- [ ] Session timeout configured

#### Authentication
- [ ] MFA available for sensitive accounts
- [ ] Password complexity requirements
- [ ] Credential stuffing protection
- [ ] Brute force mitigation
- [ ] Session fixation prevention

#### Authorization
- [ ] Principle of least privilege
- [ ] Role-based access control
- [ ] Permission checks on every request
- [ ] Token scope validation
- [ ] Tenant isolation (multi-tenant apps)

#### Session Management
- [ ] Secure session tokens
- [ ] HttpOnly, Secure, SameSite cookies
- [ ] Session timeout implemented
- [ ] Logout functionality
- [ ] Concurrent session handling

### Extended Thinking Analysis

Use Claude with extended thinking for deep security review:

```python
import anthropic

client = anthropic.Anthropic()

security_review_prompt = """
Perform a comprehensive security analysis of this authentication flow:

[Paste authentication code/flow description]

Analyze for:
1. OWASP Top 10 vulnerabilities
2. Authentication bypass possibilities
3. Token security weaknesses
4. Session management issues
5. Input validation gaps
6. Race conditions
7. Logic flaws

Provide specific findings with:
- Severity (Critical/High/Medium/Low)
- Location (file:line)
- Attack vector
- Remediation steps
"""

response = client.messages.create(
    model="claude-opus-4-5-20250514",
    max_tokens=32000,
    thinking={
        "type": "enabled",
        "budget_tokens": 20000  # High budget for security analysis
    },
    messages=[{
        "role": "user",
        "content": security_review_prompt
    }]
)

# Extract thinking and analysis
for block in response.content:
    if block.type == "thinking":
        print(f"Deep Analysis:\n{block.thinking}\n")
    elif block.type == "text":
        print(f"Findings:\n{block.text}")
```

## Threat Modeling for Authentication

### STRIDE Threat Model for Auth Systems

Adapted from [[deep-analysis]] skill threat modeling template:

```markdown
## Authentication Threat Model

### System: [Auth System Name]
**Version**: 1.0
**Last Updated**: [Date]

### Trust Boundaries

```
┌─────────────────────────────────────────┐
│         External (Untrusted)            │
│    [End Users] [Credential Stuffers]    │
│         [MITM Attackers]                │
└──────────────────┬──────────────────────┘
                   │ TLS/HTTPS
┌──────────────────┴──────────────────────┐
│         Public API (Semi-trusted)       │
│   [API Gateway] [Auth Endpoints]        │
│   [OAuth Providers] [OIDC IdP]          │
└──────────────────┬──────────────────────┘
                   │ Internal Auth
┌──────────────────┴──────────────────────┐
│        Application Layer (Trusted)      │
│   [Business Logic] [User Management]    │
└──────────────────┬──────────────────────┘
                   │ DB Protocol
┌──────────────────┴──────────────────────┐
│        Data Layer (Highly Trusted)      │
│   [User DB] [Session Store] [Secrets]   │
└─────────────────────────────────────────┘
```

### STRIDE Analysis

#### Spoofing Identity
| Threat | Likelihood | Impact | Mitigation | Status |
|--------|------------|--------|------------|--------|
| Credential theft via phishing | High | Critical | MFA, user education | ✅ |
| Session hijacking | Medium | High | Secure cookies, HTTPS | ✅ |
| Token replay attacks | Medium | High | Short token lifetime, JTI tracking | ✅ |
| OAuth state manipulation | Low | Medium | Cryptographic state validation | ✅ |
| Impersonation via stolen refresh token | Medium | Critical | Refresh token rotation, device binding | ⚠️ |

#### Tampering with Data
| Threat | Likelihood | Impact | Mitigation | Status |
|--------|------------|--------|------------|--------|
| JWT payload manipulation | Low | Critical | Signature verification, RS256 | ✅ |
| Cookie tampering | Low | High | Signed cookies, HMAC validation | ✅ |
| OAuth callback manipulation | Medium | High | Redirect URI validation | ✅ |
| Password reset token tampering | Low | High | Cryptographic tokens, time limits | ✅ |

#### Repudiation
| Threat | Likelihood | Impact | Mitigation | Status |
|--------|------------|--------|------------|--------|
| Deny unauthorized access | Medium | Medium | Comprehensive audit logging | ✅ |
| Dispute authentication events | Low | Low | Immutable audit trail, timestamps | ✅ |

#### Information Disclosure
| Threat | Likelihood | Impact | Mitigation | Status |
|--------|------------|--------|------------|--------|
| Credentials in logs | Medium | Critical | Sanitize logs, secret detection | ✅ |
| User enumeration via login | High | Medium | Generic error messages | ⚠️ |
| Token leakage in URLs | Low | High | Tokens in headers only | ✅ |
| Timing attacks on password check | Medium | Medium | Constant-time comparison | ✅ |
| JWKS endpoint information leak | Low | Low | Rate limiting, monitoring | ✅ |

#### Denial of Service
| Threat | Likelihood | Impact | Mitigation | Status |
|--------|------------|--------|------------|--------|
| Brute force attacks | High | High | Rate limiting, CAPTCHA, account lockout | ✅ |
| Resource exhaustion (bcrypt) | Medium | Medium | Request throttling, async processing | ✅ |
| Session store exhaustion | Low | High | Session limits per user, TTL | ✅ |
| OAuth callback flooding | Medium | Medium | State validation, rate limiting | ⚠️ |

#### Elevation of Privilege
| Threat | Likelihood | Impact | Mitigation | Status |
|--------|------------|--------|------------|--------|
| Role manipulation in JWT | Low | Critical | Server-side role verification | ✅ |
| Privilege escalation via API | Medium | Critical | Permission checks on every request | ✅ |
| Admin impersonation | Low | Critical | Additional auth for admin actions | ⚠️ |
| OAuth scope escalation | Low | High | Strict scope validation | ✅ |

### Risk Matrix
| Threat ID | Threat | Likelihood | Impact | Risk Score | Priority |
|-----------|--------|------------|--------|------------|----------|
| T1 | Credential stuffing attack | High | Critical | 9 | P0 |
| T2 | Refresh token theft | Medium | Critical | 8 | P1 |
| T3 | User enumeration | High | Medium | 6 | P2 |
| T4 | OAuth callback flooding | Medium | Medium | 4 | P2 |
| T5 | Admin impersonation | Low | Critical | 7 | P1 |

### Attack Scenarios

#### Scenario 1: Credential Stuffing Attack
**Attacker Goal**: Gain unauthorized access using leaked credentials

**Attack Steps**:
1. Obtain credential database from breach
2. Automate login attempts across accounts
3. Bypass rate limiting with distributed IPs
4. Identify valid credentials
5. Access user accounts

**Defenses**:
- Rate limiting per IP and per account
- CAPTCHA after N failed attempts
- Anomaly detection (impossible travel, new device)
- Breach database monitoring (HaveIBeenPwned)
- Mandatory MFA for sensitive accounts

#### Scenario 2: Token Theft via XSS
**Attacker Goal**: Steal access token to impersonate user

**Attack Steps**:
1. Inject malicious script via vulnerable input
2. Script reads token from localStorage
3. Exfiltrate token to attacker server
4. Use token to access API as victim

**Defenses**:
- Store tokens in HttpOnly cookies (not accessible to JS)
- Content Security Policy (CSP)
- Input sanitization and validation
- Regular security audits
- Short token lifetimes

### Recommendations by Priority

#### P0 (Critical - Immediate Action)
1. Implement credential stuffing protection
2. Add device fingerprinting for anomaly detection
3. Enable MFA for all admin accounts

#### P1 (High - Within Sprint)
1. Implement refresh token rotation
2. Add additional auth step for admin impersonation
3. Strengthen OAuth callback validation

#### P2 (Medium - Next Quarter)
1. Improve user enumeration protection
2. Implement risk-based authentication
3. Add behavioral biometrics
```

## Common Vulnerabilities & Mitigations

### OWASP Top 10 for Authentication

#### A01: Broken Access Control
```python
# VULNERABLE: Client-side role check only
@app.get("/admin/users")
async def get_users(user: User = Depends(get_current_user)):
    # No server-side permission check!
    return await db.users.find_all()

# SECURE: Server-side permission enforcement
@app.get("/admin/users")
async def get_users(user: User = Depends(require_permission(Permission.ADMIN))):
    # Permission verified on server
    return await db.users.find_all()
```

#### A02: Cryptographic Failures
```python
# VULNERABLE: Weak hashing
hashed = hashlib.md5(password.encode()).hexdigest()

# SECURE: Strong adaptive hashing
from passlib.context import CryptContext
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Adjust based on security/performance needs
)
hashed = pwd_context.hash(password)
```

#### A03: Injection
```python
# VULNERABLE: SQL injection in auth query
query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"

# SECURE: Parameterized queries
query = "SELECT * FROM users WHERE email = $1"
user = await db.fetch_one(query, email)
if user and pwd_context.verify(password, user.hashed_password):
    return user
```

#### A07: Identification and Authentication Failures
```python
# VULNERABLE: Weak session management
session_id = hashlib.md5(str(time.time()).encode()).hexdigest()

# SECURE: Cryptographically secure session tokens
import secrets
session_id = secrets.token_urlsafe(32)

# VULNERABLE: No rate limiting
@app.post("/auth/login")
async def login(credentials: LoginRequest):
    return await authenticate(credentials)

# SECURE: Rate limiting with slowdown
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")  # 5 attempts per minute
async def login(request: Request, credentials: LoginRequest):
    return await authenticate(credentials)
```

## Integration with Keycloak

For enterprise-grade auth, integrate with Keycloak (see [[keycloak]] skill):

```python
from keycloak import KeycloakOpenID

# Configure Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/",
    client_id="your-client",
    realm_name="your-realm",
    client_secret_key="your-secret"
)

# Get token
token = keycloak_openid.token(username, password)

# Validate token
token_info = keycloak_openid.introspect(token['access_token'])

# Get user info
user_info = keycloak_openid.userinfo(token['access_token'])

# Decode and verify token locally
KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + \
    keycloak_openid.public_key() + \
    "\n-----END PUBLIC KEY-----"

options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
token_info = keycloak_openid.decode_token(
    token['access_token'],
    key=KEYCLOAK_PUBLIC_KEY,
    options=options
)
```

## Related Skills & Resources

### Skills
- [[keycloak]] - Enterprise identity and access management
- [[deep-analysis]] - Security audit templates and threat modeling
- [[extended-thinking]] - Enable deep reasoning for security analysis
- [[complex-reasoning]] - Hypothesis-driven debugging for auth issues

### Keycloak Agents
- **keycloak-realm-admin** - Realm and client management
- **keycloak-security-auditor** - Security review and compliance
- **keycloak-auth-flow-designer** - Custom authentication flows
- **keycloak-identity-specialist** - Federation and SSO setup

### External Resources
- [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [JWT Best Practices RFC 8725](https://datatracker.ietf.org/doc/html/rfc8725)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)

## Troubleshooting

### Common Issues

#### Token Verification Failures
```bash
# Debug JWT token
python -c "import jwt; print(jwt.decode('YOUR_TOKEN', options={'verify_signature': False}))"

# Verify token signature
openssl dgst -sha256 -verify public_key.pem -signature signature.bin token_payload.txt

# Check token expiration
date -d @$(python -c "import jwt; print(jwt.decode('YOUR_TOKEN', options={'verify_signature': False})['exp'])")
```

#### OAuth Flow Issues
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Log OAuth flow steps
logger.debug(f"Redirect URI: {redirect_uri}")
logger.debug(f"State: {state}")
logger.debug(f"Code: {code}")
logger.debug(f"Token response: {token_response}")
```

#### Session Issues
```bash
# Check Redis session data
redis-cli
> KEYS session:*
> HGETALL session:abc123
> TTL session:abc123
```

---

_Last Updated: 2025-12-12_
_Version: 2.0.0_
_Enhanced with security analysis, threat modeling, and OIDC/OAuth 2.0 best practices_
