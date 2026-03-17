---
name: scope-claims-reviewer
description: Review test cases for Scope and Claims handling. Covers openid scope requirement, standard scopes (profile, email, address, phone), claims request parameter, and claim types per OIDC Core 1.0 Section 5.4 and 5.5.
---

# Scope and Claims Test Case Reviewer

Review test cases for Scope and Claims handling in OpenID Connect Basic OP.

## Scope

- **Feature**: Scope and Claims
- **Specifications**: OIDC Core 1.0 Section 5.4, 5.5
- **Profile**: Basic OP

## Review Process

1. Identify which scope/claims requirement the test targets
2. Check against the checklist below
3. Verify both success and error scenarios
4. Ensure claim filtering based on scope works correctly
5. Report gaps with specific spec section references

## OpenID Scope (Mandatory)

### OP-scope-openid

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | MUST support `openid` scope | OIDC Core 3.1.2.1 |
| [ ] | `openid` scope REQUIRED in auth request | OIDC Core 3.1.2.1 |
| [ ] | Return `invalid_scope` if openid missing | OIDC Core 3.1.2.1 |

## Standard Scopes

### Scope Definitions

| Scope | Description | Spec Reference |
|-------|-------------|----------------|
| `openid` | Required for OIDC requests | OIDC Core 3.1.2.1 |
| `profile` | Basic profile information | OIDC Core 5.4 |
| `email` | Email address and verification | OIDC Core 5.4 |
| `address` | Postal address | OIDC Core 5.4 |
| `phone` | Phone number and verification | OIDC Core 5.4 |
| `offline_access` | Refresh token (if supported) | OIDC Core 11 |

## Scope to Claims Mapping

### profile Scope

| Check | Claim | Type | Spec Reference |
|-------|-------|------|----------------|
| [ ] | `name` | string | OIDC Core 5.1 |
| [ ] | `family_name` | string | OIDC Core 5.1 |
| [ ] | `given_name` | string | OIDC Core 5.1 |
| [ ] | `middle_name` | string | OIDC Core 5.1 |
| [ ] | `nickname` | string | OIDC Core 5.1 |
| [ ] | `preferred_username` | string | OIDC Core 5.1 |
| [ ] | `profile` | string (URL) | OIDC Core 5.1 |
| [ ] | `picture` | string (URL) | OIDC Core 5.1 |
| [ ] | `website` | string (URL) | OIDC Core 5.1 |
| [ ] | `gender` | string | OIDC Core 5.1 |
| [ ] | `birthdate` | string (YYYY-MM-DD) | OIDC Core 5.1 |
| [ ] | `zoneinfo` | string (timezone) | OIDC Core 5.1 |
| [ ] | `locale` | string (BCP47) | OIDC Core 5.1 |
| [ ] | `updated_at` | number (Unix time) | OIDC Core 5.1 |

### email Scope

| Check | Claim | Type | Spec Reference |
|-------|-------|------|----------------|
| [ ] | `email` | string | OIDC Core 5.1 |
| [ ] | `email_verified` | boolean | OIDC Core 5.1 |

### address Scope

| Check | Claim | Type | Spec Reference |
|-------|-------|------|----------------|
| [ ] | `address` | JSON object | OIDC Core 5.1.1 |

Address object fields:
- `formatted` - Full mailing address
- `street_address` - Street address (may include newlines)
- `locality` - City or locality
- `region` - State, province, prefecture
- `postal_code` - Zip or postal code
- `country` - Country name

### phone Scope

| Check | Claim | Type | Spec Reference |
|-------|-------|------|----------------|
| [ ] | `phone_number` | string (E.164) | OIDC Core 5.1 |
| [ ] | `phone_number_verified` | boolean | OIDC Core 5.1 |

## Claims in ID Token vs UserInfo

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | `sub` always in ID Token | OIDC Core 2 |
| [ ] | Other claims MAY be in ID Token or UserInfo | OIDC Core 5.3 |
| [ ] | Claims based on requested scopes | OIDC Core 5.4 |

## Test Case Categories

### OpenID Scope Tests

- [ ] Valid: Request with `scope=openid`
- [ ] Valid: Request with `scope=openid profile`
- [ ] Invalid: Request without openid scope
- [ ] Error: Returns `invalid_scope`

### Profile Scope Tests

- [ ] Valid: Profile claims returned when scope=profile
- [ ] Valid: Only available claims returned (not all required)
- [ ] Valid: No error if some claims unavailable

### Email Scope Tests

- [ ] Valid: email and email_verified returned
- [ ] Valid: email_verified is boolean

### Address Scope Tests

- [ ] Valid: address object returned
- [ ] Valid: address contains expected fields
- [ ] Valid: formatted field contains full address

### Phone Scope Tests

- [ ] Valid: phone_number returned (E.164 format)
- [ ] Valid: phone_number_verified is boolean

### Multiple Scopes Tests

- [ ] Valid: `scope=openid profile email`
- [ ] Valid: Combined claims from all scopes
- [ ] Valid: Unknown scopes ignored (no error)

### Claim Location Tests

- [ ] Valid: Claims in UserInfo endpoint
- [ ] Valid: Claims in ID Token (if configured)
- [ ] Valid: `sub` consistent across both

## Handling Unknown/Unsupported Scopes

| Check | Requirement | Spec Reference |
|-------|-------------|----------------|
| [ ] | MAY ignore unknown scopes | OIDC Core 3.1.2.1 |
| [ ] | Return granted scopes if different | OAuth 2.1 4.1.4 |
| [ ] | No error for unsupported optional scopes | OIDC Core 5.4 |

## Error Cases

| Scenario | Error Code | Spec Reference |
|----------|------------|----------------|
| Missing openid scope | `invalid_scope` | OIDC Core 3.1.2.1 |
| Invalid scope format | `invalid_scope` | OAuth 2.1 4.1.2.1 |

## Conformance Test IDs

| Test ID | Feature |
|---------|---------|
| OP-scope-openid | openid scope required |
| OP-scope-profile | profile scope handling |
| OP-scope-email | email scope handling |
| OP-scope-address | address scope handling |
| OP-scope-phone | phone scope handling |
| OP-scope-All | Multiple scopes combined |

## Review Output Format

```
## Test Case: [Name]
### Target Feature: Scope/Claims - [specific scope or claim]
### Test ID: OP-scope-[xxx] or OP-claims-[xxx]
### Spec Compliance:
- [x] Covers required behavior per [spec section]
- [ ] Missing: [specific requirement]
### Scope Handling:
- [x/blank] openid scope enforced
- [x/blank] Correct claims for scope
### Verdict: PASS / FAIL / PARTIAL
### Recommendations: [if any]
```
