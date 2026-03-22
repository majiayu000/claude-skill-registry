---
name: x9-inspect-cert
description: Inspect JWKS files and certificate chains — x5c details, fingerprints, key pair validation
user-invocable: true
tools:
  - Bash
  - Read
  - Glob
context: fork
inject:
  - !find payee_db/certs payer_db/certs -name "*.jwks" -o -name "*_key.pem" 2>/dev/null || echo "(no cert files found)"
---

# X9.150 Certificate Inspector

You inspect JWKS files and certificate chains for X9.150 implementations. You wrap the project's `opencert.py` and `validatepair.py` utilities and interpret their output.

## Instructions

When the user asks to inspect certificates or keys:

1. **Identify the target** — which JWKS file or cert folder to inspect:
   - `payee_db/certs/payee.jwks` — payee certificate chain
   - `payer_db/certs/payer.jwks` — payer certificate chain
   - A custom JWKS file path provided by the user

2. **Run the appropriate tool**:
   - **Certificate chain inspection**: `python3.13 opencert.py <jwks_file>`
   - **Key pair validation**: `python3.13 validatepair.py <certs_folder>`

3. **Interpret and explain** the output

## Certificate Chain Inspection

```bash
python3.13 opencert.py payee_db/certs/payee.jwks
```

This displays for each certificate in the `x5c` chain:
- Subject and Issuer (RFC 4514 format)
- Serial Number
- Validity period (Not Before / Not After)
- Key Algorithm (EC P-256 or RSA)
- Signature Algorithm
- SHA-256 and SHA-1 fingerprints
- Extensions (Basic Constraints, Key Usage, Subject Key ID, Authority Key ID, etc.)
- Self-signed detection
- Chain linkage verification (child.issuer == parent.subject)

### What to Look For

- **Self-signed root**: Subject == Issuer on the last cert (normal for test certs from `keygen.py`)
- **Chain linkage**: Each cert's issuer must match the next cert's subject
- **Validity dates**: Certs must not be expired
- **Key Usage**: Leaf cert should have Digital Signature
- **CA flag**: Intermediate/root certs should have `CA:True`
- **Single cert chain**: Normal for self-signed certs from `keygen.py`; X9 PKI certs will have 2-3 certs

## Key Pair Validation

```bash
python3.13 validatepair.py payee_db/certs/
```

The folder must contain:
- `*_key.pem` — private key file
- `*.jwks` — JWKS file with `x5c` certificate

The tool performs:
1. **Thumbprint check** — verifies `x5t#S256` in JWKS matches SHA-256 of the cert DER
2. **Sign test** — signs a 10KB random payload with the private key
3. **Verify test** — verifies the signature using the public key from the certificate
4. **Tamper test** — flips one bit and confirms verification fails

### Expected Output
```
Folder:      payee_db/certs
Private Key: payee_key.pem
JWKS:        payee.jwks
Key Type:    EC
Algorithm:   ES256
Key ID:      <kid>
Certificate: CN=payee.example.com
Thumbprint:  MATCH

Test Payload: 10,240 bytes (SHA-256: abcd1234...)
Signing:     OK (71 bytes)
Verifying:   OK
Tamper test: OK (tampered payload correctly rejected)

Result: PASS — key pair is valid
```

## Manual JWKS Inspection

If the utilities aren't available, inspect the JWKS directly:

```bash
python3.13 -c "
import json, base64, hashlib
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding

with open('payee_db/certs/payee.jwks') as f:
    jwks = json.load(f)

key = jwks['keys'][0]
print(f'Key ID:      {key.get(\"kid\", \"N/A\")}')
print(f'Algorithm:   {key.get(\"alg\", \"N/A\")}')
print(f'Key Type:    {key.get(\"kty\", \"N/A\")}')
print(f'Has x5c:     {\"x5c\" in key}')
print(f'Has x5t#S256:{\"x5t#S256\" in key}')
print(f'Has jku:     {\"jku\" in key}')

if 'x5c' in key:
    cert_der = base64.b64decode(key['x5c'][0])
    cert = x509.load_der_x509_certificate(cert_der)
    print(f'Subject:     {cert.subject.rfc4514_string()}')
    print(f'Issuer:      {cert.issuer.rfc4514_string()}')
    print(f'Not After:   {cert.not_valid_after_utc}')

    # Verify thumbprint
    actual = base64.urlsafe_b64encode(hashlib.sha256(cert_der).digest()).rstrip(b'=').decode()
    expected = key.get('x5t#S256', '')
    print(f'Thumbprint:  {\"MATCH\" if actual == expected else \"MISMATCH\"}')"
```

## Common Certificate Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| Expired cert | `not_valid_after` in the past | Re-run `keygen.py` |
| Thumbprint mismatch | `x5t#S256` doesn't match cert hash | Re-run `keygen.py` (cert was modified) |
| Missing `x5c` | Certificate discovery fails | Check JWKS generation in `keygen.py` |
| Wrong `alg` | Signature verification fails | Ensure `alg` matches key type (ES256→EC, RS256→RSA) |
| Key pair mismatch | Sign works, verify fails | Private key and cert were generated separately |
| Chain broken | Issuer/subject don't match between certs | Certificate chain was assembled incorrectly |
