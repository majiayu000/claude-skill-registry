---
name: js-library-distribution
description: Patterns for developing distributable JavaScript/TypeScript libraries. Use when building npm packages, SDK libraries, publishing a library, writing a package for others, or any code that runs in customer environments. Do NOT use for application code that is not distributed as a package -- use typescript-patterns or the relevant language skill instead.
durability: encoded-preference
---

# Library Distribution Patterns

## Critical: No Global Pollution

Distributable libraries run in **customer environments** alongside unknown code. Global pollution can break customer sites.

### NEVER Modify Global Objects

```typescript
// ❌ CRITICAL: Never extend native prototypes
Array.prototype.customMethod = function() { ... }
String.prototype.format = function() { ... }
Object.prototype.toJSON = function() { ... }

// ❌ CRITICAL: Never modify third-party libraries
import _ from 'lodash'
_.customUtil = function() { ... }  // Pollutes lodash globally

// ❌ CRITICAL: Never assign to window/global
window.MyLib = { ... }
globalThis.MyLib = { ... }
```

### Safe Patterns

```typescript
// ✅ Export your own functions
export function customMethod(arr: unknown[]) { ... }
export function format(str: string) { ... }

// ✅ Use composition, not extension
import { map } from 'lodash'
export function customMap<T>(arr: T[]) {
  return map(arr, /* your logic */)
}

// ✅ If global is unavoidable, use unique namespace
const UNIQUE_NAMESPACE = '__myCompany_myLib_v1__'
if (typeof window !== 'undefined') {
  (window as any)[UNIQUE_NAMESPACE] = { ... }
}
```

## No Side Effects on Import

```typescript
// ❌ BAD: Side effects when imported
// This runs immediately when someone imports your library
console.log('Library loaded')
fetch('/api/init')
document.addEventListener('DOMContentLoaded', ...)

// ✅ GOOD: Explicit initialization
export function init(config: Config) {
  // Side effects only when user explicitly calls
}
```

## Bundle Considerations

### Tree-Shaking Support

```typescript
// ✅ Use named exports for tree-shaking
export { functionA } from './a'
export { functionB } from './b'

// ❌ Barrel exports can break tree-shaking
export * from './everything'
```

### Dual Package (ESM + CJS)

```json
{
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    }
  }
}
```

## Dependency Management

```typescript
// ❌ BAD: Bundling dependencies (version conflicts)
// Your lodash 4.x vs customer's lodash 3.x

// ✅ GOOD: Peer dependencies
// package.json
{
  "peerDependencies": {
    "lodash": "^4.0.0"
  }
}
```

## Checklist Before Publish

- [ ] No `prototype` modifications
- [ ] No third-party library modifications
- [ ] No implicit globals (`window.X`, `globalThis.X`)
- [ ] No side effects on import
- [ ] Named exports for tree-shaking
- [ ] Peer dependencies declared
- [ ] Tested in isolation AND alongside common libraries
