---
name: [constraint-name]
description: Critical requirement for [what the constraint enforces]. Reference when [situations where this applies].
---

# [Constraint Name] - CRITICAL REQUIREMENT

**[One-line summary of the architectural principle.]**

[Brief explanation of what this means and why it matters - 2-3 sentences max.]

## What Violates This Constraint

### 1. [Violation Category 1]

```[language]
// FORBIDDEN: [Description of what's wrong]
[code example]
```

**Why it's wrong:** [Explanation of consequences]

**Correct approach:**
```[language]
// CORRECT: [Description of the fix]
[code example]
```

### 2. [Violation Category 2]

```[language]
// FORBIDDEN: [Description]
[code example]
```

**Why it's wrong:** [Explanation]

**Correct approach:**
```[language]
// CORRECT: [Description]
[code example]
```

## Where [Constrained Code] IS Allowed

| Location | Allowed | Example |
|----------|---------|---------|
| `[path/pattern]` | Yes | [Description of what's allowed] |
| `[path/pattern]` | Yes | [Description] |
| `[path/pattern]` | No | [Why not allowed] |
| Unit tests | No | Use `[test helper]` instead |

## The Correct Pattern

All [type of code] MUST use `[correct approach]`:

```[language]
// Import the helper
use [module]::[helper];

fn test_[feature]() {
    // Create test context using the helper
    let context = [helper]();

    // Create entities/resources as needed for THIS test
    let resource = [Resource]::new("[name]")
        .with_property("[key]", [value]);

    // Test the feature
    assert!(context.[feature_works](resource));
}
```

## Why This Matters

If [constrained code] assumes [specific things]:
1. [Consequence 1]
2. [Consequence 2]
3. [Consequence 3]
4. [Overall impact]

**This requirement must survive context compaction. It is non-negotiable.**
