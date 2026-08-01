---
name: mobile-storage-mmkv
description: MMKV high-performance key-value storage for React Native - synchronous JSI-based reads/writes, encryption, typed hooks, multiple instances, listeners, persistence middleware adapters
---

# MMKV Storage Patterns

> **Quick Guide:** Use `createMMKV()` for synchronous key-value storage (~30x faster than AsyncStorage). One singleton instance per concern (global app, per-user). Use typed hooks (`useMMKVString`, `useMMKVObject`) for reactive components. Enable encryption with `encryptionKey` for sensitive data. V4 is a Nitro Module requiring `react-native-nitro-modules` and React Native 0.75+.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST reuse a single MMKV instance per concern -- NEVER call `createMMKV()` on every render or in component bodies)**

**(You MUST use typed getters (`getString`, `getNumber`, `getBoolean`) -- NEVER parse the return value of the wrong getter)**

**(You MUST use `remove()` to delete keys -- `delete()` was renamed in v4 due to C++ keyword conflict)**

**(You MUST install `react-native-nitro-modules` alongside `react-native-mmkv` -- v4 is a Nitro Module)**

</critical_requirements>

---

**Auto-detection:** MMKV, react-native-mmkv, createMMKV, useMMKVString, useMMKVNumber, useMMKVBoolean, useMMKVObject, useMMKVBuffer, useMMKVListener, useMMKVKeys, addOnValueChangedListener, encryptionKey, mmkv storage, key-value storage React Native

**When to use:**

- Persisting user preferences, auth tokens, or cached data synchronously
- Replacing AsyncStorage for faster reads/writes (~30x improvement)
- Encrypting sensitive data at rest with AES-128 or AES-256
- Sharing storage between iOS app and extensions via App Groups
- Building reactive UIs that re-render on storage changes (hooks)
- Isolating data per user or feature with multiple named instances

**Key patterns covered:**

- Instance creation with `createMMKV()` and configuration options
- Typed getters/setters and object serialization
- React hooks for reactive storage (`useMMKVString`, `useMMKVObject`, etc.)
- Value change listeners (`addOnValueChangedListener`, `useMMKVListener`)
- Multiple instances for data isolation (global vs per-user)
- Encryption at rest (AES-128/AES-256)
- Persistence middleware adapter (generic `StateStorage` interface)
- Migration from AsyncStorage

**When NOT to use:**

- Large binary files or media (use the filesystem)
- Relational or queryable data (use a local database)
- Data that must sync across devices (use a cloud-synced solution)
- Server state caching with invalidation (use your data fetching layer)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Instance setup, typed access, hooks, listeners
- [examples/advanced.md](examples/advanced.md) - Encryption, multiple instances, App Groups, multi-process, migration
- [examples/persistence.md](examples/persistence.md) - State management persistence adapter, hydration handling
- [reference.md](reference.md) - API reference, V3-to-V4 migration table, migration checklist

---

<philosophy>

## Philosophy

MMKV is a **synchronous**, JSI-based key-value store built on top of Tencent's battle-tested C++ library. The key advantage over AsyncStorage is that reads and writes are synchronous -- no `await`, no Promises, no bridge serialization. This eliminates an entire class of race conditions and simplifies code.

**Core principles:**

1. **Synchronous by design** -- `getString()` returns immediately, no async wrappers needed
2. **One instance per concern** -- export a singleton; never create instances inside components
3. **Typed access** -- use the correct getter for the stored type; MMKV does not auto-convert
4. **Encrypt sensitive data** -- tokens, keys, PII should use `encryptionKey` option
5. **Hooks for reactivity** -- `useMMKVString` etc. trigger re-renders on changes, replacing manual subscriptions

**Performance comparison with AsyncStorage:**

| Operation      | AsyncStorage | MMKV     | Speedup |
| -------------- | ------------ | -------- | ------- |
| Read 1 key     | ~5ms         | ~0.015ms | ~300x   |
| Write 1 key    | ~8ms         | ~0.018ms | ~440x   |
| Read 1000 keys | ~200ms       | ~3ms     | ~65x    |

Benchmarks vary by device, but MMKV is consistently 30-100x faster for typical operations.

**V4 architecture:** MMKV v4 is a Nitro Module (not a TurboModule). This means it uses `react-native-nitro-modules` for the native bridge, requires React Native 0.75+, and the JS API uses `createMMKV()` instead of `new MMKV()`.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Instance Creation and Singleton Export

Create one instance per storage concern at module scope. Never inside a component or hook body.

```typescript
import { createMMKV } from "react-native-mmkv";

// Global app storage -- reuse this everywhere
export const storage = createMMKV();

// Named instance for user-specific data
export const createUserStorage = (userId: string) =>
  createMMKV({ id: `user-${userId}` });
```

**Why good:** Module-level creation runs once, all consumers share the same native instance, no wasted allocations

```typescript
// BAD: Creating instance inside component
function Settings() {
  const storage = createMMKV(); // New native instance every render
  // ...
}
```

**Why bad:** Creates a new native MMKV instance on every render, wastes memory, defeats instance caching

See [examples/core.md](examples/core.md) for full configuration options (path, encryption, readOnly, compareBeforeSet).

---

### Pattern 2: Typed Getters and Setters

MMKV stores values by type. Always use the matching getter for what was stored.

```typescript
// Set typed values
storage.set("user.name", "Alice");
storage.set("user.age", 28);
storage.set("onboarded", true);

// Get with correct typed getter
const name = storage.getString("user.name"); // string | undefined
const age = storage.getNumber("user.age"); // number | undefined
const done = storage.getBoolean("onboarded"); // boolean | undefined
```

**Why good:** Each getter returns the correct type or `undefined` if key is missing -- no parsing, no type confusion

**Gotcha:** Calling `getString` on a key that was stored with `set(key, number)` returns `undefined`, not a stringified number. MMKV does not auto-convert between types.

See [examples/core.md](examples/core.md) for object serialization with `JSON.stringify`/`JSON.parse` and `ArrayBuffer` storage.

---

### Pattern 3: React Hooks for Reactive Storage

Hooks provide `useState`-like API backed by MMKV. Components re-render when the stored value changes.

```typescript
import {
  useMMKVString,
  useMMKVBoolean,
  useMMKVObject,
} from "react-native-mmkv";
import type { User } from "../types";

function ProfileScreen() {
  const [name, setName] = useMMKVString("user.name");
  const [darkMode, setDarkMode] = useMMKVBoolean("settings.darkMode");
  const [user, setUser] = useMMKVObject<User>("user.profile");

  // Set undefined to delete the key
  const clearProfile = () => setUser(undefined);
}
```

**Why good:** Reactive re-renders on change, type-safe generics for objects, setting `undefined` removes the key

**Custom instance:** Pass instance as second argument: `useMMKVString("key", userStorage)`

See [examples/core.md](examples/core.md) for all hook variants including `useMMKVBuffer` and `useMMKVKeys`.

---

### Pattern 4: Value Change Listeners

Listen to storage changes outside React components (background tasks, services, cross-instance sync).

```typescript
const listener = storage.addOnValueChangedListener((changedKey) => {
  const newValue = storage.getString(changedKey);
  console.log(`${changedKey} changed to: ${newValue}`);
});

// Cleanup when no longer needed
listener.remove();
```

**Why good:** Works outside React tree, receives the changed key (read new value yourself), cleanup via `.remove()`

For React components, prefer `useMMKVListener` hook -- it handles cleanup automatically.

See [examples/core.md](examples/core.md) for `useMMKVListener` hook usage.

---

### Pattern 5: Multiple Instances for Data Isolation

Use separate named instances to isolate data by concern. Common pattern: one global instance, one per logged-in user.

```typescript
const APP_STORAGE_ID = "app-global";

export const appStorage = createMMKV({ id: APP_STORAGE_ID });

export const createUserStorage = (userId: string) =>
  createMMKV({ id: `user-${userId}` });

// On logout: delete user-specific storage entirely
import { deleteMMKV } from "react-native-mmkv";
const handleLogout = (userId: string) => {
  deleteMMKV(`user-${userId}`);
};
```

**Why good:** User data is fully isolated from app data, `deleteMMKV` removes the entire instance on logout

See [examples/advanced.md](examples/advanced.md) for `existsMMKV` checks and instance lifecycle management.

---

### Pattern 6: Encryption

Enable AES encryption for sensitive data. Encryption applies to the entire instance -- you cannot encrypt individual keys.

```typescript
// Instance with AES-256 encryption
const secureStorage = createMMKV({
  id: "secure",
  encryptionKey: "your-encryption-key",
  encryptionType: "AES-256",
});

// Encrypt/decrypt existing instance at runtime
storage.encrypt("new-password", "AES-256");
storage.decrypt(); // Remove encryption
```

**When to use:** Auth tokens, API keys, PII, anything that should not be readable if device is compromised

See [examples/advanced.md](examples/advanced.md) for key rotation patterns and encryption type comparison.

---

### Pattern 7: Persistence Middleware Adapter

Bridge MMKV with state management persistence middleware by implementing a `StateStorage`-compatible interface.

```typescript
import { createMMKV } from "react-native-mmkv";

const storage = createMMKV();

// Implement the StateStorage interface your persist middleware expects
interface StateStorage {
  setItem: (name: string, value: string) => void;
  getItem: (name: string) => string | null;
  removeItem: (name: string) => void;
}

export const mmkvStateStorage: StateStorage = {
  setItem: (name, value) => storage.set(name, value),
  getItem: (name) => storage.getString(name) ?? null,
  removeItem: (name) => storage.remove(name),
};
```

**Why good:** Synchronous adapter eliminates async overhead, drop-in replacement for AsyncStorage adapters, works with any persist middleware that accepts `StateStorage`

See [examples/persistence.md](examples/persistence.md) for complete persistence middleware setup with hydration handling.

</patterns>

---

<decision_framework>

## Decision Framework

```
What kind of data are you storing?
|
+-> Key-value pairs (strings, numbers, booleans, small objects)?
|   +-> Sensitive data (tokens, keys, PII)?
|   |   +-> YES -> MMKV with encryptionKey
|   |   +-> NO  -> MMKV without encryption
|   +-> Need reactive UI updates?
|   |   +-> YES -> Use MMKV hooks (useMMKVString, etc.)
|   |   +-> NO  -> Use direct get/set API
|   +-> Multiple users or data domains?
|       +-> YES -> Multiple named instances
|       +-> NO  -> Single default instance
|
+-> Large files or binary media?
|   +-> Use the filesystem (not MMKV)
|
+-> Relational data with queries?
|   +-> Use a local database (not MMKV)
|
+-> Server-cached data with invalidation?
    +-> Use your data fetching layer (not MMKV)
```

### When to Use Each API Style

| Scenario                        | API                                 |
| ------------------------------- | ----------------------------------- |
| Read/write in services or utils | Direct: `storage.getString()`       |
| Reactive component state        | Hook: `useMMKVString()`             |
| Cross-component sync            | Hook or `addOnValueChangedListener` |
| Background task or service      | Direct + listener                   |
| State management persistence    | `StateStorage` adapter              |

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Calling `createMMKV()` inside a component body -- creates new native instance every render, use module-scope singleton
- Using `storage.delete()` -- renamed to `storage.remove()` in v4, `delete` is a C++ reserved keyword
- Mixing typed getters -- `getString` on a number key returns `undefined`, not a string. Use the matching getter.
- Missing `react-native-nitro-modules` peer dependency -- v4 crashes at runtime without it
- Using v4 on React Native < 0.75 -- Nitro Modules require RN 0.75+

**Medium Priority Issues:**

- Storing large objects (>1MB) in MMKV -- designed for small key-value pairs, not large blobs
- Not calling `listener.remove()` -- native listeners leak if not cleaned up
- Using default instance for sensitive data without encryption -- device compromise exposes data
- Forgetting `encryptionType: "AES-256"` when AES-256 is needed -- default is AES-128

**Gotchas & Edge Cases:**

- MMKV encryption applies to the entire instance, not individual keys -- use a separate encrypted instance for sensitive data
- `useMMKVObject<T>` uses `JSON.stringify`/`JSON.parse` internally -- objects with `Date`, `Map`, `Set` lose their types
- Setting a hook value to `undefined` deletes the key from storage -- intentional API, not a bug
- Remote JS debugging (Chrome DevTools) does not work with MMKV -- JSI requires on-device execution. Use Flipper or React DevTools
- `compareBeforeSet` option prevents writing if value is unchanged -- useful for reducing disk I/O in high-frequency updates
- iOS App Groups require `AppGroupIdentifier` in Info.plist (was `AppGroup` in v3) and `mode: "multi-process"`
- MMKV provides automatic test mocks -- `createMMKV()` works in test runners without native compilation
- `getAllKeys()` returns all keys as an array -- there is no prefix filtering, implement it yourself if needed
- `storage.size` returns bytes used -- call `storage.trim()` to reclaim space from deleted keys

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST reuse a single MMKV instance per concern -- NEVER call `createMMKV()` on every render or in component bodies)**

**(You MUST use typed getters (`getString`, `getNumber`, `getBoolean`) -- NEVER parse the return value of the wrong getter)**

**(You MUST use `remove()` to delete keys -- `delete()` was renamed in v4 due to C++ keyword conflict)**

**(You MUST install `react-native-nitro-modules` alongside `react-native-mmkv` -- v4 is a Nitro Module)**

**Failure to follow these rules will cause memory leaks, runtime crashes, or silent data loss.**

</critical_reminders>
