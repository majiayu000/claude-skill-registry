---
name: reference-educational-template
description: '[REPLACE] Teach concepts and demonstrate patterns with examples. Use
  when [REPLACE with specific triggers].'
---

---
name: reference-educational-template
description: [REPLACE] Teach concepts and demonstrate patterns with examples. Use when [REPLACE with specific triggers].
allowed-tools: Read, TodoWrite
---

# Reference-Educational Template

## Purpose

This template demonstrates educational content delivery with concept explanation, examples, and anti-patterns.

**Use this template when:**

- Teaching concepts or design patterns
- Explaining language features
- Demonstrating best practices
- Showing common mistakes to avoid

## Workflow

### Phase 1: Explain Concept

<explain>
1. Define the concept clearly
2. Explain why it exists
3. Describe when to use it
4. Compare with alternatives
</explain>

### Phase 2: Show Examples

<examples>
1. Basic usage example
2. Intermediate patterns
3. Advanced techniques
4. Real-world scenarios
</examples>

### Phase 3: Demonstrate Patterns

<patterns>
1. Common patterns
2. Best practices
3. Performance considerations
4. Type safety implications
</patterns>

### Phase 4: Highlight Pitfalls

<pitfalls>
1. Common mistakes
2. Edge cases
3. Antipatterns to avoid
4. Debugging tips
</pitfalls>

<validate>
List scripts that should be run to validate the output of this skill
</validate>

## Progressive Disclosure

**Core content (this file):**

- Concept explanation
- Basic examples
- When to use guidance

**Detailed examples (references/):**

- @references/type-guard-examples.md - Complete pattern demonstrations
- Advanced techniques and edge cases

## Example Usage

````xml
<explain>
Type guards are TypeScript constructs that narrow types within conditional blocks.
They allow the compiler to understand type refinement based on runtime checks.

Why: TypeScript needs runtime evidence to narrow union types safely.
When: Use when working with union types or unknown data.
</explain>

<examples>
Basic typeof guard:
```typescript
function process(value: string | number) {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toFixed(2);
}
````

<patterns>
Custom type predicate:
```typescript
function isString(value: unknown): value is string {
  return typeof value === "string";
}
```

<pitfalls>
❌ DON'T: Assume type narrowing persists across function boundaries
✓ DO: Use type predicates for reusable type guards
</pitfalls>
```

## See Also

- @references/type-guard-examples.md - Comprehensive type guard patterns
