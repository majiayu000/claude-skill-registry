---
name: local-state
description: This skill should be used when implementing local state management in this React Native/Expo codebase. It covers Apollo Client Reactive Variables for in-memory reactive state and React Native AsyncStorage for persistent storage. Use this skill when creating feature flags, user preferences, session state, or any client-only state that needs to survive component unmounts or app restarts.
---

# Local State Management

## Overview

This skill provides best practices for local state management in this React Native/Expo codebase. Local state is managed using two complementary approaches:

1. **Apollo Client Reactive Variables** - In-memory reactive state for UI synchronization
2. **React Native AsyncStorage** - Persistent key-value storage for data that survives app restarts

## When to Use Each Approach

| Use Case                        | Approach                         | Example                        |
| ------------------------------- | -------------------------------- | ------------------------------ |
| UI state that resets on refresh | Reactive Variable only           | Modal open state, form drafts  |
| User preferences that persist   | Reactive Variable + AsyncStorage | Theme, language, notifications |
| Feature flags                   | Reactive Variable + AsyncStorage | Beta features, profiler toggle |
| Session-scoped data             | Reactive Variable only           | Current filter selections      |
| Cross-component communication   | Reactive Variable                | Selected player ID, active tab |
| Authentication tokens           | `expo-secure-store`              | Access tokens, refresh tokens  |

## Quick Reference

### Creating a Reactive Variable

```typescript
import { makeVar } from "@apollo/client";

interface IUserPreferences {
  readonly theme: "light" | "dark";
  readonly notifications: boolean;
}

const DEFAULT_PREFERENCES: IUserPreferences = {
  theme: "light",
  notifications: true,
};

export const userPreferencesVar =
  makeVar<IUserPreferences>(DEFAULT_PREFERENCES);
```

### Reading in Components (Reactive)

```typescript
import { useReactiveVar } from "@apollo/client";

const MyComponent = () => {
  const preferences = useReactiveVar(userPreferencesVar);
  return <Text>{preferences.theme}</Text>;
};
```

### Updating Values (Immutably)

```typescript
// Update with new object reference
userPreferencesVar({
  ...userPreferencesVar(),
  theme: "dark",
});
```

### Persisting to AsyncStorage

```typescript
import AsyncStorage from "@react-native-async-storage/async-storage";

const STORAGE_KEY = "@whatever:user-preferences";

export const savePreferences = async (
  prefs: IUserPreferences
): Promise<void> => {
  userPreferencesVar(prefs); // Update reactive variable first
  try {
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    console.error("Failed to save preferences:", message);
  }
};

export const loadPreferences = async (): Promise<void> => {
  try {
    const stored = await AsyncStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored) as IUserPreferences;
      userPreferencesVar({ ...DEFAULT_PREFERENCES, ...parsed });
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    console.error("Failed to load preferences:", message);
  }
};
```

## Core Rules

### 1. Always Create New References

Never mutate existing objects or arrays. Create new references to trigger reactivity:

```typescript
// CORRECT - creates new object
userPreferencesVar({
  ...userPreferencesVar(),
  theme: "dark",
});

// INCORRECT - mutation does NOT trigger updates
const prefs = userPreferencesVar();
prefs.theme = "dark"; // This does nothing!
userPreferencesVar(prefs); // Same reference, no update
```

### 2. Use `useReactiveVar` for Reactive Components

Calling `myVar()` directly does NOT trigger re-renders. Always use the hook:

```typescript
// CORRECT - component re-renders when variable changes
const theme = useReactiveVar(themeVar);

// INCORRECT - no re-renders on variable change
const theme = themeVar();
```

### 3. Encapsulate Updates in Custom Hooks

Create custom hooks for testability and encapsulation:

```typescript
export const useTheme = () => {
  const preferences = useReactiveVar(userPreferencesVar);

  const setTheme = useCallback((theme: "light" | "dark") => {
    savePreferences({ ...userPreferencesVar(), theme });
  }, []);

  return { theme: preferences.theme, setTheme };
};
```

### 4. Use Namespace Prefixes for Storage Keys

Prefix all AsyncStorage keys with the app namespace:

```typescript
// CORRECT
const STORAGE_KEY = "@whatever:filter-values";

// INCORRECT - collision risk
const STORAGE_KEY = "filters";
```

### 5. Always Handle AsyncStorage Errors

AsyncStorage operations can fail. Always use try/catch:

```typescript
// CORRECT
try {
  await AsyncStorage.setItem(key, JSON.stringify(value));
} catch (error) {
  const message = error instanceof Error ? error.message : "Unknown error";
  console.error(`Failed to save ${key}:`, message);
}

// INCORRECT - silent failures
await AsyncStorage.setItem(key, JSON.stringify(value));
```

### 6. Never Store Sensitive Data in AsyncStorage

AsyncStorage is unencrypted. Use `expo-secure-store` for sensitive data:

```typescript
// CORRECT - use secure store for tokens
import * as SecureStore from "expo-secure-store";
await SecureStore.setItemAsync("accessToken", token);

// INCORRECT - never store tokens in AsyncStorage
await AsyncStorage.setItem("accessToken", token);
```

### 7. Load Persisted State on App Start

Initialize persisted state early in the app lifecycle:

```typescript
// In root layout or app initialization
useEffect(() => {
  loadPreferences();
}, []);
```

## File Organization

Organize reactive variables and persistence logic in dedicated store files:

```
features/
  my-feature/
    stores/
      featureState.ts        # Reactive variable + persistence logic
      index.ts               # Re-exports
```

Example store file structure:

```typescript
// stores/userPreferences.ts
import { makeVar, useReactiveVar } from "@apollo/client";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useCallback } from "react";

// Types
interface IUserPreferences {
  readonly theme: "light" | "dark";
  readonly language: string;
}

// Constants
const STORAGE_KEY = "@whatever:user-preferences";
const DEFAULT_PREFERENCES: IUserPreferences = {
  theme: "light",
  language: "en",
};

// Reactive Variable
export const userPreferencesVar =
  makeVar<IUserPreferences>(DEFAULT_PREFERENCES);

// Persistence Functions
export const loadUserPreferences = async (): Promise<void> => {
  try {
    const stored = await AsyncStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored) as IUserPreferences;
      userPreferencesVar({ ...DEFAULT_PREFERENCES, ...parsed });
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    console.error("Failed to load preferences:", message);
  }
};

const saveUserPreferences = async (prefs: IUserPreferences): Promise<void> => {
  userPreferencesVar(prefs);
  try {
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    console.error("Failed to save preferences:", message);
  }
};

// Custom Hook
export const useUserPreferences = () => {
  const preferences = useReactiveVar(userPreferencesVar);

  const setTheme = useCallback((theme: "light" | "dark") => {
    saveUserPreferences({ ...userPreferencesVar(), theme });
  }, []);

  const setLanguage = useCallback((language: string) => {
    saveUserPreferences({ ...userPreferencesVar(), language });
  }, []);

  return { preferences, setTheme, setLanguage };
};
```

## Detailed Reference

For comprehensive patterns and examples, see the reference files:

- **[references/reactive-variables.md](references/reactive-variables.md)** - Complete reactive variable patterns including TypeScript types, cache integration, and advanced use cases
- **[references/async-storage.md](references/async-storage.md)** - AsyncStorage API patterns, error handling, and performance considerations
- **[references/persistence-patterns.md](references/persistence-patterns.md)** - Patterns for persisting reactive variables including AppState-based and immediate persistence

## Anti-Patterns to Avoid

### Never mutate reactive variable values

```typescript
// WRONG - mutation
const filters = filtersVar();
filters.minAge = 25;
filtersVar(filters);

// CORRECT - new reference
filtersVar({ ...filtersVar(), minAge: 25 });
```

### Never use `localStorage` in React Native

```typescript
// WRONG - doesn't exist in React Native
localStorage.setItem("key", value);

// CORRECT - use AsyncStorage
await AsyncStorage.setItem("key", value);
```

### Never call `myVar()` expecting re-renders

```typescript
// WRONG - no reactivity
const Component = () => {
  const value = myVar(); // Does NOT trigger re-renders
  return <Text>{value}</Text>;
};

// CORRECT - reactive
const Component = () => {
  const value = useReactiveVar(myVar);
  return <Text>{value}</Text>;
};
```

### Never store without serialization

```typescript
// WRONG - AsyncStorage only accepts strings
await AsyncStorage.setItem("key", { name: "John" });

// CORRECT - serialize first
await AsyncStorage.setItem("key", JSON.stringify({ name: "John" }));
```

### Never forget to load persisted state

```typescript
// WRONG - state resets on app restart
export const filtersVar = makeVar<Filters>(DEFAULT_FILTERS);

// CORRECT - load on app start
export const filtersVar = makeVar<Filters>(DEFAULT_FILTERS);
export const loadFilters = async () => {
  /* ... */
};
// Call loadFilters() in app initialization
```

## Validation Checklist

When writing or reviewing local state code, verify:

- [ ] Reactive variables use TypeScript generics: `makeVar<Type>(default)`
- [ ] Components use `useReactiveVar()` hook, not direct `myVar()` calls
- [ ] Updates create new object/array references (spread operator)
- [ ] AsyncStorage keys use namespace prefix: `@whatever:`
- [ ] All AsyncStorage operations wrapped in try/catch
- [ ] Sensitive data uses `expo-secure-store`, not AsyncStorage
- [ ] Persisted state loaded on app initialization
- [ ] Custom hooks encapsulate update logic
- [ ] State stored in feature-specific `stores/` directory
