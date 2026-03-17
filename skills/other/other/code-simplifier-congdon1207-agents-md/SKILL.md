---
name: code-simplifier
description: Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Focuses on recently modified code unless instructed otherwise.
allowed-tools: Read, Edit, Glob, Grep, Task
infer: true
---

# Code Simplifier Skill

Simplify and refine code for clarity, consistency, and maintainability.

## Usage

```
/code-simplifier                    # Simplify recently modified files
/code-simplifier path/to/file.ts    # Simplify specific file
/code-simplifier --scope=function   # Focus on function-level simplification
```

## What It Does

1. **Analyzes** code for unnecessary complexity
2. **Identifies** opportunities to simplify without changing behavior
3. **Applies** KISS, DRY, and YAGNI principles
4. **Preserves** all existing functionality

## Simplification Targets

- Redundant code paths
- Over-engineered abstractions
- Unnecessary comments (self-documenting code preferred)
- Complex conditionals that can be flattened
- Verbose patterns that have simpler alternatives

## Execution

Use the `code-simplifier:code-simplifier` subagent:

```
Task(subagent_type="code-simplifier:code-simplifier", prompt="Review and simplify [target files]")
```

## Examples

**Before:**

```typescript
function getData() {
  const result = fetchData();
  if (result !== null && result !== undefined) {
    return result;
  } else {
    return null;
  }
}
```

**After:**

```typescript
function getData() {
  return fetchData() ?? null;
}
```
