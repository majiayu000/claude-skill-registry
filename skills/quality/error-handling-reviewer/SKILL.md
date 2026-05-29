---
name: error-handling-reviewer
description: Review test cases for OAuth/OIDC error handling. Covers authorization endpoint errors, token endpoint errors, error response formats, HTTP status codes, and all error codes per OAuth 2.1 and OIDC Core 1.0.
---

# Error Handling Test Case Reviewer

Review test cases for error handling in OpenID Connect Basic OP.

## Scope

- **Feature**: Error Responses
- **Specifications**: OAuth 2.1 Section 4.1.2.1, 5.2; OIDC Core 1.0 Section 3.1.2.6
- **Profile**: Basic OP (Authorization Code Flow)

## Review Process

1. Identify which error scenario the test targets
2. Check against the checklist below
3. Verify correct error code is returned
4. Ensure response format matches specification
5. Report gaps with specific spec section references

## Authorization Endpoint Errors

### OAuth 2.1 Error Codes (Section 4.1.2.1)

| Error Code | Condition | Spec |
|------------|-----------|------|
| `invalid_request` | Missing/malformed parameter, duplicate parameter | OAuth 2.1 4.1.2.1 |
| `unauthorized_client` | Client not authorized for grant type | OAuth 2.1 4.1.2.1 |
| `access_denied` | Resource owner or AS denied request | OAuth 2.1 4.1.2.1 |
| `unsupported_response_type` | response_type not supported | OAuth 2.1 4.1.2.1 |
| `invalid_scope` | Invalid, unknown, or malformed scope | OAuth 2.1 4.1.2.1 |
| `server_error` | Unexpected condition (use sparingly) | OAuth 2.1 4.1.2.1 |
| `temporarily_unavailable` | Server temporarily overloaded | OAuth 2.1 4.1.2.1 |

### OIDC-Specific Error Codes (Section 3.1.2.6)

| Error Code | Condition | Spec |
|------------|-----------|------|
| `interaction_required` | prompt=none but End-User interaction needed | OIDC Core 3.1.2.6 |
| `login_required` | prompt=none but End-User not authenticated | OIDC Core 3.1.2.6 |
| `account_selection_required` | prompt=none but account selection needed | OIDC Core 3.1.2.6 |
| `consent_required` | prompt=none but consent required | OIDC Core 3.1.2.6 |
| `invalid_request_uri` | request_uri invalid or unreachable | OIDC Core 3.1.2.6 |
| `invalid_request_object` | Request Object invalid | OIDC Core 3.1.2.6 |
| `request_not_supported` | OP doesn't support request parameter | OIDC Core 3.1.2.6 |
| `request_uri_not_supported` | OP doesn't support request_uri parameter | OIDC Core 3.1.2.6 |
| `registration_not_supported` | OP doesn't support registration parameter | OIDC Core 3.1.2.6 |

### Authorization Error Response Format

For Authorization Code flow, errors returned in **query component**:

```http
HTTP/1.1 302 Found
Location: https://client.example.org/cb?
  error=invalid_request
  &error_description=Unsupported%20response_type%20value
  &state=af0ifjsldkj
```

## Token Endpoint Errors

### OAuth 2.1 Error Codes (Section 5.2)

| Error Code | Condition | Spec |
|------------|-----------|------|
| `invalid_request` | Missing/malformed parameter | OAuth 2.1 5.2 |
| `invalid_client` | Client authentication failed | OAuth 2.1 5.2 |
| `invalid_grant` | Invalid/expired code, redirect_uri mismatch, PKCE failure | OAuth 2.1 5.2 |
| `unauthorized_client` | Client not authorized for grant type | OAuth 2.1 5.2 |
| `unsupported_grant_type` | grant_type not supported | OAuth 2.1 5.2 |
| `invalid_scope` | Requested scope exceeds grant | OAuth 2.1 5.2 |

### Token Error Response Format

Errors returned as JSON with **HTTP 400** (or 401 for invalid_client):

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json;charset=UTF-8
Cache-Control: no-store

{
  "error": "invalid_grant",
  "error_description": "Authorization code expired"
}
```

### HTTP Status Codes

| Error | HTTP Status |
|-------|-------------|
| `invalid_client` | 401 (if via Authorization header) or 400 |
| All others | 400 |

## Error Response Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `error` | REQUIRED | ASCII error code |
| `error_description` | OPTIONAL | Human-readable description (ASCII) |
| `error_uri` | OPTIONAL | URI with error information |
| `state` | REQUIRED if in request | Exact value from request |

## Test Cases Checklist

### Missing Required Parameters

| Scenario | Expected Error | Endpoint |
|----------|----------------|----------|
| [ ] Missing response_type | `invalid_request` | Authorization |
| [ ] Missing client_id | `invalid_request` | Authorization |
| [ ] Missing scope | `invalid_request` | Authorization |
| [ ] Missing openid in scope | `invalid_scope` | Authorization |
| [ ] Missing grant_type | `invalid_request` | Token |
| [ ] Missing code | `invalid_request` | Token |
| [ ] Missing code_verifier (when required) | `invalid_grant` | Token |

### Invalid Parameters

| Scenario | Expected Error | Endpoint |
|----------|----------------|----------|
| [ ] Unknown response_type | `unsupported_response_type` | Authorization |
| [ ] Unregistered redirect_uri | `invalid_request` | Authorization |
| [ ] Invalid redirect_uri format | `invalid_request` | Authorization |
| [ ] Invalid client_id | `unauthorized_client` or `invalid_request` | Authorization |
| [ ] Invalid/expired code | `invalid_grant` | Token |
| [ ] Code already used | `invalid_grant` | Token |
| [ ] PKCE verification failure | `invalid_grant` | Token |
| [ ] Client authentication failure | `invalid_client` | Token |

### prompt=none Specific Errors

| Scenario | Expected Error |
|----------|----------------|
| [ ] User not authenticated | `login_required` |
| [ ] Consent not yet given | `consent_required` |
| [ ] Multiple accounts, selection needed | `account_selection_required` |
| [ ] Any interaction needed | `interaction_required` |

### Redirect URI Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| [ ] Invalid/unregistered redirect_uri | MUST NOT redirect, display error |
| [ ] Valid redirect_uri but error occurred | Redirect with error in query |
| [ ] Error with state in request | Include state in error response |

## Error Response Validation Checklist

| Check | Requirement |
|-------|-------------|
| [ ] `error` parameter present |
| [ ] `error` value is valid code |
| [ ] `state` returned if sent |
| [ ] No redirect for invalid redirect_uri |
| [ ] Correct HTTP status code |
| [ ] JSON Content-Type for token endpoint |
| [ ] No caching headers (Cache-Control: no-store) |

## Conformance Test IDs

| Test ID | Scenario |
|---------|----------|
| OP-Response-Missing | Missing response_type → error |
| OP-redirect_uri-NotReg | Unregistered redirect_uri → error |
| OP-OAuth-2nd | Reused code → error |
| OP-OAuth-2nd-30s | Code reuse after 30s → error |

## Review Output Format

```
## Test Case: [Name]
### Target Feature: Error Handling - [specific scenario]
### Test ID: OP-Error-[xxx]
### Spec Compliance:
- [x] Covers required behavior per [spec section]
- [ ] Missing: [specific requirement]
### Error Response:
- [x/blank] Correct error code
- [x/blank] Correct HTTP status
- [x/blank] state included if sent
### Verdict: PASS / FAIL / PARTIAL
### Recommendations: [if any]
```
