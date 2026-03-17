---
name: userinfo-endpoint-reviewer
description: Review test cases for UserInfo Endpoint. Covers access token validation, Bearer token handling, sub claim consistency, scope-based claims, and signed responses per OIDC Core 1.0 Section 5.3.
---

# UserInfo Endpoint Test Case Reviewer

Review test cases for UserInfo Endpoint in OpenID Connect Basic OP.

## Scope

- **Feature**: UserInfo Endpoint
- **Specifications**: OIDC Core 1.0 Section 5.3, 5.4
- **Profile**: Basic OP

## Review Process

1. Identify which UserInfo requirement the test targets
2. Check against the checklist below
3. Verify both success and error scenarios
4. Ensure scope-based claim filtering is tested
5. Report gaps with specific spec section references

## Basic Requirements

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Accept access token via Authorization header (Bearer) | OIDC Core 5.3.1 |
| [ ] | Support GET method | OIDC Core 5.3.1 |
| [ ] | Support POST method | OIDC Core 5.3.1 |
| [ ] | Return `sub` claim (REQUIRED) | OIDC Core 5.3.2 |
| [ ] | `sub` matches ID Token `sub` | OIDC Core 5.3.2 |
| [ ] | Return claims based on granted scopes | OIDC Core 5.4 |

## Request Format

### GET Request

```http
GET /userinfo HTTP/1.1
Host: server.example.com
Authorization: Bearer SlAV32hkKG
```

### POST Request

```http
POST /userinfo HTTP/1.1
Host: server.example.com
Authorization: Bearer SlAV32hkKG
Content-Type: application/x-www-form-urlencoded
```

## Response Format

### JSON Response (Default)

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "sub": "248289761001",
  "name": "Jane Doe",
  "given_name": "Jane",
  "family_name": "Doe",
  "email": "janedoe@example.com",
  "email_verified": true,
  "picture": "http://example.com/janedoe/me.jpg"
}
```

### Signed Response (JWT)

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Support RS256 signed response when requested | OIDC Core 5.3.2 |
| [ ] | Honor `userinfo_signed_response_alg` registration | OIDC Core 5.3.2 |

## Subject Identifier Consistency

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | `sub` claim MUST be present | OIDC Core 5.3.2 |
| [ ] | `sub` value MUST match ID Token `sub` | OIDC Core 5.3.2 |
| [ ] | `sub` is stable for the user | OIDC Core 5.3.2 |

## Access Token Validation

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Validate access token | OIDC Core 5.3.1 |
| [ ] | Return 401 for invalid/expired token | RFC 6750 |
| [ ] | Return 403 for insufficient scope | RFC 6750 |

### Error Response

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer error="invalid_token",
  error_description="The access token expired"
```

## Test Case Categories

### Access Token Tests

- [ ] Valid: Bearer token in Authorization header
- [ ] Invalid: Missing Authorization header
- [ ] Invalid: Expired access token
- [ ] Invalid: Revoked access token
- [ ] Invalid: Malformed token

### HTTP Method Tests

- [ ] Valid: GET request with Bearer token
- [ ] Valid: POST request with Bearer token
- [ ] Invalid: Other HTTP methods (PUT, DELETE, etc.)

### Sub Claim Tests

- [ ] Valid: `sub` present in response
- [ ] Valid: `sub` matches ID Token `sub`
- [ ] Invalid: `sub` missing from response

### Scope-Based Claims Tests

- [ ] Valid: Only requested scope claims returned
- [ ] Valid: `openid` scope returns `sub` only
- [ ] Valid: `profile` scope returns profile claims
- [ ] Valid: `email` scope returns email claims
- [ ] Valid: `phone` scope returns phone claims
- [ ] Valid: `address` scope returns address claim

### Signed Response Tests (Optional)

- [ ] Valid: RS256 signed JWT response
- [ ] Valid: Signature verifiable with OP's key
- [ ] Valid: Honors registered `userinfo_signed_response_alg`

## Scope to Claims Mapping

| Scope | Claims |
|-------|--------|
| `openid` | `sub` |
| `profile` | `name`, `family_name`, `given_name`, `middle_name`, `nickname`, `preferred_username`, `profile`, `picture`, `website`, `gender`, `birthdate`, `zoneinfo`, `locale`, `updated_at` |
| `email` | `email`, `email_verified` |
| `address` | `address` |
| `phone` | `phone_number`, `phone_number_verified` |

## Error Responses

| Condition | HTTP Status | WWW-Authenticate |
|-----------|-------------|------------------|
| Missing token | 401 | `Bearer` |
| Invalid token | 401 | `Bearer error="invalid_token"` |
| Expired token | 401 | `Bearer error="invalid_token"` |
| Insufficient scope | 403 | `Bearer error="insufficient_scope"` |

## Conformance Test IDs

| Test ID | Feature |
|---------|---------|
| OP-UserInfo-Endpoint | Basic UserInfo functionality |
| OP-UserInfo-RS256 | Signed UserInfo response |
| OP-UserInfo-Header | Bearer token in header |

## Review Output Format

```
## Test Case: [Name]
### Target Feature: UserInfo Endpoint - [specific aspect]
### Test ID: OP-UserInfo-[xxx]
### Spec Compliance:
- [x] Covers required behavior per [spec section]
- [ ] Missing: [specific requirement]
### Sub Consistency:
- [x/blank] sub matches ID Token
### Verdict: PASS / FAIL / PARTIAL
### Recommendations: [if any]
```
