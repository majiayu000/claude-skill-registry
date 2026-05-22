---
name: id-token-reviewer
description: Review test cases for ID Token validation. Covers ID Token structure, required/conditional claims, signature validation (RS256), and all validation rules per OIDC Core 1.0 Section 2 and 3.1.3.7.
---

# ID Token Test Case Reviewer

Review test cases for ID Token generation and validation in OpenID Connect Basic OP.

## Scope

- **Feature**: ID Token Claims and Signature
- **Specifications**: OIDC Core 1.0 Section 2, 3.1.3.6, 3.1.3.7
- **Profile**: Basic OP (Authorization Code Flow)

## Review Process

1. Identify which ID Token requirement the test targets
2. Check against the checklist below
3. Verify both valid and invalid token scenarios
4. Ensure signature algorithm (RS256) is tested
5. Report gaps with specific spec section references

## ID Token Structure

```
Header.Payload.Signature
```

### JOSE Header Requirements

| Field | Requirement | Example |
|-------|-------------|---------|
| `alg` | REQUIRED. Signing algorithm | `RS256` |
| `kid` | RECOMMENDED. Key ID | `1e9gdk7` |
| `typ` | OPTIONAL. Type | `JWT` |

## Required Claims Checklist

| Check | Claim | Requirement | Spec Reference |
|-------|-------|-------------|----------------|
| [ ] | `iss` | REQUIRED. Issuer Identifier (HTTPS URL, no query/fragment) | OIDC Core 2 |
| [ ] | `sub` | REQUIRED. Subject Identifier (max 255 ASCII chars) | OIDC Core 2 |
| [ ] | `aud` | REQUIRED. Audience (contains client_id) | OIDC Core 2 |
| [ ] | `exp` | REQUIRED. Expiration time | OIDC Core 2 |
| [ ] | `iat` | REQUIRED. Issued at time | OIDC Core 2 |

## Conditional Claims Checklist

| Check | Claim | Condition | Spec Reference |
|-------|-------|-----------|----------------|
| [ ] | `nonce` | REQUIRED if nonce in auth request | OIDC Core 3.1.3.6 |
| [ ] | `auth_time` | REQUIRED if max_age requested or auth_time essential | OIDC Core 2 |
| [ ] | `azp` | REQUIRED if aud contains multiple values | OIDC Core 2 |
| [ ] | `at_hash` | OPTIONAL for code flow | OIDC Core 3.1.3.6 |

## Signature Requirements

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | ID Token MUST be signed JWT | OIDC Core 2 |
| [ ] | Support RS256 algorithm (MANDATORY) | OIDC Core 15.1 |
| [ ] | `alg` header parameter present | OIDC Core 2 |
| [ ] | `kid` header parameter present if multiple keys | OIDC Core 10.1 |

## Validation Rules (OP produces valid tokens)

| Check | Validation Rule | Spec Reference |
|-------|-----------------|----------------|
| [ ] | `iss` exactly matches OP's Issuer Identifier | OIDC Core 3.1.3.7 |
| [ ] | `aud` contains requesting client's client_id | OIDC Core 3.1.3.7 |
| [ ] | `exp` is in the future | OIDC Core 3.1.3.7 |
| [ ] | Signature verifiable with OP's public key | OIDC Core 3.1.3.7 |

## Test Case Categories

### Issuer (`iss`) Tests

- [ ] Valid: `iss` matches configured OP issuer exactly
- [ ] Invalid: `iss` adds query parameters
- [ ] Invalid: `iss` adds fragment
- [ ] Invalid: `iss` differs by trailing slash
- [ ] Invalid: `iss` differs by scheme (http vs https)
- [ ] Invalid: `iss` is missing

### Audience (`aud`) Tests

- [ ] Valid: `aud` equals client_id (string)
- [ ] Valid: `aud` is array containing client_id
- [ ] Invalid: `aud` doesn't contain client_id
- [ ] Invalid: `aud` is missing

### Authorized Party (`azp`) Tests

- [ ] Valid: Single aud, no azp required
- [ ] Valid: Multiple aud, azp equals client_id
- [ ] Warning: Multiple aud, azp missing
- [ ] Invalid: azp present but doesn't match client_id

### Expiration (`exp`) Tests

- [ ] Valid: exp is in future
- [ ] Valid: Small clock skew tolerance (typically 5 minutes)
- [ ] Invalid: exp is in past
- [ ] Invalid: exp is missing

### Nonce Tests

- [ ] Valid: nonce matches request nonce
- [ ] Valid: No nonce in request, no nonce in token (code flow)
- [ ] Invalid: nonce requested but missing in token
- [ ] Invalid: nonce doesn't match request

### Signature Tests

- [ ] Valid: RS256 signature verifies with OP's public key
- [ ] Valid: Retrieve key via kid from JWKS
- [ ] Invalid: Signature doesn't verify
- [ ] Invalid: Unknown kid
- [ ] Invalid: Algorithm mismatch
- [ ] Invalid: alg is none when signature required

## Review Output Format

```
## Test Case: [Name]
### Target Feature: ID Token - [specific aspect]
### Test ID: OP-IDToken-[xxx]
### Spec Compliance:
- [x] Covers required behavior per [spec section]
- [ ] Missing: [specific requirement]
### Verdict: PASS / FAIL / PARTIAL
### Recommendations: [if any]
```

## Example Valid ID Token

```json
{
  "iss": "https://server.example.com",
  "sub": "248289761001",
  "aud": "s6BhdRkqt3",
  "nonce": "n-0S6_WzA2Mj",
  "exp": 1311281970,
  "iat": 1311280970
}
```
