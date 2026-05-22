---
name: pkce-reviewer
description: Review test cases for PKCE (Proof Key for Code Exchange) implementation. Covers code_challenge/code_verifier validation, S256 transformation, and all PKCE requirements per OAuth 2.1 Sections 4.1.1, 4.1.3, 7.5.1, 7.5.2. PKCE is MANDATORY in OAuth 2.1.
---

# PKCE Test Case Reviewer

Review test cases for PKCE implementation in OAuth 2.1 / OpenID Connect Basic OP.

## Scope

- **Feature**: PKCE (Proof Key for Code Exchange)
- **Specifications**: OAuth 2.1 Section 4.1.1, 4.1.3, 7.5.1, 7.5.2
- **Status**: MANDATORY for all Authorization Code flow clients

## Review Process

1. Identify which PKCE requirement the test targets
2. Check against the checklist below
3. Verify both success and error scenarios
4. Ensure S256 transformation is tested (mandatory)
5. Report gaps with specific spec section references

## Code Verifier Requirements

| Property | Requirement | Spec Reference |
|----------|-------------|----------------|
| Characters | `[A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"` | OAuth 2.1 4.1.1 |
| Min Length | 43 characters | OAuth 2.1 4.1.1 |
| Max Length | 128 characters | OAuth 2.1 4.1.1 |
| Entropy | High entropy, cryptographically random | OAuth 2.1 4.1.1 |

## Code Challenge Transformation Methods

| Method | Calculation | Status |
|--------|-------------|--------|
| S256 | `BASE64URL(SHA256(ASCII(code_verifier)))` | MANDATORY |
| plain | `code_challenge = code_verifier` | OPTIONAL |

## Server Requirements Checklist

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Support `code_challenge` parameter | OAuth 2.1 4.1.1 |
| [ ] | Support `code_challenge_method` parameter | OAuth 2.1 4.1.1 |
| [ ] | Support S256 transformation (MANDATORY) | OAuth 2.1 4.1.1 |
| [ ] | MAY support plain transformation | OAuth 2.1 4.1.1 |
| [ ] | Verify `code_verifier` at token endpoint | OAuth 2.1 4.1.3 |
| [ ] | Reject if code_challenge present but code_verifier missing | OAuth 2.1 4.1.3 |
| [ ] | Reject if code_verifier present but no code_challenge was sent | OAuth 2.1 4.1.3 |

## Authorization Request Tests

| Test | Expected Result |
|------|-----------------|
| [ ] Valid S256 code_challenge | Accept |
| [ ] Valid plain code_challenge | Accept (if supported) |
| [ ] Missing code_challenge | Reject (OAuth 2.1) |
| [ ] Invalid code_challenge format | Reject |
| [ ] Unknown code_challenge_method | Reject |

## Token Request Tests

| Test | Expected Result |
|------|-----------------|
| [ ] Valid code_verifier matching S256 challenge | Accept |
| [ ] Valid code_verifier matching plain challenge | Accept (if supported) |
| [ ] Missing code_verifier when challenge was sent | Reject (`invalid_grant`) |
| [ ] Wrong code_verifier (hash mismatch) | Reject (`invalid_grant`) |
| [ ] code_verifier present but no challenge was sent | Reject |
| [ ] code_verifier too short (<43 chars) | Reject |
| [ ] code_verifier too long (>128 chars) | Reject |
| [ ] code_verifier with invalid characters | Reject |

## S256 Test Vector

```
code_verifier: dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk

SHA256(ASCII(code_verifier)):
  [byte array]

BASE64URL(SHA256 result):
  E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
```

## Example Authorization Request

```http
GET /authorize?
  response_type=code
  &client_id=s6BhdRkqt3
  &redirect_uri=https%3A%2F%2Fclient.example.org%2Fcb
  &scope=openid%20profile
  &state=af0ifjsldkj
  &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
  &code_challenge_method=S256
```

## Example Token Request

```http
POST /token HTTP/1.1
Host: server.example.com
Content-Type: application/x-www-form-urlencoded
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW

grant_type=authorization_code
&code=SplxlOBeZQQYbYS6WxSbIA
&code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

## Security Considerations

### Why PKCE is Mandatory in OAuth 2.1

| Attack | PKCE Protection |
|--------|-----------------|
| Code interception | Attacker lacks code_verifier |
| Code injection | code_verifier bound to original request |
| Replay attack | code_verifier is single-use |

## Review Output Format

```
## Test Case: [Name]
### Target Feature: PKCE - [specific aspect]
### Test ID: OP-PKCE-[xxx]
### Spec Compliance:
- [x] Covers required behavior per [spec section]
- [ ] Missing: [specific requirement]
### OAuth 2.1 Compliance:
- [x/blank] S256 validation included
### Verdict: PASS / FAIL / PARTIAL
### Recommendations: [if any]
```
