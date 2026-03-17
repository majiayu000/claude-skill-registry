---
name: react-native-storage-manager
description: Handles MMKV storage operations and data persistence patterns with encryption. Use when implementing data persistence, caching, or user preferences in Fitness Tracker App.
---

# React Native Storage Manager

This skill provides established patterns for data persistence using MMKV and Expo SecureStore in the Fitness Tracker App.

## When to Use This Skill

Use this skill when you need to:
- Persist data locally on the device
- Implement encrypted storage for sensitive data
- Handle user preferences or application state persistence
- Manage MMKV storage instances and keys
- Perform common CRUD operations on local storage

## Storage Initialization

The app uses an encrypted MMKV instance initialized in `app/utils/storage/index.ts`.

### Secure Encryption Key
We use Expo SecureStore to persist the encryption key securely.

```typescript
import * as SecureStore from "expo-secure-store"
import { MMKV } from "react-native-mmkv"

export const storage = new MMKV({
  id: "purrsuit-storage",
  encryptionKey: SecureStore.getItem("mmkv-encryption-key"),
})
```

## Basic CRUD Operations

Use the provided helper functions from `@/utils/storage`.

### Saving Data
```typescript
import { save, saveString } from "@/utils/storage"

save("user_preferences", { theme: "dark", notifications: true })
saveString("auth_token", "secure-token-here")
```

### Loading Data
```typescript
import { load, loadString } from "@/utils/storage"

const prefs = load<{ theme: string }>("user_preferences")
const token = loadString("auth_token")
```

### Removing Data
```typescript
import { remove, clear } from "@/utils/storage"

remove("auth_token")
clear() // Clear all data
```

## Advanced Patterns

### Typed Storage Keys
Centralize storage keys to avoid typos and ensure consistency.

```typescript
// app/utils/storage/keys.ts
export const STORAGE_KEYS = {
  USER_PREFS: "user_preferences",
  AUTH_TOKEN: "auth_token",
  ENCOUNTERS_CACHE: "workouts_cache",
} as const
```

### Integration with MST
Stores can automatically persist their state using `onSnapshot` or by loading data during `afterCreate`.

## References

See [STORAGE_PATTERNS.md](references/STORAGE_PATTERNS.md) for detailed implementation examples.

See [SECURITY_AND_ENCRYPTION.md](references/SECURITY_AND_ENCRYPTION.md) for encryption best practices.
