---
name: auth-system-design
description: |
  Authentication system design and implementation guidance with Python examples using strict typing. Use when: (1) Designing authentication flows (signup, login, logout, refresh), (2) Selecting between session vs token-based auth, (3) Designing JWT structure and claims, (4) Implementing OAuth 2.0 flows, (5) Setting up multi-service authentication patterns, (6) Creating password reset and email verification flows, (7) Implementing role-based access control (RBAC), (8) Creating security checklists for auth systems, (9) Planning frontend/backend auth integration. All examples follow Python typing standards and security best practices.
---

# Authentication System Design

Design secure and scalable authentication systems following industry best practices and security standards.

## Quick Reference

### Authentication Method Selection
- **Session-based**: Traditional web apps, server-side control
- **JWT Token**: SPA/mobile/microservices, stateless
- **OAuth 2.0**: Third-party integration, standard protocols
- **OpenID Connect**: Identity + authentication

### JWT Claims Structure
- **Standard**: iss, sub, aud, exp, nbf, iat, jti
- **Custom**: userId, roles, permissions

## Decision Workflow

### 1. Choose Authentication Method
| Method | Best For | Key Considerations |
|--------|----------|-------------------|
| Session-based | Traditional web apps | Server state required |
| JWT Token | SPA, mobile, microservices | Token revocation challenges |
| OAuth 2.0 | Third-party integration | Complex setup |
| OpenID Connect | Identity verification | More complex than OAuth |

### 2. Design Authentication Flows
- **Sign Up**: Validate → Create → Verify → Login
- **Login**: Validate → Generate tokens → Redirect
- **Logout**: Invalidate → Clear → Redirect
- **Refresh**: Check expiry → Use refresh token → Retry

### 3. JWT Structure & OAuth Selection
- Use RS256 algorithm, short expiry (15-60 min)
- Authorization Code flow for web apps, PKCE for public clients

### 4. Security Validation
- Password hashing (bcrypt/Argon2)
- Rate limiting, HTTPS, token expiration
- Input validation, secure headers

## Essential Patterns

### Secure Password Handling
```python
import bcrypt
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())
```

### JWT Token Operations
```python
import jwt
from datetime import datetime, timedelta

def create_token(user_id: str, roles: list) -> str:
    payload = {
        "user_id": user_id,
        "roles": roles,
        "exp": (datetime.utcnow() + timedelta(minutes=15)).timestamp(),
        "iss": "https://your-app.com"
    }
    return jwt.encode(payload, key="secret", algorithm="RS256")
```

## Resources

| File | Purpose |
|------|---------|
| [auth-methods.md](references/auth-methods.md) | Authentication method comparison |
| [auth-flows.md](references/auth-flows.md) | Flow diagrams and implementation |
| [jwt-structure.md](references/jwt-structure.md) | JWT guidelines and examples |
| [oauth-flows.md](references/oauth-flows.md) | OAuth 2.0 patterns |
| [multi-service-auth.md](references/multi-service-auth.md) | Multi-service strategies |
| [password-reset.md](references/password-reset.md) | Secure reset implementation |
| [rbac-system.md](references/rbac-system.md) | Role-based access control |
| [security-checklist.md](references/security-checklist.md) | Security validation |
| [integration-guide.md](references/integration-guide.md) | Frontend/backend integration |
| [jwt-template.yaml](assets/jwt-template.yaml) | JWT schema template |