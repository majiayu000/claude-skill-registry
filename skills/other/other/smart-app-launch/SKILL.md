---
name: smart-app-launch
description: Expert guidance for implementing SMART App Launch (HL7 FHIR specification for OAuth 2.0-based authorization). Use this skill when implementing FHIR app authorization, EHR launch sequences, standalone app launch, backend services authentication, SMART scopes, token handling, or capability discovery. Trigger keywords include "SMART", "SMART on FHIR", "EHR launch", "standalone launch", "FHIR authorization", "FHIR OAuth", "backend services", "system scopes", "patient scopes", "fhirUser", ".well-known/smart-configuration", "PKCE", "client_credentials", "launch context".
---

# SMART App Launch

SMART App Launch provides a standardised OAuth 2.0-based authorization framework for FHIR applications. It enables apps to securely access healthcare data with appropriate user consent and context.

## Choosing a launch pattern

Select the appropriate pattern based on your use case:

| Pattern               | Use when                           | Grant type           |
| --------------------- | ---------------------------------- | -------------------- |
| **EHR Launch**        | App launched from within EHR UI    | `authorization_code` |
| **Standalone Launch** | App launched independently by user | `authorization_code` |
| **Backend Services**  | Server-to-server, no user present  | `client_credentials` |

## Core workflow

### Step 1: Discover server capabilities

Fetch `{fhir-base}/.well-known/smart-configuration` to discover:

- `authorization_endpoint` and `token_endpoint`
- `capabilities` array (launch modes, client types, permission models)
- `code_challenge_methods_supported` (must include `S256`)

See [references/capability-discovery.md](references/capability-discovery.md) for full field reference.

### Step 2: Choose client authentication

| Client type               | Method               | Registration                  |
| ------------------------- | -------------------- | ----------------------------- |
| Public                    | PKCE only, no secret | `client_id` only              |
| Confidential (symmetric)  | Client secret        | Secret shared at registration |
| Confidential (asymmetric) | Private key JWT      | JWKS URL or keys registered   |

Backend services require asymmetric authentication. See [references/client-authentication.md](references/client-authentication.md).

### Step 3: Request authorization

**EHR Launch**: App receives `iss` and `launch` parameters, echoes `launch` in authorization request.

**Standalone Launch**: App initiates flow, may request `launch/patient` or `launch/encounter` to establish context.

Required authorization parameters:

- `response_type=code`
- `client_id`, `redirect_uri`, `scope`, `state` (122+ bits entropy)
- `aud` (FHIR server base URL)
- `code_challenge` + `code_challenge_method=S256`

See [references/app-launch.md](references/app-launch.md) for complete flow details.

### Step 4: Exchange code for tokens

POST to token endpoint with:

- `grant_type=authorization_code`
- `code`, `redirect_uri`, `code_verifier`
- Client authentication (if confidential)

Token response includes:

- `access_token`, `token_type`, `scope`, `expires_in`
- Optional: `refresh_token`, `id_token`, launch context (`patient`, `encounter`)

### Step 5: Access FHIR resources

```http
GET {fhir-base}/Patient/123
Authorization: Bearer {access_token}
```

## Scopes quick reference

```
patient/Observation.rs     # Read + search patient observations
user/Appointment.cruds     # Full access to user's appointments
system/Patient.rs          # Backend service read/search all patients
launch/patient             # Request patient context at launch
openid fhirUser            # Get user identity via OIDC
offline_access             # Request refresh token
```

Scope syntax: `{context}/{resource}.{permissions}[?{constraints}]`

See [references/scopes.md](references/scopes.md) for complete scope grammar and examples.

## Backend services

For server-to-server access without user interaction:

1. Register client with JWKS URL
2. Create signed JWT assertion with required claims (`iss`, `sub`, `aud`, `exp`, `jti`)
3. POST to token endpoint with `grant_type=client_credentials` and `client_assertion`
4. Use `system/` scopes only

See [references/backend-services.md](references/backend-services.md) for JWT structure and examples.

## Security requirements

- PKCE with S256 is mandatory for all authorization code flows
- TLS 1.2+ required for all token transmission
- Access tokens should expire within 1 hour (5 minutes for backend services)
- Validate `state` parameter to prevent CSRF
- Validate `aud` matches your FHIR endpoint

See [references/security.md](references/security.md) for comprehensive security guidance.

## References

- [references/app-launch.md](references/app-launch.md) - EHR and standalone launch flows
- [references/scopes.md](references/scopes.md) - Scope syntax and permissions
- [references/backend-services.md](references/backend-services.md) - System-to-system authentication
- [references/client-authentication.md](references/client-authentication.md) - Authentication methods
- [references/capability-discovery.md](references/capability-discovery.md) - .well-known endpoint
- [references/security.md](references/security.md) - Best practices and security
