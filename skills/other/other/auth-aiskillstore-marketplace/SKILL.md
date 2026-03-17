---
name: auth
description: Modern authentication and security patterns for web applications. Expert in JWT tokens, OAuth2 flows, session management, RBAC, MFA, API security, and zero-trust architectures. Framework-agnostic patterns that work with any tech stack.
license: MIT
---

# Authentication & Security Patterns

This skill provides comprehensive authentication and security patterns for modern web applications in 2025, focusing on JWT tokens, OAuth2, multi-factor authentication, and zero-trust security principles that work across different frameworks and databases.

## When to Use This Skill

Use this skill when you need to:
- Implement secure authentication with JWT tokens
- Set up OAuth2 social login providers
- Implement role-based access control (RBAC)
- Add multi-factor authentication (MFA)
- Secure API endpoints with proper middleware
- Handle session management and token refresh
- Implement zero-trust security patterns
- Set up WebSocket authentication
- Create audit trails and security logging

## Modern Authentication Architecture

### 1. JWT Token Management with Refresh Tokens

```python
# core/auth.py
import jwt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

class TokenManager:
    """JWT token management with security best practices"""

    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", self._generate_secret())
        self.algorithm = "HS256"
        self.access_token_expire = timedelta(minutes=15)
        self.refresh_token_expire = timedelta(days=7)
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=120000
        )

    def _generate_secret(self) -> str:
        """Generate cryptographically secure secret"""
        return secrets.token_urlsafe(32)

    def create_password_hash(self, password: str) -> str:
        """Create secure password hash"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + self.access_token_expire

        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access",
            "jti": secrets.token_urlsafe(16)  # JWT ID
        })

        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        return encoded_jwt

    def create_refresh_token(
        self,
        user_id: str,
        device_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create secure refresh token with device binding"""
        jti = secrets.token_urlsafe(32)

        token_data = {
            "sub": user_id,
            "jti": jti,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + self.refresh_token_expire,
            "type": "refresh",
            "device": device_info or {}
        }

        # Store refresh token in database or cache
        refresh_token = jwt.encode(
            token_data,
            self.secret_key,
            algorithm=self.algorithm
        )

        # Store token hash for revocation checking
        token_hash = self._hash_token(refresh_token)

        return {
            "token": refresh_token,
            "jti": jti,
            "expires_at": token_data["exp"],
            "token_hash": token_hash
        }

    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": True}
            )

            if payload.get("type") != token_type:
                raise ValueError("Invalid token type")

            return payload

        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.JWTError:
            raise ValueError("Invalid token")

    def revoke_token(self, jti: str):
        """Revoke a token (add to blacklist)"""
        # Implement token blacklisting (Redis or database)
        pass

    def _hash_token(self, token: str) -> str:
        """Hash token for storage"""
        return self.pwd_context.hash(token)

# Singleton instance
token_manager = TokenManager()
```

### 2. OAuth2 Provider Integration

```python
# core/oauth.py
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import httpx
from urllib.parse import urlencode, parse_qs

class OAuth2Provider(ABC):
    """Base OAuth2 provider implementation"""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: list
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes

    @abstractmethod
    def get_authorization_url(self, state: str) -> str:
        """Get OAuth2 authorization URL"""
        pass

    @abstractmethod
    async def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        pass

    @abstractmethod
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from provider"""
        pass

class GoogleOAuth2Provider(OAuth2Provider):
    """Google OAuth2 provider implementation"""

    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    def get_authorization_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "state": state,
            "access_type": "offline",  # For refresh tokens
            "prompt": "consent"
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri
            }

            response = await client.post(self.TOKEN_URL, data=data)
            response.raise_for_status()

            return response.json()

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get(
                self.USER_INFO_URL,
                headers=headers
            )
            response.raise_for_status()
            return response.json()

class GitHubOAuth2Provider(OAuth2Provider):
    """GitHub OAuth2 provider implementation"""

    AUTH_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_INFO_URL = "https://api.github.com/user"

    def get_authorization_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "state": state
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            headers = {"Accept": "application/json"}
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code"
            }

            response = await client.post(
                self.TOKEN_URL,
                headers=headers,
                data=data
            )
            response.raise_for_status()

            return response.json()

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"token {access_token}",
                "User-Agent": "MyApp"
            }
            response = await client.get(
                self.USER_INFO_URL,
                headers=headers
            )
            response.raise_for_status()
            return response.json()

# Factory for creating OAuth2 providers
def create_oauth2_provider(
    provider: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    scopes: list
) -> OAuth2Provider:
    """Factory method to create OAuth2 provider"""
    providers = {
        "google": GoogleOAuth2Provider,
        "github": GitHubOAuth2Provider,
        # Add more providers as needed
    }

    provider_class = providers.get(provider.lower())
    if not provider_class:
        raise ValueError(f"Unsupported OAuth2 provider: {provider}")

    return provider_class(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scopes=scopes
    )
```

### 3. Role-Based Access Control (RBAC)

```python
# core/rbac.py
from enum import Enum
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
from functools import wraps
import inspect

class Permission(str, Enum):
    """Permission identifiers"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    CREATE = "create"
    UPDATE = "update"
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    VIEW_AUDIT_LOGS = "view_audit_logs"

class Role(str, Enum):
    """User roles"""
    ANONYMOUS = "anonymous"
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

@dataclass
class RolePermission:
    """Role to permissions mapping"""
    role: Role
    permissions: Set[Permission]

class RBACManager:
    """Role-Based Access Control Manager"""

    def __init__(self):
        self._role_permissions = self._initialize_roles()
        self._user_roles: Dict[str, Set[Role]] = {}

    def _initialize_roles(self) -> Dict[Role, Set[Permission]]:
        """Initialize default roles and permissions"""
        return {
            Role.ANONYMOUS: {Permission.READ},
            Role.USER: {
                Permission.READ,
                Permission.WRITE,
                Permission.CREATE,
                Permission.UPDATE,
                Permission.DELETE  # Own resources
            },
            Role.MODERATOR: {
                Permission.READ,
                Permission.WRITE,
                Permission.CREATE,
                Permission.UPDATE,
                Permission.DELETE,
                Permission.MANAGE_ROLES
            },
            Role.ADMIN: {
                Permission.READ,
                Permission.WRITE,
                Permission.CREATE,
                Permission.UPDATE,
                Permission.DELETE,
                Permission.MANAGE_USERS,
                Permission.MANAGE_ROLES,
                Permission.VIEW_AUDIT_LOGS
            },
            Role.SUPER_ADMIN: {
                Permission.ADMIN,  # All admin permissions
                # Add super admin specific permissions if needed
            }
        }

    def assign_role_to_user(self, user_id: str, role: Role):
        """Assign role to user"""
        if user_id not in self._user_roles:
            self._user_roles[user_id] = set()
        self._user_roles[user_id].add(role)

    def remove_role_from_user(self, user_id: str, role: Role):
        """Remove role from user"""
        if user_id in self._user_roles:
            self._user_roles[user_id].discard(role)

    def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """Get all permissions for a user based on their roles"""
        permissions = set()
        roles = self._user_roles.get(user_id, {Role.ANONYMOUS})

        for role in roles:
            role_perms = self._role_permissions.get(role, set())
            permissions.update(role_perms)

        return permissions

    def has_permission(
        self,
        user_id: str,
        permission: Permission,
        resource_owner_id: Optional[str] = None
    ) -> bool:
        """Check if user has permission"""
        permissions = self.get_user_permissions(user_id)

        # Super admin has all permissions
        if Permission.ADMIN in permissions:
            return True

        # Check resource ownership for non-admin permissions
        if permission in {Permission.READ, Permission.WRITE, Permission.DELETE}:
            if resource_owner_id and user_id == resource_owner_id:
                return True

        return permission in permissions

# Decorator for checking permissions
def requires_permission(permission: Permission, resource_owner_param: Optional[str] = None):
    """Decorator to check if user has required permission"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get current user from session or token
            current_user_id = kwargs.get("current_user_id")
            if not current_user_id:
                raise PermissionError("Authentication required")

            # Get resource owner ID if specified
            resource_owner_id = None
            if resource_owner_param:
                resource_owner_id = kwargs.get(resource_owner_param)

            # Check permission
            rbac = RBACManager()
            if not rbac.has_permission(
                current_user_id,
                permission,
                resource_owner_id
            ):
                raise PermissionError(
                    f"Permission denied. Requires: {permission.value}"
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage example
@requires_permission(Permission.DELETE, "user_id")
async def delete_user(user_id: str, current_user_id: str):
    """Delete user (only owner or admin)"""
    # Implementation here
    pass
```

### 4. Multi-Factor Authentication (MFA)

```python
# core/mfa.py
import pyotp
import qrcode
import io
import base64
from typing import Optional
from fastapi import HTTPException
from enum import Enum

class MFAMethod(str, Enum):
    TOTP = "totp"
    SMS = "sms"
    EMAIL = "email"
    PUSH = "push"

class MFAService:
    """Multi-Factor Authentication service"""

    def __init__(self):
        self.totp_window = 1  # 30-second window tolerance

    def generate_totp_secret(self) -> str:
        """Generate new TOTP secret for user"""
        return pyotp.random_base32()

    def generate_qr_code(self, user_email: str, secret: str) -> str:
        """Generate QR code for TOTP setup"""
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name="MyApp"
        )

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{img_str}"

    def verify_totp(self, secret: str, token: str) -> bool:
        """Verify TOTP token"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=self.totp_window)

    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """Generate backup codes for MFA recovery"""
        codes = []
        for _ in range(count):
            code = f"{secrets.randbelow(10**6):06d}"
            codes.append(code)
        return codes

    def verify_backup_code(
        self,
        provided_code: str,
        backup_codes: List[str]
    ) -> bool:
        """Verify backup code and remove it if valid"""
        if provided_code in backup_codes:
            backup_codes.remove(provided_code)
            return True
        return False

    async def send_sms_code(self, phone_number: str, code: str):
        """Send SMS verification code (using SMS service)"""
        # Implementation depends on SMS service
        # Example with Twilio:
        # twilio_client.messages.create(
        #     body=f"Your verification code is: {code}",
        #     from_="+1234567890",
        #     to=phone_number
        # )
        pass

    async def send_email_code(self, email: str, code: str):
        """Send email verification code"""
        # Implementation depends on email service
        # Example with SendGrid:
        # sendgrid_client.send(
        #     from_email="noreply@myapp.com",
        #     to=email,
        #     subject="Verification Code",
        #     html_content=f"Your code is: {code}"
        # )
        pass
```

### 5. Security Middleware

```python
# middleware/security.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://api.example.com; "
            "frame-ancestors 'none'"
        )

        # Remove server information
        response.headers.pop("Server", None)
        response.headers.pop("X-Powered-By", None)

        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""

    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = {}

    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Clean old entries
        self.clients = {
            ip: times for ip, times in self.clients.items()
            if current_time - max(times) < self.period
        }

        # Check rate limit
        if client_ip in self.clients:
            recent_calls = [
                t for t in self.clients[client_ip]
                if current_time - t < self.period
            ]
            if len(recent_calls) >= self.calls:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded"
                )
            self.clients[client_ip] = recent_calls + [current_time]
        else:
            self.clients[client_ip] = [current_time]

        return await call_next(request)

class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """Audit logging middleware"""

    def __init__(self, app, sensitive_fields: list = None):
        super().__init__(app)
        self.sensitive_fields = sensitive_fields or [
            "password", "token", "secret", "key"
        ]

    async def dispatch(self, request, call_next):
        start_time = time.time()

        # Log request
        request_data = {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client_ip": request.client.host
        }

        # Remove sensitive information
        self._remove_sensitive_data(request_data)

        logger.info(f"Request: {request_data}")

        try:
            response = await call_next(request)

            # Log response
            duration = time.time() - start_time
            response_data = {
                "status_code": response.status_code,
                "duration": f"{duration:.3f}s"
            }

            logger.info(f"Response: {response_data}")

            return response
        except Exception as e:
            logger.error(f"Error: {str(e)}", exc_info=True)
            raise

    def _remove_sensitive_data(self, data: dict):
        """Remove sensitive data from logs"""
        if isinstance(data, dict):
            for key in self.sensitive_fields:
                if key in data:
                    data[key] = "[REDACTED]"
            for value in data.values():
                if isinstance(value, dict):
                    self._remove_sensitive_data(value)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    self._remove_sensitive_data(item)
```

### 6. Zero-Trust Security Patterns

```python
# core/zero_trust.py
from typing import Optional, Dict, Any, List
import ipaddress
from datetime import datetime, timedelta

class ZeroTrustManager:
    """Zero-trust security manager"""

    def __init__(self):
        self.trusted_networks = self._load_trusted_networks()
        self.device_policies = self._load_device_policies()

    def validate_access_request(
        self,
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate access request with zero-trust principles"""

        validation_result = {
            "allowed": False,
            "risk_score": 0,
            "factors": []
        }

        # Factor 1: Device Trust
        device_trust = self._validate_device(request_data)
        validation_result["factors"].append(device_trust)

        # Factor 2: Network Trust
        network_trust = self._validate_network(request_data)
        validation_result["factors"].append(network_trust)

        # Factor 3: Behavioral Analysis
        behavior_trust = self._analyze_behavior(request_data)
        validation_result["factors"].append(behavior_trust)

        # Factor 4: Time-based Anomaly Detection
        time_trust = self._validate_timing(request_data)
        validation_result["factors"].append(time_trust)

        # Calculate overall risk score
        validation_result["risk_score"] = sum(
            factor["risk"] for factor in validation_result["factors"]
        )

        # Determine if access is allowed
        validation_result["allowed"] = (
            validation_result["risk_score"] < 50 and
            all(factor["trusted"] for factor in validation_result["factors"])
        )

        return validation_result

    def _validate_device(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate device trust"""
        device_id = request_data.get("device_id")
        user_agent = request_data.get("user_agent")

        if not device_id:
            return {"trusted": False, "risk": 30, "reason": "No device ID"}

        # Check if device is known and trusted
        # Implementation depends on your device management system
        device_trusted = self._is_device_trusted(device_id, user_agent)

        return {
            "trusted": device_trusted,
            "risk": 0 if device_trusted else 20,
            "reason": "Unknown device"
        }

    def _validate_network(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate network trust"""
        client_ip = request_data.get("client_ip")

        try:
            ip_obj = ipaddress.ip_address(client_ip)
        except ValueError:
            return {"trusted": False, "risk": 40, "reason": "Invalid IP"}

        # Check if IP is in trusted networks
        for trusted_network in self.trusted_networks:
            if ip_obj in trusted_network:
                return {"trusted": True, "risk": 0, "reason": "Trusted network"}

        # Check if it's a private network
        if ip_obj.is_private:
            return {"trusted": True, "risk": 5, "reason": "Private network"}

        return {"trusted": False, "risk": 15, "reason": "Untrusted network"}

    def _analyze_behavior(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user behavior for anomalies"""
        user_id = request_data.get("user_id")
        location = request_data.get("location")
        timestamp = request_data.get("timestamp", datetime.utcnow())

        # Check for anomalies (same user from different locations)
        # Implementation would involve storing and analyzing user patterns
        anomalies = self._detect_behavioral_anomalies(user_id, location, timestamp)

        return {
            "trusted": len(anomalies) == 0,
            "risk": min(len(anomalies) * 10, 30),
            "reason": f"Anomalies detected: {anomalies}"
        }

    def _validate_timing(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate request timing"""
        timestamp = request_data.get("timestamp", datetime.utcnow())

        # Check for off-hours access
        hour = timestamp.hour
        if hour < 6 or hour > 22:
            return {
                "trusted": True,
                "risk": 10,
                "reason": "Off-hours access"
            }

        return {"trusted": True, "risk": 0, "reason": "Normal hours"}

    def _is_device_trusted(self, device_id: str, user_agent: str) -> bool:
        """Check if device is trusted"""
        # Implementation depends on your device management system
        # This could check against a database of registered devices
        return True  # Placeholder

    def _detect_behavioral_anomalies(
        self,
        user_id: str,
        location: Optional[str],
        timestamp: datetime
    ) -> List[str]:
        """Detect behavioral anomalies"""
        anomalies = []

        # Implement behavioral analysis logic
        # - Same user from multiple locations
        # - Rapid sequential requests
        # - Unusual access patterns
        # - Geographic impossibilities

        return anomalies

    def _load_trusted_networks(self):
        """Load trusted network ranges"""
        return [
            ipaddress.ip_network("192.168.1.0/24"),
            ipaddress.ip_network("10.0.0.0/8"),
            ipaddress.ip_network("172.16.0.0/12"),
            # Add your trusted networks here
        ]

    def _load_device_policies(self):
        """Load device security policies"""
        return {
            "require_device_trust": True,
            "max_devices_per_user": 5,
            "session_timeout": 3600
        }
```

### 7. Production Security Checklist

```yaml
# security/production_checklist.yaml
authentication:
  jwt:
    secret_key_length: 32
    algorithm: HS256
    access_token_expiry: 15m
    refresh_token_expiry: 7d
    refresh_rotation: true

  password:
    min_length: 12
    complexity_requirements:
      - uppercase
      - lowercase
      - numbers
      - special_characters
    hash_algorithm: pbkdf2_sha256
    rounds: 120000

  mfa:
    required_for_admin: true
    optional_for_users: true
    backup_codes_count: 10

  oauth2:
    providers:
      - google
      - github
      - microsoft
    state_validation: true
    pkce: true

security:
  headers:
    strict_transport_security: true
    content_security_policy: true
    x_frame_options: deny
    x_xss_protection: true

  rate_limiting:
    default: 100/minute
    auth_endpoints: 10/minute
    admin_endpoints: 5/minute

  session_management:
    idle_timeout: 30m
    absolute_timeout: 8h
    concurrent_sessions: 3

  audit_logging:
    log_all_auth_events: true
    log_sensitive_data: false
    retention_period: 90d

  zero_trust:
    device_validation: true
    network_validation: true
    behavioral_analysis: true
    risk_scoring: true

  encryption:
    at_rest: AES-256
    in_transit: TLS-1.3
    key_rotation: 90d

  secrets_management:
    use_vault: true
    environment_variables: false
    rotation_enabled: true
```

This comprehensive authentication skill provides modern security patterns for 2025, including JWT tokens, OAuth2 integration, RBAC, MFA, zero-trust principles, and production-ready security middleware that can be implemented across any web application framework.