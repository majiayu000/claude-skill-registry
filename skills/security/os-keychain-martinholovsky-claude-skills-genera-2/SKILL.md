# OS Keychain Skill

---
name: os-keychain
version: 1.1.0
domain: security/credential-storage
risk_level: HIGH
languages: [python, typescript, rust, go]
frameworks: [keyring, security-framework, libsecret]
requires_security_review: true
compliance: [GDPR, HIPAA, PCI-DSS, SOC2]
last_updated: 2025-01-15
---

> **MANDATORY READING PROTOCOL**: Before implementing credential storage, read `references/advanced-patterns.md` for cross-platform patterns and `references/security-examples.md` for platform-specific implementations.

## 1. Overview

### 1.1 Purpose and Scope

This skill provides secure credential storage using OS-native keychain services:

- **Windows**: Credential Manager (DPAPI-backed)
- **macOS**: Keychain Services (Secure Enclave integration)
- **Linux**: Secret Service API (GNOME Keyring, KWallet)

### 1.2 Risk Assessment

**Risk Level**: HIGH

**Justification**:
- Master keys and sensitive credentials stored
- Compromise exposes all dependent systems
- Platform API misuse leads to insecure storage
- Privilege escalation can access all credentials

**Attack Surface**:
- Inter-process communication (D-Bus, XPC)
- Access control misconfigurations
- Memory disclosure attacks
- Privilege escalation to access keychain

## 2. Core Principles

1. **TDD First** - Write tests before implementing credential operations
2. **Performance Aware** - Cache credentials, batch operations, minimize keychain calls
3. **Platform-native storage** - Use OS keychain services for all credentials
4. **Access isolation** - Unique service names prevent cross-contamination
5. **Secure by default** - Reject insecure backends automatically
6. **Cross-platform support** - Unified API across Windows, macOS, Linux

### 2.1 Security Principles

- **NEVER** store secrets in environment variables or files
- **NEVER** log credential values or access patterns with identifiers
- **ALWAYS** use platform-native keychain services
- **ALWAYS** validate application identity before credential access
- **ALWAYS** use unique service names per credential type

## 3. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```python
import pytest
from unittest.mock import MagicMock, patch

class TestCredentialStoreOperations:
    """TDD tests for credential store - write these FIRST."""

    def test_store_credential_success(self):
        """Test storing a credential in keychain."""
        # Arrange
        store = SecureCredentialStore("test-service")

        # Act
        store.store("api-key", "sk-test-12345")

        # Assert
        assert store.exists("api-key") is True
        assert store.retrieve("api-key") == "sk-test-12345"

    def test_retrieve_nonexistent_raises_keyerror(self):
        """Test retrieving nonexistent credential raises KeyError."""
        store = SecureCredentialStore("test-service")

        with pytest.raises(KeyError, match="Credential not found"):
            store.retrieve("nonexistent-key")

    def test_delete_removes_credential(self):
        """Test deletion completely removes credential."""
        store = SecureCredentialStore("test-service")
        store.store("temp-key", "temp-value")

        store.delete("temp-key")

        assert store.exists("temp-key") is False

    def test_credential_isolation_between_namespaces(self):
        """Test credentials are isolated by namespace."""
        store1 = SecureCredentialStore("namespace-a")
        store2 = SecureCredentialStore("namespace-b")

        store1.store("shared-key", "value-a")
        store2.store("shared-key", "value-b")

        assert store1.retrieve("shared-key") == "value-a"
        assert store2.retrieve("shared-key") == "value-b"

    def test_rejects_insecure_backend(self):
        """Test rejection of insecure keyring backends."""
        import keyring
        from keyring.backends import null

        original = keyring.get_keyring()
        try:
            keyring.set_keyring(null.Keyring())
            with pytest.raises(RuntimeError, match="Insecure"):
                SecureCredentialStore("test")
        finally:
            keyring.set_keyring(original)
```

### Step 2: Implement Minimum to Pass

```python
import keyring
from keyring.errors import KeyringError
import logging

logger = logging.getLogger(__name__)

class SecureCredentialStore:
    """Minimal implementation to pass tests."""

    SERVICE_PREFIX = "com.jarvis.assistant"

    def __init__(self, namespace: str):
        self._service = f"{self.SERVICE_PREFIX}.{namespace}"
        self._verify_backend()

    def _verify_backend(self):
        backend = keyring.get_keyring()
        backend_name = type(backend).__name__
        insecure = ['PlaintextKeyring', 'NullKeyring', 'ChainerBackend']
        if backend_name in insecure:
            raise RuntimeError(f"Insecure keyring backend: {backend_name}")

    def store(self, key: str, secret: str) -> None:
        keyring.set_password(self._service, key, secret)

    def retrieve(self, key: str) -> str:
        secret = keyring.get_password(self._service, key)
        if secret is None:
            raise KeyError(f"Credential not found: {key}")
        return secret

    def delete(self, key: str) -> None:
        keyring.delete_password(self._service, key)

    def exists(self, key: str) -> bool:
        return keyring.get_password(self._service, key) is not None
```

### Step 3: Refactor with Performance Patterns

After tests pass, add caching and logging (see Performance Patterns section).

### Step 4: Run Full Verification

```bash
# Run all tests with coverage
pytest tests/security/test_keychain.py -v --cov=src/security/keychain

# Run security-specific tests
pytest tests/security/ -k "keychain or credential" -v

# Verify no credential leaks in logs
grep -r "sk-\|password\|secret" logs/ && echo "FAIL: Credentials in logs"
```

## 4. Performance Patterns

### 4.1 Credential Caching

```python
# BAD: Repeated keychain access
class SlowCredentialStore:
    def get_api_key(self):
        return keyring.get_password(self._service, "api-key")  # Slow IPC every call

# GOOD: In-memory cache with TTL
from functools import lru_cache
from threading import Lock
import time

class CachedCredentialStore:
    def __init__(self, namespace: str, cache_ttl: int = 300):
        self._service = f"com.jarvis.{namespace}"
        self._cache: dict[str, tuple[str, float]] = {}
        self._lock = Lock()
        self._ttl = cache_ttl

    def retrieve(self, key: str) -> str:
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < self._ttl:
                    return value

            secret = keyring.get_password(self._service, key)
            if secret is None:
                raise KeyError(f"Credential not found: {key}")

            self._cache[key] = (secret, time.time())
            return secret

    def invalidate(self, key: str = None):
        with self._lock:
            if key:
                self._cache.pop(key, None)
            else:
                self._cache.clear()
```

### 4.2 Batch Operations

```python
# BAD: Individual keychain calls
def load_all_credentials():
    db_pass = keyring.get_password("jarvis", "db-password")
    api_key = keyring.get_password("jarvis", "api-key")
    secret = keyring.get_password("jarvis", "encryption-key")
    return db_pass, api_key, secret  # 3 separate IPC calls

# GOOD: Batch loading with single initialization
class BatchCredentialLoader:
    def __init__(self, namespace: str, keys: list[str]):
        self._service = f"com.jarvis.{namespace}"
        self._credentials = self._load_batch(keys)

    def _load_batch(self, keys: list[str]) -> dict[str, str]:
        """Load multiple credentials in optimized batch."""
        result = {}
        for key in keys:
            value = keyring.get_password(self._service, key)
            if value:
                result[key] = value
        return result

    def get(self, key: str) -> str:
        if key not in self._credentials:
            raise KeyError(f"Credential not loaded: {key}")
        return self._credentials[key]

# Usage - single initialization at startup
loader = BatchCredentialLoader("secrets", ["db-password", "api-key", "encryption-key"])
```

### 4.3 Lazy Loading

```python
# BAD: Load all credentials at import
class EagerStore:
    def __init__(self):
        self.db_password = keyring.get_password("jarvis", "db")  # Loaded immediately
        self.api_key = keyring.get_password("jarvis", "api")

# GOOD: Load only when accessed
class LazyCredentialStore:
    def __init__(self, namespace: str):
        self._service = f"com.jarvis.{namespace}"
        self._cache: dict[str, str] = {}

    def __getattr__(self, name: str) -> str:
        if name.startswith('_'):
            raise AttributeError(name)

        if name not in self._cache:
            value = keyring.get_password(self._service, name.replace('_', '-'))
            if value is None:
                raise KeyError(f"Credential not found: {name}")
            self._cache[name] = value

        return self._cache[name]

# Usage - credentials loaded on first access
store = LazyCredentialStore("api-keys")
# No keychain calls yet
key = store.openai_key  # First access triggers load
```

### 4.4 Connection Reuse

```python
# BAD: Create new backend each time
def get_credential(key: str) -> str:
    store = SecureCredentialStore("service")  # Backend verification each call
    return store.retrieve(key)

# GOOD: Singleton pattern for store instances
class CredentialStoreFactory:
    _instances: dict[str, 'SecureCredentialStore'] = {}
    _lock = Lock()

    @classmethod
    def get_store(cls, namespace: str) -> 'SecureCredentialStore':
        with cls._lock:
            if namespace not in cls._instances:
                cls._instances[namespace] = SecureCredentialStore(namespace)
            return cls._instances[namespace]

# Usage - reuses existing store instance
store = CredentialStoreFactory.get_store("api-keys")
```

### 4.5 Memory-Safe Handling

```python
# BAD: Credentials persist in memory
class UnsafeStore:
    def get_credential(self, key: str) -> str:
        secret = keyring.get_password(self._service, key)
        self.last_retrieved = secret  # Persists in memory
        return secret

# GOOD: Secure memory handling with cleanup
import ctypes
import gc

class SecureMemoryStore:
    def retrieve_and_use(self, key: str, callback) -> None:
        """Retrieve credential, use it, then clear from memory."""
        secret = keyring.get_password(self._service, key)
        if secret is None:
            raise KeyError(f"Credential not found: {key}")

        try:
            callback(secret)
        finally:
            # Overwrite string in memory (best effort in Python)
            if secret:
                secret_bytes = secret.encode()
                ctypes.memset(id(secret_bytes) + 32, 0, len(secret_bytes))
            del secret
            gc.collect()

    def with_credential(self, key: str):
        """Context manager for secure credential access."""
        class CredentialContext:
            def __init__(ctx_self, store, key):
                ctx_self._store = store
                ctx_self._key = key
                ctx_self._value = None

            def __enter__(ctx_self):
                ctx_self._value = keyring.get_password(
                    ctx_self._store._service, ctx_self._key
                )
                return ctx_self._value

            def __exit__(ctx_self, *args):
                if ctx_self._value:
                    del ctx_self._value
                gc.collect()

        return CredentialContext(self, key)

# Usage
store = SecureMemoryStore("secrets")
with store.with_credential("api-key") as api_key:
    make_api_call(api_key)
# Credential cleared after context exits
```

## 5. Core Responsibilities

### 5.1 Primary Functions

1. **Store secrets securely** using OS-native encryption
2. **Retrieve secrets** with proper access control verification
3. **Manage credential lifecycle** including rotation and deletion
4. **Abstract platform differences** for cross-platform code
5. **Integrate with encryption skill** for master key storage

## 6. Technology Stack

### 6.1 Recommended Libraries

| Platform | Library | API | Notes |
|----------|---------|-----|-------|
| Python (cross-platform) | `keyring` | Unified | Auto-detects backend |
| macOS | `Security.framework` | Keychain Services | Native Swift/ObjC |
| Windows | `Windows.Security.Credentials` | Credential Manager | WinRT API |
| Linux | `libsecret` | Secret Service D-Bus | GNOME Keyring backend |

### 6.2 Platform Requirements

- **macOS**: 10.15+ (Keychain Access improvements)
- **Windows**: 10 1903+ (Credential Guard support)
- **Linux**: libsecret 0.20+, GNOME Keyring 3.36+

## 7. Implementation Patterns

### 7.1 Cross-Platform Python Implementation

```python
import keyring
from keyring.errors import KeyringError
import logging

logger = logging.getLogger(__name__)

class SecureCredentialStore:
    """Cross-platform credential storage using OS keychain."""

    SERVICE_PREFIX = "com.jarvis.assistant"

    def __init__(self, namespace: str):
        self._service = f"{self.SERVICE_PREFIX}.{namespace}"
        self._verify_backend()

    def _verify_backend(self):
        """Verify secure keyring backend is available."""
        backend = keyring.get_keyring()
        backend_name = type(backend).__name__

        insecure_backends = ['PlaintextKeyring', 'NullKeyring', 'ChainerBackend']
        if backend_name in insecure_backends:
            raise RuntimeError(f"Insecure keyring backend: {backend_name}")

        logger.info("keychain.backend.initialized", extra={'backend': backend_name})

    def store(self, key: str, secret: str) -> None:
        """Store a credential securely."""
        keyring.set_password(self._service, key, secret)
        logger.info("keychain.credential.stored", extra={'key': key})

    def retrieve(self, key: str) -> str:
        """Retrieve a credential. Raises KeyError if not found."""
        secret = keyring.get_password(self._service, key)
        if secret is None:
            raise KeyError(f"Credential not found: {key}")
        return secret

    def delete(self, key: str) -> None:
        """Delete a credential."""
        keyring.delete_password(self._service, key)
        logger.info("keychain.credential.deleted", extra={'key': key})

    def exists(self, key: str) -> bool:
        """Check if credential exists."""
        return keyring.get_password(self._service, key) is not None
```

### 7.2 Platform-Specific Implementations

For detailed platform-specific implementations with advanced features:

- **macOS Keychain** (ACLs, Touch ID, Secure Enclave): See `references/security-examples.md#macos-keychain`
- **Windows Credential Manager** (DPAPI, Credential Guard): See `references/security-examples.md#windows-credential-manager`
- **Linux Secret Service** (D-Bus, GNOME Keyring): See `references/security-examples.md#linux-secret-service`

## 8. Security Standards

### 8.1 Known Vulnerabilities

| CVE | Severity | Platform | Mitigation |
|-----|----------|----------|------------|
| CVE-2023-21726 | High (7.8) | Windows | Windows Update Jan 2023 |
| CVE-2024-54490 | High | macOS | Update to macOS 15.2+ |
| CVE-2024-44162 | High | macOS | Update to macOS 14.7+ |
| CVE-2024-44243 | High | macOS | Update to macOS 15.2+ |
| CVE-2024-1086 | High (7.8) | Linux | Kernel 6.6.15+ |

### 8.2 OWASP Mapping

| OWASP 2025 | Implementation |
|------------|----------------|
| A01: Broken Access Control | OS-level ACLs, app sandboxing |
| A02: Cryptographic Failures | Platform-native encryption |
| A04: Insecure Design | Defense in depth, least privilege |
| A07: Identification Failures | Credential isolation per service |

### 8.3 Platform Security Features

**macOS**: Secure Enclave, per-item ACLs, code signing, Touch ID gating

**Windows**: DPAPI encryption, Credential Guard, virtualization-based security

**Linux**: D-Bus access control, collection locking, session keyring isolation

For detailed threat analysis, see `references/threat-model.md`.

## 9. Common Mistakes

### 9.1 Critical Anti-Patterns

**Environment Variables for Secrets**
```python
# NEVER: Visible in /proc, logs
api_key = os.environ.get('API_KEY')

# ALWAYS: OS keychain
api_key = SecureCredentialStore("api").retrieve("api-key")
```

**Hardcoded Credentials**
```python
# NEVER: In source code
DATABASE_PASSWORD = "production-password-123"

# ALWAYS: Retrieved at runtime
password = SecureCredentialStore("database").retrieve("password")
```

**Insecure File Storage**
```python
# NEVER: Plain files
with open('~/.config/app/credentials.json') as f:
    creds = json.load(f)

# ALWAYS: Platform keychain
token = SecureCredentialStore("app").retrieve("access-token")
```

**Logging Credentials**
```python
# NEVER: Log values
logger.info(f"Retrieved API key: {api_key}")

# ALWAYS: Log metadata only
logger.info("credential.retrieved", extra={'service': service, 'key': key})
```

**Single Service Name**
```python
# NEVER: All credentials under one service
store = SecureCredentialStore("jarvis")

# ALWAYS: Namespace by credential type
db_store = SecureCredentialStore("database")
api_store = SecureCredentialStore("api-keys")
```

## 10. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Read `references/advanced-patterns.md` for cross-platform patterns
- [ ] Read `references/security-examples.md` for platform implementations
- [ ] Review threat model in `references/threat-model.md`
- [ ] Identify required credential namespaces
- [ ] Design test cases for credential operations
- [ ] Plan caching strategy for performance

### Phase 2: During Implementation

- [ ] Write failing tests first (TDD workflow)
- [ ] Implement minimum code to pass tests
- [ ] Add credential caching with TTL
- [ ] Implement batch loading for multiple credentials
- [ ] Use lazy loading for optional credentials
- [ ] Add memory-safe handling for sensitive operations
- [ ] Verify secure keyring backend at startup
- [ ] Log operations without credential values

### Phase 3: Before Committing

- [ ] All tests pass with `pytest -v`
- [ ] No credentials in test fixtures or logs
- [ ] Cross-platform tests verified
- [ ] Memory leak tests pass
- [ ] Security scan shows no credential leaks
- [ ] Code review for anti-patterns complete

### Platform-Specific Verification

- [ ] **macOS**: Code signing verified for Keychain access
- [ ] **Windows**: Credential Guard compatibility tested
- [ ] **Linux**: Secret Service daemon running, D-Bus accessible
- [ ] OS security updates applied (check CVE list above)

## 11. Summary

### Key Objectives

1. **TDD workflow**: Write tests before implementing credential operations
2. **Performance optimization**: Cache credentials, batch operations, lazy loading
3. **Platform-native storage**: Use OS keychain services for all credentials
4. **Access isolation**: Unique service names prevent cross-contamination
5. **Secure by default**: Reject insecure backends automatically

### Security Reminders

- Credentials in environment variables are NOT secure
- File-based credential storage is NOT secure
- Always verify keyring backend at application startup
- Log credential operations but NEVER values
- Keep OS updated to address keychain vulnerabilities

### References

- `references/advanced-patterns.md` - Cross-platform patterns, migration, testing
- `references/security-examples.md` - Complete platform implementations
- `references/threat-model.md` - Attack scenarios and mitigations

---

**The OS keychain is your first line of defense. Misuse negates all downstream encryption.**
