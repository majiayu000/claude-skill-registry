# Auth Connect Skill

## Metadata

| Field | Value |
|-------|-------|
| **Name** | auth-connect |
| **Version** | 1.0.0 |
| **Agent** | SecurityLead |
| **Created** | 2026-01-02 |

## Purpose

JWT-based authentication and authorization system for the Physical AI Educational Book FastAPI backend. Provides secure user authentication, session management, and role-based access control.

## Features

- JWT token generation and verification
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Session management
- API key generation
- Token refresh mechanism
- Secure middleware for FastAPI

## Requirements

- Python 3.9+
- FastAPI backend
- Neon Postgres database
- Environment variables configured

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize auth tables (requires DATABASE_URL)
.claude/skills/auth-connect/scripts/setup.sh --init

# Generate JWT secret
.claude/skills/auth-connect/scripts/setup.sh --generate-secret
```

## Usage

### CLI Commands

```bash
# Initialize auth system
./scripts/setup.sh --init

# Generate new JWT secret
./scripts/setup.sh --generate-secret

# Create a new user
./scripts/setup.sh --create-user --email user@example.com --role student

# List all roles
./scripts/setup.sh --list-roles

# Verify a token
./scripts/setup.sh --verify-token <token>

# Generate API key
./scripts/setup.sh --generate-api-key --name "My App"

# Show configuration
./scripts/setup.sh --show-config

# Run health check
./scripts/setup.sh --health
```

### Python Integration

```python
from auth import AuthManager, TokenPayload, verify_password, hash_password

# Initialize
auth = AuthManager()

# Hash password
hashed = hash_password("my_secure_password")

# Verify password
is_valid = verify_password("my_secure_password", hashed)

# Create access token
token = auth.create_access_token(
    user_id="user123",
    email="user@example.com",
    role="student"
)

# Verify token
payload = auth.verify_token(token)
if payload:
    print(f"User: {payload.user_id}, Role: {payload.role}")

# Create refresh token
refresh_token = auth.create_refresh_token(user_id="user123")

# Refresh access token
new_token = auth.refresh_access_token(refresh_token)
```

### FastAPI Middleware

```python
from fastapi import FastAPI, Depends, HTTPException
from auth import AuthManager, get_current_user, require_role

app = FastAPI()
auth = AuthManager()

# Protect endpoint with authentication
@app.get("/api/profile")
async def get_profile(user: TokenPayload = Depends(get_current_user)):
    return {"user_id": user.user_id, "email": user.email}

# Require specific role
@app.get("/api/admin")
async def admin_only(user: TokenPayload = Depends(require_role("admin"))):
    return {"message": "Welcome, admin!"}

# Multiple roles allowed
@app.put("/api/content")
async def edit_content(user: TokenPayload = Depends(require_role(["admin", "instructor"]))):
    return {"message": "Content updated"}
```

## Configuration

### Environment Variables

```bash
# Required
JWT_SECRET=your-256-bit-secret-key
DATABASE_URL=postgresql://user:pass@host/db

# Optional
JWT_ALGORITHM=HS256           # Default: HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30 # Default: 30
REFRESH_TOKEN_EXPIRE_DAYS=7    # Default: 7
```

### auth_config.json

```json
{
  "jwt": {
    "algorithm": "HS256",
    "access_token_expire_minutes": 30,
    "refresh_token_expire_days": 7
  },
  "password": {
    "min_length": 8,
    "require_uppercase": true,
    "require_lowercase": true,
    "require_digit": true,
    "require_special": false
  },
  "session": {
    "max_sessions_per_user": 5,
    "session_timeout_minutes": 60
  }
}
```

### roles.json

```json
{
  "roles": {
    "admin": {
      "description": "Full system access",
      "permissions": ["read", "write", "delete", "manage_users", "manage_content"]
    },
    "instructor": {
      "description": "Content creator and manager",
      "permissions": ["read", "write", "manage_content"]
    },
    "student": {
      "description": "Standard learner access",
      "permissions": ["read", "chat", "save_progress"]
    },
    "guest": {
      "description": "Limited read-only access",
      "permissions": ["read"]
    }
  }
}
```

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sessions table
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    refresh_token VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT
);

-- API Keys table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    prefix VARCHAR(10) NOT NULL,
    permissions JSONB DEFAULT '["read"]',
    is_active BOOLEAN DEFAULT true,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_refresh_token ON sessions(refresh_token);
CREATE INDEX idx_api_keys_prefix ON api_keys(prefix);
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Request                            │
│                    (with Authorization header)                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Middleware                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  Auth Middleware                           │  │
│  │  1. Extract token from Authorization header               │  │
│  │  2. Verify JWT signature                                  │  │
│  │  3. Check token expiration                                │  │
│  │  4. Validate user role/permissions                        │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
┌───────────────────────┐   ┌───────────────────────┐
│   Valid Token         │   │   Invalid Token       │
│   → Process Request   │   │   → 401 Unauthorized  │
└───────────────────────┘   └───────────────────────┘
```

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/auth/register` | POST | No | Register new user |
| `/api/auth/login` | POST | No | Login and get tokens |
| `/api/auth/logout` | POST | Yes | Invalidate session |
| `/api/auth/refresh` | POST | No | Refresh access token |
| `/api/auth/me` | GET | Yes | Get current user |
| `/api/auth/change-password` | PUT | Yes | Change password |

## Error Codes

| Code | Error | Description |
|------|-------|-------------|
| 401 | `INVALID_TOKEN` | Token is invalid or malformed |
| 401 | `TOKEN_EXPIRED` | Token has expired |
| 401 | `INVALID_CREDENTIALS` | Wrong email or password |
| 403 | `INSUFFICIENT_PERMISSIONS` | User lacks required role |
| 409 | `USER_EXISTS` | Email already registered |
| 422 | `WEAK_PASSWORD` | Password doesn't meet requirements |

## Testing

```bash
# Run all tests
./scripts/test.sh

# Run Python unit tests only
python scripts/test_auth.py
```

## Files

```
auth-connect/
├── SKILL.md              # This documentation
├── requirements.txt      # Python dependencies
├── assets/
│   ├── auth_config.json  # Auth configuration
│   └── roles.json        # Role definitions
└── scripts/
    ├── setup.sh          # CLI entry point
    ├── auth.py           # Main auth module
    ├── test.sh           # Bash test runner
    └── test_auth.py      # Python unit tests
```

## Changelog

### v1.0.0 (2026-01-02)
- Initial release
- JWT authentication
- Password hashing with bcrypt
- Role-based access control
- Session management
- API key generation
- FastAPI middleware integration
