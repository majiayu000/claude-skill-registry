---
name: oauth21-token-endpoint
description: OAuth 2.1 Token Endpoint implementation guide. Use when implementing token endpoint requirements beyond OpenID Connect, including grant types, token response format, Cache-Control headers, CORS support, and error handling. Covers OAuth 2.1 Section 3.2 and Section 4 requirements.
---

# OAuth 2.1 Token Endpoint

Token Endpoint requirements specific to OAuth 2.1 (beyond OpenID Connect).

## Endpoint Requirements

### HTTP Method

- MUST use POST method
- Other methods not allowed

### Content Type

- MUST accept `application/x-www-form-urlencoded`
- UTF-8 character encoding

### TLS

- MUST use HTTPS
- Except localhost for development

### CORS Support

For browser-based apps:
- Token endpoint MUST support CORS headers
- Return appropriate `Access-Control-Allow-Origin`

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://client.example.com
Content-Type: application/json
```

## Supported Grant Types

### authorization_code

```http
POST /token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=SplxlOBeZQQYbYS6WxSbIA
&code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

### refresh_token

```http
POST /token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&refresh_token=tGzv3JOkF0XG5Qx2TlKWIA
```

### client_credentials

```http
POST /token HTTP/1.1
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
```

## Token Request Processing

### Client Authentication

```python
def process_token_request(request):
    # 1. Authenticate confidential clients
    if client.is_confidential:
        if not authenticate_client(request):
            return error_response("invalid_client")
    
    # 2. Validate grant type specific parameters
    # 3. Issue tokens
```

### Parameter Handling

- MUST ignore unrecognized parameters
- Parameters without value treated as omitted
- Parameters MUST NOT be included more than once

## Token Response

### Success Response

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store

{
  "access_token": "2YotnFZFEjr1zCsicMWpAA",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
  "scope": "openid profile"
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `access_token` | REQUIRED. The access token |
| `token_type` | REQUIRED. Type of token (e.g., "Bearer") |

### Optional Fields

| Field | Description |
|-------|-------------|
| `expires_in` | RECOMMENDED. Lifetime in seconds |
| `refresh_token` | OPTIONAL. Refresh token |
| `scope` | RECOMMENDED if same as request, REQUIRED if different |

### Token Type

- Value is case-insensitive
- `Bearer`, `bearer`, `BEARER` are all valid

## Required Headers

### Cache-Control

```http
Cache-Control: no-store
```

MUST include in any response containing tokens.

### Pragma (Legacy)

```http
Pragma: no-cache
```

May include for legacy HTTP/1.0 compatibility.

## Error Response

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "invalid_grant",
  "error_description": "Authorization code expired",
  "error_uri": "https://example.com/docs/errors#invalid_grant"
}
```

### Error Codes

| Error | Description |
|-------|-------------|
| `invalid_request` | Missing/invalid parameter |
| `invalid_client` | Client authentication failed (401 status) |
| `invalid_grant` | Invalid grant (code, refresh_token, etc.) |
| `unauthorized_client` | Client not authorized for grant type |
| `unsupported_grant_type` | Grant type not supported |
| `invalid_scope` | Invalid/unknown scope |

### Error Field Character Restrictions

- `error`: %x20-21 / %x23-5B / %x5D-7E
- `error_description`: %x20-21 / %x23-5B / %x5D-7E
- `error_uri`: URI-reference syntax

## Authorization Code Grant Specifics

### Request Parameters

| Parameter | Requirement |
|-----------|-------------|
| `grant_type` | REQUIRED. Value: `authorization_code` |
| `code` | REQUIRED. The authorization code |
| `code_verifier` | REQUIRED if code_challenge was present |
| `client_id` | REQUIRED if not authenticating otherwise |

### Validation

1. Authenticate client if confidential
2. Verify code issued to this client
3. Verify code is valid and not expired
4. Verify code_verifier (see PKCE skill)
5. Return access token only once per code

### Code Reuse Handling

```python
def handle_code_reuse(code):
    if code.already_used:
        # MUST deny request
        # SHOULD revoke all tokens from this code
        revoke_tokens_for_code(code)
        return error_response("invalid_grant")
```

## Refresh Token Grant Specifics

### Request Parameters

| Parameter | Requirement |
|-----------|-------------|
| `grant_type` | REQUIRED. Value: `refresh_token` |
| `refresh_token` | REQUIRED. The refresh token |
| `scope` | OPTIONAL. Must not exceed original scope |

### Public Client Requirements

For public clients, refresh tokens MUST be either:
- Sender-constrained (bound to client proof)
- One-time use (rotation)

### Refresh Token Rotation

```python
def handle_refresh_token(refresh_token):
    # Issue new access token
    access_token = generate_access_token()
    
    # Optionally rotate refresh token
    if should_rotate:
        new_refresh_token = generate_refresh_token()
        invalidate(refresh_token)
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token
        }
    
    return {"access_token": access_token}
```

## Client Credentials Grant Specifics

### Request Parameters

| Parameter | Requirement |
|-----------|-------------|
| `grant_type` | REQUIRED. Value: `client_credentials` |
| `scope` | OPTIONAL |

### Requirements

- MUST only be used by confidential clients
- MUST authenticate client

## Removed from OAuth 2.1

These grant types are NOT in OAuth 2.1:

- **Implicit Grant** (`response_type=token`)
- **Resource Owner Password Credentials Grant**

## Implementation Checklist

1. [ ] Use POST method only
2. [ ] Accept application/x-www-form-urlencoded
3. [ ] Use HTTPS (except localhost)
4. [ ] Support CORS for browser apps
5. [ ] Include Cache-Control: no-store
6. [ ] Support authorization_code grant
7. [ ] Support refresh_token grant
8. [ ] Support client_credentials grant
9. [ ] Validate PKCE code_verifier
10. [ ] Enforce single-use authorization codes
11. [ ] Revoke tokens on code reuse
12. [ ] Handle refresh token rotation for public clients
13. [ ] Return proper error responses
14. [ ] Ignore unrecognized parameters
