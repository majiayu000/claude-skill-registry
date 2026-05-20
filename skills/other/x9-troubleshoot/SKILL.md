---
name: x9-troubleshoot
description: Diagnose X9.150 implementation issues — keys, certs, servers, JWKS, common errors
user-invocable: true
tools:
  - Bash
  - Read
  - Glob
  - Grep
context: fork
inject:
  - !ls payee_db/certs/ 2>/dev/null || echo "(no payee certs — run keygen.py)"
  - !ls payer_db/certs/ 2>/dev/null || echo "(no payer certs — run keygen.py)"
  - !lsof -iTCP:5001 -iTCP:5005 -iTCP:5010 -sTCP:LISTEN 2>/dev/null || echo "(no servers running)"
---

# X9.150 Troubleshooter

You diagnose common issues with X9.150 implementations. You check the environment, validate key/cert setup, test server connectivity, and explain error messages.

## Diagnostic Workflow

When the user reports a problem:

1. **Gather context** — what command/operation failed, what error message appeared
2. **Run diagnostics** from the checklist below
3. **Identify root cause** and provide a fix
4. **Verify the fix** if possible

## Diagnostic Checklist

### 1. Key and Certificate Files

Expected files after running `keygen.py`:

```
payee_db/certs/
├── payee_key.pem      # Private key (PKCS8 PEM)
├── payee.jwks         # JWKS with x5c, kid, alg, x5t#S256
└── payee.csr          # Certificate Signing Request

payer_db/certs/
├── payer_key.pem      # Private key (PKCS8 PEM)
├── payer.jwks         # JWKS with x5c, kid, alg, x5t#S256
└── payer.csr          # Certificate Signing Request
```

Check commands:
```bash
# Verify files exist
ls -la payee_db/certs/ payer_db/certs/

# Check private key is valid PEM
openssl ec -in payee_db/certs/payee_key.pem -check -noout 2>&1

# Check JWKS structure
python3.13 -c "import json; j=json.load(open('payee_db/certs/payee.jwks')); print(json.dumps(j, indent=2))"
```

### 2. JWKS Validation

A valid JWKS must have:
```json
{
  "keys": [{
    "kty": "EC",           // or "RSA"
    "crv": "P-256",        // for EC keys
    "alg": "ES256",        // or "RS256"
    "kid": "<key-id>",
    "x5t#S256": "<thumbprint>",
    "x5c": ["<base64-der-cert>"],
    "x": "<base64url>",    // EC public key x coordinate
    "y": "<base64url>"     // EC public key y coordinate
  }]
}
```

Common JWKS issues:
- Missing `alg` field → defaults to ES256, fails with RSA certs
- Missing `x5c` → certificate discovery falls back to `jku`
- Missing `x5t#S256` → cache lookup disabled
- `x5c` uses standard Base64, NOT urlsafe

### 3. Server Connectivity

```bash
# Check which servers are running
lsof -iTCP:5001 -iTCP:5005 -iTCP:5010 -sTCP:LISTEN

# Test certserv (5001)
curl -s http://localhost:5001/certs/payee.jwks | python3.13 -m json.tool

# Test qr_server fetch endpoint (5005) — requires JWS
curl -s -o /dev/null -w "%{http_code}" http://localhost:5005/fetch/test

# Test qr_appserver health (5010) — plain JSON proxy
curl -s http://localhost:5010/
```

### 4. Generated QR Codes and Payloads

```bash
# Check generated payloads
ls -la payee_db/qrs/

# Check generated QR files
ls -la payer_db/qrs/

# Verify a payload is valid JSON
python3.13 -c "import json; print(json.dumps(json.load(open('payee_db/qrs/<id>.json')), indent=2))"
```

### 5. Python Environment

```bash
# Check Python version (must be 3.13)
python3.13 --version

# Check virtual environment
which python3.13

# Check critical dependencies
python3.13 -c "import jose; print('python-jose:', jose.__version__)" 2>&1
python3.13 -c "import flask; print('flask:', flask.__version__)" 2>&1
python3.13 -c "import yaml; print('pyyaml: OK')" 2>&1
python3.13 -c "import jsonschema; print('jsonschema:', jsonschema.__version__)" 2>&1
python3.13 -c "from cryptography import x509; print('cryptography: OK')" 2>&1
```

## Common Error Messages

### "payee_key.pem not found. Run keygen.py first."
**Cause**: Keys haven't been generated yet.
**Fix**: `python3.13 keygen.py`

### "No certificate found in JWS headers or cache"
**Cause**: JWS header lacks `x5c`, `x5t#S256` (no cache hit), and `jku` (or certserv is down).
**Fix**:
- If using self-signed certs: start certserv (`python3.13 certserv.py`)
- If using X9 PKI certs: ensure `x5c` is in the JWKS file
- Check JWKS has `jku` field pointing to running certserv

### "iat is too old (N seconds ago)"
**Cause**: JWS `iat` is more than 480 seconds (8 minutes) old.
**Fix**: System clocks may be out of sync, or the JWS was created too long ago. Re-send the request.

### "JWS has expired (ttl)"
**Cause**: Current time (milliseconds) exceeds the JWS `ttl` field.
**Fix**: The request took too long. Default TTL is 60 seconds. Re-send immediately.

### "Critical header 'X' is missing"
**Cause**: A field listed in `crit` is not present in the JWS header.
**Fix**: Ensure `iat`, `ttl`, and `correlationId` are all in the protected header. Check `--failjwscustom` flag isn't set.

### "correlationId mismatch"
**Cause**: Server returned a different correlationId than the one sent in the request.
**Fix**: Check `--failCorrelationId` flag. In production, this indicates a replay or MITM attack.

### "Invalid Signature"
**Cause**: JWS signature doesn't match the payload/header.
**Fix**: Check `--failSignature` flag. Ensure the signing key matches the certificate in JWKS. Run `python3.13 validatepair.py payee_db/certs/` to verify key pair.

### "Sanctioned wallet"
**Cause**: The payer's blockchain address matches `--sanctionedWallet` argument.
**Fix**: This is a security feature test. Use a different wallet address.

### "Payload not found" (404)
**Cause**: No JSON file exists for the requested payload ID.
**Fix**: Run `qr_generator.py` to generate a payload. Check `payee_db/qrs/` for available IDs.

### "coincurve fails on Python 3.14+"
**Cause**: Python 3.14 has a breaking change in cffi's wheel building.
**Fix**: Use Python 3.13: `python3.13 -m venv venv && source venv/bin/activate`

## Quick Health Check Script

Run all diagnostics at once:
```bash
python3.13 -c "
import os, json, sys

checks = []

# Keys
for role in ['payee', 'payer']:
    key = f'{role}_db/certs/{role}_key.pem'
    jwks = f'{role}_db/certs/{role}.jwks'
    checks.append((f'{role} private key', os.path.exists(key)))
    checks.append((f'{role} JWKS', os.path.exists(jwks)))
    if os.path.exists(jwks):
        j = json.load(open(jwks))
        k = j['keys'][0]
        checks.append((f'{role} JWKS has alg', 'alg' in k))
        checks.append((f'{role} JWKS has x5c', 'x5c' in k))
        checks.append((f'{role} JWKS has x5t#S256', 'x5t#S256' in k))

# Payloads
qrs = os.listdir('payee_db/qrs') if os.path.exists('payee_db/qrs') else []
checks.append((f'Generated payloads', len([f for f in qrs if f.endswith('.json')])))

# Print results
for name, result in checks:
    status = 'OK' if result else 'MISSING'
    if isinstance(result, int):
        status = str(result)
    print(f'  [{status:>7}] {name}')
"
```
