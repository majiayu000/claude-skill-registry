---
name: jwt-attack-surface
description: Audit JWT implementation for algorithm confusion, secret weakness, claim validation issues, and token handling vulnerabilities. Use when reviewing authentication systems using JWT.
---

# JWT Attack Surface Audit

## Purpose

Identify JWT implementation vulnerabilities including algorithm confusion, weak secrets, missing validation, and token handling issues.

## Focus Areas

- **Algorithm Confusion**: alg=none, RS256→HS256 confusion
- **Weak Secrets**: Short/guessable HMAC secrets
- **Missing Validation**: Signature bypass, claim verification
- **Token Handling**: Storage, transmission, revocation
- **Claim Issues**: Expiration bypass, privilege escalation

## Critical Vulnerabilities

### Algorithm None Attack
```javascript
// VULNERABLE - accepts "alg": "none"
jwt.verify(token, secret, { algorithms: ['HS256', 'none'] });

// SECURE - explicit algorithm whitelist
jwt.verify(token, secret, { algorithms: ['HS256'] });
```

### RS256 to HS256 Confusion
```python
# If server uses RS256 (asymmetric):
# - Attacker gets public key
# - Signs token with public key using HS256
# - Server verifies with public key as HMAC secret

# VULNERABLE - accepts multiple algorithms
jwt.decode(token, public_key, algorithms=['RS256', 'HS256'])

# SECURE - single algorithm only
jwt.decode(token, public_key, algorithms=['RS256'])
```

### Weak HMAC Secret
```javascript
// VULNERABLE - short/guessable secret
const secret = "secret123";
jwt.sign(payload, secret);

// SECURE - strong random secret (>= 256 bits)
const secret = crypto.randomBytes(64).toString('hex');
```

### Missing Expiration Check
```go
// VULNERABLE - ignoring exp claim
claims, _ := jwt.Parse(token, keyFunc)
// No expiration validation!

// SECURE - validate expiration
claims, err := jwt.ParseWithClaims(token, &Claims{}, keyFunc)
if err != nil || claims.ExpiresAt.Before(time.Now()) {
    return ErrExpired
}
```

## Output Format

```yaml
findings:
  - title: "JWT accepts 'none' algorithm"
    severity: critical
    attack_scenario: "Attacker crafts unsigned JWT with alg=none, bypasses authentication"
    preconditions: "None"
    reachability: public
    impact: "Complete authentication bypass"
    confidence: high
    cwe_id: "CWE-327"
    affected_assets:
      - "src/auth/jwt.rs:45"
      - "/api/auth/verify"
```

## Audit Checklist

### Token Generation
```
[ ] Secret is cryptographically random (>= 256 bits)
[ ] Algorithm is explicitly set (not from token)
[ ] Claims include: iat, exp, iss, aud
[ ] Expiration is reasonable (< 24h for access tokens)
[ ] Sensitive data not in payload (use references)
```

### Token Verification
```
[ ] Algorithm whitelist (single algorithm preferred)
[ ] Signature verification BEFORE parsing claims
[ ] Expiration (exp) validated
[ ] Issuer (iss) validated
[ ] Audience (aud) validated
[ ] Not-before (nbf) validated if present
```

### Token Handling
```
[ ] Stored in httpOnly cookie (not localStorage)
[ ] Transmitted over HTTPS only
[ ] Revocation mechanism exists
[ ] Refresh token rotation implemented
[ ] Token not leaked in URLs/logs
```

## Attack Scenarios

### 1. None Algorithm
```
Header: {"alg": "none", "typ": "JWT"}
Payload: {"sub": "admin", "role": "admin"}
Signature: (empty)
```

### 2. Key Confusion (RS256→HS256)
```
# Get public key from /api/.well-known/jwks.json
# Sign with public key using HS256
# Server uses public key as HMAC secret
```

### 3. Weak Secret Brute Force
```
# Tools: hashcat, jwt_tool
hashcat -m 16500 jwt.txt wordlist.txt
```

### 4. Claim Tampering
```
# Modify claims if signature not verified
{"sub": "user", "role": "user"} → {"sub": "admin", "role": "admin"}
```

## Severity Guidelines

| Issue | Severity |
|-------|----------|
| alg=none accepted | Critical |
| Algorithm confusion possible | Critical |
| Weak/guessable secret | Critical |
| No signature verification | Critical |
| No expiration validation | High |
| Token in URL/logs | High |
| No issuer/audience validation | Medium |
| Token in localStorage | Medium |
| Long expiration (> 24h) | Low |

## KYCo Integration

Register JWT implementation vulnerabilities:

### 1. Check Active Project
```bash
kyco project list
```

### 2. Register Finding
```bash
kyco finding create \
  --title "JWT accepts 'none' algorithm" \
  --project PROJECT_ID \
  --severity critical \
  --cwe CWE-327 \
  --attack-scenario "Attacker crafts unsigned JWT with alg=none, bypasses authentication" \
  --impact "Complete authentication bypass" \
  --assets "src/auth/jwt.rs:45,/api/auth/verify"
```

### 3. Import Scanner Results
```bash
# Import semgrep JWT rules
semgrep --config p/jwt --sarif -o jwt-audit.sarif .
kyco finding import jwt-audit.sarif --project PROJECT_ID
```

### Common CWE IDs for JWT Issues
- CWE-327: Use of Broken or Risky Cryptographic Algorithm
- CWE-287: Improper Authentication
- CWE-347: Improper Verification of Cryptographic Signature
- CWE-798: Use of Hard-coded Credentials (weak secret)
- CWE-613: Insufficient Session Expiration
