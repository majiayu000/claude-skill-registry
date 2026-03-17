---
name: crypto
description: Client-side cryptography with libsodium. Use when working on files in src/lib/crypto/.
---

# Crypto Guidelines

**All crypto happens client-side. Server NEVER sees plaintext.**

## Architecture

- Seed phrase (128-bit) → Ed25519 keypair (signing) → X25519 keypair (encryption)
- Vault key (random 256-bit) wrapped with user's X25519 public key
- Data encrypted with XChaCha20-Poly1305

## Critical Rules

1. **Never log keys or sensitive data** - not even in development
2. **Use libsodium** - don't implement crypto primitives
3. **Async everywhere** - all functions async (libsodium-wrappers)
4. **Constant-time comparisons** - `sodium.compare` for secrets
5. **Zeroize secrets** - `sodium.memzero` when done
6. **Type-safe keys** - use branded types (VaultKey, SigningKey)

## Common Pitfalls

- Don't use `crypto.randomBytes` → use `sodium.randombytes_buf`
- Don't concatenate key material → use proper KDFs
- Don't store keys in localStorage without encryption
- Don't forget `await sodium.ready` before operations

## Testing

Use property-based tests for roundtrip verification with fast-check.
