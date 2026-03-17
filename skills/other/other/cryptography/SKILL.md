---
name: cryptography
description: |
    Use when selecting or implementing cryptographic controls for data protection. Covers TLS configuration, password hashing algorithms, key management, secrets management, and encryption standards across all platforms.
    USE FOR: TLS, encryption, hashing, Argon2, bcrypt, scrypt, key management, secrets management, AES, RSA, ECDSA, certificate management, HashiCorp Vault, AWS KMS, homomorphic encryption, FHE
    DO NOT USE FOR: authentication protocol design (use authentication), network security appliances, custom cryptographic algorithm design (use established libraries instead)
license: MIT
metadata:
  displayName: "Cryptography"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "NIST SP 800-57 Recommendation for Key Management"
    url: "https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final"
  - title: "OWASP Cryptographic Storage Cheat Sheet"
    url: "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html"
  - title: "NIST SP 800-175B Guide to Secure Web Services"
    url: "https://csrc.nist.gov/publications/detail/sp/800-175b/rev-1/final"
---

# Cryptography

## Overview

Cryptography is the foundation of trust in modern software systems. It underpins confidentiality, integrity, authentication, and non-repudiation for data in transit and at rest. Every secure communication channel, every stored password, and every signed artifact relies on well-implemented cryptographic primitives.

The cardinal rule of applied cryptography is **never roll your own crypto**. Use established, peer-reviewed libraries and standards. Custom cryptographic algorithms or ad-hoc constructions are almost guaranteed to contain exploitable weaknesses. Rely on proven implementations such as OpenSSL, libsodium, Bouncy Castle, or the native cryptography modules provided by your platform.

## TLS Configuration

Transport Layer Security protects data in transit. All services must enforce a minimum of **TLS 1.2**, and should prefer **TLS 1.3** wherever supported.

### Disabled Protocols

| Protocol  | Status     | Reason                                      |
|-----------|------------|---------------------------------------------|
| SSL 3.0   | **Disabled** | Vulnerable to POODLE attack                |
| TLS 1.0   | **Disabled** | Deprecated by RFC 8996; known weaknesses   |
| TLS 1.1   | **Disabled** | Deprecated by RFC 8996; no modern benefits |

### Recommended Cipher Suites

| Cipher Suite              | Protocol | Notes                              |
|---------------------------|----------|------------------------------------|
| AES-128-GCM / AES-256-GCM | TLS 1.2+ | Authenticated encryption, hardware-accelerated on modern CPUs |
| ChaCha20-Poly1305         | TLS 1.2+ | Excellent performance on devices without AES-NI |

- In TLS 1.3, cipher suite negotiation is simplified and only secure options are available by default.
- Disable CBC-mode ciphers when possible to avoid padding oracle attacks.
- Always enable **HSTS** (HTTP Strict Transport Security) to prevent protocol downgrade attacks:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

## Password Hashing

Passwords must be hashed with a slow, memory-hard function designed specifically for password storage. General-purpose hash functions are not suitable.

### Algorithm Comparison

| Algorithm | Status         | Memory-Hard | GPU Resistant | Recommended Parameters          |
|-----------|----------------|-------------|---------------|---------------------------------|
| Argon2id  | Gold standard  | Yes         | Yes           | m=64MB, t=3, p=4               |
| bcrypt    | Secure         | 4KB fixed   | Partial       | cost=12+                        |
| scrypt    | Secure         | Yes         | Yes           | N=16384, r=8, p=1              |
| PBKDF2    | Legacy         | No          | No            | 600,000+ iterations (SHA-256)  |

**Argon2id** is the recommended default. It won the Password Hashing Competition and combines resistance to both side-channel and GPU-based attacks.

> **Never use MD5 or SHA-family functions (SHA-1, SHA-256, SHA-512) for password hashing.** These are general-purpose hash functions optimized for speed, which makes them trivially brute-forceable for password cracking. They lack salting by design and have no work-factor parameter.

## Symmetric Encryption

Symmetric encryption uses a single shared key for both encryption and decryption.

- **AES-256-GCM** is the standard for data at rest. GCM mode provides both confidentiality and integrity (authenticated encryption with associated data, or AEAD).
- **ChaCha20-Poly1305** is an excellent alternative, especially on platforms without hardware AES acceleration. It is the default in TLS 1.3 for non-AES-NI environments.
- **Never use ECB mode.** ECB encrypts identical plaintext blocks to identical ciphertext blocks, leaking patterns in the data. Always use an authenticated mode such as GCM or an encrypt-then-MAC construction.

When using AES-GCM:
- Use a unique nonce (IV) for every encryption operation under the same key.
- Limit the amount of data encrypted under a single key to avoid nonce reuse (approximately 2^32 encryptions with random 96-bit nonces).
- Rotate keys before reaching these limits.

## Asymmetric Encryption

Asymmetric (public-key) cryptography uses a key pair: a public key for encryption or verification and a private key for decryption or signing.

### Key Sizes and Algorithms

| Algorithm | Use Case             | Minimum Key Size | Recommended           | Notes                                  |
|-----------|----------------------|------------------|-----------------------|----------------------------------------|
| RSA       | Encryption, signing  | 2048 bits        | 3072+ bits            | Widely supported; use OAEP for encryption, PSS for signing |
| ECDSA     | Signing              | P-256 (256 bits) | P-256 or P-384        | Smaller keys, faster operations than RSA |
| Ed25519   | Signing              | 256 bits (fixed) | 256 bits (fixed)      | Modern, fast, resistant to side-channel attacks; preferred for new systems |
| X25519    | Key exchange         | 256 bits (fixed) | 256 bits (fixed)      | Used in TLS 1.3 and modern protocols  |

- **Ed25519** is the recommended choice for digital signatures in new systems due to its simplicity, performance, and security properties.
- RSA keys below 2048 bits are considered insecure and must not be used.
- For encryption use cases, prefer hybrid encryption: use asymmetric crypto to exchange a symmetric key, then encrypt the payload with AES-GCM.

## Homomorphic Encryption

Homomorphic encryption (HE) allows computation on encrypted data without decrypting it first. The result, when decrypted, matches the result of performing the same operations on the plaintext. This enables data processing by untrusted parties (cloud providers, third-party analytics) while preserving confidentiality.

### Schemes

| Scheme | Operations Supported | Performance | Use Case |
|--------|---------------------|-------------|----------|
| **Partially Homomorphic (PHE)** | Addition OR multiplication (not both) | Fast | Simple aggregations, voting |
| **Somewhat Homomorphic (SHE)** | Limited additions and multiplications | Moderate | Bounded computations |
| **Fully Homomorphic (FHE)** | Arbitrary additions and multiplications | Slow (improving) | General-purpose encrypted computation |

### Libraries and Frameworks

| Library | Language | Scheme | Maintainer |
|---------|----------|--------|------------|
| **Microsoft SEAL** | C++ (with .NET, Python wrappers) | BFV, CKKS | Microsoft Research |
| **OpenFHE** | C++ (with Python bindings) | BGV, BFV, CKKS, TFHE, FHEW | DARPA-funded consortium |
| **TFHE-rs** | Rust | TFHE | Zama |
| **Concrete** | Python / Rust | TFHE | Zama |
| **HElib** | C++ | BGV, CKKS | IBM |

### Practical Considerations

- **Performance**: FHE is orders of magnitude slower than plaintext computation. Use it only when the confidentiality requirement justifies the overhead.
- **CKKS vs BFV/BGV**: CKKS supports approximate arithmetic on real numbers (good for ML inference). BFV/BGV support exact integer arithmetic (good for counting, voting, database queries).
- **Bootstrapping**: FHE schemes accumulate noise with each operation. Bootstrapping refreshes ciphertexts but is expensive. Leveled HE avoids bootstrapping by pre-setting the maximum circuit depth.
- **Key sizes**: HE keys and ciphertexts are much larger than traditional encryption (megabytes vs bytes). Plan for storage and bandwidth overhead.
- **Use cases**: Privacy-preserving ML inference, encrypted database queries, secure multi-party computation, confidential cloud analytics, healthcare data analysis without exposure.

> **When to use HE**: When you need a third party to compute on your data but cannot afford to reveal the plaintext — and you can tolerate the performance overhead. For most applications, traditional encryption with access controls is simpler and sufficient.

## Key Management

Cryptographic keys have a defined lifecycle that must be managed rigorously:

```
Generation --> Storage --> Distribution --> Usage --> Rotation --> Revocation --> Destruction
```

### Lifecycle Principles

1. **Generation** — Use cryptographically secure random number generators (CSPRNG). Never use `Math.random()` or similar non-cryptographic sources.
2. **Storage** — Keys must never be stored in plaintext. Use Hardware Security Modules (HSMs) for high-value keys. HSMs provide tamper-resistant storage and perform cryptographic operations without exposing key material.
3. **Distribution** — Use secure channels (TLS, out-of-band exchange). Never transmit keys alongside the data they protect.
4. **Usage** — Limit key usage to a single purpose (encryption OR signing, not both). Enforce access controls.
5. **Rotation** — Rotate keys on a regular schedule and immediately after any suspected compromise.
6. **Revocation** — Maintain revocation lists (CRL) or use OCSP for certificates. Ensure revoked keys are no longer accepted.
7. **Destruction** — Securely erase keys when they are no longer needed. Overwrite key material in memory.

### Cloud KMS Services

| Service             | Provider   | HSM-Backed | Auto-Rotation | Key Types                     |
|---------------------|------------|------------|---------------|-------------------------------|
| AWS KMS             | AWS        | Yes        | Yes (annual)  | Symmetric, RSA, ECC          |
| Azure Key Vault     | Microsoft  | Yes        | Yes           | Symmetric, RSA, EC           |
| GCP Cloud KMS       | Google     | Yes        | Yes           | Symmetric, RSA, EC, Ed25519  |
| HashiCorp Vault     | HashiCorp  | Optional   | Yes           | All types; transit secrets engine |

## Secrets Management

Secrets include API keys, database credentials, tokens, certificates, and encryption keys. Mismanaged secrets are one of the most common causes of security breaches.

### Rules

- **Never store secrets in source code or version control.** Even if a repository is private, secrets in VCS persist in history and are easily leaked.
- **Use dedicated secrets management tools.** These provide encryption, access control, audit logging, and automatic rotation.
- **Inject secrets at runtime** via environment variables, mounted files, or API calls — never bake them into container images or build artifacts.

### Secrets Management Tools

| Tool                          | Provider   | Dynamic Secrets | Auto-Rotation | Audit Log | Notes                            |
|-------------------------------|------------|-----------------|---------------|-----------|----------------------------------|
| HashiCorp Vault               | HashiCorp  | Yes             | Yes           | Yes       | Industry standard; self-hosted or cloud |
| AWS Secrets Manager           | AWS        | Yes             | Yes           | Yes       | Native AWS integration           |
| Azure Key Vault               | Microsoft  | No              | Yes           | Yes       | Integrated with Azure AD         |
| GCP Secret Manager            | Google     | No              | Yes           | Yes       | IAM-based access control         |
| Doppler                       | Doppler    | No              | Yes           | Yes       | Developer-friendly; multi-cloud  |
| 1Password Secrets Automation  | 1Password  | No              | No            | Yes       | Good for smaller teams; CLI and SDK support |

## Best Practices

- **Use established cryptographic libraries** (libsodium, OpenSSL, Bouncy Castle, platform-native crypto APIs) rather than implementing primitives yourself.
- **Enforce TLS 1.2 as the minimum** for all communications, and prefer TLS 1.3 where supported.
- **Hash passwords with Argon2id** as the default; fall back to bcrypt (cost 12+) if Argon2 is unavailable.
- **Use authenticated encryption** (AES-GCM or ChaCha20-Poly1305) for all symmetric encryption; never use unauthenticated modes like ECB or plain CBC.
- **Rotate cryptographic keys on a defined schedule** and immediately upon suspected compromise.
- **Store all secrets in a dedicated secrets management tool** with audit logging and access controls — never in code, configuration files, or version control.
- **Use Hardware Security Modules (HSMs)** or cloud KMS for high-value key storage and cryptographic operations.
- **Keep cryptographic dependencies up to date** and monitor for vulnerability disclosures affecting the algorithms and libraries you use.
