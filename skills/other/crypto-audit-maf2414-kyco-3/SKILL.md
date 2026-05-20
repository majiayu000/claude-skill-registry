---
name: crypto-audit
description: Audit cryptographic implementations for weak algorithms, insecure defaults, predictable randomness, key management issues, and timing attacks. Use when reviewing security-critical crypto code.
---

# Cryptography Audit

## Purpose

Identify cryptographic vulnerabilities including weak algorithms, insecure configurations, predictable randomness, improper key management, and timing side-channels.

## Focus Areas

- **Weak Algorithms**: MD5, SHA1, DES, RC4, ECB mode
- **Insecure Defaults**: Short keys, no salt, weak IVs
- **Predictable Randomness**: Math.random(), time-based seeds
- **Key Management**: Hardcoded keys, keys in code
- **Timing Attacks**: Non-constant-time comparisons
- **Protocol Issues**: SSL/TLS misconfigurations

## Dangerous Patterns

### Weak Hash Functions (Passwords)
```rust
// VULNERABLE - MD5/SHA1 for passwords
let hash = md5::compute(password);
let hash = sha1::digest(password);

// SECURE - Use bcrypt/argon2/scrypt
let hash = bcrypt::hash(password, bcrypt::DEFAULT_COST)?;
```

### Weak Encryption
```python
# VULNERABLE - DES, RC4, ECB mode
cipher = DES.new(key, DES.MODE_ECB)
cipher = ARC4.new(key)
cipher = AES.new(key, AES.MODE_ECB)  # ECB leaks patterns

# SECURE - AES-GCM or ChaCha20-Poly1305
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
```

### Predictable Randomness
```javascript
// VULNERABLE - predictable
const token = Math.random().toString(36);
const id = Date.now();

// SECURE - cryptographic randomness
const token = crypto.randomBytes(32).toString('hex');
```

### Non-Constant-Time Comparison
```go
// VULNERABLE - timing attack
if password == storedHash {
    return true
}

// SECURE - constant time
if subtle.ConstantTimeCompare([]byte(a), []byte(b)) == 1 {
    return true
}
```

## Output Format

```yaml
findings:
  - title: "MD5 used for password hashing"
    severity: high
    attack_scenario: "Attacker cracks MD5 hashes using rainbow tables or GPU cracking"
    preconditions: "Access to password database (via SQLi, backup, breach)"
    reachability: internal_only
    impact: "Mass credential compromise"
    confidence: high
    cwe_id: "CWE-328"
    affected_assets:
      - "src/auth/password.rs:23"
    taint_path: "user.password -> md5::compute() -> db.store()"
```

## Security Requirements by Use Case

### Password Storage
```
Required: bcrypt, argon2, scrypt
Cost factor: >= 10 (bcrypt), memory >= 64MB (argon2)
Salt: Unique per password, >= 16 bytes
```

### Data Encryption
```
Algorithm: AES-256-GCM, ChaCha20-Poly1305
Key size: >= 256 bits
IV/Nonce: Unique per encryption, never reused
Mode: AEAD (authenticated encryption)
```

### Token Generation
```
Source: CSPRNG (crypto/rand, secrets module)
Length: >= 32 bytes (256 bits)
Format: hex or base64url
```

### TLS Configuration
```
Minimum: TLS 1.2 (prefer 1.3)
Ciphers: AEAD only (GCM, ChaCha20)
Certificates: Valid chain, not expired
HSTS: Enabled with long max-age
```

## Severity Guidelines

| Issue | Severity |
|-------|----------|
| MD5/SHA1 for passwords | High |
| No salt for passwords | High |
| DES/RC4 encryption | High |
| ECB mode | Medium-High |
| Math.random() for tokens | High |
| Timing attack on auth | Medium |
| TLS < 1.2 | Medium |
| Hardcoded crypto keys | Critical |
| Reused IV/nonce | High |
| Short key length (<128 bit) | High |

## KYCo Integration

Register cryptographic vulnerability findings:

### 1. Check Active Project
```bash
kyco project list
```

### 2. Register Finding
```bash
kyco finding create \
  --title "MD5 used for password hashing" \
  --project PROJECT_ID \
  --severity high \
  --cwe CWE-328 \
  --attack-scenario "Attacker cracks MD5 hashes using rainbow tables or GPU" \
  --impact "Mass credential compromise" \
  --assets "src/auth/password.rs:23"
```

### Common CWE IDs for Crypto Issues
- CWE-328: Reversible One-Way Hash (weak hash)
- CWE-327: Use of Broken Crypto Algorithm
- CWE-330: Insufficient Random Values
- CWE-321: Hardcoded Cryptographic Key
- CWE-326: Inadequate Encryption Strength
- CWE-916: Password Hash Without Salt
