---
name: keyarc-crypto-flows
description: Use when implementing signup flow, login flow, team sharing, key derivation with Argon2, AES encryption operations, or RSA/ECC key management for KeyArc cryptographic workflows.
---

# KeyArc Cryptographic Flows

## Overview

Implementation patterns for KeyArc's three core cryptographic workflows: signup, login, and team sharing. Provides code examples for Argon2 key derivation, AES-GCM encryption, and RSA-OAEP key sharing.

**All cryptographic operations happen client-side (browser).** The backend services only receive encrypted data:
- **Auth Service** receives: authHash, encrypted vaultKey, encrypted privateKey, publicKey
- **Key Service** receives: encrypted secrets (ciphertext only)
- **Account Service** receives: encrypted teamKey copies (for team sharing)

## When to Use

✅ **Use this skill for:**
- Implementing user signup with key generation
- Implementing user login with key decryption
- Implementing team creation and member addition
- Working with Argon2 key derivation
- Encrypting/decrypting with AES-GCM
- Public key encryption for sharing

## The Three Core Flows

### 1. Signup Flow

**Purpose:** Establish user's encryption keys without server seeing master password.

**Steps:**
```
1. Derive masterKey from password (Argon2)
2. Generate vaultKey (random AES-256)
3. Generate RSA keypair (for sharing)
4. Encrypt vaultKey with masterKey
5. Encrypt privateKey with masterKey
6. Compute authHash from masterKey
7. Send encrypted keys + authHash to server
```

**Key algorithms:** Argon2id for key derivation, AES-256-GCM for encryption, RSA-OAEP for sharing

### 2. Login Flow

**Purpose:** Authenticate user and decrypt their keys client-side.

**Steps:**
```
1. Derive masterKey from password (same Argon2 params)
2. Compute authHash from masterKey
3. Send authHash to server (NOT password!)
4. Server validates authHash, returns encrypted keys
5. Decrypt vaultKey with masterKey
6. Decrypt privateKey with masterKey
7. Store keys in memory for session
```

### 3. Team Sharing Flow

**Purpose:** Share secrets with team using public key cryptography.

**Steps:**
```
Create Team:
1. Generate teamKey (random AES-256)
2. Encrypt teamKey with creator's publicKey
3. Store encrypted teamKey

Add Member:
1. Get new member's publicKey
2. Decrypt teamKey with current member's privateKey
3. Re-encrypt teamKey with new member's publicKey
4. Store new encrypted copy

Share Secret:
1. Encrypt secret with teamKey
2. Store encrypted secret linked to team
```

## Quick Reference: Crypto Parameters

| Operation | Algorithm | Parameters |
|-----------|-----------|------------|
| Key Derivation | Argon2id | time=3, mem=64MB, parallelism=4, hashLen=32 |
| Symmetric Encryption | AES-256-GCM | 256-bit key, 12-byte IV |
| Asymmetric Encryption | RSA-OAEP | 2048-bit, SHA-256 hash |
| Auth Hash | PBKDF2-SHA256 | 100,000 iterations, 256 bits |

## Common Patterns

### Argon2 Key Derivation

```typescript
async function deriveMasterKey(password: string, email: string): Promise<CryptoKey> {
  const salt = new TextEncoder().encode(email.toLowerCase());

  const result = await argon2.hash({
    pass: password,
    salt: salt,
    type: argon2.ArgonType.Argon2id,
    hashLen: 32,
    time: 3,
    mem: 65536,  // 64 MB
    parallelism: 4
  });

  return await crypto.subtle.importKey(
    'raw',
    result.hash,
    { name: 'PBKDF2' },
    false,
    ['deriveKey', 'deriveBits']
  );
}
```

### AES-GCM Encryption

```typescript
async function encryptSecret(
  plaintext: string,
  key: CryptoKey
): Promise<string> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encoded = new TextEncoder().encode(plaintext);

  const ciphertext = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    encoded
  );

  // Return base64: iv + ciphertext
  return btoa(
    String.fromCharCode(...iv) +
    String.fromCharCode(...new Uint8Array(ciphertext))
  );
}

async function decryptSecret(
  encrypted: string,
  key: CryptoKey
): Promise<string> {
  const bytes = Uint8Array.from(atob(encrypted), c => c.charCodeAt(0));
  const iv = bytes.slice(0, 12);
  const ciphertext = bytes.slice(12);

  const decrypted = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv },
    key,
    ciphertext
  );

  return new TextDecoder().decode(decrypted);
}
```

### RSA-OAEP for Team Sharing

```typescript
async function encryptTeamKey(
  teamKey: CryptoKey,
  memberPublicKey: CryptoKey
): Promise<string> {
  const teamKeyBytes = await crypto.subtle.exportKey('raw', teamKey);

  const encrypted = await crypto.subtle.encrypt(
    { name: 'RSA-OAEP' },
    memberPublicKey,
    teamKeyBytes
  );

  return btoa(String.fromCharCode(...new Uint8Array(encrypted)));
}

async function decryptTeamKey(
  encryptedTeamKey: string,
  memberPrivateKey: CryptoKey
): Promise<CryptoKey> {
  const bytes = Uint8Array.from(atob(encryptedTeamKey), c => c.charCodeAt(0));

  const decrypted = await crypto.subtle.decrypt(
    { name: 'RSA-OAEP' },
    memberPrivateKey,
    bytes
  );

  return await crypto.subtle.importKey(
    'raw',
    decrypted,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt']
  );
}
```

## Error Handling

```typescript
// Good: Specific crypto error handling
try {
  const secret = await decryptSecret(encrypted, vaultKey);
  return secret;
} catch (error) {
  if (error.name === 'OperationError') {
    throw new Error('Failed to decrypt secret - invalid key');
  }
  throw error;
}

// Good: Failed auth (wrong password = wrong authHash)
if (authHash !== storedAuthHash) {
  // Generic error (don't reveal which part failed)
  throw new Error('Invalid credentials');
}
```

## Testing Crypto Flows

```typescript
describe('Crypto Flows', () => {
  it('should round-trip encrypt/decrypt', async () => {
    const key = await generateVaultKey();
    const plaintext = 'my-secret-value';

    const encrypted = await encryptSecret(plaintext, key);
    const decrypted = await decryptSecret(encrypted, key);

    expect(decrypted).toBe(plaintext);
    expect(encrypted).not.toBe(plaintext);
  });

  it('should derive same masterKey from same password', async () => {
    const password = 'test-password-123';
    const email = 'test@example.com';

    const key1 = await deriveMasterKey(password, email);
    const key2 = await deriveMasterKey(password, email);

    // Derive same auth hash
    const hash1 = await computeAuthHash(key1);
    const hash2 = await computeAuthHash(key2);

    expect(hash1).toBe(hash2);
  });

  it('should fail decryption with wrong key', async () => {
    const key1 = await generateVaultKey();
    const key2 = await generateVaultKey();

    const encrypted = await encryptSecret('secret', key1);

    await expect(
      decryptSecret(encrypted, key2)
    ).rejects.toThrow();
  });
});
```

## Security Checklist

- [ ] Argon2 used for password-based key derivation
- [ ] AES-256-GCM for symmetric encryption
- [ ] Random IVs generated for each encryption
- [ ] RSA-OAEP with SHA-256 for asymmetric encryption
- [ ] Auth hash uses PBKDF2 (not raw masterKey)
- [ ] All operations use WebCrypto API
- [ ] Keys marked non-extractable where appropriate
- [ ] Sensitive keys cleared from memory when done

## Common Mistakes

**Reusing IVs:**
```typescript
// ❌ BAD: Same IV for multiple encryptions
const iv = crypto.getRandomValues(new Uint8Array(12));
const encrypted1 = await encrypt(secret1, key, iv);
const encrypted2 = await encrypt(secret2, key, iv);  // NEVER reuse IV!

// ✅ GOOD: New IV each time
async function encrypt(data, key) {
  const iv = crypto.getRandomValues(new Uint8Array(12));  // Fresh IV
  // ... encrypt and return iv + ciphertext
}
```

**Weak key derivation:**
```typescript
// ❌ BAD: Weak password hashing
const key = await crypto.subtle.digest('SHA-256', password);

// ✅ GOOD: Argon2 with proper parameters
const key = await deriveMasterKey(password, email);  // Uses Argon2id
```

**Not handling decryption failures:**
```typescript
// ❌ BAD: Assumes decryption always works
const secret = await decryptSecret(encrypted, key);

// ✅ GOOD: Handle potential decryption failure
try {
  const secret = await decryptSecret(encrypted, key);
} catch (error) {
  // Wrong key, corrupted data, etc.
  handleDecryptionError(error);
}
```

## Key Principles

1. **Argon2 for passwords**: Strong, memory-hard key derivation
2. **AES-GCM for secrets**: Authenticated encryption
3. **Fresh IVs**: Never reuse initialization vectors
4. **RSA-OAEP for sharing**: Secure key exchange
5. **WebCrypto API**: Use browser's native crypto
6. **Error handling**: Gracefully handle crypto failures
7. **Testing**: Verify round-trip and failure cases

**Crypto is hard - follow established patterns exactly.**

## Future: OAuth Support

The architecture supports adding OAuth providers (Google, GitHub) while maintaining zero-knowledge:
- OAuth proves identity (who you are)
- Vault password still required for decryption (access to secrets)
- Flow: OAuth login → Auth Service validates identity → Client prompts for vault password → Derive masterKey → Decrypt vaultKey

This maintains zero-knowledge because the OAuth provider and server never see the vault password or masterKey.
