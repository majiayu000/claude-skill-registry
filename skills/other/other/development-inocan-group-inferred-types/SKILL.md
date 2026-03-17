---
name: development
description: Provides expertise on development practices and code quality standards for this repo
---

## Overview

This skill provides comprehensive guidance on development practices, code quality standards, and the proper approach to handling incomplete work during implementation.

**Core Principles:**

- **Completeness over speed** - Never leave TODO markers or stub implementations
- **Design before code** - Every TODO discovered requires technical design first
- **Type-driven development** - Types are not optional, they are the contract
- **No technical debt** - Address issues immediately, don't defer them

---

## 🚨 CRITICAL: TODO Markers Are FORBIDDEN

### The Hard Rule

**TODO/FIXME/XXX/HACK markers in committed code are UNACCEPTABLE.**

When you discover a TODO marker (whether you created it or inherited it), this is **NOT** a reminder for later work. This is a **BLOCKING SIGNAL** that:

1. ✅ There is incomplete design work
2. ✅ There is missing implementation
3. ✅ The code is broken or insufficient
4. ✅ You must stop and address it NOW

### Why TODO Markers Are Problematic

```typescript
// ❌ WRONG - This is a broken contract
export type StripTags<T extends string> = T;  // TODO: implement actual stripping

// ❌ WRONG - This defeats the purpose of the function
export function parseComplexData(input: string): ParsedResult {
    // TODO: implement proper parsing
    return {} as ParsedResult;
}

// ❌ WRONG - This is technical debt from day one
export function validateConfig(config: unknown): boolean {
    // FIXME: add validation logic
    return true;
}
```

**Problems with the above:**

1. **Broken contracts** - Users expect `StripTags` to strip tags, but it doesn't
2. **Type lies** - Return types promise something the implementation doesn't deliver
3. **Hidden bugs** - Code appears to work but fails in production
4. **Compounding debt** - One TODO leads to workarounds that create more TODOs
5. **Lost context** - Future you won't remember why the TODO exists or what it needs

---

## The Proper Workflow When You Encounter a TODO

When you find a TODO marker (in existing code or while planning new code), follow this workflow:

### Step 1: STOP Immediately

**Do not proceed with any other work.** TODOs are blocking issues.

```bash
# Immediately search for ALL TODOs in the affected area
rg -i "TODO|FIXME|XXX|HACK" modules/lib/src/

# Document what you found
echo "Found TODO in X: <description>" >> .ai/logs/current-phase.md
```

### Step 2: Understand the Context

Ask yourself:

1. **What is this TODO supposed to do?**
   - Read the surrounding code
   - Check the function signature / type definition
   - Look at how it's being used
   - Review any related documentation

2. **Why was it left incomplete?**
   - Was it a lack of knowledge?
   - Was it complexity avoidance?
   - Was it a placeholder during design?
   - Was it genuinely forgotten?

3. **What would a complete implementation look like?**
   - What are the inputs and outputs?
   - What edge cases need handling?
   - What type-level computation is needed?
   - What tests would verify correctness?

### Step 3: Technical Design

**BEFORE writing any code**, create a technical design for the complete solution.

**For Type Utilities:**

```typescript
// DESIGN NOTES for StripSimpleTags<T>

/**
 * Goal: Remove all SimpleTag markup from a string literal type
 *
 * Input: "Hello <soft>world</soft> and <loud>universe</loud>"
 * Output: "Hello world and universe"
 *
 * Approach:
 * 1. Use recursive conditional types with template literals
 * 2. Pattern match each tag type: <soft>, </soft>, <loud>, </loud>, etc.
 * 3. For each match: extract before/after, strip tag, recurse
 * 4. Base case: no more tags found, return string as-is
 *
 * Edge Cases:
 * - Nested tags: <soft><loud>text</loud></soft>
 * - Multiple tags: <soft>a</soft> <loud>b</loud>
 * - No tags: "plain text"
 * - Empty string: ""
 * - Unclosed tags: <soft>text (treat as-is? or error?)
 *
 * Type Complexity: Medium (recursive template literals)
 * Estimated LOC: ~30-50 lines
 */
```

**For Runtime Functions:**

```typescript
// DESIGN NOTES for parseComplexData()

/**
 * Goal: Parse structured data from string input
 *
 * Input Format: "key1=value1,key2=value2"
 * Output Format: { key1: string, key2: string }
 *
 * Algorithm:
 * 1. Split by commas to get key-value pairs
 * 2. Split each pair by '=' to separate key/value
 * 3. Trim whitespace from keys and values
 * 4. Build result object
 *
 * Edge Cases:
 * - Empty string: return {}
 * - Missing '=': throw error or skip?
 * - Duplicate keys: last wins or error?
 * - Special characters in values: escape handling?
 *
 * Error Handling:
 * - Invalid format: throw ParseError
 * - Malformed pairs: skip with warning or fail fast?
 *
 * Tests Needed:
 * - Happy path: valid input → correct output
 * - Empty input: "" → {}
 * - Malformed: "key1value1" → error
 * - Duplicates: "a=1,a=2" → {a: "2"}
 *
 * Estimated LOC: ~20-30 lines + error handling
 */
```

### Step 4: Add to TODO List

Track this as a **blocking task** in your active todo list:

```typescript
TodoWrite({
    todos: [
        // ... existing todos
        {
            content: "Implement StripSimpleTags type utility with recursive template literal parsing",
            activeForm: "Implementing StripSimpleTags type utility",
            status: "in_progress"
        },
        {
            content: "Add comprehensive type tests for StripSimpleTags",
            activeForm: "Adding type tests for StripSimpleTags",
            status: "pending"
        }
    ]
});
```

### Step 5: Implement Completely

Implement the **full, complete solution** - no shortcuts, no new TODOs.

**For Type Utilities:**

```typescript
/**
 * Strips all SimpleTag markup from a string literal type
 *
 * Handles: <soft>, </soft>, <loud>, </loud>, <fast>, </fast>, <slow>, </slow>
 */
export type StripSimpleTags<T extends string> =
    // Match <soft> opening tag
    T extends `${infer Before}<soft>${infer After}`
        ? StripSimpleTags<`${Before}${StripSimpleTags<After>}`>
    // Match </soft> closing tag
    : T extends `${infer Before}</soft>${infer After}`
        ? StripSimpleTags<`${Before}${StripSimpleTags<After>}`>
    // Match <loud> opening tag
    : T extends `${infer Before}<loud>${infer After}`
        ? StripSimpleTags<`${Before}${StripSimpleTags<After>}`>
    // Match </loud> closing tag
    : T extends `${infer Before}</loud>${infer After}`
        ? StripSimpleTags<`${Before}${StripSimpleTags<After>}`>
    // ... continue for all SimpleTags
    // Base case: no more tags
    : T;
```

**For Runtime Functions:**

```typescript
export function parseComplexData(input: string): ParsedResult {
    if (!input || input.trim() === "") {
        return {};
    }

    const pairs = input.split(",");
    const result: Record<string, string> = {};

    for (const pair of pairs) {
        const [key, value] = pair.split("=");

        if (!key || !value) {
            throw new ParseError(`Invalid key-value pair: "${pair}"`);
        }

        result[key.trim()] = value.trim();
    }

    return result;
}
```

### Step 6: Add Tests

**Tests are not optional.** Every implementation needs verification.

**For Type Utilities:**

```typescript
describe("StripSimpleTags<T>", () => {
    it("should strip <soft> tags", () => {
        type Test1 = StripSimpleTags<"<soft>hello</soft>">;
        type Test2 = StripSimpleTags<"world <soft>hello</soft> universe">;

        type cases = [
            Expect<AssertEqual<Test1, "hello">>,
            Expect<AssertEqual<Test2, "world hello universe">>
        ];
    });

    it("should handle nested tags", () => {
        type Test = StripSimpleTags<"<soft><loud>hello</loud></soft>">;

        type cases = [
            Expect<AssertEqual<Test, "hello">>
        ];
    });

    it("should handle no tags", () => {
        type Test = StripSimpleTags<"hello world">;

        type cases = [
            Expect<AssertEqual<Test, "hello world">>
        ];
    });

    it("should handle empty string", () => {
        type Test = StripSimpleTags<"">;

        type cases = [
            Expect<AssertEqual<Test, "">>
        ];
    });
});
```

**For Runtime Functions:**

```typescript
describe("parseComplexData()", () => {
    it("should parse valid input", () => {
        const result = parseComplexData("key1=value1,key2=value2");

        expect(result).toEqual({
            key1: "value1",
            key2: "value2"
        });
    });

    it("should handle empty string", () => {
        const result = parseComplexData("");

        expect(result).toEqual({});
    });

    it("should throw on invalid format", () => {
        expect(() => parseComplexData("invalid")).toThrow(ParseError);
    });

    it("should handle duplicate keys (last wins)", () => {
        const result = parseComplexData("key=first,key=second");

        expect(result).toEqual({ key: "second" });
    });
});
```

### Step 7: Verify and Mark Complete

Only after **implementation + tests both pass**:

```bash
# Run tests
pnpm test
pnpm test:types

# Verify no TODOs remain in the affected files
rg -i "TODO|FIXME" path/to/file.ts

# Update todo list
TodoWrite({ todos: [...] })  # Mark as completed
```

---

## Common Scenarios and Solutions

### Scenario 1: "I don't know how to implement this"

**❌ WRONG Response:**
```typescript
// TODO: Figure out how to implement this later
export function complexAlgorithm(): Result {
    return {} as Result;
}
```

**✅ CORRECT Response:**

1. **Research first** - Look for similar implementations in codebase or libraries
2. **Ask for help** - Use documentation, search GitHub, ask the user
3. **Break it down** - Decompose into smaller, manageable pieces
4. **Prototype** - Try a simple version first, then refine
5. **Document** - Write design notes explaining your approach

### Scenario 2: "This is too complex for right now"

**❌ WRONG Response:**
```typescript
// TODO: Optimize this later, current impl is slow
export function slowFunction(): void {
    // naive implementation
}
```

**✅ CORRECT Response:**

1. **Implement it properly first** - Even if not optimal, make it correct
2. **Add performance tests** - Measure actual impact before optimizing
3. **Document tradeoffs** - Explain why simple approach was chosen
4. **No TODO** - If it works correctly, it's complete

```typescript
/**
 * Processes data using naive O(n²) algorithm
 *
 * NOTE: For datasets < 1000 items, performance is acceptable.
 * If profiling shows this is a bottleneck, consider:
 * - Hash table approach: O(n)
 * - Binary search: O(n log n)
 *
 * Current implementation prioritizes correctness and readability.
 */
export function processData(items: Item[]): Result {
    // correct implementation
}
```

### Scenario 3: "This needs a major refactor"

**❌ WRONG Response:**
```typescript
// FIXME: This whole module needs refactoring
export class LegacyClass {
    // messy code
}
```

**✅ CORRECT Response:**

1. **File an issue** - Document the refactor need in issue tracker
2. **Make it work** - Ensure current code is correct, even if messy
3. **Plan the refactor** - Create a separate refactor plan
4. **No FIXME** - Working code doesn't get TODO markers

```typescript
/**
 * LegacyClass - Provides X functionality
 *
 * NOTE: This class has grown complex. See issue #123 for refactor plan.
 * Despite complexity, all public methods are tested and working correctly.
 */
export class LegacyClass {
    // working implementation
}
```

---

## Type Utility Development Guidelines

### The Type Utility Contract

When you write a type utility, you're making a **compile-time promise** to users:

```typescript
// This signature is a CONTRACT
export type ParseJSON<T extends string> = /* ... */;

// Users expect:
// - Input: JSON string literal
// - Output: Typed object matching the JSON structure
// - Edge cases: Invalid JSON → never or error type
```

### Red Flags for Incomplete Type Utilities

```typescript
// ❌ Pass-through (does nothing)
export type MyUtility<T> = T;

// ❌ Always returns same type
export type HasProperty<T, K> = false;

// ❌ Uses 'any' as cop-out
export type ParseSomething<T> = any;

// ❌ TODO marker
// TODO: implement this
export type Incomplete<T> = T;
```

### Proper Type Utility Implementation

```typescript
// ✅ Does actual type-level computation
export type StrictExtract<T, U> = T extends U ? T : never;

// ✅ Uses conditional types correctly
export type IsArray<T> = T extends readonly unknown[] ? true : false;

// ✅ Complex but complete
export type DeepReadonly<T> = {
    readonly [K in keyof T]: T[K] extends object
        ? DeepReadonly<T[K]>
        : T[K]
};
```

---

## Runtime Implementation Guidelines

### The Function Contract

When you write a function signature, you're making a **runtime promise**:

```typescript
// This signature is a CONTRACT
export async function fetchUser(id: number): Promise<User>;

// Users expect:
// - Input: valid number
// - Output: Promise that resolves to User object
// - Errors: Rejects on failure (network, not found, etc.)
// - Side effects: Documented (API call)
```

### Red Flags for Incomplete Functions

```typescript
// ❌ Returns mock/fake data
export function getRealData(): Data {
    return { fake: "data" } as Data;
}

// ❌ No implementation
export function complexCalculation(): number {
    return 0; // TODO: implement
}

// ❌ Catches and hides errors
export function dangerousOperation(): void {
    try {
        // something
    } catch {
        // TODO: proper error handling
    }
}
```

### Proper Function Implementation

```typescript
// ✅ Complete implementation
export async function fetchUser(id: number): Promise<User> {
    if (!Number.isInteger(id) || id <= 0) {
        throw new ValidationError("User ID must be positive integer");
    }

    try {
        const response = await fetch(`/api/users/${id}`);

        if (!response.ok) {
            throw new ApiError(`Failed to fetch user: ${response.status}`);
        }

        const data = await response.json();
        return validateUser(data);
    } catch (error) {
        if (error instanceof ApiError || error instanceof ValidationError) {
            throw error;
        }
        throw new NetworkError("Failed to connect to API", { cause: error });
    }
}
```

---

## Quality Checklist

Before committing any code, verify:

### Type Quality
- [ ] No TODO/FIXME/XXX/HACK markers
- [ ] No pass-through type utilities (unless intentional)
- [ ] All type utilities have meaningful implementations
- [ ] Complex types have JSDoc explaining the approach
- [ ] Type tests verify the utility works correctly
- [ ] Edge cases are handled (never, unknown, etc.)

### Runtime Quality
- [ ] No TODO/FIXME/XXX/HACK markers
- [ ] All functions have complete implementations
- [ ] Error cases are handled explicitly
- [ ] Edge cases have tests
- [ ] Function signatures match implementation behavior
- [ ] No return type assertions (as Type) masking incomplete code

### Testing Quality
- [ ] Runtime tests cover happy path + edge cases + errors
- [ ] Type tests verify type inference and narrowing
- [ ] Tests are deterministic (no flaky tests)
- [ ] All tests pass: `pnpm test && pnpm test:types`

---

## When You're Stuck

If you genuinely can't complete something:

### 1. Don't Leave a TODO

**❌ WRONG:**
```typescript
// TODO: implement this
export function incomplete(): void {}
```

### 2. Implement a Minimal Version

**✅ CORRECT:**
```typescript
/**
 * Validates input data
 *
 * CURRENT: Basic validation checking required fields
 * FUTURE: Could be enhanced with schema validation, custom rules, etc.
 *
 * See issue #456 for enhancement ideas
 */
export function validateInput(input: unknown): ValidationResult {
    // Simple but COMPLETE implementation
    if (!input || typeof input !== "object") {
        return { valid: false, errors: ["Input must be an object"] };
    }

    return { valid: true, errors: [] };
}
```

### 3. Ask for Help

**In your message to the user:**

"I'm implementing X and need guidance on Y. I've researched Z and found A and B as potential approaches. Which direction should I take?"

**NOT:**

"I'll add a TODO and come back to this later."

---

## Summary

**The Golden Rule: No TODOs in Committed Code**

Every TODO marker represents:
- ✅ Incomplete design work → Do the design now
- ✅ Missing implementation → Implement it now
- ✅ Insufficient knowledge → Research/ask now
- ✅ Deferred technical debt → Address it now

**When you find a TODO:**

1. **STOP** - Don't proceed with other work
2. **DESIGN** - Write technical design notes
3. **TRACK** - Add to todo list as blocking task
4. **IMPLEMENT** - Write complete solution
5. **TEST** - Verify it works
6. **VERIFY** - Confirm no TODOs remain

**A phase with unresolved TODOs is an INCOMPLETE phase.**

---

## Quick Reference

```bash
# Search for TODOs before committing
rg -i "TODO|FIXME|XXX|HACK" modules/lib/src/

# Search specific areas
rg -i "TODO" modules/lib/src/types/
rg -i "FIXME" modules/lib/src/utils/

# Verify implementation completeness
rg "export type.*= T;$"  # Find pass-through types
rg "return.*as.*;"        # Find type assertions (often masking incomplete code)
rg "throw new Error\(\"Not implemented\"\)"  # Find stub functions
```
