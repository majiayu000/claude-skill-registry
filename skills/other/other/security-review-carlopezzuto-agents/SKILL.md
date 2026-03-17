---
name: security-review
description: Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns.
---

# Security Review Skill

This skill ensures all code follows security best practices and identifies potential vulnerabilities.

## When to Activate

- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Working with secrets or credentials
- Implementing payment features
- Storing or transmitting sensitive data
- Integrating third-party APIs

## Security Checklist

### 1. Secrets Management

#### NEVER Do This

```python
api_key = "sk-proj-xxxxx"  # Hardcoded secret
db_password = "password123"  # In source code
```

#### ALWAYS Do This

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
db_url = os.environ.get("DATABASE_URL")

# Verify secrets exist
if not api_key:
    raise ValueError("OPENAI_API_KEY not configured")
```

#### Using Pydantic Settings (Recommended)

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # Raises ValidationError if missing
```

#### Verification Steps

- [ ] No hardcoded API keys, tokens, or passwords
- [ ] All secrets in environment variables
- [ ] `.env` in .gitignore
- [ ] No secrets in git history
- [ ] Production secrets in hosting platform (Railway, Render, AWS)

### 2. Input Validation

#### Always Validate User Input with Pydantic

```python
from pydantic import BaseModel, EmailStr, field_validator


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str
    age: int

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, v: str) -> str:
        if len(v) < 1 or len(v) > 100:
            raise ValueError("Name must be 1-100 characters")
        return v.strip()

    @field_validator("age")
    @classmethod
    def age_must_be_valid(cls, v: int) -> int:
        if v < 0 or v > 150:
            raise ValueError("Age must be 0-150")
        return v


# FastAPI automatically validates
@app.post("/users")
async def create_user(request: CreateUserRequest):
    return await db.users.create(request.model_dump())
```

#### File Upload Validation

```python
from pathlib import Path
from fastapi import UploadFile, HTTPException


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


async def validate_file_upload(file: UploadFile) -> bool:
    # Content type check
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(400, "Invalid file type")

    # Extension check
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Invalid file extension")

    # Size check (read content to verify)
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, f"File too large (max {MAX_FILE_SIZE // 1024 // 1024}MB)")

    # Reset file position for later use
    await file.seek(0)
    return True
```

#### Verification Steps

- [ ] All user inputs validated with Pydantic schemas
- [ ] File uploads restricted (size, type, extension)
- [ ] No direct use of user input in queries
- [ ] Whitelist validation (not blacklist)
- [ ] Error messages don't leak sensitive info

### 3. SQL Injection Prevention

#### NEVER Concatenate SQL

```python
# DANGEROUS - SQL Injection vulnerability
query = f"SELECT * FROM users WHERE email = '{user_email}'"
await db.execute(query)
```

#### ALWAYS Use Parameterized Queries

```python
# Safe - SQLAlchemy ORM
from sqlalchemy import select

stmt = select(User).where(User.email == user_email)
result = await session.execute(stmt)

# Safe - Raw parameterized query
await db.execute(
    "SELECT * FROM users WHERE email = :email",
    {"email": user_email}
)

# Safe - asyncpg
await conn.fetch("SELECT * FROM users WHERE email = $1", user_email)
```

#### Verification Steps

- [ ] All database queries use parameterized queries
- [ ] No string concatenation/f-strings in SQL
- [ ] ORM/query builder used correctly
- [ ] SQLAlchemy queries properly sanitized

### 4. Authentication & Authorization

#### JWT Token Handling

```python
from fastapi import Response
from datetime import datetime, timedelta
import jwt

# WRONG: Storing in response body (client stores in localStorage)
# Vulnerable to XSS

# CORRECT: httpOnly cookies
def set_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  # HTTPS only
        samesite="strict",
        max_age=3600,  # 1 hour
    )
```

#### Authorization Checks

```python
from fastapi import Depends, HTTPException, status

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return user


async def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: str, admin: User = Depends(require_admin)):
    await db.users.delete(user_id)
```

#### Row Level Security (PostgreSQL)

```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can only view their own data
CREATE POLICY "Users view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- Users can only update their own data
CREATE POLICY "Users update own data"
  ON users FOR UPDATE
  USING (auth.uid() = id);
```

#### Verification Steps

- [ ] Tokens stored in httpOnly cookies (not localStorage)
- [ ] Authorization checks before sensitive operations
- [ ] Row Level Security enabled if using PostgreSQL
- [ ] Role-based access control implemented
- [ ] Session management secure

### 5. XSS Prevention

#### Sanitize HTML

```python
import bleach

# ALWAYS sanitize user-provided HTML
def sanitize_html(html: str) -> str:
    return bleach.clean(
        html,
        tags=["b", "i", "em", "strong", "p", "br"],
        attributes={},
        strip=True,
    )
```

#### Content Security Policy (FastAPI)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://api.example.com"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response


app = FastAPI()
app.add_middleware(SecurityHeadersMiddleware)
```

#### Verification Steps

- [ ] User-provided HTML sanitized with bleach
- [ ] CSP headers configured
- [ ] No unvalidated dynamic content rendering
- [ ] Jinja2 auto-escaping enabled (default)

### 6. CSRF Protection

#### CSRF Tokens (FastAPI)

```python
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel


class CsrfSettings(BaseModel):
    secret_key: str = "your-secret-key"


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.post("/api/transfer")
async def transfer(csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf()
    # Process request
```

#### SameSite Cookies

```python
response.set_cookie(
    key="session",
    value=session_id,
    httponly=True,
    secure=True,
    samesite="strict",
)
```

#### Verification Steps

- [ ] CSRF tokens on state-changing operations
- [ ] SameSite=Strict on all cookies
- [ ] Double-submit cookie pattern implemented

### 7. Rate Limiting

#### API Rate Limiting (FastAPI)

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/api/endpoint")
@limiter.limit("100/15minutes")
async def endpoint(request: Request):
    return {"status": "ok"}


# Stricter limits for expensive operations
@app.get("/api/search")
@limiter.limit("10/minute")
async def search(request: Request, q: str):
    return await perform_search(q)
```

#### Verification Steps

- [ ] Rate limiting on all API endpoints
- [ ] Stricter limits on expensive operations
- [ ] IP-based rate limiting
- [ ] User-based rate limiting (authenticated)

### 8. Sensitive Data Exposure

#### Logging

```python
import structlog

logger = structlog.get_logger()

# WRONG: Logging sensitive data
logger.info("User login", email=email, password=password)
logger.info("Payment", card_number=card_number, cvv=cvv)

# CORRECT: Redact sensitive data
logger.info("User login", email=email, user_id=user_id)
logger.info("Payment", last4=card.last4, user_id=user_id)
```

#### Error Messages

```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

# WRONG: Exposing internal details
@app.get("/api/data")
async def get_data():
    try:
        return await fetch_data()
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # Leaks info!

# CORRECT: Generic error messages
@app.get("/api/data")
async def get_data():
    try:
        return await fetch_data()
    except Exception as e:
        logger.exception("Internal error fetching data")
        raise HTTPException(500, detail="An error occurred. Please try again.")
```

#### Verification Steps

- [ ] No passwords, tokens, or secrets in logs
- [ ] Error messages generic for users
- [ ] Detailed errors only in server logs
- [ ] No stack traces exposed to users

### 9. Dependency Security

#### Regular Updates

```bash
# Check for vulnerabilities
pip-audit

# Or with safety
safety check

# Update dependencies
pip install --upgrade -r requirements.txt

# Check for outdated packages
pip list --outdated
```

#### Lock Files

```bash
# ALWAYS commit lock files
git add requirements.txt  # or pyproject.toml + poetry.lock

# Use pip-compile for reproducible builds
pip-compile requirements.in -o requirements.txt

# In CI/CD
pip install -r requirements.txt --no-deps
```

#### Verification Steps

- [ ] Dependencies up to date
- [ ] No known vulnerabilities (pip-audit clean)
- [ ] Lock files committed
- [ ] Dependabot/Renovate enabled on GitHub
- [ ] Regular security updates

### 10. Path Traversal Prevention

#### NEVER Trust User Paths

```python
from pathlib import Path

# WRONG: Path traversal vulnerability
@app.get("/files/{filename}")
async def get_file(filename: str):
    return FileResponse(f"/uploads/{filename}")  # ../../../etc/passwd!

# CORRECT: Validate and resolve paths
UPLOAD_DIR = Path("/uploads").resolve()


@app.get("/files/{filename}")
async def get_file(filename: str):
    # Resolve and validate path
    file_path = (UPLOAD_DIR / filename).resolve()

    # Ensure path is within upload directory
    if not file_path.is_relative_to(UPLOAD_DIR):
        raise HTTPException(403, "Access denied")

    if not file_path.exists():
        raise HTTPException(404, "File not found")

    return FileResponse(file_path)
```

## Security Testing

### Automated Security Tests

```python
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_requires_authentication(client: AsyncClient):
    """Protected endpoints require auth."""
    response = await client.get("/api/protected")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_requires_admin_role(client: AsyncClient, user_token: str):
    """Admin endpoints require admin role."""
    response = await client.get(
        "/api/admin",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_rejects_invalid_input(client: AsyncClient):
    """Invalid input is rejected."""
    response = await client.post(
        "/api/users",
        json={"email": "not-an-email"},
    )
    assert response.status_code == 422  # Pydantic validation error


@pytest.mark.asyncio
async def test_enforces_rate_limits(client: AsyncClient):
    """Rate limiting is enforced."""
    responses = [
        await client.get("/api/endpoint")
        for _ in range(101)
    ]
    too_many_requests = [r for r in responses if r.status_code == 429]
    assert len(too_many_requests) > 0
```

## Pre-Deployment Security Checklist

Before ANY production deployment:

- [ ] **Secrets**: No hardcoded secrets, all in env vars
- [ ] **Input Validation**: All user inputs validated with Pydantic
- [ ] **SQL Injection**: All queries parameterized (SQLAlchemy/asyncpg)
- [ ] **XSS**: User content sanitized with bleach
- [ ] **CSRF**: Protection enabled
- [ ] **Authentication**: Proper token handling (httpOnly cookies)
- [ ] **Authorization**: Role checks in place
- [ ] **Rate Limiting**: Enabled on all endpoints (slowapi)
- [ ] **HTTPS**: Enforced in production
- [ ] **Security Headers**: CSP, X-Frame-Options configured
- [ ] **Error Handling**: No sensitive data in errors
- [ ] **Logging**: No sensitive data logged
- [ ] **Dependencies**: Up to date, no vulnerabilities (pip-audit)
- [ ] **Row Level Security**: Enabled if using PostgreSQL
- [ ] **CORS**: Properly configured
- [ ] **File Uploads**: Validated (size, type, path traversal)
- [ ] **Path Traversal**: All file paths validated

## Python Security Libraries

| Library             | Purpose                           |
| ------------------- | --------------------------------- |
| `pydantic`          | Input validation                  |
| `bleach`            | HTML sanitization                 |
| `python-jose`       | JWT handling                      |
| `passlib`           | Password hashing                  |
| `slowapi`           | Rate limiting                     |
| `pip-audit`         | Dependency vulnerability scanning |
| `safety`            | Dependency vulnerability scanning |
| `bandit`            | Static security analysis          |
| `python-dotenv`     | Environment variable management   |
| `pydantic-settings` | Typed settings from env vars      |

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [OWASP Python Security](https://cheatsheetseries.owasp.org/cheatsheets/Python_Security_Cheat_Sheet.html)

---

**Remember**: Security is not optional. One vulnerability can compromise the entire platform. When in doubt, err on the side of caution.
