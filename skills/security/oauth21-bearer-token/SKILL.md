---
name: oauth21-bearer-token
description: OAuth 2.1 Bearer Token usage guide. Use when implementing access token transmission, Authorization header support, resource server validation, and security requirements. Covers query parameter prohibition and token protection. Based on OAuth 2.1 Section 5 requirements.
---

# OAuth 2.1 Bearer Token

Bearer Token usage requirements for OAuth 2.1 resource requests.

## Bearer Token Definition

A bearer token is a security token where any party in possession can use the token. No proof of possession is required.

## Token Transmission Methods

### Authorization Header (REQUIRED)

Primary method. Resource servers MUST support this.

```http
GET /resource HTTP/1.1
Host: server.example.com
Authorization: Bearer mF_9.B5f-4.1JqM
```

#### Case Insensitivity

The string "Bearer" is case-insensitive:

```http
Authorization: Bearer mF_9.B5f-4.1JqM   ✓
Authorization: bearer mF_9.B5f-4.1JqM   ✓
Authorization: BEARER mF_9.B5f-4.1JqM   ✓
Authorization: bEaReR mF_9.B5f-4.1JqM   ✓
```

### Form-Encoded Body (CONDITIONAL)

Only when ALL conditions met:

1. Content-Type is `application/x-www-form-urlencoded`
2. Content is single-part
3. Content consists entirely of ASCII
4. HTTP method has defined body semantics (NOT GET)

```http
POST /resource HTTP/1.1
Host: server.example.com
Content-Type: application/x-www-form-urlencoded

access_token=mF_9.B5f-4.1JqM
```

### URI Query Parameter (PROHIBITED)

```http
# NEVER do this in OAuth 2.1
GET /resource?access_token=mF_9.B5f-4.1JqM   ✗ PROHIBITED
```

- Clients MUST NOT send tokens in query parameters
- Resource servers MUST ignore tokens in query parameters

## Token Structure

### Reference Token

Opaque string referencing server-stored authorization data.

```
access_token = "2YotnFZFEjr1zCsicMWpAA"
```

Requires token introspection to validate.

### Self-Contained Token (JWT)

Contains encoded authorization data.

```
access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
```

Can be validated locally with public key.

## Token Properties

### Unpredictability

- Tokens MUST be infeasible for attackers to guess
- Use cryptographically random strings
- Sufficient length (128+ bits of entropy)

### Integrity Protection

If token encodes authorization info:
- MUST use integrity protection (signature)
- JWT Profile (RFC 9068) recommended

## Resource Server Validation

### Validation Steps

1. Extract token from request
2. Verify token format is valid
3. Check token has not expired
4. Verify token scope covers requested resource
5. Validate token signature (if self-contained)
6. Or introspect token (if reference)

### Token Introspection

For reference tokens, use RFC 7662:

```http
POST /introspect HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW

token=mF_9.B5f-4.1JqM
```

Response:

```json
{
  "active": true,
  "client_id": "s6BhdRkqt3",
  "scope": "openid profile",
  "sub": "248289761001",
  "exp": 1419356238
}
```

## Error Responses

### WWW-Authenticate Header

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="example",
  error="invalid_token",
  error_description="The access token expired"
```

### Error Codes

| Error | HTTP Status | Description |
|-------|-------------|-------------|
| `invalid_request` | 400 | Malformed request |
| `invalid_token` | 401 | Token invalid, expired, or revoked |
| `insufficient_scope` | 403 | Token lacks required scope |

### Missing Token

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="example"
```

## Security Requirements

### TLS Required

- Clients MUST use TLS (HTTPS) when sending bearer tokens
- Resource servers SHOULD require TLS

### Certificate Validation

- Clients MUST validate TLS certificate chains
- Prevents DNS hijacking attacks

### Token Storage

- MUST NOT store in cookies (unless properly secured)
- MUST NOT store in browser history
- MUST NOT log tokens

### Short Lifetime

- Authorization servers SHOULD issue short-lived tokens
- Reduces impact of token leakage
- Especially important for browser environments

### Audience Restriction

- Tokens SHOULD contain audience restriction
- Limits token use to intended resource servers

### Scope Restriction

- Issue tokens with minimum required scope
- Reduces impact of compromise

## Sender-Constrained Tokens (RECOMMENDED)

Bind token to specific sender for enhanced security.

### DPoP (Demonstrating Proof of Possession)

```http
GET /resource HTTP/1.1
Host: server.example.com
Authorization: DPoP eyJhbGciOiJSUzI1NiJ9...
DPoP: eyJhbGciOiJFUzI1NiIsInR5cCI6ImRwb3Arand0In0...
```

### Mutual TLS

Client certificate bound to token.

```http
GET /resource HTTP/1.1
Host: server.example.com
Authorization: Bearer mF_9.B5f-4.1JqM
# (mTLS client certificate in TLS handshake)
```

## Comparison with OAuth 2.0

### Removed in OAuth 2.1

| Feature | OAuth 2.0 | OAuth 2.1 |
|---------|-----------|-----------|
| Query parameter token | Allowed | PROHIBITED |
| Implicit grant | Defined | Removed |

## Implementation Checklist

### Client

1. [ ] Use Authorization header for token transmission
2. [ ] Use form body only when header not possible
3. [ ] NEVER use query parameter
4. [ ] Always use TLS
5. [ ] Validate TLS certificates
6. [ ] Do not log tokens
7. [ ] Do not store in cookies

### Resource Server

1. [ ] Support Authorization header
2. [ ] Ignore tokens in query parameters
3. [ ] Validate token on every request
4. [ ] Check token expiration
5. [ ] Verify scope covers resource
6. [ ] Return proper WWW-Authenticate on error
7. [ ] Require TLS
