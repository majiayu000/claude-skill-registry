---
name: keyarc-zero-knowledge
description: Use when implementing client-side encryption, master key derivation, vault key management, secret storage, or any cryptographic operation for KeyArc. Ensures server never sees plaintext secrets or passwords.
---

# KeyArc Zero-Knowledge Architecture

## Core Principle
**"The server must never be able to decrypt user data."**

KeyArc implements Bitwarden-style zero-knowledge encryption where ALL cryptographic operations happen client-side. The server stores only encrypted ciphertext and authentication hashes.

**This applies to all backend services:**
- **Auth Service** - stores encrypted keys, validates authHash (not passwords)
- **Account Service** - stores encrypted teamKey copies
- **Key Service** - stores encrypted secrets (ciphertext only)

## Iron Law
**NEVER SEND PLAINTEXT SECRETS OR MASTER PASSWORDS TO THE SERVER**

Any code that sends unencrypted secrets or master passwords to the server must be deleted and redesigned.

## When to Use This Skill

✅ **Always apply for:**
- User signup/registration flow
- User login/authentication flow
- Secret creation or updates
- Team sharing functionality
- Key derivation operations
- Any operation involving master password
- Any operation involving encryption keys
- API endpoint design for secrets

## Core Architecture Principles

### 1. Server Blindness
The server CANNOT and MUST NOT be able to decrypt user data at any time.

**What server knows:**
- Encrypted vaultKey (encrypted with masterKey)
- Encrypted privateKey (encrypted with masterKey)
- Public key (for sharing, not sensitive)
- Auth hash (derived from masterKey, for authentication)
- Encrypted secrets (ciphertext only)

**What server NEVER knows:**
- Master password
- Master key (derived from master password)
- Vault key (decrypted)
- Private key (decrypted)
- Plaintext secrets

### 2. Client-Side Only Crypto
ALL encryption and decryption happens in the browser using WebCrypto API.

**Client responsibilities:**
- Master password handling
- Key derivation (Argon2)
- Encryption/decryption operations
- Key generation (vault keys, keypairs)
- Computing auth hashes

**Server responsibilities:**
- Store encrypted data (ciphertext)
- Validate auth hashes (NOT passwords)
- Serve encrypted keys back to client
- Enforce access control on encrypted data

### 3. No Plaintext Transit
Only encrypted ciphertext and hashes cross the network boundary.

**Safe to send to server:**
- ✅ Encrypted vault key
- ✅ Encrypted private key
- ✅ Auth hash
- ✅ Encrypted secrets (ciphertext)
- ✅ Public keys
- ✅ Email, metadata, timestamps

**NEVER send to server:**
- ❌ Master password
- ❌ Master key
- ❌ Decrypted vault key
- ❌ Decrypted private key
- ❌ Plaintext secrets
- ❌ Decryption keys

## Implementation Checklist

Before implementing ANY feature involving secrets:

- [ ] Master password stays client-side only?
- [ ] Key derivation uses Argon2 with correct parameters?
- [ ] Encryption uses WebCrypto API in browser?
- [ ] Server receives only ciphertext, never plaintext?
- [ ] Auth uses authHash, never password?
- [ ] Error messages don't leak secret values?
- [ ] Logs don't contain sensitive data?
- [ ] API endpoints validate encrypted payloads?

## Good vs Bad Examples

### Master Password Handling

```typescript
// ❌ BAD: Sending password to server
async function login(email: string, password: string) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })  // NEVER!
  });
}

// ✅ GOOD: Derive key client-side, send only authHash
async function login(email: string, password: string) {
  // All crypto happens in browser
  const masterKey = await deriveMasterKey(password, email);
  const authHash = await computeAuthHash(masterKey);

  // Only hash sent to server
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, authHash })
  });

  // Server validates authHash and returns encrypted keys
  const { encrypted_vault_key, encrypted_private_key } = await response.json();

  // Decrypt keys client-side
  const vaultKey = await decryptVaultKey(encrypted_vault_key, masterKey);
  const privateKey = await decryptPrivateKey(encrypted_private_key, masterKey);

  return { vaultKey, privateKey };
}
```

### Secret Storage

```typescript
// ❌ BAD: Sending plaintext secret to server
async function createSecret(name: string, value: string) {
  await fetch('/api/secrets', {
    method: 'POST',
    body: JSON.stringify({ name, value })  // Plaintext! NEVER!
  });
}

// ✅ GOOD: Encrypt client-side, send ciphertext
async function createSecret(
  name: string,
  value: string,
  vaultKey: CryptoKey
) {
  // Encrypt in browser
  const encryptedValue = await encryptSecret(value, vaultKey);

  // Send only ciphertext
  await fetch('/api/secrets', {
    method: 'POST',
    body: JSON.stringify({
      name,  // Metadata can be plaintext
      encrypted_value: encryptedValue  // Ciphertext only
    })
  });
}
```

### Server-Side Validation

```python
# ❌ BAD: Server decrypts data (impossible anyway without keys)
@router.post("/secrets/")
async def create_secret(secret: SecretCreate, db: AsyncSession):
    plaintext = decrypt(secret.value, server_key)  # NEVER!
    db_secret = Secret(value=plaintext)
    # ...

# ✅ GOOD: Server validates it's encrypted, stores ciphertext
@router.post("/secrets/")
async def create_secret(secret: SecretCreate, db: AsyncSession):
    # Validate encrypted_value looks like ciphertext
    if not is_valid_ciphertext(secret.encrypted_value):
        raise HTTPException(400, "Invalid encrypted format")

    # Store ciphertext as-is, never decrypt
    db_secret = Secret(
        name=secret.name,
        encrypted_value=secret.encrypted_value  # Store ciphertext
    )
    db.add(db_secret)
    await db.commit()
    return db_secret
```

## Flow Principles Summary

**Signup:** Generate keys client-side → Encrypt with masterKey → Send ciphertext to server
**Login:** Derive masterKey → Compute authHash → Server validates → Decrypt keys client-side
**Sharing:** Each member gets teamKey encrypted with their publicKey (server can't decrypt)

## Common Mistakes to Avoid

### 1. Validating Passwords Server-Side
```python
# ❌ BAD: Server validates password
def login(password: str, stored_hash: str):
    return bcrypt.verify(password, stored_hash)

# ✅ GOOD: Server validates authHash
def login(auth_hash: str, stored_auth_hash: str):
    return auth_hash == stored_auth_hash
```

### 2. Logging Sensitive Data
```python
# ❌ BAD: Logging secrets
logger.info(f"Creating secret: {secret.value}")  # NEVER!

# ✅ GOOD: Log only metadata
logger.info(f"Creating secret: {secret.id}, user: {user.id}")
```

### 3. Error Messages Leaking Data
```typescript
// ❌ BAD: Error contains secret
throw new Error(`Invalid secret value: ${secretValue}`);

// ✅ GOOD: Generic error
throw new Error('Invalid secret format');
```

### 4. Accepting Plaintext in API
```python
# ❌ BAD: API accepts plaintext
class SecretCreate(BaseModel):
    value: str  # Plaintext! Never!

# ✅ GOOD: API requires encrypted format
class SecretCreate(BaseModel):
    encrypted_value: str  # Ciphertext only
    iv: str  # Initialization vector
    # ... other crypto metadata
```

## Security Review Checklist

Before merging ANY code involving cryptography:

**Client-Side (TypeScript/Angular):**
- [ ] Master password never sent to server
- [ ] All key derivation uses Argon2
- [ ] All encryption uses WebCrypto API
- [ ] Keys stored in memory only, never persisted
- [ ] Auth hash computed from master key
- [ ] Secrets encrypted before API calls

**Server-Side (Python/FastAPI):**
- [ ] Endpoints accept only encrypted payloads
- [ ] No decryption operations exist (server can't decrypt)
- [ ] Auth validates authHash, not passwords
- [ ] No plaintext secrets in database
- [ ] Audit logs don't contain sensitive data
- [ ] Error responses don't leak secrets

**Testing:**
- [ ] Test that server cannot decrypt user data
- [ ] Test that master password never transits network
- [ ] Test encryption/decryption round-trips
- [ ] Test auth hash validation
- [ ] Test error cases don't expose secrets

## Red Flags Requiring Immediate Fix

🚩 Master password sent in HTTP request
🚩 Server code attempts to decrypt user secrets
🚩 Plaintext secrets in database
🚩 Password validation instead of authHash validation
🚩 Secrets in log messages
🚩 API accepting plaintext instead of ciphertext
🚩 WebCrypto operations on server-side
🚩 Storing keys unencrypted

**Any red flag above is a critical security violation. Stop and redesign.**

## Key Principles

1. **Server blindness**: Server can never decrypt
2. **Client-side crypto**: All encryption in browser
3. **Hash-based auth**: authHash, never password
4. **Encrypted transit**: Only ciphertext crosses network
5. **Zero trust**: Assume server is compromised
6. **Audit everything**: Log access, not values
7. **Fail secure**: Errors don't leak data

**Zero-knowledge means the server learns NOTHING about user secrets.**
