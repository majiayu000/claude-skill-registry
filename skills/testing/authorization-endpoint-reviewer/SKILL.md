---
name: authorization-endpoint-reviewer
description: Review test cases for Authorization Endpoint. Covers response_type=code, request parameters (scope, client_id, redirect_uri, state, nonce, prompt, display, max_age), and authorization response per OIDC Core 1.0 Section 3.1.2.
---

# Authorization Endpoint Test Case Reviewer

Review test cases for Authorization Endpoint in OpenID Connect Basic OP.

## Scope

- **Feature**: Authorization Endpoint
- **Specifications**: OIDC Core 1.0 Section 3.1.2; OAuth 2.1 Section 4.1
- **Profile**: Basic OP (Authorization Code Flow, `response_type=code`)

## Review Process

1. Identify which authorization endpoint requirement the test targets
2. Check against the checklist below
3. Verify both success and error scenarios
4. Ensure all mandatory parameters are tested
5. Report gaps with specific spec section references

## Response Type

### OP-Response-code

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Accept authorization request with `response_type=code` | OIDC Core 3.1.2.1 |
| [ ] | Return authorization code in query component of redirect URI | OIDC Core 3.1.2.5 |
| [ ] | Include `state` in response if present in request | OIDC Core 3.1.2.5 |

### OP-Response-Missing

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Return error if `response_type` parameter is missing | OAuth 2.1 4.1.2.1 |
| [ ] | Error code MUST be `invalid_request` | OAuth 2.1 4.1.2.1 |

## Mandatory Request Parameters

| Check | Parameter | Requirement | Spec Reference |
|-------|-----------|-------------|----------------|
| [ ] | `scope` | MUST include openid | OIDC Core 3.1.2.1 |
| [ ] | `response_type` | REQUIRED | OIDC Core 3.1.2.1 |
| [ ] | `client_id` | REQUIRED | OIDC Core 3.1.2.1 |
| [ ] | `redirect_uri` | REQUIRED if multiple registered | OIDC Core 3.1.2.1 |

## Redirect URI Validation

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Exact string match comparison | OAuth 2.1 4.1.3 |
| [ ] | Reject if redirect_uri doesn't match registered | OIDC Core 3.1.2.1 |
| [ ] | MUST NOT redirect if redirect_uri invalid | OAuth 2.1 4.1.2.1 |

## State Parameter

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Return `state` unchanged if present in request | OAuth 2.1 4.1.2 |
| [ ] | Include in both success and error responses | OAuth 2.1 4.1.2 |

## Nonce Parameter (Code Flow)

### OP-Req-nonce

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Accept request without nonce when using code flow | OIDC Core 3.1.2.1 |
| [ ] | If nonce provided, include in ID Token | OIDC Core 3.1.3.6 |

## Prompt Parameter (OIDC Core 15.1 - Mandatory)

| Check | Value | Requirement | Spec Reference |
|-------|-------|-------------|----------------|
| [ ] | `none` | No UI displayed; error if auth required | OIDC Core 3.1.2.1 |
| [ ] | `login` | Force re-authentication | OIDC Core 3.1.2.1 |
| [ ] | `consent` | Request consent even if previously given | OIDC Core 3.1.2.1 |
| [ ] | `select_account` | Prompt user to select account | OIDC Core 3.1.2.1 |

### prompt=none Error Cases

| Check | Condition | Expected Error |
|-------|-----------|----------------|
| [ ] | User not authenticated | `login_required` |
| [ ] | Consent required | `consent_required` |
| [ ] | Account selection needed | `account_selection_required` |
| [ ] | Any interaction needed | `interaction_required` |

## Display Parameter (OIDC Core 15.1 - Mandatory)

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Support `display` parameter | OIDC Core 3.1.2.1 |
| [ ] | Values: page, popup, touch, wap | OIDC Core 3.1.2.1 |

## Optional Parameters (no error if unsupported)

| Check | Parameter | Test ID | Spec Reference |
|-------|-----------|---------|----------------|
| [ ] | `max_age` | OP-Req-max_age | OIDC Core 3.1.2.1 |
| [ ] | `ui_locales` | OP-Req-ui_locales | OIDC Core 3.1.2.1 |
| [ ] | `claims_locales` | OP-Req-claims_locales | OIDC Core 3.1.2.1 |
| [ ] | `acr_values` | OP-Req-acr_values | OIDC Core 3.1.2.1 |
| [ ] | `login_hint` | OP-Req-login_hint | OIDC Core 3.1.2.1 |

## Authorization Response (Success)

```http
HTTP/1.1 302 Found
Location: https://client.example.org/cb?
  code=SplxlOBeZQQYbYS6WxSbIA
  &state=af0ifjsldkj
```

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | Return `code` parameter | OIDC Core 3.1.2.5 |
| [ ] | Return `state` if provided | OIDC Core 3.1.2.5 |
| [ ] | Use query component for code flow | OIDC Core 3.1.2.5 |

## Test Case Categories

### Response Type Tests

- [ ] Valid: `response_type=code` accepted
- [ ] Invalid: Missing response_type
- [ ] Invalid: Unknown response_type

### Redirect URI Tests

- [ ] Valid: Exact match with registered URI
- [ ] Invalid: Unregistered redirect_uri
- [ ] Invalid: redirect_uri with extra query params
- [ ] Invalid: redirect_uri with fragment

### Scope Tests

- [ ] Valid: `scope=openid` present
- [ ] Invalid: Missing openid scope
- [ ] Valid: Additional scopes (profile, email, etc.)

### Prompt Parameter Tests

- [ ] Valid: prompt=none (user authenticated)
- [ ] Valid: prompt=login (force re-auth)
- [ ] Valid: prompt=consent (force consent)
- [ ] Valid: prompt=select_account
- [ ] Error: prompt=none but login required
- [ ] Error: prompt=none but consent required

### State Parameter Tests

- [ ] Valid: state returned unchanged
- [ ] Valid: state included in error response
- [ ] Valid: Request without state (optional)

## Conformance Test IDs

| Test ID | Feature |
|---------|---------|
| OP-Response-code | response_type=code |
| OP-Response-Missing | Reject missing response_type |
| OP-nonce-NoReq-code | Accept no nonce in code flow |
| OP-nonce-code | Include nonce if requested |
| OP-redirect_uri-NotReg | Reject unregistered redirect_uri |
| OP-Req-* | Request parameter handling |

## Review Output Format

```
## Test Case: [Name]
### Target Feature: Authorization Endpoint - [specific aspect]
### Test ID: OP-[xxx]
### Spec Compliance:
- [x] Covers required behavior per [spec section]
- [ ] Missing: [specific requirement]
### Verdict: PASS / FAIL / PARTIAL
### Recommendations: [if any]
```
