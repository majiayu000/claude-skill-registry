---
name: test-encryption
description: Write Jest tests for encryption/decryption flows in React Native apps using expo-secure-store mocks and crypto-js. Use when testing encrypted data storage, verifying encryption roundtrips, mocking secure storage in tests, or testing SQLite with encrypted content.
---

# Testing Encryption

Jest testing patterns for encrypted data flows in React Native.

## Setup

### Mock Secure Store

```typescript
// __mocks__/expo-secure-store.ts
const store = new Map<string, string>();

export default {
  getItemAsync: jest.fn((key: string) => Promise.resolve(store.get(key) || null)),
  setItemAsync: jest.fn((key: string, value: string) => {
    store.set(key, value);
    return Promise.resolve();
  }),
  deleteItemAsync: jest.fn((key: string) => {
    store.delete(key);
    return Promise.resolve();
  }),
};

// Clear between tests
beforeEach(() => store.clear());
```

### Mock Expo Crypto

```typescript
// __mocks__/expo-crypto.ts
export const getRandomBytesAsync = jest.fn((length: number) => {
  return Promise.resolve(new Uint8Array(length).fill(0x42));
});

export const randomUUID = jest.fn(() => 'mock-uuid-123');
```

## Core Encryption Tests

### Roundtrip Test (Critical)

```typescript
import { encryptContent, decryptContent, generateEncryptionKey } from '../encryption';

describe('Encryption', () => {
  beforeEach(async () => {
    await generateEncryptionKey();
  });

  it('should encrypt and decrypt to return original text', async () => {
    const plaintext = 'My sensitive journal entry about recovery';

    const encrypted = await encryptContent(plaintext);

    // Verify encrypted format
    expect(encrypted).toContain(':');
    expect(encrypted).not.toBe(plaintext);

    // Decrypt and verify
    const decrypted = await decryptContent(encrypted);
    expect(decrypted).toBe(plaintext);
  });

  it('should produce different ciphertexts for same plaintext (unique IV)', async () => {
    const plaintext = 'Same text';

    const encrypted1 = await encryptContent(plaintext);
    const encrypted2 = await encryptContent(plaintext);

    expect(encrypted1).not.toBe(encrypted2);
  });
});
```

### MAC Verification Tests

```typescript
it('should throw on tampered ciphertext', async () => {
  const plaintext = 'Original text';
  const encrypted = await encryptContent(plaintext);

  // Tamper with the ciphertext
  const parts = encrypted.split(':');
  parts[1] = parts[1].substring(0, parts[1].length - 4) + 'dead';
  const tampered = parts.join(':');

  await expect(decryptContent(tampered)).rejects.toThrow('Integrity check failed');
});

it('should throw on tampered IV', async () => {
  const plaintext = 'Original text';
  const encrypted = await encryptContent(plaintext);

  const parts = encrypted.split(':');
  parts[0] = 'aabbccdd'; // Change IV
  const tampered = parts.join(':');

  await expect(decryptContent(tampered)).rejects.toThrow('Integrity check failed');
});
```

### Edge Cases

```typescript
it('should handle empty string', async () => {
  const encrypted = await encryptContent('');
  const decrypted = await decryptContent(encrypted);
  expect(decrypted).toBe('');
});

it('should handle Unicode characters', async () => {
  const plaintext = '🎉 Emoji test ñ 中文';
  const encrypted = await encryptContent(plaintext);
  const decrypted = await decryptContent(encrypted);
  expect(decrypted).toBe(plaintext);
});

it('should handle large content', async () => {
  const plaintext = 'x'.repeat(10000);
  const encrypted = await encryptContent(plaintext);
  const decrypted = await decryptContent(encrypted);
  expect(decrypted).toBe(plaintext);
});

it('should throw when no encryption key exists', async () => {
  await SecureStore.deleteItemAsync('journal_encryption_key');

  await expect(encryptContent('test')).rejects.toThrow('Encryption key not found');
});
```

## Database + Encryption Integration

```typescript
describe('Journal with Encryption', () => {
  let db: SQLiteDatabase;

  beforeEach(async () => {
    db = await openDatabase(':memory:');
    await db.execAsync(`
      CREATE TABLE journal (
        id TEXT PRIMARY KEY,
        encrypted_body TEXT NOT NULL,
        created_at INTEGER
      )
    `);
    await generateEncryptionKey();
  });

  it('should store and retrieve encrypted entries', async () => {
    const entry = {
      id: 'entry-1',
      content: 'My private thoughts',
      created_at: Date.now(),
    };

    // Encrypt and store
    const encrypted = await encryptContent(entry.content);
    await db.runAsync(
      'INSERT INTO journal (id, encrypted_body, created_at) VALUES (?, ?, ?)',
      entry.id,
      encrypted,
      entry.created_at,
    );

    // Retrieve and decrypt
    const row = await db.getFirstAsync<{ encrypted_body: string }>(
      'SELECT encrypted_body FROM journal WHERE id = ?',
      entry.id,
    );

    const decrypted = await decryptContent(row!.encrypted_body);
    expect(decrypted).toBe(entry.content);
  });
});
```

## Testing Sync with Encrypted Data

```typescript
describe('Sync Queue with Encryption', () => {
  it('should sync encrypted data without decryption', async () => {
    const entry = {
      id: 'entry-1',
      content: 'Secret content',
    };

    // Store locally (encrypted)
    const encrypted = await encryptContent(entry.content);
    await db.runAsync(
      'INSERT INTO journal (id, encrypted_body) VALUES (?, ?)',
      entry.id,
      encrypted,
    );

    // Queue for sync (send encrypted data)
    await enqueueSync(db, 'journal', entry.id, 'INSERT', {
      id: entry.id,
      encrypted_body: encrypted,
    });

    // Verify sync queue has encrypted data
    const queueItem = await db.getFirstAsync('SELECT * FROM sync_queue');
    const data = JSON.parse(queueItem.data);

    // Data should still be encrypted in queue
    expect(data.encrypted_body).toBe(encrypted);
    expect(data.encrypted_body).not.toContain(entry.content);
  });
});
```

## Mocking Strategies

### Deterministic Crypto for Snapshots

```typescript
// __mocks__/expo-crypto.ts
let mockIndex = 0;
const mockBytes = [
  new Uint8Array(16).fill(0x01), // IV
  new Uint8Array(32).fill(0x02), // Key material
];

export const getRandomBytesAsync = jest.fn((length: number) => {
  const bytes = mockBytes[mockIndex % mockBytes.length] || new Uint8Array(length);
  mockIndex++;
  return Promise.resolve(bytes.slice(0, length));
});

beforeEach(() => {
  mockIndex = 0;
});
```

### Testing Key Rotation

```typescript
it('should handle key rotation gracefully', async () => {
  // Create entry with old key
  const oldKey = await generateEncryptionKey();
  const encrypted = await encryptContent('Important data');

  // Rotate key
  await deleteEncryptionKey();
  await generateEncryptionKey();

  // Old data should still decrypt (if key was backed up)
  // OR should fail gracefully
  await expect(decryptContent(encrypted)).rejects.toThrow();
});
```

## Test Coverage Requirements

```json
{
  "coverageThreshold": {
    "./src/utils/encryption.ts": {
      "statements": 90,
      "branches": 85,
      "functions": 90,
      "lines": 90
    }
  }
}
```

## CI Best Practices

```yaml
# .github/workflows/test.yml
- name: Run Encryption Tests
  run: npm run test:encryption
  env:
    CI: true
    NODE_ENV: test
```

## Checklist

- [ ] Roundtrip test (encrypt → decrypt matches original)
- [ ] Unique IV test (same plaintext → different ciphertext)
- [ ] MAC tampering tests (IV, ciphertext, MAC modifications)
- [ ] Edge cases (empty, Unicode, large content)
- [ ] Missing key error handling
- [ ] Database integration tests
- [ ] Sync queue tests (encrypted data flows)
