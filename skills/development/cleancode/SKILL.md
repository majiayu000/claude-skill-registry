---
name: cleanCode
description: Refactor/clean/simplify code - eliminate duplication, small functions, readable names. USE WHEN user says "clean", "simplify", "refactor", "readable", "messy", "complex", or code has >15 line functions or copy-paste.
---

# Code Simplification

**Core principle:** Code reads like English prose.

**Influences:** Douglas Crockford's "JavaScript: The Good Parts", Robert C. Martin's "Clean Code"

**🚨 TypeScript:** Before writing TypeScript, run `/cleanTypes` for type annotation best practices.

## 1. Small Functions, Clear Names

**Target: 3-15 lines per function.** Name describes exactly what it does.

```typescript
// Bad: Generic name, does multiple things (40 lines)
function process(filename) { ... }

// Good: Small functions with precise names
const extractExtension = (filename) => filename.replace(/.*symlink/, '')
const removeSymlinkAndExtension = (filename) => filename.replace(/\.symlink.*$/, '')
const replaceDOTWithDot = (str) => str.replace(/DOT/g, '.')
```

**Naming rules:**
- Verbs for actions: `createLink()`, `handleExistingFile()`
- Booleans: `isSymlink()`, `hasExtension()`, `canWrite()`
- No generic names: `process()`, `handle()`, `do()` → What specifically?

## 2. No Duplication

If you copy-paste code, stop. Extract a function.

```typescript
// Bad: 3 similar blocks, 40 lines each
function renderIdentity(json) { /* extract fields, print */ }
function renderCard(json) { /* extract fields, print */ }
function renderLogin(json) { /* extract fields, print */ }

// Good: Extract common pattern
function renderEntry(json) {
  const fields = extractFields(json)
  fields.forEach(field => printField(field))
}
```

## 3. Iterate the Source, Not Type Dispatch

**Red flag:** Multiple `extractTypeA()`, `extractTypeB()`, `extractTypeC()` functions.

**Instead:** Iterate the data structure directly.

```javascript
// Bad: Type-specific extractors + dispatch
const extractIdentity = (json) => [/* hardcode identity fields */]
const extractCard = (json) => [/* hardcode card fields */]
const extractLogin = (json) => [/* hardcode login fields */]

if (isIdentity(json)) return extractIdentity(json)
if (isCard(json)) return extractCard(json)
return extractLogin(json)

// Good: Generic extraction - iterate what exists
const extractFields = (json) =>
  Object.entries(json.data || {})
    .filter(([key, value]) => value && typeof value === 'string')
    .map(([key, value]) => ({
      label: humanizeKey(key),
      displayValue: shouldMask(key) ? '•••' : value
    }))

// Works for all types, no type checking
```

**Key insight:** Don't ask "what type is this?" Ask "what data exists?"

## 4. Module Splitting: ~250 Lines

When a file exceeds 250 lines, look for natural module boundaries.

```typescript
// Before: links.ts - 247 lines (path utils + file ops + handlers + class + orchestration)

// After: Split by responsibility
// symlink/path-transform.ts - 23 lines
// symlink/file-ops.ts - 40 lines
// symlink/handlers.ts - 43 lines
// symlink/operation.ts - 76 lines
// links.ts - 77 lines (orchestration only)
```

**Don't split prematurely:** 200-line focused file > 5 poorly-abstracted 40-line files.

## 5. Fluent APIs for Sequential Operations

Chain methods to describe operations in natural language.

```typescript
// Bad: Imperative control flow, needs comments
function safeLink(src: string, dest: string | null) {
  // Handle unparseable destination
  if (!dest) return { ... }

  // Handle existing symlink
  if (isSymlink(dest)) { ... }

  // Handle existing file
  if (fileExists(dest)) { ... }

  // Create symlink
  fs.mkdirSync(...)
  return createLink(src, dest)
}

// Good: Reads like English, no comments needed
const safeLink = (src: string, dest: string | null) =>
  new SymlinkOperation(src, dest)
    .handleNullDestination()
    .handleSymlink()
    .handleExistingFile()
    .createSymlink()
    .result()
```

**Implementation pattern:**
```typescript
class Operation {
  private result: Result | null = null

  step1() {
    if (this.result) return this  // Short-circuit if done
    // Check condition, maybe set this.result
    return this
  }

  result() { return this.result! }
}
```

**When to use:** Sequential operations with decision points, each step is a clear named concern.

## 6. Explicit Failures Over Silent Filtering

Make failures visible with error results, don't silently skip.

```typescript
// Bad: Silent failure - lost information
function buildPlan() {
  return files.map(transformPath).filter(path => path !== null)
}
// Which files failed? Unknown.

// Good: Explicit failure - trackable
function buildPlan() {
  return files.map(file => ({ from: file, to: transformPath(file) }))
}

function executePlan(plan: Array<{from: string, to: string | null}>) {
  return plan.map(({ from, to }) => safeLink(from, to))
}

function safeLink(src: string, dest: string | null) {
  if (!dest) return { from: src, to: '<unparseable>', success: false }
  // ... continue
}

// Now: results.filter(r => !r.success).length shows exactly what failed
```

## 7. Eliminate Special Cases

Every special case must justify its existence. Default to uniform handling.

```javascript
// Bad: Unnecessary special case
if (files.length === 1) {
  return handleSingleFile(files[0])
} else {
  return handleMultipleFiles(files)
}

// Good: Unified handling (works for n=1 too)
return files.map(handleFile)
```

**Ask:** "What if I handle both cases uniformly?"

## 8. Arrow Functions for Simple Transformations

```typescript
// Bad: Verbose
function executeSymlinkPlan(plan: SymlinkPlan[]): LinkResult[] {
  const results: LinkResult[] = []
  for (const { from, to } of plan) {
    results.push(safeLink(from, to))
  }
  return results
}

// Good: Concise
const executeSymlinkPlan = (plan: SymlinkPlan[]) =>
  plan.map(({ from, to }) => safeLink(from, to))
```

**Note side effects:** Add comment if `.map()` has side effects (creates files, mutates state).

## Refactoring Checklist

Before code is "done":

1. **Function names read like English?** Should describe exactly what they do
2. **Any copy-pasted code?** Extract to function
3. **Multiple extractType functions?** Replace with `Object.entries(source).map()`
4. **Any function >20 lines?** Break into subfunctions
5. **File >250 lines?** Look for natural module boundaries
6. **Sequential operations with branches?** Consider fluent API
7. **Silently filtering failures?** Make them explicit with error results
8. **Special cases that can be unified?** Handle uniformly when possible

## Complexity Limits

- Function >25 lines → Extract subfunctions
- File >250 lines → Consider splitting by responsibility
- Nested blocks >2 deep → Extract function

**Self-prompt:** "Do I have extractTypeA/B/C functions? Can I iterate the source instead? Would a fluent API make this read better? Are failures explicit? Does the code read like English?"
