---
name: formatting-conditional-types
description: Formatting rules for TypeScript conditional types. Use when writing complex conditional types to ensure debuggable, maintainable formatting with proper alignment.
---

# Formatting Conditional Types

## Goal

Enable commenting out individual cases without breaking syntax (useful for debugging).

## Two Patterns

### FLAT PATTERN (prefer when possible)

Use for mutually exclusive top-level cases:

* All top-level conditions start at __same indentation__
* Place `:` at __end of line__ for each case
* Next condition returns to __base indentation__
* Align `?` symbols vertically within each case

### NESTED PATTERN (only when logic requires it)

Use when conditions are inherently nested (one inside another):

* Each nesting level increases indentation
* Align `?` and `:` symbols at each level

## Examples

```typescript
// ✅ GOOD - FLAT pattern for mutually exclusive cases
// Each top-level case can be commented out safely
type Result<$T> = $T extends string ? 'string'
  : $T extends number ? 'number'
  // $T extends boolean                  ? 'boolean' :  // ← Can comment out
  : $T extends undefined ? 'undefined'
  : 'unknown' // ← Final else, aligned

// ✅ GOOD - FLAT pattern with inner ternary
type LengthSlow<$S, $Acc> = $S extends `${string}${string}${string}${string}${infer __r__}`
  ? string extends __r__ // Inner ternary (nested logic)
    ? number
  : LengthSlow<__r__, [...$Acc, 0, 0, 0, 0]> // ← : at end
  : $S extends `${string}${string}${string}${infer __r__}` // ← Back to base
    ? string extends __r__ ? number
    : [...$Acc, 0, 0, 0]['length'] // ← : at end
  : $Acc['length'] // ← Final else

// ✅ GOOD - NESTED pattern (inherent logic requires it)
type DeepCheck<$S> = $S extends `${infer __c__}${infer __rest__}` ? string extends __rest__ ? number
  : __rest__ extends '' ? 1
  : __rest__ extends `${infer __c2__}${infer __r2__}` ? string extends __r2__ ? number
    : __r2__ extends '' ? 2
    : never
  : never
  : 0

// ❌ BAD - Misaligned flat pattern
type Bad<$T> = $T extends string ? 'string' // ← Alignment lost
  : $T extends number ? 'number' // ← Alignment lost
  : 'unknown'

// ❌ BAD - Using nested when flat would work
type Bad2<$T> = $T extends string ? 'string'
  : $T extends number ? 'number' // ← Unnecessary nesting
  : $T extends boolean ? 'boolean'
  : 'unknown'
```

## Notes

* Use `//dprint-ignore` before long conditional types to preserve alignment
* Align on `?` and `:` for readability
