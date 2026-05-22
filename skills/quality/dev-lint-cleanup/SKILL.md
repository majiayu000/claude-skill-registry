---
name: Lint Cleanup
description: FIX ESLint errors safely without breaking code. Prefix unused variables with `_`, fix no-case-declarations, add default props, and verify builds after each batch. Use when lint cleanup is needed for easier refactoring & faster Claude Code editing.
---

# Safe Lint Cleanup

## Instructions

This skill provides safe patterns for fixing ESLint errors without breaking code.

### Pre-Flight Checklist

**BEFORE starting any lint cleanup:**

```bash
# 1. Get baseline count
npm run lint 2>&1 | tail -5

# 2. Save full output for reference
npm run lint 2>&1 > /tmp/lint-output.txt

# 3. Verify build works
npm run build

# 4. Check git status (ensure clean state)
git status
```

---

## Error Categories & Fixes

### 1. Unused Variables (`@typescript-eslint/no-unused-vars`)

#### Pattern 1: Prefix Unused Variables with `_`

This is the SAFEST fix - silences the error without changing logic:

```typescript
// BEFORE (error)
const unusedVar = someValue

// AFTER (no error)
const _unusedVar = someValue
```

#### Pattern 2: Prefix Unused Function Parameters

```typescript
// BEFORE
const handleClick = (event: MouseEvent) => {
  // doesn't use event
}

// AFTER
const handleClick = (_event: MouseEvent) => {
  // doesn't use event
}
```

#### Pattern 3: Destructuring with Rename

```typescript
// BEFORE
const { unusedProp, usedProp } = options

// AFTER
const { unusedProp: _unusedProp, usedProp } = options
```

#### Pattern 4: Unused Type Imports

```typescript
// BEFORE
import { SomeType, UsedType } from '@/types'

// AFTER
import type { SomeType as _SomeType, UsedType } from '@/types'
```

#### Pattern 5: Remove Completely Unused Imports

```typescript
// BEFORE
import { ref, watch, computed } from 'vue'  // watch never used

// AFTER
import { ref, computed } from 'vue'
```

---

### 2. Case Declarations (`no-case-declarations`)

**Error**: `Unexpected lexical declaration in case block`

**Cause**: Using `const`, `let`, or `class` directly in a `case` block without braces.

**Fix**: Wrap case block contents in `{}` to create block scope.

```typescript
// BEFORE (error)
switch (type) {
  case 'foo':
    const value = computeValue()  // ERROR!
    doSomething(value)
    break
  case 'bar':
    const other = computeOther()  // ERROR!
    doOther(other)
    break
}

// AFTER (fixed)
switch (type) {
  case 'foo': {
    const value = computeValue()
    doSomething(value)
    break
  }
  case 'bar': {
    const other = computeOther()
    doOther(other)
    break
  }
}
```

**Quick find pattern:**
```bash
# Find files with case declarations errors
npm run lint 2>&1 | grep "no-case-declarations" -B1 | grep -E "^/" | sort -u
```

---

### 3. Vue Default Props (`vue/require-default-prop`)

**Error**: `Prop 'X' requires default value to be set`

**Cause**: Optional props without default values in Vue 3 `<script setup>`.

**Fix**: Use `withDefaults()` to provide default values.

```vue
<!-- BEFORE (error) -->
<script setup lang="ts">
interface Props {
  title?: string
  count?: number
  items?: string[]
}
const props = defineProps<Props>()
</script>

<!-- AFTER (fixed) -->
<script setup lang="ts">
interface Props {
  title?: string
  count?: number
  items?: string[]
}
const props = withDefaults(defineProps<Props>(), {
  title: '',
  count: 0,
  items: () => []  // Use factory for arrays/objects
})
</script>
```

**Default value rules:**
- Primitives: Use direct value (`''`, `0`, `false`, `null`)
- Arrays: Use factory function `() => []`
- Objects: Use factory function `() => ({})`

---

### 4. Boolean Shorthand (`vue/prefer-true-attribute-shorthand`)

**Error**: `Boolean attribute should be written in shorthand form`

**Cause**: Using `:prop="true"` instead of just `prop`.

```vue
<!-- BEFORE (error) -->
<MyComponent :is-active="true" :show-header="true" />

<!-- AFTER (fixed) -->
<MyComponent is-active show-header />
```

---

### 5. Empty Object Types (`@typescript-eslint/no-empty-object-type`)

**Error**: `The {} type is not recommended`

**Cause**: Using `{}` as a type in TypeScript (especially in `.d.ts` files).

**Fix**: Use `object` or `Record<string, never>` instead, OR exclude `.d.ts` files:

```typescript
// In eslint.config.js ignores:
ignores: ['**/*.d.ts']
```

---

### 6. ESLint Config Alignment

**Problem**: Files excluded from `tsconfig.json` but not from ESLint cause parsing errors.

**Fix**: Keep ESLint ignores aligned with tsconfig excludes:

```javascript
// eslint.config.js
{
  ignores: [
    'node_modules/**',
    'dist/**',
    '**/*.d.ts',
    // Match tsconfig.json exclude patterns:
    'src/stories/**',
    'src/composables/adapters/**',
    'src/sync/**',
    'src/utils/emojiDetection.ts',
    'src/utils/logger.ts',
    // etc.
  ]
}
```

---

### ESLint Config for Underscore Pattern

**CRITICAL**: The underscore pattern must be configured for BOTH `.ts` AND `.vue` files:

```javascript
// eslint.config.js

// For TypeScript files
{
  files: ['**/*.ts', '**/*.tsx'],
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', {
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_',
      caughtErrorsIgnorePattern: '^_'
    }]
  }
}

// For Vue files - MUST BE SEPARATE!
{
  files: ['**/*.vue'],
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', {
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_',
      caughtErrorsIgnorePattern: '^_'
    }]
  }
}
```

---

## Verification Process

After every batch of fixes:

```bash
# 1. Run build
npm run build 2>&1 | tail -10

# 2. Check new lint count
npm run lint 2>&1 | tail -5

# 3. Calculate progress
# (baseline - current) / baseline * 100 = % fixed
```

---

## Files to Be Careful With

| File Type | Reason |
|-----------|--------|
| Vue components with templates | Variables might be used in template |
| Store files | Exported functions might appear unused |
| Composables | Returned values might appear unused |
| Test files | May have intentional unused vars |
| `.d.ts` files | Type declarations may use special patterns |

---

## Error Priority Order

Fix errors in this order (highest impact first):

1. **Parsing errors** - ESLint ignores alignment with tsconfig
2. **no-case-declarations** - Structural fixes, wrap in `{}`
3. **require-default-prop** - Add `withDefaults()`
4. **no-unused-vars** - Prefix with `_` or remove
5. **prefer-true-attribute-shorthand** - Simple template fixes
6. **no-explicit-any** - Requires proper typing (lower priority)

---

## Quick Reference Commands

```bash
# Get current lint count
npm run lint 2>&1 | tail -5

# Save full output
npm run lint 2>&1 > /tmp/lint-output.txt

# Find files with specific error
npm run lint 2>&1 | grep "ERROR_NAME" -B1 | grep -E "^/" | sort -u

# Count specific error type
grep "ERROR_NAME" /tmp/lint-output.txt | wc -l

# Check specific file errors
cat /tmp/lint-output.txt | grep -A20 "YourFile.vue$" | head -25

# Run --fix for auto-fixable errors (safe)
npm run lint -- --fix

# Find case declarations by file
awk '/^\/home.*\.(vue|ts)$/ { file=$0 } /no-case-declarations/ { print file }' /tmp/lint-output.txt | sort -u
```

---

## Common Gotchas

1. **Multiple Matches**: Add more surrounding context to make match unique
2. **Variable Used in Template**: Check `<template>` section before prefixing
3. **Exported but Appears Unused**: Don't prefix exports - used externally
4. **Store/Composable Return Values**: Check if values are returned for consumers
5. **Case Block Fallthrough**: Ensure `break` is inside the `{}` braces
6. **Factory Functions for Props**: Arrays/objects need `() => []` not `[]`

See `lint-cleanup-guide.md` for complete documentation.
