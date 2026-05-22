---
name: cryptography
description: Comprehensive cryptography guidance covering encryption algorithms, password hashing, TLS configuration, key management, and post-quantum considerations. Use when implementing encryption, choosing hashing algorithms, configuring TLS/SSL, managing cryptographic keys, or reviewing cryptographic implementations.
allowed-tools: Read, Glob, Grep, Task
---

# Cryptography

Comprehensive guidance for implementing cryptographic operations securely, covering encryption algorithms, password hashing, TLS, and key management.

## When to Use This Skill

Use this skill when:

- Choosing encryption algorithms
- Implementing password hashing
- Configuring TLS/SSL
- Managing cryptographic keys
- Implementing digital signatures
- Generating random values
- Reviewing cryptographic implementations
- Considering post-quantum readiness

## Algorithm Quick Reference

### Encryption Algorithms

| Algorithm | Type | Key Size | Use Case | Status |
|-----------|------|----------|----------|--------|
| AES-256-GCM | Symmetric | 256 bits | Data encryption | ✅ Recommended |
| ChaCha20-Poly1305 | Symmetric | 256 bits | Data encryption (mobile) | ✅ Recommended |
| RSA-OAEP | Asymmetric | 2048+ bits | Key exchange | ✅ Recommended |
| ECDH (P-256) | Asymmetric | 256 bits | Key agreement | ✅ Recommended |
| X25519 | Asymmetric | 256 bits | Key agreement | ✅ Recommended |
| DES | Symmetric | 56 bits | None | ❌ Deprecated |
| 3DES | Symmetric | 168 bits | Legacy only | ⚠️ Avoid |
| Blowfish | Symmetric | 32-448 bits | None | ⚠️ Avoid |

### Signature Algorithms

| Algorithm | Type | Key Size | Use Case | Status |
|-----------|------|----------|----------|--------|
| Ed25519 | EdDSA | 256 bits | Signatures | ✅ Recommended |
| ECDSA (P-256) | ECC | 256 bits | Signatures, JWT | ✅ Recommended |
| RSA-PSS | RSA | 2048+ bits | Signatures | ✅ Recommended |
| RSA PKCS#1 v1.5 | RSA | 2048+ bits | Legacy signatures | ⚠️ Use PSS instead |

### Hash Functions

| Algorithm | Output Size | Use Case | Status |
|-----------|-------------|----------|--------|
| SHA-256 | 256 bits | General hashing | ✅ Recommended |
| SHA-384 | 384 bits | Higher security | ✅ Recommended |
| SHA-512 | 512 bits | Highest security | ✅ Recommended |
| SHA-3-256 | 256 bits | Alternative to SHA-2 | ✅ Recommended |
| BLAKE2b | 256-512 bits | Fast hashing | ✅ Recommended |
| MD5 | 128 bits | None (broken) | ❌ Never use |
| SHA-1 | 160 bits | None (broken) | ❌ Never use |

## Password Hashing

**Never use general-purpose hash functions (SHA-256, MD5) for passwords.**

### Algorithm Comparison

| Algorithm | Recommended | Memory-Hard | Notes |
|-----------|-------------|-------------|-------|
| Argon2id | ✅ Best | Yes | Winner of PHC, recommended for new systems |
| bcrypt | ✅ Good | No | Widely supported, proven |
| scrypt | ✅ Good | Yes | Good but complex to tune |
| PBKDF2 | ⚠️ Acceptable | No | NIST approved, but GPU-vulnerable |

### Argon2id (Recommended)

```csharp
using Konscious.Security.Cryptography;
using System.Security.Cryptography;
using System.Text;

/// <summary>
/// Argon2id password hasher with OWASP 2023 recommended parameters.
/// </summary>
public static class Argon2PasswordHasher
{
    private const int DegreeOfParallelism = 4;
    private const int MemorySize = 65536;  // 64 MB
    private const int Iterations = 3;
    private const int HashLength = 32;
    private const int SaltLength = 16;

    /// <summary>
    /// Hash password with Argon2id.
    /// </summary>
    public static string Hash(string password)
    {
        var salt = RandomNumberGenerator.GetBytes(SaltLength);
        var hash = ComputeHash(password, salt);

        // Return in PHC format: $argon2id$v=19$m=65536,t=3,p=4$salt$hash
        return $"$argon2id$v=19$m={MemorySize},t={Iterations},p={DegreeOfParallelism}${Convert.ToBase64String(salt)}${Convert.ToBase64String(hash)}";
    }

    /// <summary>
    /// Verify password against stored hash.
    /// </summary>
    public static bool Verify(string storedHash, string password)
    {
        var parts = ParseHash(storedHash);
        if (parts is null) return false;

        var computedHash = ComputeHash(password, parts.Value.Salt);
        return CryptographicOperations.FixedTimeEquals(computedHash, parts.Value.Hash);
    }

    private static byte[] ComputeHash(string password, byte[] salt)
    {
        using var argon2 = new Argon2id(Encoding.UTF8.GetBytes(password))
        {
            Salt = salt,
            DegreeOfParallelism = DegreeOfParallelism,
            MemorySize = MemorySize,
            Iterations = Iterations
        };
        return argon2.GetBytes(HashLength);
    }

    private static (byte[] Salt, byte[] Hash)? ParseHash(string storedHash)
    {
        // Parse PHC format: $argon2id$v=19$m=...,t=...,p=...$salt$hash
        var parts = storedHash.Split('$');
        if (parts.Length < 6) return null;

        var salt = Convert.FromBase64String(parts[4]);
        var hash = Convert.FromBase64String(parts[5]);
        return (salt, hash);
    }
}

// Usage
var hash = Argon2PasswordHasher.Hash("user_password");
// Returns: $argon2id$v=19$m=65536,t=3,p=4$...

if (Argon2PasswordHasher.Verify(hash, "user_password"))
{
    // Password valid
}
```

### bcrypt

```csharp
using BCrypt.Net;

// Hash password (work factor 12 = 2^12 iterations)
var passwordHash = BCrypt.Net.BCrypt.HashPassword("user_password", workFactor: 12);

// Verify password
if (BCrypt.Net.BCrypt.Verify("user_password", passwordHash))
{
    Console.WriteLine("Password valid");
}
```

### Work Factor Guidelines

| Algorithm | Minimum | Recommended | High Security |
|-----------|---------|-------------|---------------|
| Argon2id | t=2, m=19MB | t=3, m=64MB | t=4, m=128MB |
| bcrypt | 10 | 12 | 14 |
| scrypt | N=2^14 | N=2^16 | N=2^18 |
| PBKDF2 | 310,000 | 600,000 | 1,000,000 |

**For detailed password hashing guidance:** See [Password Hashing Reference](references/password-hashing.md)

## Symmetric Encryption

### AES-256-GCM (Recommended)

```csharp
using System.Security.Cryptography;

/// <summary>
/// AES-256-GCM encryption utilities.
/// </summary>
public static class AesGcmEncryption
{
    private const int NonceSize = 12;  // 96 bits
    private const int TagSize = 16;    // 128 bits
    private const int KeySize = 32;    // 256 bits

    /// <summary>
    /// Encrypt data with AES-256-GCM. Returns nonce + ciphertext + tag.
    /// </summary>
    public static byte[] Encrypt(ReadOnlySpan<byte> plaintext, ReadOnlySpan<byte> key)
    {
        var nonce = RandomNumberGenerator.GetBytes(NonceSize);
        var ciphertext = new byte[plaintext.Length];
        var tag = new byte[TagSize];

        using var aes = new AesGcm(key, TagSize);
        aes.Encrypt(nonce, plaintext, ciphertext, tag);

        // Combine: nonce + ciphertext + tag
        var result = new byte[NonceSize + ciphertext.Length + TagSize];
        nonce.CopyTo(result.AsSpan(0, NonceSize));
        ciphertext.CopyTo(result.AsSpan(NonceSize));
        tag.CopyTo(result.AsSpan(NonceSize + ciphertext.Length));

        return result;
    }

    /// <summary>
    /// Decrypt data with AES-256-GCM. Input is nonce + ciphertext + tag.
    /// </summary>
    public static byte[] Decrypt(ReadOnlySpan<byte> combined, ReadOnlySpan<byte> key)
    {
        var nonce = combined[..NonceSize];
        var ciphertext = combined[NonceSize..^TagSize];
        var tag = combined[^TagSize..];

        var plaintext = new byte[ciphertext.Length];

        using var aes = new AesGcm(key, TagSize);
        aes.Decrypt(nonce, ciphertext, tag, plaintext);

        return plaintext;
    }

    /// <summary>
    /// Generate a secure 256-bit key.
    /// </summary>
    public static byte[] GenerateKey() => RandomNumberGenerator.GetBytes(KeySize);
}

// Usage
var key = AesGcmEncryption.GenerateKey();
var encrypted = AesGcmEncryption.Encrypt("sensitive data"u8, key);
var decrypted = AesGcmEncryption.Decrypt(encrypted, key);
```

### Key Derivation from Password

```csharp
using System.Security.Cryptography;
using System.Text;

/// <summary>
/// Derive encryption key from password using PBKDF2.
/// </summary>
public static class KeyDerivation
{
    private const int SaltSize = 16;
    private const int KeySize = 32;  // 256 bits for AES-256
    private const int Iterations = 600000;  // OWASP 2023 recommendation

    /// <summary>
    /// Derive encryption key from password. Returns (key, salt).
    /// </summary>
    public static (byte[] Key, byte[] Salt) DeriveKey(string password, byte[]? salt = null)
    {
        salt ??= RandomNumberGenerator.GetBytes(SaltSize);

        var key = Rfc2898DeriveBytes.Pbkdf2(
            password: Encoding.UTF8.GetBytes(password),
            salt: salt,
            iterations: Iterations,
            hashAlgorithm: HashAlgorithmName.SHA256,
            outputLength: KeySize
        );

        return (key, salt);  // Store salt with encrypted data
    }
}
```

## Asymmetric Encryption

### RSA Key Generation

```csharp
using System.Security.Cryptography;

/// <summary>
/// RSA encryption with OAEP padding.
/// </summary>
public static class RsaEncryption
{
    /// <summary>
    /// Generate RSA key pair. Use 2048 minimum; 4096 for long-term security.
    /// </summary>
    public static RSA GenerateKeyPair(int keySizeInBits = 2048)
    {
        return RSA.Create(keySizeInBits);
    }

    /// <summary>
    /// Encrypt with public key using OAEP-SHA256.
    /// </summary>
    public static byte[] Encrypt(byte[] plaintext, RSA publicKey)
    {
        return publicKey.Encrypt(plaintext, RSAEncryptionPadding.OaepSHA256);
    }

    /// <summary>
    /// Decrypt with private key using OAEP-SHA256.
    /// </summary>
    public static byte[] Decrypt(byte[] ciphertext, RSA privateKey)
    {
        return privateKey.Decrypt(ciphertext, RSAEncryptionPadding.OaepSHA256);
    }
}

// Usage
using var rsa = RsaEncryption.GenerateKeyPair(4096);
var publicKey = rsa.ExportRSAPublicKey();

var ciphertext = RsaEncryption.Encrypt(plaintext, rsa);
var decrypted = RsaEncryption.Decrypt(ciphertext, rsa);
```

### Digital Signatures

```csharp
using System.Security.Cryptography;

/// <summary>
/// Ed25519 digital signatures (via ECDsa with curve).
/// Note: .NET 10 has native Ed25519 support.
/// </summary>
public static class DigitalSignatures
{
    /// <summary>
    /// Create ECDSA key pair (P-256, widely supported).
    /// </summary>
    public static ECDsa CreateEcdsaKeyPair()
    {
        return ECDsa.Create(ECCurve.NamedCurves.nistP256);
    }

    /// <summary>
    /// Sign message with ECDSA-SHA256.
    /// </summary>
    public static byte[] Sign(byte[] message, ECDsa privateKey)
    {
        return privateKey.SignData(message, HashAlgorithmName.SHA256);
    }

    /// <summary>
    /// Verify signature.
    /// </summary>
    public static bool Verify(byte[] message, byte[] signature, ECDsa publicKey)
    {
        return publicKey.VerifyData(message, signature, HashAlgorithmName.SHA256);
    }
}

// Usage
using var ecdsa = DigitalSignatures.CreateEcdsaKeyPair();

var signature = DigitalSignatures.Sign(message, ecdsa);

if (DigitalSignatures.Verify(message, signature, ecdsa))
{
    Console.WriteLine("Signature valid");
}
else
{
    Console.WriteLine("Signature invalid");
}
```

**For detailed algorithm selection guidance:** See [Algorithm Selection Guide](references/algorithm-selection.md)

## TLS Configuration

### Recommended TLS Settings

```nginx
# Nginx TLS configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;

# HSTS (HTTP Strict Transport Security)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
```

### TLS Version Requirements

| Version | Status | Notes |
|---------|--------|-------|
| TLS 1.3 | ✅ Required | Best security, improved performance |
| TLS 1.2 | ✅ Acceptable | Still secure with proper ciphers |
| TLS 1.1 | ❌ Deprecated | Disabled since 2020 |
| TLS 1.0 | ❌ Deprecated | Major vulnerabilities |
| SSL 3.0 | ❌ Broken | POODLE attack |
| SSL 2.0 | ❌ Broken | Many vulnerabilities |

**For detailed TLS configuration:** See [TLS Configuration Guide](references/tls-configuration.md)

## Key Management

### Key Hierarchy

```text
┌─────────────────────────────────────┐
│  Master Key (KEK)                   │  <- Stored in HSM or KMS
│  - Encrypts all other keys          │
└──────────────────┬──────────────────┘
                   │
       ┌───────────┴───────────┐
       ▼                       ▼
┌──────────────┐      ┌──────────────┐
│  Data Key 1  │      │  Data Key 2  │  <- Encrypted with KEK
│  (DEK)       │      │  (DEK)       │
└──────────────┘      └──────────────┘
```

### Key Rotation Strategy

```csharp
/// <summary>
/// Key manager with automatic rotation support.
/// </summary>
public sealed class KeyManager(IKmsClient kmsClient) : IDisposable
{
    private static readonly TimeSpan RotationPeriod = TimeSpan.FromDays(90);

    private string? _currentKeyId;
    private DateTime? _keyExpiry;
    private readonly SemaphoreSlim _lock = new(1, 1);

    /// <summary>
    /// Get current encryption key, rotating if needed.
    /// </summary>
    public async Task<string> GetCurrentKeyAsync(CancellationToken cancellationToken = default)
    {
        await _lock.WaitAsync(cancellationToken);
        try
        {
            if (NeedsRotation())
            {
                await RotateKeyAsync(cancellationToken);
            }
            return _currentKeyId!;
        }
        finally
        {
            _lock.Release();
        }
    }

    private bool NeedsRotation() =>
        _keyExpiry is null || DateTime.UtcNow > _keyExpiry;

    private async Task RotateKeyAsync(CancellationToken cancellationToken)
    {
        // Create new key in KMS
        var newKey = await kmsClient.CreateKeyAsync(
            description: $"Data key created {DateTime.UtcNow:O}",
            keyUsage: KeyUsage.EncryptDecrypt,
            cancellationToken: cancellationToken
        );

        _currentKeyId = newKey.KeyId;
        _keyExpiry = DateTime.UtcNow.Add(RotationPeriod);

        // Keep old keys for decryption (don't delete immediately)
        // Data encrypted with old keys can still be decrypted
    }

    public void Dispose() => _lock.Dispose();
}

// KMS client interface (implement for Azure Key Vault, AWS KMS, etc.)
public interface IKmsClient
{
    Task<KmsKey> CreateKeyAsync(string description, KeyUsage keyUsage, CancellationToken cancellationToken);
}

public enum KeyUsage { EncryptDecrypt, SignVerify }
public sealed record KmsKey(string KeyId, DateTime CreatedAt);
```

## Random Number Generation

```csharp
using System.Security.Cryptography;

// For cryptographic use - ALWAYS use these
var secureRandomBytes = RandomNumberGenerator.GetBytes(32);  // 32 random bytes
var secureRandomHex = Convert.ToHexString(RandomNumberGenerator.GetBytes(32));  // 64 hex chars
var secureRandomUrl = Convert.ToBase64String(RandomNumberGenerator.GetBytes(32))
    .Replace('+', '-').Replace('/', '_').TrimEnd('=');  // URL-safe base64

// For random integers in a range (e.g., tokens, OTPs)
var randomInt = RandomNumberGenerator.GetInt32(100000, 999999);  // 6-digit OTP

// NEVER use for cryptography
var random = new Random();
random.Next();  // NOT cryptographically secure - for games/simulations only
```

## Post-Quantum Considerations

Current asymmetric algorithms (RSA, ECDSA, ECDH) are vulnerable to quantum computers.

### NIST Post-Quantum Standards (2024)

| Algorithm | Type | Status |
|-----------|------|--------|
| ML-KEM (Kyber) | Key Encapsulation | ✅ Standardized |
| ML-DSA (Dilithium) | Digital Signature | ✅ Standardized |
| SLH-DSA (SPHINCS+) | Digital Signature | ✅ Standardized |

### Hybrid Approach (Recommended Now)

```csharp
// Combine classical and post-quantum algorithms
// If either is broken, the other still provides security

// Key exchange: X25519 + ML-KEM-768
// Signature: ECDSA P-256 + ML-DSA-65

// .NET 10+ will include ML-KEM and ML-DSA support
// Until then, use libraries like BouncyCastle for PQ algorithms

// This provides defense-in-depth during the transition period:
// 1. Classical algorithms handle today's threats
// 2. PQ algorithms protect against future quantum attacks
// 3. Combined key material ensures security if either is compromised
```

## Quick Decision Tree

**What cryptographic operation do you need?**

1. **Encrypt data at rest** → AES-256-GCM
2. **Encrypt data in transit** → TLS 1.3
3. **Hash passwords** → Argon2id
4. **Hash data (non-password)** → SHA-256 or BLAKE2b
5. **Digital signatures** → Ed25519 or ECDSA P-256
6. **Key exchange** → X25519 or ECDH P-256
7. **Message authentication** → HMAC-SHA256
8. **Generate random values** → `RandomNumberGenerator.GetBytes()` or `RandomNumberGenerator.GetInt32()`

## Security Checklist

### Encryption

- [ ] Use authenticated encryption (AES-GCM, ChaCha20-Poly1305)
- [ ] Generate keys with sufficient entropy (256 bits)
- [ ] Never reuse nonces/IVs
- [ ] Implement proper key management

### Password Hashing

- [ ] Use Argon2id, bcrypt, or scrypt
- [ ] Never use MD5, SHA-1, or unsalted hashes
- [ ] Use appropriate work factors
- [ ] Implement rehashing when parameters change

### TLS

- [ ] TLS 1.2 minimum, prefer TLS 1.3
- [ ] Strong cipher suites only
- [ ] Valid certificates from trusted CA
- [ ] Enable HSTS

### Keys

- [ ] Secure key generation
- [ ] Proper key storage (HSM/KMS for sensitive keys)
- [ ] Key rotation policy
- [ ] Secure key destruction

## References

- [Algorithm Selection Guide](references/algorithm-selection.md) - Detailed algorithm comparison
- [Password Hashing Reference](references/password-hashing.md) - Password hashing deep dive
- [TLS Configuration Guide](references/tls-configuration.md) - TLS setup for various platforms

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `authentication-patterns` | Uses cryptography for JWT, sessions |
| `secrets-management` | Secure storage of cryptographic keys |
| `secure-coding` | General secure implementation patterns |

## Version History

- v1.0.0 (2025-12-26): Initial release with algorithms, password hashing, TLS, key management

---

**Last Updated:** 2025-12-26
