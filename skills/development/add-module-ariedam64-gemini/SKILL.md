---
name: add-module
description: Create a new core infrastructure module with standard API, lazy init, and proper structure
aliases: [new-module, create-module]
---

# Add Module Skill

## Usage
```
/add-module <ModuleName>
```

**Note:** Modules are core infrastructure (always-on). For toggleable functionality, use `/add-feature` instead.

---

## Step 1: Ask Questions

### 1. Module Purpose
```
What infrastructure does this module provide?
Brief description:
```

### 2. Data Source
```
Where does the module get its data?

A) Game runtime - Hooks into game code
B) Network - Captures WebSocket/HTTP
C) Assets - Game assets (sprites, audio, etc.)
D) Computed - Derives from other modules
E) Other: ___
```

### 3. Dependencies
```
Which existing modules does it depend on?

[ ] MGData      [ ] MGSprite    [ ] MGTile
[ ] MGPixi      [ ] MGAudio     [ ] MGCosmetic
[ ] MGVersion   [ ] MGAssets    [ ] MGManifest
[ ] MGEnvironment  [ ] MGCalculators  [ ] None
```

### 4. State Type
```
Does it need runtime state?

A) Yes - Caches data in memory (needs state.ts)
B) No - Stateless utilities only
```

### 5. Public API Methods
```
What methods should the module expose?
(Besides required init/isReady)

Examples:
- get(key) - Get data by key
- calculate(params) - Perform calculation
- render(target) - Render something
```

---

## Step 2: Create Structure

```
src/modules/<moduleName>/
├── index.ts        # Public façade (MG<ModuleName>)
├── types.ts        # Type definitions
├── state.ts        # Runtime state (if needed)
└── logic/
    └── core.ts     # Business logic
```

**No `logic/index.ts`** - Import directly from logic files.

---

## Step 3: File Templates

### types.ts

```typescript
/**
 * <ModuleName> Module Types
 */

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

export interface <ModuleName>Data {
    // Define data structures
}

// ─────────────────────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────────────────────

export const <MODULE_NAME>_CONSTANTS = {
    // Define constants
} as const;
```

### state.ts (if needed)

```typescript
/**
 * <ModuleName> Module State
 *
 * Runtime cache/state management.
 */

import type { <ModuleName>Data } from './types';

// ─────────────────────────────────────────────────────────────────────────────
// State
// ─────────────────────────────────────────────────────────────────────────────

let cache: <ModuleName>Data | null = null;
let ready = false;

// ─────────────────────────────────────────────────────────────────────────────
// Accessors
// ─────────────────────────────────────────────────────────────────────────────

export function getCache(): <ModuleName>Data | null {
    return cache;
}

export function setCache(data: <ModuleName>Data): void {
    cache = data;
    ready = true;
}

export function isReady(): boolean {
    return ready;
}

export function reset(): void {
    cache = null;
    ready = false;
}
```

### logic/core.ts

```typescript
/**
 * <ModuleName> Core Logic
 */

import { setCache, getCache } from '../state';
import type { <ModuleName>Data } from '../types';

// ─────────────────────────────────────────────────────────────────────────────
// Initialization
// ─────────────────────────────────────────────────────────────────────────────

export async function initialize(): Promise<void> {
    // Initialization logic
    // Capture data, setup hooks, etc.

    const data: <ModuleName>Data = {
        // ...
    };

    setCache(data);
}

// ─────────────────────────────────────────────────────────────────────────────
// Public Methods
// ─────────────────────────────────────────────────────────────────────────────

export function getData(): <ModuleName>Data | null {
    return getCache();
}
```

### index.ts

```typescript
/**
 * <ModuleName> Module
 *
 * <Brief description>
 *
 * @example
 * ```typescript
 * await MG<ModuleName>.init();
 * const data = MG<ModuleName>.get();
 * ```
 */

import { initialize, getData } from './logic/core';
import { isReady as checkReady } from './state';

// ─────────────────────────────────────────────────────────────────────────────
// State
// ─────────────────────────────────────────────────────────────────────────────

let initialized = false;

// ─────────────────────────────────────────────────────────────────────────────
// Public API
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Initialize the module
 * Idempotent - safe to call multiple times
 */
async function init(): Promise<void> {
    if (initialized) return;
    initialized = true;

    await initialize();
    console.log('[<ModuleName>] Initialized');
}

/**
 * Check if module is ready
 */
function isReady(): boolean {
    return checkReady();
}

/**
 * Get module data
 */
function get() {
    return getData();
}

// ─────────────────────────────────────────────────────────────────────────────
// Export
// ─────────────────────────────────────────────────────────────────────────────

export const MG<ModuleName> = {
    // Required (standard API)
    init,
    isReady,

    // Module-specific
    get,
    // Add other public methods
};

export type { <ModuleName>Data } from './types';
```

---

## Step 4: Register

### Export → `src/modules/index.ts`

```typescript
export { MG<ModuleName> } from './<moduleName>';
export type { <ModuleName>Data } from './<moduleName>';
```

### API → `src/api/index.ts`

```typescript
import { MG<ModuleName> } from '../modules/<moduleName>';

Modules: {
    // ... existing
    <ModuleName>: MG<ModuleName>,
}
```

### Bootstrap → `src/ui/loader/bootstrap.ts`

```typescript
import { MG<ModuleName> } from '../../modules/<moduleName>';

// In initModules():
await MG<ModuleName>.init();
```

---

## Step 5: Validate

### Structure
- [ ] `index.ts` exports `MG<ModuleName>`
- [ ] `types.ts` defines types/constants
- [ ] `state.ts` exists (if stateful)
- [ ] `logic/` folder for business logic
- [ ] No `logic/index.ts` barrel file

### API
- [ ] `init()` - Required, idempotent
- [ ] `isReady()` - Required, returns boolean
- [ ] Other methods are module-specific

### Rules
- [ ] No toggles (modules are always-on)
- [ ] No UI rendering (DOM in src/ui/ only)
- [ ] No direct WS sends (use websocket/api.ts)
- [ ] No side effects on import

### Registration
- [ ] Exported from `src/modules/index.ts`
- [ ] Exposed in `src/api/index.ts`
- [ ] Initialized in bootstrap

---

## Module vs Feature

| Aspect | Module | Feature |
|--------|--------|---------|
| Toggle | Always on | `enabled: boolean` |
| Location | `src/modules/` | `src/features/` |
| Purpose | Infrastructure | Enhancement |
| API | `MG<Name>` | `MG<Name>` |
| Storage | `MODULE_KEYS` (rare) | `FEATURE_KEYS` |

---

## References

- Rules: `.claude/rules/modules.md`
- Existing modules: `src/modules/*/`
