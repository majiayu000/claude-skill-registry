---
name: oauth
description: OAuth 2.0 and OpenID Connect implementation patterns. Use when implementing authentication, authorization flows, or integrating with OAuth providers like Google, GitHub, or custom identity providers.
user-invocable: false
---

# OAuth Skill

This skill provides guidance for OAuth 2.0 and OpenID Connect implementations.

## OAuth 2.0 Flows

### Authorization Code Flow (Recommended for web apps)
```
1. User → App: Click "Login with Google"
2. App → Auth Server: Redirect with client_id, redirect_uri, scope
3. User → Auth Server: Authenticate and consent
4. Auth Server → App: Redirect with authorization code
5. App → Auth Server: Exchange code for tokens
6. Auth Server → App: Access token + refresh token
```

### PKCE Extension (Required for SPAs/mobile)
```python
# Generate code verifier and challenge
code_verifier = secrets.token_urlsafe(32)
code_challenge = base64url(sha256(code_verifier))

# Include in authorization request
params = {
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
}
```

## Token Management

```python
@dataclass
class TokenSet:
    access_token: str
    refresh_token: str
    expires_at: datetime
    token_type: str = "Bearer"

async def refresh_tokens(refresh_token: str) -> TokenSet:
    # Exchange refresh token for new access token
    pass
```

## Security Best Practices

1. **Always use HTTPS**
2. **Use PKCE for public clients**
3. **Validate redirect URIs strictly**
4. **Store tokens securely** (HttpOnly cookies or secure storage)
5. **Implement token rotation**
6. **Set appropriate scopes** (principle of least privilege)

## OpenID Connect

Extends OAuth 2.0 with identity:

```python
# ID token contains user identity claims
claims = {
    "sub": "user123",        # Subject (unique user ID)
    "email": "user@example.com",
    "name": "John Doe",
    "iat": 1234567890,       # Issued at
    "exp": 1234567890,       # Expiration
}
```

## Implementation Checklist

- [ ] Use authorization code flow with PKCE
- [ ] Validate state parameter against CSRF
- [ ] Verify ID token signature
- [ ] Check token expiration
- [ ] Implement secure token storage
- [ ] Handle token refresh gracefully
