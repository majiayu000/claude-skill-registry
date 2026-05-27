---
version: 1.0.0
name: bitcoin-auth-diagnostics
description: Diagnose and troubleshoot bitcoin-auth token generation and verification issues. This skill should be used when users encounter authentication failures, signature verification errors, or integration problems with the bitcoin-auth library.
location: user
---

# Bitcoin Auth Diagnostics

## Overview

This skill enables comprehensive diagnosis of bitcoin-auth authentication issues across client and server implementations. Use this skill when encountering token generation failures, signature verification errors, or integration problems with the bitcoin-auth library.

## When to Use This Skill

Use this skill when:
- Bitcoin auth token verification is failing
- Investigating "invalid signature" or "invalid token" errors
- Debugging integration with bitcoin-auth in APIs (especially Sigma Auth)
- Token generation produces unexpected results
- Time skew or timestamp-related authentication failures occur
- Body hash mismatches are suspected
- Scheme confusion between bsm and brc77 exists

## Bitcoin Auth Token Format

All bitcoin-auth tokens follow this pipe-delimited format:

```
pubkey|scheme|timestamp|requestPath|signature
```

**Components:**
- `pubkey`: Hex-encoded public key (66 characters)
- `scheme`: Either `bsm` (legacy) or `brc77` (recommended)
- `timestamp`: ISO8601 format (e.g., `2025-01-15T14:30:00.000Z`)
- `requestPath`: Full path including query parameters (e.g., `/api/endpoint?param=value`)
- `signature`: Base64-encoded signature

**Example valid token:**
```
02a1b2c3d4e5f6...|brc77|2025-01-15T14:30:00.123Z|/api/status|dGVzdHNpZ25hdHVyZQ==
```

## Diagnostic Workflow

### Step 1: Token Structure Validation

First, validate the token structure before checking cryptographic validity:

```typescript
import { parseAuthToken } from 'bitcoin-auth';

const token = "..."; // The failing token
const parsed = parseAuthToken(token);

if (!parsed) {
  console.error("FAILED: Token structure is invalid");
  // Check: Does token have exactly 5 pipe-delimited parts?
  const parts = token.split('|');
  console.log(`Token has ${parts.length} parts (expected 5)`);
  console.log("Parts:", parts);

  // Common issues:
  // - Missing parts (incomplete token)
  // - Extra pipes in requestPath or other fields
  // - Invalid scheme (not 'bsm' or 'brc77')
} else {
  console.log("✅ Token structure is valid");
  console.log("Parsed token:", parsed);
}
```

### Step 2: Component Validation

Validate each component individually:

```typescript
const { pubkey, scheme, timestamp, requestPath, signature } = parsed;

// Validate public key
console.log("Public key length:", pubkey.length); // Should be 66 chars
console.log("Public key starts with 02/03:", pubkey.startsWith('02') || pubkey.startsWith('03'));

// Validate scheme
console.log("Scheme:", scheme); // Must be 'bsm' or 'brc77'

// Validate timestamp
const tokenTime = new Date(timestamp);
console.log("Token timestamp:", tokenTime.toISOString());
console.log("Current time:", new Date().toISOString());
console.log("Age (minutes):", (Date.now() - tokenTime.getTime()) / 60000);
// Default timePad is 5 minutes - token older than 5 minutes will fail

// Validate request path
console.log("Request path:", requestPath);
// Must match EXACTLY including query parameters and their order

// Validate signature
console.log("Signature (base64):", signature);
console.log("Signature length:", signature.length);
```

### Step 3: Signature Verification

If structure is valid, diagnose verification failures:

```typescript
import { verifyAuthToken } from 'bitcoin-auth';
import type { AuthPayload } from 'bitcoin-auth';

const authPayload: AuthPayload = {
  requestPath: "/api/endpoint?param=value", // Must match token exactly
  timestamp: new Date().toISOString(),       // Server's current time
  body: requestBody // Optional, must match if token was signed with body
};

const isValid = verifyAuthToken(
  token,
  authPayload,
  5,        // timePad in minutes (default 5)
  'utf8'    // bodyEncoding: 'utf8', 'hex', or 'base64'
);

if (!isValid) {
  console.error("FAILED: Signature verification failed");

  // Diagnose specific failures:

  // 1. Request path mismatch
  if (parsed.requestPath !== authPayload.requestPath) {
    console.error("❌ Request path mismatch:");
    console.error("  Token path:", parsed.requestPath);
    console.error("  Verify path:", authPayload.requestPath);
    // Common issue: Query parameter order differs
  }

  // 2. Timestamp issues
  const tokenTimestamp = new Date(parsed.timestamp);
  const targetTime = new Date(authPayload.timestamp);
  targetTime.setMinutes(targetTime.getMinutes() + 5); // Add timePad
  if (tokenTimestamp > targetTime) {
    console.error("❌ Token timestamp too far in future");
    console.error("  Token time:", tokenTimestamp.toISOString());
    console.error("  Target time:", targetTime.toISOString());
  }

  // 3. Body hash mismatch
  if (authPayload.body) {
    console.log("Verifying with body present");
    console.log("  Body encoding:", 'utf8'); // Check encoding matches
    console.log("  Body length:", authPayload.body.length);
    // Try different encodings if utf8 fails
  }

  // 4. Scheme-specific issues
  if (parsed.scheme === 'bsm') {
    console.log("Using legacy BSM signature scheme");
    // BSM uses different signature format than BRC77
  } else {
    console.log("Using BRC77 signature scheme (recommended)");
  }
}
```

### Step 4: Common Integration Issues

Check for common integration mistakes:

**Server-side (verification):**
```typescript
// ❌ WRONG: Using token's timestamp (defeats the purpose)
const authPayload = {
  requestPath,
  timestamp: parsedToken.timestamp, // DON'T DO THIS
  body
};

// ✅ CORRECT: Use server's current time
const serverTime = new Date().toISOString();
const authPayload = {
  requestPath,
  timestamp: serverTime,
  body
};
```

**Client-side (generation):**
```typescript
// ✅ Token generation
import { getAuthToken } from 'bitcoin-auth';

const token = getAuthToken({
  privateKeyWif,
  requestPath: '/api/endpoint?param=value', // Include full path with query
  body: JSON.stringify(requestBody),        // If POST/PUT with body
  scheme: 'brc77',                          // Default, recommended
  bodyEncoding: 'utf8'                      // Default
});

// Include in request headers
fetch(url + requestPath, {
  method: 'POST',
  headers: {
    'X-Auth-Token': token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(requestBody)
});
```

## Common Error Patterns

### "Invalid bitcoin-auth token format"

**Cause**: Token doesn't have exactly 5 pipe-delimited parts

**Solutions:**
- Check token isn't truncated or corrupted
- Verify no extra pipes in requestPath or signature
- Ensure token is properly URL-encoded if passed in query params

### "Bitcoin signature verification failed"

**Cause**: Signature doesn't match the payload

**Solutions:**
1. Verify request path matches exactly (including query params)
2. Check timestamp isn't older than timePad (default 5 minutes)
3. Ensure body hash matches (if body present)
4. Confirm correct bodyEncoding (utf8, hex, base64)
5. Verify scheme matches (bsm vs brc77)

### "Invalid token: time skew"

**Cause**: Token timestamp too far from server time

**Solutions:**
- Increase timePad parameter (default 5 minutes)
- Check client/server clock synchronization
- Verify timestamp format is ISO8601

### "Request path mismatch"

**Cause**: Token requestPath doesn't match verification path

**Solutions:**
- Include full path with query parameters
- Ensure query parameter order is consistent
- Don't include domain/protocol in requestPath
- Match case sensitivity

### "Body hash mismatch"

**Cause**: Body used for signing doesn't match verification body

**Solutions:**
- Use exact same body string (not re-serialized JSON)
- Check bodyEncoding matches (utf8, hex, base64)
- Verify body isn't modified between signing and verification
- Ensure Content-Type header matches body encoding

## Integration with Sigma Auth

When working with Sigma Auth (auth.sigmaidentity.com), common patterns:

**Better Auth / Sigma Plugin issues** (403 on token exchange, CSRF/trustedOrigins, callback URL mismatches) are covered in `references/common-issues.md` under "Better Auth / Sigma Plugin Issues".

**Token verification endpoint:**
```typescript
// POST /api/auth/token-for-endpoint
// Body: { authToken: "...", requestBody: "..." }

// Server parses and verifies:
const parsed = parseAuthToken(authToken);
const authPayload = {
  requestPath: "/api/auth/token-for-endpoint",
  timestamp: new Date().toISOString(),
  body: requestBody
};
const isValid = verifyAuthToken(authToken, authPayload);
```

**Wallet connect flow:**
```typescript
// Uses BSM scheme for compatibility
const token = getAuthToken({
  privateKeyWif,
  requestPath: "/wallet/connect",
  scheme: 'bsm'
});
```

## Reference Documentation

For detailed API documentation and implementation examples, see:
- `references/bitcoin-auth-api.md` - Complete API reference
- `references/common-issues.md` - Detailed troubleshooting guide
- `references/identity-terminology.md` - BAP ID vs BRC-31 identity key terminology matrix
- Bitcoin Auth GitHub: https://github.com/b-open-io/bitcoin-auth
- BRC-77 Specification: https://github.com/bitcoin-sv/BRCs/blob/master/peer-to-peer/0077.md

## Environment Requirements

- Node.js/Bun runtime with `@bsv/sdk` peer dependency
- bitcoin-auth library installed: `bun add bitcoin-auth`
- For testing: Access to bitcoin-auth repository test suite

## Security Considerations

**Never log private keys or WIF strings** - Only log public keys, tokens, and diagnostic information.

When diagnosing authentication issues:
- Use test/development keys for diagnostics
- Sanitize logs before sharing (remove signatures/private data)
- Verify token expiry (timePad) is appropriate for your use case
- Use BRC77 scheme (default) for new implementations
