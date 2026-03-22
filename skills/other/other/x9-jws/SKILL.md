---
name: x9-jws
description: JWS security implementation guide — signing, verification, headers, certificate discovery, freshness, non-repudiation
user-invocable: true
tools:
  - Read
  - Glob
  - Grep
---

# X9.150 JWS Security Guide

You are an expert guide for implementing the JWS (JSON Web Signature) security layer of X9.150. You help developers understand signing, verification, protected header construction, certificate discovery, freshness validation, and non-repudiation.

## How to Help

When the developer asks about JWS in X9.150:

1. **Explain the concept** in the context of payment security
2. **Point to reference implementations** in the codebase
3. **Provide code snippets** adapted to the developer's language/framework
4. **Warn about common pitfalls** specific to X9.150

Always read the reference implementations when giving specific guidance:
- `qr_server.py` — `sign_jws()` and `verify_jws()` functions are the canonical implementation
- `qr_payer.py` — payer-side JWS construction and verification

## JWS Structure in X9.150

A JWS token is three Base64url-encoded parts separated by dots: `Header.Payload.Signature`

### Protected Header Construction

```json
{
  "alg": "ES256",
  "typ": "payreq+jws",
  "kid": "<key-id-from-jwks>",
  "iat": 1706745600,
  "ttl": 1706745660000,
  "correlationId": "123e4567-e89b-12d3-a456-426614174000",
  "crit": ["iat", "ttl", "correlationId"],
  "x5t#S256": "<base64url-sha256-thumbprint>",
  "x5c": ["<base64-der-cert>"],
  "jku": "http://localhost:5001/certs/payee.jwks"
}
```

### Key Header Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `alg` | Yes | string | `ES256` (ECC P-256) or `RS256` (RSA) — **read dynamically from JWKS `alg` field** |
| `typ` | Yes | string | `payreq+jws` for requests, `payresp+jws` for responses |
| `kid` | Yes | string | Key identifier from JWKS |
| `iat` | Yes | int64 | Issued At — Unix timestamp in **seconds** |
| `ttl` | Yes | int64 | Time To Live — expiration in Unix **milliseconds** |
| `correlationId` | Yes | UUID | Standard UUID with dashes for request/response linking |
| `crit` | Yes | string[] | Must be `["iat", "ttl", "correlationId"]` |
| `x5t#S256` | Recommended | string | Base64url SHA-256 thumbprint of certificate (for cache lookup) |
| `x5c` | Conditional | string[] | Base64-encoded DER certificate chain (used by X9 PKI certs) |
| `jku` | Conditional | URI | JWKS URL (used by self-signed certs from keygen.py) |

### Algorithm Selection

The algorithm is NOT hardcoded — it's read from the JWKS file:

```python
# From payee.jwks or payer.jwks
jwk_metadata = jwks["keys"][0]
alg = jwk_metadata.get("alg", "ES256")  # ES256 for ECC, RS256 for RSA
```

This supports both ECC (P-256) certificates from `keygen.py` and RSA certificates from X9 Financial PKI.

## Certificate Discovery

Verification follows a strict priority order:

### Priority 1: `x5t#S256` — Thumbprint Cache Lookup
```python
thumbprint = header.get("x5t#S256")
cache_path = f"payee_db/cache/{thumbprint}.pem"
if os.path.exists(cache_path):
    cert = x509.load_pem_x509_certificate(open(cache_path, "rb").read())
```

### Priority 2: `x5c` — Embedded Certificate Chain
```python
if "x5c" in header:
    cert_der = base64.b64decode(header["x5c"][0])  # First cert = leaf
    cert = x509.load_der_x509_certificate(cert_der)
```

### Priority 3: `jku` — Fetch JWKS from URL
```python
if header.get("jku"):
    response = requests.get(header["jku"])
    jwks = response.json()
    for key in jwks["keys"]:
        if key["kid"] == header["kid"] and "x5c" in key:
            cert_der = base64.b64decode(key["x5c"][0])
            cert = x509.load_der_x509_certificate(cert_der)
```

### Thumbprint Calculation
```python
import hashlib, base64
from cryptography.hazmat.primitives.serialization import Encoding

cert_der = cert.public_bytes(Encoding.DER)
sha256 = hashlib.sha256(cert_der).digest()
thumbprint = base64.urlsafe_b64encode(sha256).rstrip(b'=').decode('ascii')
```

### Certificate Caching
After successful verification, cache the certificate by thumbprint:
```python
cache_path = f"cache/{thumbprint}.pem"
with open(cache_path, "wb") as f:
    f.write(cert.public_bytes(Encoding.PEM))
```

## Signing a JWS

Reference: `qr_server.py:sign_jws()`

```python
from jose import jws
import time, uuid

def sign_jws(payload, private_key_pem, correlation_id=None):
    iat = int(time.time())
    ttl = (iat * 1000) + 60000  # 1 minute TTL

    headers = {
        "alg": alg,  # from JWKS
        "typ": "payresp+jws",
        "kid": jwk_metadata["kid"],
        "iat": iat,
        "ttl": ttl,
        "correlationId": correlation_id or str(uuid.uuid4()),
        "crit": ["correlationId", "iat", "ttl"],
        "x5t#S256": thumbprint,
    }
    # Include x5c for PKI certs, jku for self-signed
    if x5c:
        headers["x5c"] = x5c
    elif jku:
        headers["jku"] = jku

    return jws.sign(payload, private_key_pem, headers=headers, algorithm=alg)
```

## Verifying a JWS

Reference: `qr_server.py:verify_jws()` and `validate_jws_headers()`

### Step 1: Extract and Validate Headers
```python
header = jws.get_unverified_header(token)
```

### Step 2: Check Freshness
```python
now = int(time.time())
iat = header.get("iat")
ttl = header.get("ttl")

# iat must not be in the future (60s clock skew)
if iat > now + 60:
    raise ValueError("iat is in the future")

# iat must not be too old (8 minute threshold)
if now - iat > 480:
    raise ValueError(f"iat is too old ({now - iat}s ago)")

# ttl (milliseconds) must not have expired
now_ms = int(time.time() * 1000)
if now_ms > ttl:
    raise ValueError("JWS has expired (ttl)")
```

### Step 3: Enforce `crit` (RFC 7515)
```python
crit = header.get("crit", [])
for field in crit:
    if field not in header:
        raise ValueError(f"Critical header '{field}' is missing")
```

### Step 4: Discover Certificate (see priority order above)

### Step 5: Verify Signature
```python
payload = jws.verify(token, cert.public_key(), algorithms=['ES256', 'RS256'])
```

### Step 6: Validate correlationId (Non-Repudiation)
```python
# For fetch responses: response correlationId must match request correlationId
if response_header["correlationId"] != request_correlation_id:
    raise ValueError("correlationId mismatch — possible replay or MITM")
```

## Common Pitfalls

### 1. iat vs ttl units
- `iat` is in **seconds** (Unix timestamp)
- `ttl` is in **milliseconds** (Unix timestamp × 1000 + offset)
- Computing ttl: `ttl = (iat * 1000) + 60000` (1 min after iat)

### 2. x5c encoding
- `x5c` uses standard Base64 (NOT urlsafe)
- `x5t#S256` uses Base64url (no padding)
- These are different encodings for different purposes

### 3. Content-Type
- All JWS endpoints must use `Content-Type: application/jose`
- The body IS the JWS token string (not JSON-wrapped)

### 4. correlationId flow
- Payer generates a correlationId for the fetch request
- Server MUST echo the same correlationId in the fetch response
- This proves the response was generated for THIS specific request
- For notify, either side can generate the correlationId

### 5. Algorithm hardcoding
- NEVER hardcode `ES256` — always read from JWKS `alg` field
- The system supports both ECC (`ES256`) and RSA (`RS256`) certificates
- X9 Financial PKI uses RSA; self-signed test certs use ECC

### 6. Missing crit enforcement
- If a field is listed in `crit` but absent from the header, the JWS MUST be rejected
- Recipients MUST validate all fields listed in `crit`
- This is per RFC 7515 Section 4.1.11

### 7. Signature corruption detection
- Use `--failSignature` flag to test signature verification
- The server modifies the first character of the signature part
- Your implementation should catch `InvalidSignatureError`

## Testing JWS Security

Use the built-in test flags to verify your implementation handles failures:

```bash
# Test signature verification
python qr_server.py --failSignature

# Test freshness (iat 11 min ago — exceeds 8 min threshold)
python qr_server.py --failiat

# Test TTL expiration
python qr_server.py --failttl

# Test correlationId non-repudiation
python qr_server.py --failCorrelationId

# Test missing mandatory headers
python qr_payer.py --failjwscustom
```
