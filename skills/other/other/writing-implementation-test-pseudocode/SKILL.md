---
name: writing-implementation-test-pseudocode
description: Use when adding test pseudocode to user stories or implementation guides - creates MEDIUM-IMPLEMENTATION abstraction showing test structure with Vitest terminology, placeholder comments for logic, and strategic comments (Research/Fixture/Integration/Verification/Pattern/Decision) that guide what to research and decide, not complete implementations
---

# Writing Implementation Test Pseudocode

## Overview

**Test implementation pseudocode uses Vitest syntax with placeholder comments** that show WHAT to test and WHY it matters, without providing complete HOW implementations.

This follows MEDIUM-IMPLEMENTATION abstraction level: shows test structure and architectural decisions while using placeholder comments for complex logic. Teaches developers what to research and decide, not line-by-line implementation.

**Core principle:** Guide architectural thinking for tests, not implementation details.

## When to Use

Use when:
- Adding test examples to user stories (Dev Notes sections)
- Documenting test patterns in technical specifications
- Showing test structure for developers who will implement
- Token efficiency matters (~60% reduction vs full implementation)

Don't use for:
- Complete working test code (use actual tests)
- Test documentation for end users (use prose)
- Abstract test theory (use traditional documentation)

## Required Elements

**Every test pseudocode MUST include:**
1. **Vitest terminology** (describe, it, expect, beforeEach) - teaches framework correctly
2. **Placeholder comments** for complex logic (`/* filter logic */` not `.filter(x => x.valid)`)
3. **Strategic comments** (Research/Fixture/Integration/Verification/Pattern/Decision)
4. **Test phase markers** (Given-When-Then or Arrange-Act-Assert)
5. **What's real vs abstract** - mark integration boundaries explicitly

**Without these elements, test pseudocode is incomplete.**

## Core Pattern

### Before (Complete Implementation - Too Detailed)

```javascript
it("should derive summary counts from enriched links", async () => {
  const { summary, links } = await validator.validateFile(mixedValidationSourcePath);

  const manualCounts = {
    total: links.length,
    valid: links.filter(link => link.validation.status === "valid").length,
    errors: links.filter(link => link.validation.status === "error").length,
    warnings: links.filter(link => link.validation.status === "warning").length
  };

  expect(summary.total).toBe(manualCounts.total);
  expect(summary.valid).toBe(manualCounts.valid);
});
```

### After (MEDIUM-IMPLEMENTATION - Architectural Guidance)

```javascript
it("should derive summary counts from enriched links", async () => {
  // Given: File with 3 valid, 2 error, 1 warning links
  // When: Validation completes
  const { summary, links } = /* await validator.validateFile(...) */;

  // Then: Summary matches link.validation.status counts
  // Verification: Summary derives from links, not separate calculation
  const manualCounts = {
    total: links.length,
    valid: /* count links where validation.status === "valid" */,
    errors: /* count links where validation.status === "error" */,
    warnings: /* count links where validation.status === "warning" */
  };

  // Pattern: Compare aggregate calculation to stored summary
  expect(summary.total).toBe(manualCounts.total);
  expect(summary.valid).toBe(manualCounts.valid);
});
```

## Quick Reference

| Element | Purpose | Example |
|---------|---------|---------|
| **Vitest Structure** | Framework terminology | `describe`, `it`, `expect`, `beforeEach` |
| **Placeholder Comment** | Abstract complex logic | `/* count links where status === "valid" */` |
| **Research Comment** | What to investigate | `// Research: Vitest fixture patterns` |
| **Fixture Comment** | Test data decisions | `// Fixture: Real file with mixed valid/invalid` |
| **Integration Comment** | Real vs mocked boundary | `// Integration: Real parser, null validator` |
| **Verification Comment** | What's being tested | `// Verification: Summary derives from links` |
| **Pattern Comment** | Test structure approach | `// Pattern: Given-When-Then structure` |
| **Decision Comment** | Edge case rationale | `// Decision: Verify no correlation needed` |
| **Phase Markers** | Test organization | `// Given:`, `// When:`, `// Then:` |

## Strategic Comment Types

### Research
Marks what developer needs to investigate - external patterns, libraries, or approaches.

```javascript
// Research: Vitest fixture patterns for workspace isolation
// Research: DI setup for test components without mocks
beforeEach(() => {
  /* setup test environment */
});
```

### Fixture
Explains test data and environment setup decisions - what's realistic vs minimal.

```javascript
// Fixture: Real markdown file with mixed valid/invalid citations
const testFile = /* resolve fixture path */;

// Fixture: Use actual file system, not in-memory mock (integration test)
const validator = /* create with real dependencies */;
```

### Integration
Shows what's real vs mocked - critical for understanding test boundaries.

```javascript
// Integration: Real MarkdownParser with file system access
// Integration: Null for unused LinkResolver dependency (not under test)
validator = /* new CitationValidator(cache, null) */;
```

### Verification
Explains what's being tested and why - the assertion strategy.

```javascript
// Verification: LinkObject enriched with validation property (not separate results)
expect(link).toHaveProperty("validation");

// Verification: Valid links have status="valid" with no error fields
expect(validLink.validation.status).toBe("valid");
expect(validLink.validation).not.toHaveProperty("error");
```

### Pattern
Identifies test structure or algorithm approach being demonstrated.

```javascript
// Pattern: Given-When-Then structure for behavioral testing
// Given: Real markdown file
// When: Validate file
// Then: Verify enriched structure

// Pattern: Compare aggregate calculation to stored summary
const manualCounts = /* derive from links array */;
expect(summary.total).toBe(manualCounts.total);
```

### Decision
Explains why test makes particular choices, especially edge cases.

```javascript
// Decision: Verify summary derives FROM links, not vice versa (directionality)
const manualCounts = /* count from links.validation.status */;

// Decision: Test illegal state prevention (valid should never have error)
expect(validLink.validation).not.toHaveProperty("error");
```

## Placeholder Comment Patterns

Use placeholder comments to abstract implementation details:

```javascript
// ❌ Too detailed - shows complete implementation
const valid = links.filter(link => link.validation.status === "valid").length;

// ✅ Abstracted - shows intent, developer implements
const valid = /* count links where validation.status === "valid" */;

// ❌ Too detailed - complete object construction
const validator = new CitationValidator(new ParsedFileCache(new MarkdownParser(fs)), null);

// ✅ Abstracted - shows what's real vs null
validator = /* new CitationValidator(cache, null) */;

// ❌ Too detailed - actual import syntax
import { describe, it, expect, beforeEach } from "vitest";

// ✅ Abstracted - shows framework, not import mechanics
import { /* Vitest test functions */ } from "vitest";
```

## Test Phase Markers

Always mark test phases explicitly:

```javascript
it("should enrich valid links with validation status", async () => {
  // Given: File with valid citations
  const result = /* await validator.validateFile(testFile) */;

  // When: Validation completes
  const { links } = result;

  // Then: Valid links enriched with status="valid"
  // Verification: Status exists and correct, no error properties
  const validLink = /* find first valid link */;
  expect(validLink.validation.status).toBe("valid");
  expect(validLink.validation).not.toHaveProperty("error");
});
```

## Real vs Abstract Guidelines

### SHOW (concrete)
- Vitest structure (describe, it, beforeEach blocks)
- Test phases (Given-When-Then comments)
- Property access patterns (link.validation.status)
- Strategic architectural decisions
- What's being verified (expect statements with clear purpose)

### ABSTRACT (placeholder comments)
- Complex filtering/mapping logic
- Object construction with dependencies
- Import details
- Loop bodies
- Count/aggregate calculations
- Array manipulation

```javascript
// ✅ SHOW: Test structure and phases
describe("CitationValidator Enrichment", () => {
  beforeEach(() => {
    // Integration: Real components with DI (no mocks)
    validator = /* new CitationValidator(cache, null) */;
  });

  it("should derive summary from links", async () => {
    // Given: File with mixed validation states
    // When: Validation completes
    const { summary, links } = /* await validator.validateFile(...) */;

    // Then: Summary matches link counts
    // ABSTRACT: Count logic
    const manualCounts = {
      total: links.length,  // SHOW: Simple property access
      valid: /* count links where validation.status === "valid" */  // ABSTRACT: Filter logic
    };

    expect(summary.valid).toBe(manualCounts.valid);
  });
});
```

## Token Efficiency

Test pseudocode in user stories should target **~200-300 words** vs **~800+ words** for complete implementation.

**Techniques:**
- Use placeholder comments for all complex logic
- One excellent example, not multiple variations
- Strategic comments only where they add architectural value
- Omit obvious Vitest patterns (standard beforeEach setup)

**Before (863 words):**

```javascript
// Complete implementation with all details
const manualCounts = {
  total: links.length,
  valid: links.filter(link => link.validation.status === "valid").length,
  errors: links.filter(link => link.validation.status === "error").length,
  warnings: links.filter(link => link.validation.status === "warning").length
};
```

**After (320 words):**

```javascript
// MEDIUM-IMPLEMENTATION abstraction
const manualCounts = {
  total: links.length,
  valid: /* count links where validation.status === "valid" */,
  errors: /* count where status === "error" */,
  warnings: /* count where status === "warning" */
};
```

## Red Flags - STOP and Add Abstraction

If your test pseudocode has any of these, it's too detailed:

- ❌ Complete filter/map/reduce implementations
- ❌ Actual lambda expressions in code
- ❌ No placeholder comments for logic
- ❌ No Research/Fixture/Verification strategic comments
- ❌ Using implementation comment taxonomy (Boundary instead of Fixture)
- ❌ Complete object construction with all parameters
- ❌ More than 500 words for a single test example

**All of these mean: Add placeholder comments and strategic guidance now.**

## Resisting Pressure for Complete Implementations

You will face pressure to provide complete implementations instead of MEDIUM-IMPLEMENTATION abstraction. Resist these rationalizations:

| Pressure | Rationalization | Reality |
|----------|----------------|---------|
| **Authority** | "Senior architect needs complete code" | Architects review architectural decisions, not implementation details |
| **Helper instinct** | "Junior dev needs to see how it works" | Juniors learn by implementing, not copy-pasting |
| **Time pressure** | "Need production-ready code now" | Pseudocode guides faster than complete code requires maintenance |
| **Past problems** | "Team had issues with incomplete docs" | Incomplete ≠ abstracted. Strategic guidance IS complete. |
| **Copy-paste request** | "Devs should be able to copy-paste" | Copy-paste skips learning. Goal is understanding, not shortcuts. |

**When asked for complete implementations:**
1. Acknowledge the concern (time pressure, clarity needs, etc.)
2. Explain MEDIUM-IMPLEMENTATION abstraction purpose (learning, token efficiency)
3. Provide pseudocode following skill guidelines
4. If they insist on complete code, redirect to actual test files in repository (don't write it)

**Never rationalize:**
- "I'll make it complete to be helpful"
- "This one time won't hurt"
- "They're senior, they must know better"
- "The skill allows complete code in some cases" (it doesn't)

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Complete implementations | Provides HOW instead of WHAT | Use placeholder comments |
| No strategic comments | Missing architectural context | Add Research/Fixture/Integration/Verification |
| Wrong comment taxonomy | Using implementation style | Use test-specific taxonomy |
| No test phase markers | Unclear test structure | Add Given-When-Then comments |
| Verbose for user stories | Token budget exceeded | Target ~200-300 words |
| No Research markers | Developer doesn't know what to investigate | Mark integration points needing research |
| All code shown | No abstraction guidance | Mix concrete structure with abstract logic |

## When Strategic Comments Add Value

**Use strategic comments when:**
- Test crosses integration boundaries (real vs mocked)
- Developer needs to research patterns (fixtures, DI setup)
- Verification strategy matters (what's being tested, why)
- Test structure pattern is non-obvious (Given-When-Then, AAA)
- Edge cases need explanation (illegal state prevention)

**Don't overuse:**

```javascript
// ❌ Too many strategic comments
// Pattern: Array access
const link = links[0];

// ✅ Only when it adds value
// Verification: Single object provides both structure and validation (no correlation)
const link = links[0];
```

## Real-World Impact

**Before (baseline test result):**
- Complete implementations (~860 words)
- Wrong strategic comment taxonomy (Boundary/Integration)
- No Research markers for patterns to investigate
- Token inefficient for user stories

**After (with test pseudocode skill):**
- MEDIUM-IMPLEMENTATION abstraction (~300 words)
- Test-specific taxonomy (Research/Fixture/Verification)
- Clear guidance on what to research and decide
- 60% token reduction for user stories

Developers can implement faster because they understand WHAT to test, WHY it matters, WHAT to research, and WHERE integration boundaries are - without being given complete implementations that skip learning.

## Complete Example

```javascript
// tools/citation-manager/test/integration/citation-validator-enrichment.test.js
import { /* Vitest test functions */ } from "vitest";
import { /* real system dependencies */ } from "...";

describe("CitationValidator Validation Enrichment Pattern", () => {
  let validator;
  let testFixturePath;

  beforeEach(() => {
    // Research: Vitest fixture patterns for isolation
    // Integration: Real components with DI (no mocks)
    const parser = /* new MarkdownParser with real fs */;
    const cache = /* new ParsedFileCache(parser) */;
    validator = /* new CitationValidator(cache, null) */;

    // Fixture: Real file with mixed valid/invalid links
    testFixturePath = /* resolve fixture path */;
  });

  it("should return ValidationResult with summary and enriched links", async () => {
    // Given: Real markdown file with citations
    // When: Validate file using enrichment pattern
    const result = /* await validator.validateFile(testFixturePath) */;

    // Then: Result has correct structure
    // Verification: New contract with summary + links (not separate results)
    expect(result).toHaveProperty("summary");
    expect(result).toHaveProperty("links");
    expect(result).not.toHaveProperty("results"); // OLD contract removed
  });

  it("should enrich valid LinkObjects with validation status", async () => {
    // Given: File with valid citations
    // When: Validation completes
    const { links } = /* await validator.validateFile(...) */;

    // Then: Valid links enriched with status="valid"
    // Verification: Valid state has no error/suggestion properties
    const validLink = /* links.find(link => link has valid target) */;
    expect(validLink).toHaveProperty("validation");
    expect(validLink.validation.status).toBe("valid");
    expect(validLink.validation).not.toHaveProperty("error");
  });

  it("should derive summary counts from enriched links", async () => {
    // Given: File with 3 valid, 2 error, 1 warning links
    // When: Validation completes
    const { summary, links } = /* await validator.validateFile(...) */;

    // Then: Summary matches link.validation.status counts
    // Pattern: Aggregate from links array to verify summary derivation
    const manualCounts = {
      total: links.length,
      valid: /* count links where validation.status === "valid" */,
      errors: /* count links where validation.status === "error" */,
      warnings: /* count links where validation.status === "warning" */
    };

    // Decision: Verify summary derives FROM links (directionality matters)
    expect(summary.total).toBe(manualCounts.total);
    expect(summary.valid).toBe(manualCounts.valid);
    expect(summary.errors).toBe(manualCounts.errors);
  });
});
```
