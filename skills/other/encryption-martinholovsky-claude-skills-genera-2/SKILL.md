# Encryption Skill

---
name: encryption
version: 1.0.0
domain: security/cryptography
risk_level: HIGH
languages: [python, typescript, rust, go]
frameworks: [sqlcipher, cryptography, libsodium]
requires_security_review: true
compliance: [GDPR, HIPAA, PCI-DSS, SOC2]
last_updated: 2025-01-15
---

> **MANDATORY READING PROTOCOL**: Before implementing ANY encryption, read `references/advanced-patterns.md` for key derivation and `references/security-examples.md` for implementation patterns.

## 1. Overview

### 1.1 Purpose and Scope

This skill provides secure-by-default patterns for implementing encryption in JARVIS AI Assistant, covering:

- **SQLCipher**: Encrypted SQLite database with AES-256-GCM
- **Argon2id**: Memory-hard key derivation function
- **Key Management**: Secure generation, storage, rotation, and destruction
- **Secure Memory**: Protection against memory disclosure attacks

### 1.2 Risk Assessment

**Risk Level**: HIGH

**Justification**:
- Cryptographic failures expose all protected data
- Key compromise leads to complete confidentiality loss
- Implementation errors are catastrophic and often undetectable
- Regulatory violations (GDPR, HIPAA, PCI-DSS) carry severe penalties

**Attack Surface**:
- Key derivation weaknesses
- Insecure random number generation
- Timing side-channels
- Memory disclosure (cold boot, crash dumps)
- Key reuse across contexts

## 2. Core Responsibilities

### 2.1 Primary Functions

1. **Encrypt data at rest** using AES-256-GCM with authenticated encryption
2. **Derive keys securely** using Argon2id with appropriate parameters
3. **Manage key lifecycle** including rotation, escrow, and destruction
4. **Protect key material** in memory and during operations
5. **Integrate with OS keychains** for master key storage

### 2.2 Core Principles

1. **TDD First** - Write tests before implementation; test encryption/decryption round-trips, authentication failures, and edge cases
2. **Performance Aware** - Cache derived keys, use streaming for large data, leverage hardware acceleration
3. **Security by Default** - Use authenticated encryption modes, memory-hard KDFs, secure random sources
4. **Defense in Depth** - Multiple layers of protection, fail securely, minimize key exposure

### 2.3 Security Principles

- **NEVER** implement custom cryptographic algorithms
- **NEVER** use ECB mode or unauthenticated encryption
- **ALWAYS** use cryptographically secure random number generators
- **ALWAYS** validate ciphertext authenticity before decryption
- **ALWAYS** use constant-time comparison for authentication tags

## 3. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```python
import pytest
from cryptography.exceptions import InvalidTag

class TestEncryptionTDD:
    """TDD tests for encryption implementation."""

    def test_encrypt_decrypt_roundtrip(self):
        """Test that encryption followed by decryption returns original data."""
        from jarvis.security.encryption import SecureEncryption

        key = secrets.token_bytes(32)
        encryptor = SecureEncryption(key)

        plaintext = b"sensitive data for JARVIS"
        ciphertext = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(ciphertext)

        assert decrypted == plaintext
        assert ciphertext != plaintext  # Must be encrypted

    def test_tampered_ciphertext_raises_error(self):
        """Test that tampered ciphertext is rejected."""
        from jarvis.security.encryption import SecureEncryption

        key = secrets.token_bytes(32)
        encryptor = SecureEncryption(key)

        ciphertext = encryptor.encrypt(b"secret")
        tampered = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])

        with pytest.raises(InvalidTag):
            encryptor.decrypt(tampered)

    def test_key_derivation_consistency(self):
        """Same password + salt = same key; different salt = different key."""
        from jarvis.security.encryption import SecureKeyDerivation
        password = "strong_password_123"
        salt = secrets.token_bytes(16)
        key1, _ = SecureKeyDerivation.derive_key(password, salt)
        key2, _ = SecureKeyDerivation.derive_key(password, salt)
        assert key1 == key2 and len(key1) == 32

        key3, salt3 = SecureKeyDerivation.derive_key(password)
        assert key1 != key3  # Different salt = different key
```

### Step 2: Implement Minimum to Pass

Implement only what's needed to pass the tests. Start with basic encryption/decryption, then add key derivation.

### Step 3: Refactor Following Patterns

After tests pass, add: memory protection, error handling, AAD support, key caching.

### Step 4: Run Full Verification

```bash
# Run encryption tests with coverage
pytest tests/security/test_encryption.py -v --cov=jarvis.security.encryption --cov-fail-under=90

# Run security-specific tests
pytest tests/security/ -k "encryption or crypto" -v

# Check for timing vulnerabilities
pytest tests/security/test_timing.py -v

# Verify no secrets in output
pytest --log-cli-level=DEBUG 2>&1 | grep -i "key\|secret\|password" && echo "WARNING: Secrets in logs!"
```

## 4. Technology Stack

### 4.1 Recommended Libraries

| Language | Library | Version | Notes |
|----------|---------|---------|-------|
| Python | `cryptography` | >=42.0.0 | Uses OpenSSL 3.x backend |
| Python | `argon2-cffi` | >=23.1.0 | Reference Argon2 implementation |
| TypeScript | `@noble/ciphers` | >=0.5.0 | Audited pure-JS implementation |
| Rust | `ring` | >=0.17.0 | BoringSSL-backed |
| Go | `crypto/cipher` | stdlib | Use with `golang.org/x/crypto` |

### 4.2 SQLCipher Configuration

**Minimum Version**: SQLCipher 4.5.6+ (includes SQLite 3.44.2)

```python
# SQLCipher secure configuration
SQLCIPHER_PRAGMAS = {
    'key': None,  # Set via secure key injection
    'cipher': 'aes-256-gcm',
    'kdf_iter': 256000,  # PBKDF2 iterations
    'cipher_page_size': 4096,
    'cipher_kdf_algorithm': 'PBKDF2_HMAC_SHA512',
    'cipher_hmac_algorithm': 'HMAC_SHA512',
    'cipher_plaintext_header_size': 0,
}
```

## 5. Performance Patterns

### 5.1 Key Caching

**Bad:** Deriving key on every operation (~500ms per Argon2id call)

**Good - Cache with TTL:**
```python
class CachedKeyManager:
    def __init__(self, cache_ttl: int = 300):
        self._cache: dict[str, tuple[bytes, float]] = {}
        self._ttl = cache_ttl

    def get_key(self, password: str, salt: bytes) -> bytes:
        cache_key = f"{hash(password)}:{salt.hex()}"
        if cache_key in self._cache:
            key, ts = self._cache[cache_key]
            if time.time() - ts < self._ttl:
                return key
        key, _ = SecureKeyDerivation.derive_key(password, salt)
        self._cache[cache_key] = (key, time.time())
        return key
```

### 5.2 Streaming Encryption for Large Data

**Bad:** `data = f.read()` loads entire file into memory

**Good - Stream with chunking (64KB chunks):**
```python
nonce = secrets.token_bytes(12)
encryptor = Cipher(algorithms.AES(key), modes.GCM(nonce)).encryptor()
with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
    fout.write(nonce)
    while chunk := fin.read(64 * 1024):
        fout.write(encryptor.update(chunk))
    fout.write(encryptor.finalize() + encryptor.tag)
```

### 5.3 Hardware Acceleration

**Bad:** PyCryptodome without OpenSSL backend (10-100x slower)

**Good:** Use `cryptography` library - auto-detects AES-NI via OpenSSL 3.x backend

### 5.4 Batch Operations

**Bad - Individual loop with append:**
```python
results = []
for record in records:
    results.append(encryptor.encrypt(record))
```

**Good - List comprehension with single encryptor:**
```python
encryptor = SecureEncryption(key)
results = [encryptor.encrypt(record) for record in records]

# For large batches, use ProcessPoolExecutor for parallelization
```

### 5.5 Memory-Safe Key Handling

**Bad - Keys remain in memory:**
```python
self.key = SecureKeyDerivation.derive_key(password)  # Never cleared
```

**Good - Zero keys after use with context manager:**
```python
import ctypes

class SecureKeyHolder:
    def __init__(self, password: str):
        self._key, self.salt = SecureKeyDerivation.derive_key(password)

    def __exit__(self, *args):
        if self._key:
            key_buffer = (ctypes.c_char * len(self._key)).from_buffer_copy(self._key)
            ctypes.memset(key_buffer, 0, len(self._key))
            self._key = None

# Usage: with SecureKeyHolder(password) as kh: encrypt(kh._key, data)
```

## 6. Implementation Patterns

### 6.1 Key Derivation with Argon2id

```python
from argon2 import PasswordHasher
from argon2.low_level import hash_secret_raw, Type
import secrets

class SecureKeyDerivation:
    """Derive encryption keys from passwords using Argon2id."""

    # OWASP recommended parameters for sensitive data
    TIME_COST = 3        # Iterations
    MEMORY_COST = 65536  # 64 MiB
    PARALLELISM = 4      # Threads
    HASH_LEN = 32        # 256 bits for AES-256
    SALT_LEN = 16        # 128 bits minimum

    @classmethod
    def derive_key(cls, password: str, salt: bytes = None) -> tuple[bytes, bytes]:
        """
        Derive a 256-bit key from password.

        Returns:
            tuple: (derived_key, salt) for storage
        """
        if salt is None:
            salt = secrets.token_bytes(cls.SALT_LEN)

        # Validate inputs
        if not password or len(password) < 12:
            raise ValueError("Password must be at least 12 characters")

        key = hash_secret_raw(
            secret=password.encode('utf-8'),
            salt=salt,
            time_cost=cls.TIME_COST,
            memory_cost=cls.MEMORY_COST,
            parallelism=cls.PARALLELISM,
            hash_len=cls.HASH_LEN,
            type=Type.ID  # Argon2id
        )

        return key, salt
```

### 6.2 AES-256-GCM Encryption

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets

class SecureEncryption:
    """AES-256-GCM authenticated encryption."""

    NONCE_SIZE = 12  # 96 bits recommended for GCM
    KEY_SIZE = 32    # 256 bits

    def __init__(self, key: bytes):
        if len(key) != self.KEY_SIZE:
            raise ValueError(f"Key must be {self.KEY_SIZE} bytes")
        self._aesgcm = AESGCM(key)

    def encrypt(self, plaintext: bytes, associated_data: bytes = None) -> bytes:
        """
        Encrypt with random nonce, prepended to ciphertext.

        Returns:
            bytes: nonce || ciphertext || tag
        """
        nonce = secrets.token_bytes(self.NONCE_SIZE)
        ciphertext = self._aesgcm.encrypt(nonce, plaintext, associated_data)
        return nonce + ciphertext

    def decrypt(self, ciphertext: bytes, associated_data: bytes = None) -> bytes:
        """
        Decrypt and verify authenticity.

        Raises:
            InvalidTag: If authentication fails
        """
        if len(ciphertext) < self.NONCE_SIZE + 16:  # nonce + tag minimum
            raise ValueError("Ciphertext too short")

        nonce = ciphertext[:self.NONCE_SIZE]
        actual_ciphertext = ciphertext[self.NONCE_SIZE:]

        return self._aesgcm.decrypt(nonce, actual_ciphertext, associated_data)
```

### 6.3 SQLCipher Database Integration

```python
import sqlcipher3
from contextlib import contextmanager

class EncryptedDatabase:
    """Encrypted SQLite database using SQLCipher."""

    def __init__(self, db_path: str, key: bytes):
        self._db_path = db_path
        self._key = key
        self._conn = None

    @contextmanager
    def connect(self):
        """Context manager for database connections."""
        conn = sqlcipher3.connect(self._db_path)
        try:
            # Apply security pragmas
            conn.execute(f"PRAGMA key = \"x'{self._key.hex()}'\";")
            conn.execute("PRAGMA cipher = 'aes-256-gcm';")
            conn.execute("PRAGMA kdf_iter = 256000;")
            conn.execute("PRAGMA cipher_page_size = 4096;")

            # Verify encryption is active
            result = conn.execute("PRAGMA cipher_version;").fetchone()
            if not result:
                raise RuntimeError("SQLCipher encryption not active")

            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def rekey(self, new_key: bytes):
        """Rotate database encryption key."""
        with self.connect() as conn:
            conn.execute(f"PRAGMA rekey = \"x'{new_key.hex()}'\";")
        self._key = new_key
```

## 7. Security Standards

### 7.1 Known Vulnerabilities

| CVE | Severity | Component | Description | Mitigation |
|-----|----------|-----------|-------------|------------|
| CVE-2020-27207 | High | SQLCipher <4.4.1 | Use-after-free in codec pragma | Upgrade to 4.5.6+ |
| CVE-2024-0232 | Medium | SQLite <3.44.0 | Heap use-after-free in JSON | Upgrade SQLCipher 4.5.6+ |
| CVE-2023-42811 | High | aes-gcm (Rust) | Plaintext exposure on auth failure | Upgrade to 0.10.3+ |
| CVE-2024-4603 | Medium | OpenSSL | Key derivation timing attack | Upgrade OpenSSL 3.3+ |
| CVE-2023-48056 | Medium | Crypto libs | IV reuse detection failure | Use random nonces |

### 7.2 OWASP Mapping

| OWASP 2025 | Relevance | Implementation |
|------------|-----------|----------------|
| A02: Cryptographic Failures | Critical | AES-256-GCM, Argon2id, secure RNG |
| A04: Insecure Design | High | Threat modeling, key rotation |
| A05: Security Misconfiguration | High | Secure defaults, validation |
| A08: Software Integrity Failures | Medium | Authenticated encryption |

### 7.3 Cryptography Standards

**Approved Algorithms**:
- Symmetric: AES-256-GCM (primary), ChaCha20-Poly1305 (alternative)
- KDF: Argon2id (primary), PBKDF2-HMAC-SHA512 (SQLCipher)
- Hash: SHA-256, SHA-512, BLAKE2b
- RNG: OS CSPRNG only (`secrets` module, `/dev/urandom`)

**Prohibited**:
- DES, 3DES, RC4, Blowfish
- MD5, SHA-1 for security purposes
- ECB mode for any cipher
- Custom random number generators

## 8. Testing Requirements

See Section 3 (Implementation Workflow - TDD) for comprehensive test examples including:
- Encryption/decryption round-trips
- Ciphertext tampering detection
- Key derivation consistency
- Nonce uniqueness validation

## 9. Common Mistakes

### 9.1 Critical Anti-Patterns

| Anti-Pattern | Never Do | Always Do |
|--------------|----------|-----------|
| ECB Mode | `modes.ECB()` | `AESGCM(key)` |
| Hardcoded Keys | `SECRET_KEY = b"..."` | `os_keychain.get_key()` |
| Predictable Nonces | `struct.pack(">Q", time())` | `secrets.token_bytes(12)` |
| No Auth | `modes.CBC(iv)` | `aesgcm.encrypt(nonce, pt, aad)` |
| Weak KDF | `sha256(password)` | `Argon2id.derive_key()` |

## 10. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Read threat model in `references/threat-model.md`
- [ ] Identify data classification (PII, PHI, credentials)
- [ ] Choose appropriate algorithm (AES-256-GCM or ChaCha20-Poly1305)
- [ ] Design key derivation strategy (Argon2id parameters)
- [ ] Plan key storage (OS keychain integration)
- [ ] Write failing tests for encrypt/decrypt round-trips
- [ ] Write tests for authentication tag verification
- [ ] Write tests for key derivation consistency

### Phase 2: During Implementation

- [ ] Use `cryptography` library (not custom implementations)
- [ ] Generate nonces with `secrets.token_bytes(12)`
- [ ] Implement key caching with TTL for performance
- [ ] Use streaming for files >10MB
- [ ] Zero key material after use (SecureKeyHolder pattern)
- [ ] Add associated data (AAD) for context binding
- [ ] Handle InvalidTag exceptions without leaking info
- [ ] Run tests after each function implementation

### Phase 3: Before Committing

- [ ] All TDD tests pass with 90%+ coverage
- [ ] Nonce uniqueness validated over 10,000+ operations
- [ ] Key derivation timing variance <10%
- [ ] No secrets in logs (`grep -i "key\|secret\|password"`)
- [ ] Dependency scanning clean (no CVEs)
- [ ] Performance benchmarks meet targets:
  - Key derivation: <1s
  - Encryption: >100MB/s
  - Batch operations: Linear scaling
- [ ] Security review requested for HIGH risk code

## 11. Summary

**Key Objectives**: AES-256-GCM with random nonces, Argon2id KDF, OS keychain integration, authenticated encryption, key rotation support.

**Security Reminders**: No custom crypto, use audited libraries, test auth tags, rotate keys on schedule.

**References**: `references/advanced-patterns.md`, `references/security-examples.md`, `references/threat-model.md`

---

**Encryption done wrong is worse than no encryption - it provides false confidence.**
