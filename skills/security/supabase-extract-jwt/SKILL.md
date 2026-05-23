---
name: supabase-extract-jwt
description: Extract and decode Supabase-related JWTs from client-side code, cookies, and local storage patterns.
---

# Supabase JWT Extraction

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write to context files **AS YOU GO**, not just at the end.
> - Write to `.sb-pentest-context.json` **IMMEDIATELY after each discovery**
> - Log to `.sb-pentest-audit.log` **BEFORE and AFTER each action**
> - **DO NOT** wait until the skill completes to update files
> - If the skill crashes or is interrupted, all prior findings must already be saved
>
> **This is not optional. Failure to write progressively is a critical error.**

This skill extracts and analyzes JSON Web Tokens (JWTs) related to Supabase from client-side code.

## When to Use This Skill

- To find all JWT tokens exposed in client code
- To analyze token claims and expiration
- To detect hardcoded user tokens (security issue)
- To understand the authentication flow

## Prerequisites

- Target application accessible
- Supabase detection completed (auto-invokes if needed)

## Types of JWTs in Supabase

| Type | Purpose | Client Exposure |
|------|---------|-----------------|
| Anon Key | API authentication | ✅ Expected |
| Service Role Key | Admin access | ❌ Never |
| Access Token | User session | ⚠️ Dynamic only |
| Refresh Token | Token renewal | ⚠️ Dynamic only |

## Detection Patterns

### 1. API Keys (Static)

```javascript
// Supabase API keys are JWTs
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
```

### 2. Hardcoded User Tokens (Problem)

```javascript
// ❌ Should never be hardcoded
const userToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIn0...'
```

### 3. Storage Key Patterns

```javascript
// Code referencing where JWTs are stored
localStorage.getItem('supabase.auth.token')
localStorage.getItem('sb-abc123-auth-token')
sessionStorage.getItem('supabase_session')
```

## Usage

### Basic Extraction

```
Extract JWTs from https://myapp.example.com
```

### With Claim Analysis

```
Extract and analyze all JWTs from https://myapp.example.com
```

## Output Format

```
═══════════════════════════════════════════════════════════
 JWT EXTRACTION RESULTS
═══════════════════════════════════════════════════════════

 Found: 3 JWTs

 ─────────────────────────────────────────────────────────
 JWT #1: Supabase Anon Key
 ─────────────────────────────────────────────────────────
 Type: API Key (anon)
 Status: ✅ Expected in client code

 Header:
 ├── alg: HS256
 └── typ: JWT

 Payload:
 ├── iss: supabase
 ├── ref: abc123def
 ├── role: anon
 ├── iat: 2021-12-20T00:00:00Z
 └── exp: 2031-12-20T00:00:00Z

 Location: /static/js/main.js:1247

 ─────────────────────────────────────────────────────────
 JWT #2: Hardcoded User Token ⚠️
 ─────────────────────────────────────────────────────────
 Type: User Access Token
 Status: ⚠️ P1 - Should not be hardcoded

 Header:
 ├── alg: HS256
 └── typ: JWT

 Payload:
 ├── sub: 12345678-1234-1234-1234-123456789012
 ├── email: developer@company.com
 ├── role: authenticated
 ├── iat: 2025-01-15T10:00:00Z
 └── exp: 2025-01-15T11:00:00Z (EXPIRED)

 Location: /static/js/debug.js:45

 Risk: This token may belong to a real user account.
       Even if expired, it reveals user information.

 ─────────────────────────────────────────────────────────
 JWT #3: Storage Reference
 ─────────────────────────────────────────────────────────
 Type: Storage Key Pattern
 Status: ℹ️ Informational

 Pattern: localStorage.getItem('sb-abc123def-auth-token')
 Location: /static/js/auth.js:89

 Note: This is the expected storage key for user sessions.
       Actual token value is set at runtime.

═══════════════════════════════════════════════════════════
```

## JWT Claim Analysis

The skill identifies key claims:

### Standard Claims

| Claim | Description | Security Impact |
|-------|-------------|-----------------|
| `sub` | User ID | Identifies specific user |
| `email` | User email | PII exposure if hardcoded |
| `role` | Permission level | `service_role` is critical |
| `exp` | Expiration | Expired tokens less risky |
| `iat` | Issued at | Indicates when created |

### Supabase-Specific Claims

| Claim | Description |
|-------|-------------|
| `ref` | Project reference |
| `iss` | Should be "supabase" |
| `aal` | Authenticator assurance level |
| `amr` | Authentication methods used |

## Security Findings

### P0 - Critical

```
🔴 Service role key exposed (role: service_role)
   → Immediate key rotation required
```

### P1 - High

```
🟠 User token hardcoded with PII (email, sub visible)
   → Remove from code, may need to notify user
```

### P2 - Medium

```
🟡 Expired test token in code
   → Clean up, potential information disclosure
```

## Context Output

Saved to `.sb-pentest-context.json`:

```json
{
  "jwts": {
    "found": 3,
    "api_keys": [
      {
        "type": "anon",
        "project_ref": "abc123def",
        "location": "/static/js/main.js:1247"
      }
    ],
    "user_tokens": [
      {
        "type": "access_token",
        "hardcoded": true,
        "severity": "P1",
        "claims": {
          "sub": "12345678-1234-1234-1234-123456789012",
          "email": "developer@company.com",
          "expired": true
        },
        "location": "/static/js/debug.js:45"
      }
    ],
    "storage_patterns": [
      {
        "pattern": "sb-abc123def-auth-token",
        "storage": "localStorage",
        "location": "/static/js/auth.js:89"
      }
    ]
  }
}
```

## Common Issues

❌ **Problem:** JWT appears truncated
✅ **Solution:** May span multiple lines. The skill attempts to reassemble.

❌ **Problem:** JWT won't decode
✅ **Solution:** May be encrypted (JWE) or custom format. Noted as undecodable.

❌ **Problem:** Many false positives
✅ **Solution:** Base64 strings that look like JWTs. Skill validates structure.

## Remediation for Hardcoded Tokens

### Before (Wrong)

```javascript
// ❌ Never hardcode user tokens
const adminToken = 'eyJhbGciOiJIUzI1NiI...'
fetch('/api/admin', {
  headers: { Authorization: `Bearer ${adminToken}` }
})
```

### After (Correct)

```javascript
// ✅ Get token from Supabase session
const { data: { session } } = await supabase.auth.getSession()
fetch('/api/admin', {
  headers: { Authorization: `Bearer ${session.access_token}` }
})
```

## MANDATORY: Progressive Context File Updates

⚠️ **This skill MUST update tracking files PROGRESSIVELY during execution, NOT just at the end.**

### Critical Rule: Write As You Go

**DO NOT** batch all writes at the end. Instead:

1. **Before starting any action** → Log the action to `.sb-pentest-audit.log`
2. **After each discovery** → Immediately update `.sb-pentest-context.json`
3. **After each significant step** → Log completion to `.sb-pentest-audit.log`

This ensures that if the skill is interrupted, crashes, or times out, all findings up to that point are preserved.

### Required Actions (Progressive)

1. **Update `.sb-pentest-context.json`** with extracted data:
   ```json
   {
     "jwts": {
       "found": 3,
       "api_keys": [ ... ],
       "user_tokens": [ ... ],
       "storage_patterns": [ ... ]
     }
   }
   ```

2. **Log to `.sb-pentest-audit.log`**:
   ```
   [TIMESTAMP] [supabase-extract-jwt] [START] Beginning JWT extraction
   [TIMESTAMP] [supabase-extract-jwt] [SUCCESS] Found 3 JWTs
   [TIMESTAMP] [supabase-extract-jwt] [CONTEXT_UPDATED] .sb-pentest-context.json updated
   ```

3. **If files don't exist**, create them before writing.

**FAILURE TO UPDATE CONTEXT FILES IS NOT ACCEPTABLE.**

## MANDATORY: Evidence Collection

📁 **Evidence Directory:** `.sb-pentest-evidence/02-extraction/`

### Evidence Files to Create

| File | Content |
|------|---------|
| `extracted-jwts.json` | All JWTs found with analysis |

### Evidence Format

```json
{
  "evidence_id": "EXT-JWT-001",
  "timestamp": "2025-01-31T10:08:00Z",
  "category": "extraction",
  "type": "jwt_extraction",

  "jwts_found": [
    {
      "type": "anon_key",
      "severity": "info",
      "location": "/static/js/main.js:1247",
      "decoded_payload": {
        "iss": "supabase",
        "ref": "abc123def",
        "role": "anon"
      }
    },
    {
      "type": "hardcoded_user_token",
      "severity": "P1",
      "location": "/static/js/debug.js:45",
      "decoded_payload": {
        "sub": "[REDACTED]",
        "email": "[REDACTED]@example.com",
        "role": "authenticated",
        "exp": "2025-01-15T11:00:00Z"
      },
      "expired": true,
      "issue": "Hardcoded user token with PII"
    }
  ],

  "storage_patterns_found": [
    {
      "pattern": "localStorage.getItem('sb-abc123def-auth-token')",
      "location": "/static/js/auth.js:89"
    }
  ]
}
```

## Related Skills

- `supabase-extract-anon-key` — Specifically extracts the anon key
- `supabase-extract-service-key` — Checks for service key (critical)
- `supabase-audit-auth-config` — Analyzes auth configuration
