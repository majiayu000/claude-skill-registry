---
name: oauth21-compliance
description: OAuth 2.1 compliance checklist for authorization servers. Use when implementing OAuth 2.1 beyond OpenID Connect Basic OP requirements, verifying OAuth 2.1 specific features, or understanding differences from OAuth 2.0. Covers all OAuth 2.1 draft-ietf-oauth-v2-1-14 requirements not in Basic OP.
---

# OAuth 2.1 Compliance Checklist

Requirements for OAuth 2.1 compliance beyond OpenID Connect Basic OP certification.

## Key Differences from OAuth 2.0

| Feature | OAuth 2.0 | OAuth 2.1 |
|---------|-----------|-----------|
| PKCE | Optional extension | REQUIRED |
| Implicit grant | Supported | REMOVED |
| Password grant | Supported | REMOVED |
| redirect_uri match | Flexible | Exact string match |
| Query token | Discouraged | PROHIBITED |
| Refresh (public) | No constraint | Sender-constrained/rotation |
| redirect_uri in token | Optional | Removed |

## PKCE Requirements

### Authorization Server

| Requirement | Priority |
|-------------|----------|
| Support `code_challenge` parameter | MUST |
| Support `code_challenge_method=S256` | MUST (MTI) |
| Support `code_challenge_method=plain` | MAY |
| Reject unsupported method with `invalid_request` | MUST |
| Associate challenge with issued code | MUST |
| Require `code_verifier` if challenge present | MUST |
| Validate verifier against stored challenge | MUST |
| Reject public clients without challenge | MUST |
| Not expose challenge in response | MUST NOT |

### Exemption Conditions

PKCE MAY be skipped only when BOTH:
1. Client is confidential
2. Client properly implements OIDC nonce

Even then, PKCE is RECOMMENDED.

## Token Endpoint Requirements

| Requirement | Priority |
|-------------|----------|
| Accept POST method only | MUST |
| Accept `application/x-www-form-urlencoded` | MUST |
| Ignore unrecognized parameters | MUST |
| Include `Cache-Control: no-store` | MUST |
| Support client credentials in body | MUST |
| Support CORS for browser apps | SHOULD |
| Validate PKCE on code exchange | MUST |
| Enforce single-use codes | MUST |
| Revoke tokens on code reuse | SHOULD |

## Authorization Code Requirements

| Requirement | Priority |
|-------------|----------|
| Maximum 10 minute lifetime | RECOMMENDED |
| Bind to client_id | MUST |
| Bind to code_challenge | MUST |
| Bind to redirect_uri | MUST |
| Single use | MUST |
| Revoke tokens on second valid request | SHOULD |

## Bearer Token Requirements

| Requirement | Priority |
|-------------|----------|
| Support Authorization header | MUST (RS) |
| Query parameter transmission | MUST NOT |
| Ignore query parameter tokens | MUST (RS) |
| Form body when conditions met | MAY |

## Refresh Token Requirements

| Requirement | Priority |
|-------------|----------|
| Bind to issued client | MUST |
| Bind to scope and resources | MUST |
| Verify binding on use | MUST |
| Public client: sender-constrained OR rotation | MUST |
| Confidential client: require authentication | MUST |
| Not guessable/generatable | MUST |

## Redirect URI Requirements

| Requirement | Priority |
|-------------|----------|
| Register complete URI | MUST |
| Exact string comparison | MUST |
| Allow loopback port variation | MUST |
| HTTPS required (except loopback) | MUST |

## HTTP Redirect Requirements

| Requirement | Priority |
|-------------|----------|
| Not use 307 for credential redirects | MUST NOT |
| Use 303 for such redirects | SHOULD |

## Removed Features (MUST NOT Implement)

| Feature | Reason |
|---------|--------|
| `response_type=token` | Token leakage, no sender-constraint |
| `grant_type=password` | Exposes credentials, no MFA |
| Query parameter tokens | Leakage via logs, history |

## Token Response Requirements

| Field | Requirement |
|-------|-------------|
| `access_token` | REQUIRED |
| `token_type` | REQUIRED (case-insensitive) |
| `expires_in` | RECOMMENDED |
| `scope` | REQUIRED if different, RECOMMENDED if same |
| `refresh_token` | OPTIONAL |

## Error Response Requirements

### Error Codes

| Error | Use Case |
|-------|----------|
| `invalid_request` | Missing/invalid parameter |
| `invalid_client` | Client auth failed |
| `invalid_grant` | Invalid code/token |
| `unauthorized_client` | Not authorized for grant |
| `unsupported_grant_type` | Grant not supported |
| `invalid_scope` | Invalid scope |
| `server_error` | Internal error |
| `temporarily_unavailable` | Temporary overload |

### Error Field Constraints

- `error`: %x20-21 / %x23-5B / %x5D-7E
- `error_description`: %x20-21 / %x23-5B / %x5D-7E
- `error_uri`: URI-reference syntax

## Security Recommendations

| Requirement | Priority |
|-------------|----------|
| Use TLS 1.3 | RECOMMENDED |
| Validate TLS certificates | MUST |
| Sender-constrained tokens (DPoP/mTLS) | SHOULD |
| End-to-end TLS | RECOMMENDED |
| Short-lived access tokens | SHOULD |
| Audience restriction | SHOULD |
| Minimum scope | SHOULD |

## Checklist by Component

### Authorization Endpoint

- [ ] Support `code_challenge`
- [ ] Support `code_challenge_method=S256`
- [ ] Reject unsupported methods
- [ ] Store challenge with code
- [ ] Exact redirect_uri matching
- [ ] Loopback port exception
- [ ] Not use 307 redirect
- [ ] Include `iss` in response (optional)

### Token Endpoint

- [ ] POST only
- [ ] Cache-Control: no-store
- [ ] CORS headers for browser apps
- [ ] Validate code_verifier
- [ ] Single-use codes
- [ ] Revoke on reuse
- [ ] Client credentials in body
- [ ] Proper error responses

### Bearer Token Handling

- [ ] Authorization header support
- [ ] No query parameter support
- [ ] Form body (conditional)
- [ ] TLS required

### Refresh Token Handling

- [ ] Client binding
- [ ] Scope/resource binding
- [ ] Sender-constraint (public) OR rotation
- [ ] Client auth (confidential)

### Not Implemented

- [ ] Implicit grant removed
- [ ] Password grant removed
- [ ] Query token removed

## Compliance Testing

Unlike OpenID Connect, there is no official OAuth 2.1 certification program. Verify compliance by:

1. Manual review against specification
2. Security testing
3. Interoperability testing with clients
4. Reviewing implementation against this checklist

## Related Skills

- `oauth21-pkce` - Detailed PKCE implementation
- `oauth21-token-endpoint` - Token endpoint specifics
- `oauth21-bearer-token` - Bearer token handling
- `oauth21-refresh-token` - Refresh token requirements
- `oauth21-security` - Security requirements
