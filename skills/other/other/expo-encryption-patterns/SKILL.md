---
name: expo-encryption-patterns
description: Implement AES-256-CBC encryption with secure key storage for Expo/React Native apps using expo-secure-store and crypto-js. Use when encrypting sensitive user data (journal entries, health data, PII), storing encryption keys securely, implementing encrypt-then-MAC patterns, or working with expo-sqlite encrypted data. Covers key generation, encryption/decryption flows, and platform-agnostic crypto operations.
---

# Expo Encryption Patterns

Implement production-grade encryption for Expo/React Native apps with secure key management.

## Core Pattern

### 1. Key Management

Store encryption keys ONLY in `expo-secure-store` (Keychain/Keystore). Never use AsyncStorage.

```typescript
import * as SecureStore from 'expo-secure-store';

const ENCRYPTION_KEY_NAME = 'app_encryption_key';

async function getOrCreateKey(): Promise<string> {
  let key = await SecureStore.getItemAsync(ENCRYPTION_KEY_NAME);
  if (!key) {
    key = await generateSecureKey();
    await SecureStore.setItemAsync(ENCRYPTION_KEY_NAME, key);
  }
  return key;
}
```

### 2. Encrypt Content (AES-256-CBC + HMAC)

Format: `{iv}:{ciphertext}:{mac}`

```typescript
import CryptoJS from 'crypto-js';
import * as Crypto from 'expo-crypto';

async function encryptContent(plaintext: string): Promise<string> {
  const key = await getOrCreateKey();

  // Generate unique IV
  const ivBytes = await Crypto.getRandomBytesAsync(16);
  const iv = Array.from(ivBytes)
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');

  const ivWordArray = CryptoJS.enc.Hex.parse(iv);
  const keyWordArray = CryptoJS.enc.Hex.parse(key);

  // Encrypt
  const encrypted = CryptoJS.AES.encrypt(plaintext, keyWordArray, {
    iv: ivWordArray,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7,
  });

  // Generate MAC (encrypt-then-MAC)
  const payload = `${iv}:${encrypted.toString()}`;
  const macKey = CryptoJS.SHA256(keyWordArray);
  const mac = CryptoJS.HmacSHA256(payload, macKey).toString(CryptoJS.enc.Hex);

  return `${payload}:${mac}`;
}
```

### 3. Decrypt Content with MAC Verification

```typescript
async function decryptContent(encrypted: string): Promise<string> {
  const key = await getOrCreateKey();
  const parts = encrypted.split(':');

  if (parts.length !== 3) throw new Error('Invalid format');
  const [iv, ciphertext, mac] = parts;

  // Verify MAC (constant-time comparison)
  const keyWordArray = CryptoJS.enc.Hex.parse(key);
  const macKey = CryptoJS.SHA256(keyWordArray);
  const payload = `${iv}:${ciphertext}`;
  const expectedMac = CryptoJS.HmacSHA256(payload, macKey).toString(CryptoJS.enc.Hex);

  if (!constantTimeEqual(expectedMac, mac)) {
    throw new Error('Integrity check failed');
  }

  // Decrypt
  const ivWordArray = CryptoJS.enc.Hex.parse(iv);
  const decrypted = CryptoJS.AES.decrypt(ciphertext, keyWordArray, {
    iv: ivWordArray,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7,
  });

  return decrypted.toString(CryptoJS.enc.Utf8);
}

function constantTimeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let result = 0;
  for (let i = 0; i < a.length; i++) {
    result |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return result === 0;
}
```

## Platform-Agnostic Crypto

Use different crypto sources for native vs web:

```typescript
import { Platform } from 'react-native';

async function getRandomBytes(length: number): Promise<Uint8Array> {
  if (Platform.OS === 'web') {
    return crypto.getRandomValues(new Uint8Array(length));
  }
  const { getRandomBytesAsync } = await import('expo-crypto');
  return getRandomBytesAsync(length);
}
```

## Key Derivation (PBKDF2)

For user-password-based keys:

```typescript
function deriveKey(password: string, salt: string): string {
  return CryptoJS.PBKDF2(password, salt, {
    keySize: 256 / 32,
    iterations: 100000,
  }).toString();
}
```

## Integration with SQLite

Encrypt before storing, decrypt after retrieval:

```typescript
// Storing
const encrypted = await encryptContent(journalEntry);
await db.runAsync('INSERT INTO journal (encrypted_body) VALUES (?)', encrypted);

// Retrieving
const rows = await db.getAllAsync('SELECT encrypted_body FROM journal');
const entries = await Promise.all(
  rows.map(async (row) => ({
    ...row,
    content: await decryptContent(row.encrypted_body),
  })),
);
```

## Security Checklist

- [ ] Keys stored only in SecureStore
- [ ] Unique IV generated per encryption
- [ ] MAC verification before decryption
- [ ] Constant-time MAC comparison
- [ ] PBKDF2 for password-based keys (100k+ iterations)
- [ ] No sensitive data in logs
- [ ] Keys deleted on logout/account deletion

## See Also

- [references/web-crypto.md](references/web-crypto.md) - Web-specific crypto patterns
- [test-encryption skill](../test-encryption/SKILL.md) - Testing encrypted flows
