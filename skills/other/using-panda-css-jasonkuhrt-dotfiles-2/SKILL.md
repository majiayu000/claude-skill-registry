---
name: using-panda-css
description: Panda CSS type safety rules for token references. Use when styling with css(), cva(), or token paths.
---

# Using Panda CSS

## CRITICAL: Token Type Safety

Panda CSS's `css()` and `cva()` functions are __NOT type-safe__ for token references due to the `AnyString` escape hatch.

### The Problem

```typescript
// styled-system/types/style-props.d.ts
type AnyString = (string & {})
maxWidth?: ConditionalValue<... | AnyString>  // ❌ Accepts ANY string!
```

### FORBIDDEN - String Literals

```typescript
// These compile but are NOT type-safe:
css({ maxWidth: 'sizes.container.wide' }) // ❌ AnyString escape hatch
css({ paddingInline: '4' }) // ❌ Would accept 'INVALID' too
```

### REQUIRED - token() Function

```typescript
import { token } from '../styled-system/tokens'

css({ maxWidth: token('sizes.container.wide') }) // ✅ Type-safe
css({ paddingInline: token('spacing.4') }) // ✅ Type-safe
// css({ color: token('colors.INVALID.500') })       // ❌ TypeScript error!
```

## Rule

If a string looks like a token path (contains `.` and starts with a token category like `sizes`, `spacing`, `colors`, `fontSizes`), it __MUST__ use `token()`.

__Only exceptions__: literal CSS values like `'100%'`, `'auto'`, `'bold'`, numeric values.
