<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: cryptography
description: >-
  Applied cryptography security including TLS configuration and testing, certificate
  management (PKI/CA), key management best practices, cryptographic algorithm selection,
  common crypto failures (OWASP A02:2021), password hashing (Argon2/bcrypt/scrypt),
  HSM integration, quantum-readiness assessment, and crypto agility planning.
domain: cybersecurity
subdomain: cryptography
tags:
  - cryptography
  - tls
  - pki
  - certificate-management
  - key-management
  - password-hashing
  - hsm
  - quantum-cryptography
  - encryption
  - crypto-agility
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1557", "T1040", "T1552.004"]
  owasp: ["A02:2021"]
  nist-csf: ["PR.DS-1", "PR.DS-2", "PR.DS-5"]
  frameworks: ["NIST SP 800-57", "NIST SP 800-175B", "NIST PQC"]
---

# Cryptography

## When to Use

Activate when the operator asks about TLS hardening, certificate management,
key rotation, password hashing, encryption implementation, PKI design, HSM,
quantum cryptography readiness, or crypto failures.

Mode: `[MODE: ARCHITECT]` for crypto design; `[MODE: BLUE]` for crypto auditing; `[MODE: RED]` for crypto attacks.

## Quick Reference

| Task | Tool / Command | Purpose |
|------|---------------|---------|
| TLS scan | `sslyze --regular target.com` | TLS config audit |
| TLS test | `testssl.sh target.com:443` | Comprehensive TLS test |
| Cert check | `openssl s_client -connect target.com:443 < /dev/null 2>/dev/null \| openssl x509 -text` | Certificate inspection |
| Cert expiry | `echo \| openssl s_client -connect target.com:443 2>/dev/null \| openssl x509 -noout -dates` | Expiration check |
| Key generation | `openssl genpkey -algorithm ed25519 -out private.pem` | Ed25519 key |
| CSR creation | `openssl req -new -key private.pem -out cert.csr` | Certificate signing request |
| Hash password | `python3 -c "from argon2 import PasswordHasher; print(PasswordHasher().hash('pass'))"` | Password hashing |
| Entropy check | `ent file.bin` / `dieharder -a -f file.bin` | Randomness testing |

## Workflow

### 1. Algorithm Selection Guide

```
Encryption (symmetric):
├── AES-256-GCM — Recommended for all new implementations
├── ChaCha20-Poly1305 — Alternative for mobile/embedded (no AES-NI)
├── AES-256-CBC — Acceptable with HMAC (encrypt-then-MAC)
└── ❌ DES, 3DES, RC4, Blowfish — Deprecated, do not use

Encryption (asymmetric):
├── X25519/Ed25519 — Recommended for key exchange/signatures
├── RSA-4096 — Acceptable (RSA-2048 minimum)
├── ECDSA P-256 — Acceptable for signatures
└── ❌ RSA-1024, DSA — Deprecated

Hashing:
├── SHA-256/SHA-384/SHA-512 — General purpose
├── SHA-3 — Alternative to SHA-2
├── BLAKE3 — High performance
└── ❌ MD5, SHA-1 — Deprecated (collision attacks)

Password hashing:
├── Argon2id — Recommended (memory-hard, GPU-resistant)
├── bcrypt (cost ≥ 12) — Acceptable
├── scrypt — Acceptable
└── ❌ PBKDF2-SHA1, MD5, SHA-256 without salt — Do not use

Key derivation:
├── HKDF — Recommended for key derivation from shared secrets
├── Argon2 — When deriving from passwords
└── PBKDF2-SHA256 (600,000+ iterations) — Acceptable per OWASP 2023
```

### 2. TLS Hardening

```bash
# Test TLS configuration
testssl.sh --severity HIGH target.com:443
sslyze --regular --certinfo target.com

# Nginx TLS configuration (modern)
ssl_protocols TLSv1.3;
ssl_prefer_server_ciphers off;
# TLS 1.3 ciphersuites are automatically configured

# Nginx TLS configuration (intermediate — supports TLS 1.2)
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;

# HSTS header
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

# OCSP stapling
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/ssl/certs/chain.pem;

# Certificate Transparency
# Certificates must be logged to CT logs (Chrome requires it)
```

### 3. Certificate Management

```bash
# Let's Encrypt with certbot (automated)
certbot certonly --nginx -d example.com -d www.example.com
# Auto-renewal: certbot renew (runs via cron/systemd timer)

# Internal PKI with step-ca
step ca init --name "Internal CA" --provisioner admin --address ":443"
step ca certificate internal.example.com cert.pem key.pem

# Certificate monitoring
# Monitor expiry across all certificates
echo | openssl s_client -connect target.com:443 2>/dev/null | \
  openssl x509 -noout -enddate -subject

# Certificate transparency monitoring
# Monitor CT logs for unauthorized certs for your domain
# https://crt.sh/?q=%.example.com
curl -s "https://crt.sh/?q=%.example.com&output=json" | jq '.[0:10]'
```

### 4. Key Management

```
Key management lifecycle:
├── Generation: Use cryptographically secure RNG (CSPRNG)
├── Storage: HSM, cloud KMS, or Vault (never filesystem/env vars for long-term keys)
├── Distribution: TLS, out-of-band, or key wrapping
├── Rotation: Annual for data keys, on compromise immediately
├── Archival: Retain decryption keys for data retention period
├── Destruction: Crypto-shred when no longer needed

HSM integration:
├── AWS CloudHSM / Azure Dedicated HSM / GCP Cloud HSM
├── PKCS#11 interface for application integration
├── Key material never leaves HSM boundary
└── FIPS 140-2 Level 3 (tamper-evident)

Envelope encryption pattern:
├── Data Encryption Key (DEK): Random per-object, encrypts data
├── Key Encryption Key (KEK): Stored in KMS/HSM, wraps DEK
├── Encrypted DEK stored alongside ciphertext
└── Rotation: Rotate KEK, re-wrap DEKs (no re-encryption of data)
```

### 5. Post-Quantum Readiness

```
Quantum threat timeline:
├── Current: No cryptographically relevant quantum computers
├── 2030-2035: Estimated threat to RSA/ECC (harvest now, decrypt later)
├── Action now: Inventory all crypto, prepare for migration

NIST PQC Standards (August 2024):
├── ML-KEM (FIPS 203, formerly CRYSTALS-Kyber): Key encapsulation
├── ML-DSA (FIPS 204, formerly CRYSTALS-Dilithium): Digital signatures
├── SLH-DSA (FIPS 205, formerly SPHINCS+): Stateless hash signatures
└── FN-DSA (forthcoming, formerly FALCON): Compact signatures

Migration strategy:
├── Phase 1: Inventory all cryptographic assets (algorithms, key lengths, locations)
├── Phase 2: Implement crypto agility (abstraction layer for easy algorithm swap)
├── Phase 3: Hybrid mode (classical + PQC combined)
├── Phase 4: Full PQC migration for new deployments
└── Phase 5: Retire classical-only implementations
```

## Verification

- [ ] TLS 1.2+ only (TLS 1.3 preferred), no weak cipher suites
- [ ] All certificates valid, monitored for expiry (>30 days warning)
- [ ] HSTS deployed with preload
- [ ] Password hashing uses Argon2id or bcrypt (cost ≥12)
- [ ] Encryption at rest uses AES-256-GCM or ChaCha20-Poly1305
- [ ] Key rotation schedule defined and automated
- [ ] No deprecated algorithms (MD5, SHA1, DES, RC4) in use
- [ ] Post-quantum migration plan documented
