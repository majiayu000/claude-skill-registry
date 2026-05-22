---
name: token-endpoint-reviewer
description: Review test cases for Token Endpoint. Covers grant_type=authorization_code, client authentication (client_secret_basic, client_secret_post), token request/response validation, and all requirements per OIDC Core 1.0 Section 3.1.3 and OAuth 2.1.
---

# Token Endpoint Test Case Reviewer

Review test cases for Token Endpoint in OpenID Connect Basic OP.

## Scope

- **Feature**: Token Endpoint
- **Specifications**: OIDC Core 1.0 Section 3.1.3; OAuth 2.1 Section 3.2, 4.1.3, 4.1.4
- **Profile**: Basic OP (Authorization Code Flow)

## Review Process

1. Identify which token endpoint requirement the test targets
2. Check against the checklist below
3. Verify both success and error scenarios
4. Ensure client authentication is tested
5. Report gaps with specific spec section references

## Basic Requirements

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Accept POST requests only | OAuth 2.1 Section 3.2 |
| [ ] | Require HTTPS (TLS) for non-localhost; allow HTTP for localhost | OIDC Core 3.1.3 |
| [ ] | Support `grant_type=authorization_code` | OIDC Core 3.1.3.1 |

## Client Authentication

### Supported Methods

| Check | Method | Requirement | Spec Reference |
|-------|--------|-------------|----------------|
| [ ] | `client_secret_basic` | HTTP Basic auth with client_id:client_secret | OIDC Core 9 |
| [ ] | `client_secret_post` | client_id and client_secret in request body | OAuth 2.1 Section 2.4.1 |

### Authentication Requirements

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Authenticate confidential clients | OIDC Core 3.1.3.1 |
| [ ] | Return `invalid_client` on auth failure | OAuth 2.1 5.2 |

### client_secret_basic Example

```http
POST /token HTTP/1.1
Host: server.example.com
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA
```

### client_secret_post Example

```http
POST /token HTTP/1.1
Host: server.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=SplxlOBeZQQYbYS6WxSbIA
&client_id=s6BhdRkqt3
&client_secret=gX1fBat3bV
```

## Token Request Parameters

| Check | Parameter | Requirement | Spec Reference |
|-------|-----------|-------------|----------------|
| [ ] | `grant_type` | REQUIRED. Value: `authorization_code` | OAuth 2.1 4.1.3 |
| [ ] | `code` | REQUIRED. Authorization code | OAuth 2.1 4.1.3 |
| [ ] | `redirect_uri` | REQUIRED if included in auth request | OAuth 2.1 4.1.3 |
| [ ] | `code_verifier` | REQUIRED if code_challenge was sent | OAuth 2.1 4.1.3 |
| [ ] | `client_id` | REQUIRED for public clients | OAuth 2.1 4.1.3 |

## Token Response

### Required Fields

| Check | Field | Requirement | Spec Reference |
|-------|-------|-------------|----------------|
| [ ] | `access_token` | REQUIRED | OAuth 2.1 4.1.4 |
| [ ] | `token_type` | REQUIRED. Value: `Bearer` | OAuth 2.1 4.1.4, OIDC Core 3.1.3.3 |
| [ ] | `id_token` | REQUIRED (OIDC) | OIDC Core 3.1.3.3 |

### Optional Fields

| Check | Field | Requirement | Spec Reference |
|-------|-------|-------------|----------------|
| [ ] | `expires_in` | RECOMMENDED | OAuth 2.1 4.1.4 |
| [ ] | `refresh_token` | OPTIONAL | OAuth 2.1 4.1.4 |
| [ ] | `scope` | REQUIRED if different from request | OAuth 2.1 4.1.4 |

### Example Success Response

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: no-store

{
  "access_token": "SlAV32hkKG",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "8xLOxBtZp8",
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Authorization Code Validation

### OP-OAuth-2nd (Code Reuse)

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Return error on second token request with same code | OAuth 2.1 7.5.3 |
| [ ] | SHOULD revoke tokens issued from that code | OAuth 2.1 4.1.3 |
| [ ] | Error code: `invalid_grant` | OAuth 2.1 5.2 |

### Code Validation

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Code is valid (not expired) | OAuth 2.1 4.1.3 |
| [ ] | Code was issued to authenticated client | OAuth 2.1 4.1.3 |
| [ ] | redirect_uri matches (if provided in auth request) | OAuth 2.1 4.1.3 |

## Test Case Categories

### Client Authentication Tests

- [ ] Valid: client_secret_basic authentication
- [ ] Valid: client_secret_post authentication
- [ ] Invalid: Wrong client_secret
- [ ] Invalid: Missing client authentication
- [ ] Invalid: Unknown client_id

### Token Request Tests

- [ ] Valid: Complete token request
- [ ] Invalid: Missing grant_type
- [ ] Invalid: Missing code
- [ ] Invalid: Invalid/expired code
- [ ] Invalid: Code already used (replay)
- [ ] Invalid: redirect_uri mismatch

### Token Response Tests

- [ ] Valid: Contains access_token
- [ ] Valid: Contains id_token
- [ ] Valid: token_type is Bearer
- [ ] Valid: No caching (Cache-Control: no-store)

### Code Reuse Tests

- [ ] First use: Success
- [ ] Second use: `invalid_grant` error
- [ ] After 30s: Code expired (`invalid_grant`)
- [ ] After code reuse: Previous tokens revoked

## Error Responses

| Condition | Error Code | HTTP Status |
|-----------|------------|-------------|
| Client auth failed | `invalid_client` | 401 |
| Invalid/expired code | `invalid_grant` | 400 |
| Missing parameter | `invalid_request` | 400 |
| PKCE mismatch | `invalid_grant` | 400 |
| Wrong grant_type | `unsupported_grant_type` | 400 |

## Conformance Test IDs

| Test ID | Feature |
|---------|---------|
| OP-Token-Endpoint | Basic token endpoint functionality |
| OP-OAuth-2nd | Reject code reuse |
| OP-OAuth-2nd-30s | Reject code reuse after 30s |

## Review Output Format

```
## Test Case: [Name]
### Target Feature: Token Endpoint - [specific aspect]
### Test ID: OP-Token-[xxx]
### Spec Compliance:
- [x] Covers required behavior per [spec section]
- [ ] Missing: [specific requirement]
### Client Auth:
- [x/blank] client_secret_basic tested
- [x/blank] client_secret_post tested
### Verdict: PASS / FAIL / PARTIAL
### Recommendations: [if any]
```
