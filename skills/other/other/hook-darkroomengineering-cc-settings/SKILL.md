---
name: hook
description: |
  Create custom React hooks following Darkroom standards. Use when:
  - User says "create hook", "new hook", "custom hook"
  - User wants to extract logic into a reusable hook
  - User mentions "use" prefix like "useAuth", "useScroll"
argument-hint: "[hookName]"
---

# Create Custom Hook

Create a custom React hook following Darkroom conventions.

## Structure

```
lib/hooks/<name>.ts    # Hook implementation
```

## Template

```tsx
'use client'

import { useState, useEffect } from 'react'

interface Use<Name>Options {
  // Hook configuration options
}

interface Use<Name>Return {
  // Return type definition
}

export function use<Name>(options?: Use<Name>Options): Use<Name>Return {
  // Implementation

  return {
    // Return values
  }
}
```

## Conventions

1. **Always `'use client'`** - Hooks use React APIs that require client
2. **Type everything** - Options interface, return interface
3. **Named export** - `export function useX`, not default
4. **Prefix with `use`** - React hook naming convention
5. **No memoization** - React Compiler handles it automatically

## Before You Start

If this hook uses an external library, **fetch docs first**:
1. Run `/docs <library>` to get current API via context7
2. Run `bun info <package>` to check latest version

## Consider Using Hamo

For common use cases, prefer `hamo` hooks (run `/docs hamo` first):

```tsx
import { useWindowSize, useRect, useIntersectionObserver } from 'hamo'
```

Only create custom hooks when `hamo` doesn't cover the use case.

## Example

```
User: "create a useLocalStorage hook"
→ Creates lib/hooks/use-local-storage.ts
```

## Arguments

- `$ARGUMENTS` - Hook name (e.g., "useAuth", "useLocalStorage")
