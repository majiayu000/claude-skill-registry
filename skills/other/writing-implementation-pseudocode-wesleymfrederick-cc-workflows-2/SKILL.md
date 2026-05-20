---
name: writing-implementation-pseudocode
description: Use when adding pseudocode examples to implementation guides or technical documentation - creates readable TypeScript-style pseudocode with strategic comments (Boundary, Integration, Pattern, Decision) that guide developers during implementation
---

# Writing Implementation Pseudocode

## Overview

**Implementation pseudocode is actual TypeScript/JavaScript with strategic comments** that help developers understand not just WHAT the code does, but WHERE it touches external systems (Boundary), HOW it integrates with dependencies (Integration), WHICH algorithm it uses (Pattern), and WHY it makes choices (Decision).

This style makes pseudocode directly translatable to production code while preserving architectural guidance.

## When to Use

Use when:
- Adding pseudocode to implementation guides
- Documenting algorithms in technical specifications
- Showing method implementations in API documentation
- Creating code examples for developers who will implement

Don't use for:
- Abstract algorithm descriptions (use traditional pseudocode)
- User-facing documentation (use prose)
- Quick code sketches (use actual working code)

## Required Elements

**Every implementation pseudocode MUST include:**
1. **JSDoc header** with Integration note
2. **Strategic comments** (Boundary/Integration/Pattern/Decision) for key operations
3. **Section separators** (`---`) for multi-phase algorithms
4. **Actual TypeScript syntax** (not abstract pseudocode)

**Without these elements, pseudocode is incomplete.**

## Core Pattern

### Before (Generic Comments)

```typescript
extractBlock(anchorId: string): string | null {
  // Step 1: Find the block anchor in parsed anchors
  const anchor = this._data.anchors.find(a =>
    a.anchorType === 'block' && a.id === anchorId
  );

  // Not found? Return null
  if (!anchor) return null;

  // Step 2: Split content into lines
  const lines = this._data.content.split('\n');
  const lineIndex = anchor.line - 1;

  // Step 3: Validate line index
  if (lineIndex < 0 || lineIndex >= lines.length) {
    return null;
  }

  // Step 4: Extract and return line
  return lines[lineIndex];
}
```

### After (Strategic Comments)

```typescript
/**
 * Extract content for a specific block reference by anchor ID.
 * Integration: Uses anchor metadata from MarkdownParser output.
 *
 * @param anchorId - Block anchor ID without ^ prefix
 * @returns Single line content string or null if not found
 */
extractBlock(anchorId: string): string | null {
  // --- Anchor Lookup ---
  // Integration: Query anchors array from parser output
  const anchor = this._data.anchors.find(a =>
    a.anchorType === 'block' && a.id === anchorId
  );

  // Decision: Return null if block anchor not found (edge case handling)
  if (!anchor) return null;

  // --- Line Positioning ---
  // Boundary: Split raw content into lines for line-based extraction
  const lines = this._data.content.split('\n');
  const lineIndex = anchor.line - 1;  // Pattern: Convert 1-based to 0-based indexing

  // Decision: Validate line index within bounds (edge case handling)
  if (lineIndex < 0 || lineIndex >= lines.length) return null;

  // --- Content Extraction ---
  return lines[lineIndex];
}
```

## Quick Reference

| Element | Purpose | Example |
|---------|---------|---------|
| **JSDoc Header** | Method purpose, integration context, params | `/** Integration: Uses marked.js tokens */` |
| **Section Separator** | Group related operations | `// --- Phase 1: Token Walking ---` |
| **Boundary Comment** | Marks external system interaction | `// Boundary: File system read` |
| **Integration Comment** | Shows dependency usage | `// Integration: Uses marked.js lexer` |
| **Pattern Comment** | Identifies algorithm approach | `// Pattern: Binary search` |
| **Decision Comment** | Explains branching logic | `// Decision: Return null if not found` |
| **Inline Comment** | Short explanation on same line | `const idx = line - 1;  // Pattern: 1-based to 0-based` |

## Strategic Comment Types

### Boundary
Marks where code crosses system boundaries (file I/O, network, database, external data access).

```typescript
// Boundary: Direct access to encapsulated raw content
return this._data.content;

// Boundary: Split raw content into lines for line-based extraction
const lines = this._data.content.split('\n');
```

### Integration
Shows how code integrates with external libraries, frameworks, or components.

```typescript
// Integration: Uses marked.js token tree for structural navigation
const walkTokens = (tokenList) => { ... };

// Integration: Query anchors array from parser output
const anchor = this._data.anchors.find(...);
```

### Pattern
Identifies the algorithm, data structure, or design pattern being used.

```typescript
// Pattern: Child-before-sibling traversal ensures in-order token collection
if (token.tokens) walkTokens(token.tokens);

// Pattern: Convert 1-based to 0-based indexing
const lineIndex = anchor.line - 1;
```

### Decision
Explains why code makes a particular choice, especially for edge cases and branching.

```typescript
// Decision: Return null if target heading not found (edge case handling)
if (targetIndex === -1) return null;

// Decision: Validate line index within bounds (edge case handling)
if (lineIndex < 0 || lineIndex >= lines.length) return null;
```

## Section Separators

Use semantic names, not step numbers:

```typescript
// ❌ Bad: Generic step numbers
// Step 1: Find anchor
// Step 2: Split lines
// Step 3: Validate
// Step 4: Extract

// ✅ Good: Semantic section names
// --- Anchor Lookup ---
// --- Line Positioning ---
// --- Content Extraction ---
```

For multi-phase algorithms, use phase names:

```typescript
// --- Phase 1: Token Walking & Target Location ---
// --- Phase 2: Boundary Detection ---
// --- Phase 3: Content Reconstruction ---
```

## JSDoc Headers

Always include:
- **Purpose**: What the method does
- **Integration note**: Key external dependencies
- **@param**: Parameter descriptions
- **@returns**: Return value description

```typescript
/**
 * Extract content for a specific section by heading text and level.
 * Integration: Uses marked.js token tree for structural navigation.
 *
 * @param headingText - Exact heading text to find
 * @param headingLevel - Heading depth (1-6)
 * @returns Section content string or null if not found
 */
```

## Inline Comments

Use for brief explanations that fit on one line:

```typescript
const lineIndex = anchor.line - 1;  // Pattern: Convert 1-based to 0-based
if (targetIndex === -1) return null;  // Not found? Return null
```

## Grouping Operations

Group related operations under section headers:

```typescript
// --- Anchor Lookup ---
const anchor = this._data.anchors.find(a =>
  a.anchorType === 'block' && a.id === anchorId
);
if (!anchor) return null;

// --- Line Positioning ---
const lines = this._data.content.split('\n');
const lineIndex = anchor.line - 1;
if (lineIndex < 0 || lineIndex >= lines.length) return null;

// --- Content Extraction ---
return lines[lineIndex];
```

## Red Flags - STOP and Add Strategic Comments

If your pseudocode has any of these, it's incomplete:

- ❌ No Boundary/Integration/Pattern/Decision comments
- ❌ Using "Step 1, Step 2, Step 3" labels
- ❌ No `---` section separators for multi-phase algorithms
- ❌ JSDoc missing Integration note
- ❌ No strategic comments on key operations

**All of these mean: Add strategic comments now.**

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Numbered steps | Generic, no semantic meaning | Use `---` section names with strategic comments |
| Verbose comments | "Split content into lines for line-based extraction" | "Boundary: Split raw content into lines" |
| No strategic markers | Missing architectural context | Add Boundary/Integration/Pattern/Decision |
| Abstract syntax | `field x`, `method foo()` | Use actual TypeScript syntax |
| No JSDoc | Missing integration context | Add header with Integration note |
| All comments above code | Hard to scan | Use inline for brief notes |
| Generic phases | "Phase 1, Phase 2" without strategic context | Use strategic comments within phases |

## When Strategic Comments Add Value

**Use strategic comments when:**
- Code crosses boundaries (file I/O, network, DB)
- Code integrates with external systems/libraries
- Algorithm choice matters (binary search, traversal pattern)
- Edge case handling needs explanation
- Index conversions happen (1-based to 0-based)

**Don't overuse:**

```typescript
// ❌ Too many strategic comments
// Integration: Uses JavaScript array method
const items = array.filter(x => x.active);

// ✅ Only when it adds value
// Integration: Uses marked.js token tree for structural navigation
const tokens = marked.lexer(content);
```

## Real-World Impact

**Before (baseline test result):**
- Generic step numbers
- No architectural context
- Developer has to infer integration points
- Missing boundary markers

**After (with strategic comments):**
- Clear section organization
- Explicit integration points marked
- Boundary crossings identified
- Pattern choices documented
- Decision rationale explained

Developers can implement faster because they know WHERE code touches external systems, HOW it integrates, WHICH patterns to use, and WHY decisions were made.
