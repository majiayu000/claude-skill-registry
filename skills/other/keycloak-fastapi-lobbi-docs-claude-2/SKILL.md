---
name: Keycloak FastAPI Integration
description: This skill should be used when the user asks to "add Keycloak authentication", "implement OIDC", "configure SSO", "validate JWT token", "add role-based access", "protect API endpoint", or mentions Keycloak, OAuth2, OpenID Connect, identity provider, or authentication in FastAPI. Provides Keycloak/OIDC integration patterns.
version: 0.1.0
---

# Keycloak Integration for FastAPI

This skill provides patterns for integrating Keycloak as an identity provider with FastAPI applications using OIDC/OAuth2.

## Configuration

### Settings

```python
from pydantic_settings import BaseSettings

class KeycloakSettings(BaseSettings):
    keycloak_url: str = "https://auth.example.com"
    keycloak_realm: str = "my-realm"
    keycloak_client_id: str = "my-api"
    keycloak_client_secret: str = ""

    @property
    def openid_config_url(self) -> str:
        return f"{self.keycloak_url}/realms/{self.keycloak_realm}/.well-known/openid-configuration"

    @property
    def jwks_url(self) -> str:
        return f"{self.keycloak_url}/realms/{self.keycloak_realm}/protocol/openid-connect/certs"

    @property
    def token_url(self) -> str:
        return f"{self.keycloak_url}/realms/{self.keycloak_realm}/protocol/openid-connect/token"

    class Config:
        env_file = ".env"
```

## JWT Token Validation

### Token Validator

```python
import httpx
from jose import jwt, JWTError
from jose.jwk import construct
from functools import lru_cache
from typing import Optional, Dict, Any

class KeycloakTokenValidator:
    def __init__(self, settings: KeycloakSettings):
        self.settings = settings
        self._jwks: Optional[Dict] = None

    async def get_jwks(self) -> Dict:
        if self._jwks is None:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.settings.jwks_url)
                response.raise_for_status()
                self._jwks = response.json()
        return self._jwks

    async def validate_token(self, token: str) -> Dict[str, Any]:
        try:
            jwks = await self.get_jwks()

            # Get key ID from token header
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")

            # Find matching key
            key = None
            for jwk in jwks.get("keys", []):
                if jwk.get("kid") == kid:
                    key = jwk
                    break

            if not key:
                raise JWTError("Key not found")

            # Decode and validate
            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=self.settings.keycloak_client_id,
                issuer=f"{self.settings.keycloak_url}/realms/{self.settings.keycloak_realm}"
            )

            return payload

        except JWTError as e:
            raise ValueError(f"Invalid token: {str(e)}")
```

## FastAPI Dependencies

### Current User Dependency

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer(auto_error=False)

class TokenUser:
    def __init__(self, payload: Dict[str, Any]):
        self.sub: str = payload.get("sub", "")
        self.email: str = payload.get("email", "")
        self.name: str = payload.get("name", "")
        self.preferred_username: str = payload.get("preferred_username", "")
        self.roles: list = self._extract_roles(payload)
        self.raw_payload = payload

    def _extract_roles(self, payload: Dict) -> list:
        # Realm roles
        realm_roles = payload.get("realm_access", {}).get("roles", [])

        # Client roles
        resource_access = payload.get("resource_access", {})
        client_roles = resource_access.get(
            settings.keycloak_client_id, {}
        ).get("roles", [])

        return list(set(realm_roles + client_roles))

async def get_token_validator() -> KeycloakTokenValidator:
    return KeycloakTokenValidator(get_settings())

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    validator: KeycloakTokenValidator = Depends(get_token_validator)
) -> TokenUser:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        payload = await validator.validate_token(credentials.credentials)
        return TokenUser(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    validator: KeycloakTokenValidator = Depends(get_token_validator)
) -> Optional[TokenUser]:
    if not credentials:
        return None
    try:
        payload = await validator.validate_token(credentials.credentials)
        return TokenUser(payload)
    except ValueError:
        return None
```

### Role-Based Access Control

```python
from functools import wraps
from typing import List

def require_roles(*required_roles: str):
    """Dependency that checks for required roles."""
    async def role_checker(
        user: TokenUser = Depends(get_current_user)
    ) -> TokenUser:
        if not any(role in user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {', '.join(required_roles)}"
            )
        return user
    return role_checker

def require_all_roles(*required_roles: str):
    """Dependency that checks user has ALL required roles."""
    async def role_checker(
        user: TokenUser = Depends(get_current_user)
    ) -> TokenUser:
        missing = [r for r in required_roles if r not in user.roles]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing roles: {', '.join(missing)}"
            )
        return user
    return role_checker

# Usage in routes
@router.get("/admin/users")
async def list_users(user: TokenUser = Depends(require_roles("admin", "user-manager"))):
    """Only admins or user-managers can access."""
    return {"users": []}

@router.delete("/admin/system")
async def system_action(user: TokenUser = Depends(require_all_roles("admin", "super-admin"))):
    """Requires BOTH admin AND super-admin roles."""
    return {"status": "ok"}
```

## Protected Routes

```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1", tags=["Protected"])

@router.get("/profile")
async def get_profile(user: TokenUser = Depends(get_current_user)):
    """Get current user's profile."""
    return {
        "sub": user.sub,
        "email": user.email,
        "name": user.name,
        "roles": user.roles
    }

@router.get("/public")
async def public_endpoint():
    """Public endpoint - no auth required."""
    return {"message": "Public data"}

@router.get("/optional-auth")
async def optional_auth(user: Optional[TokenUser] = Depends(get_current_user_optional)):
    """Returns different data based on auth status."""
    if user:
        return {"message": f"Hello, {user.name}!", "authenticated": True}
    return {"message": "Hello, guest!", "authenticated": False}
```

## Token Refresh Flow

```python
import httpx
from typing import Tuple

class KeycloakAuthService:
    def __init__(self, settings: KeycloakSettings):
        self.settings = settings

    async def refresh_token(self, refresh_token: str) -> Tuple[str, str]:
        """Exchange refresh token for new access token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.settings.token_url,
                data={
                    "grant_type": "refresh_token",
                    "client_id": self.settings.keycloak_client_id,
                    "client_secret": self.settings.keycloak_client_secret,
                    "refresh_token": refresh_token
                }
            )

            if response.status_code != 200:
                raise ValueError("Failed to refresh token")

            data = response.json()
            return data["access_token"], data["refresh_token"]

    async def exchange_code(self, code: str, redirect_uri: str) -> dict:
        """Exchange authorization code for tokens."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.settings.token_url,
                data={
                    "grant_type": "authorization_code",
                    "client_id": self.settings.keycloak_client_id,
                    "client_secret": self.settings.keycloak_client_secret,
                    "code": code,
                    "redirect_uri": redirect_uri
                }
            )

            if response.status_code != 200:
                raise ValueError("Failed to exchange code")

            return response.json()
```

## Middleware for Token Refresh

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class TokenRefreshMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Check if token is about to expire (from custom header)
        token_exp = request.state.get("token_exp")
        if token_exp and token_exp - time.time() < 300:  # 5 min
            # Token expires soon - add header to signal frontend
            response.headers["X-Token-Expiring"] = "true"

        return response
```

## Additional Resources

### Reference Files

For detailed configuration and advanced patterns:
- **`references/keycloak-setup.md`** - Keycloak realm/client configuration
- **`references/multi-tenant.md`** - Multi-tenant authentication patterns
- **`references/testing.md`** - Testing authenticated endpoints

### Example Files

Working examples in `examples/`:
- **`examples/auth_dependencies.py`** - Complete auth dependencies
- **`examples/protected_router.py`** - Protected route examples
- **`examples/keycloak_service.py`** - Full Keycloak service
