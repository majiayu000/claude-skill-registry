---
name: review-and-simplify
description: Review and simplify implementation
user-invocable: true
---

# Review and Simplify Implementation

## Steps

1. **Get diff against main**:

   ```bash
   git diff main...HEAD --name-only | grep -E '\.(ts|tsx)$' | grep -v '\.test\.'
   ```

2. **For each changed file** (excluding tests):

   Read the file and identify:
   - **Dead code**: Unused imports, variables, functions
   - **Over-abstraction**: Unnecessary indirection, premature generalization
   - **Unclear naming**: Variables/functions that don't describe their purpose
   - **Redundant logic**: Duplicate code, unnecessary conditions
   - **Complex expressions**: Code that could be simplified

3. **For each simplification**:

   a. Make the change

   b. Run tests to verify no breakage:

   ```bash
   npm test --workspaces --if-present
   ```

   c. If tests fail, revert and skip that simplification

4. **If any simplifications were made**, commit:
   ```bash
   git commit -m "refactor: simplify implementation"
   ```

## What to Simplify

**DO**:

- Remove unused imports
- Remove unused variables and functions
- Simplify complex conditionals
- Inline single-use abstractions
- Improve variable/function names for clarity
- Remove redundant type annotations
- Simplify nested callbacks/promises

**DO NOT**:

- Add new features
- Change observable behavior
- Add documentation or comments
- Refactor code that wasn't changed in this feature
- Add error handling that wasn't in the original
- "Improve" working code just because you can

## Example Simplifications

```typescript
// Before: Over-complicated
const isValid = data !== null && data !== undefined && data.length > 0;

// After: Simplified
const isValid = data?.length > 0;
```

```typescript
// Before: Unused abstraction
function createHandler(fn: Function) {
  return (req, res) => fn(req, res);
}
app.get("/api", createHandler(handleRequest));

// After: Direct usage
app.get("/api", handleRequest);
```

## Notes

- This is a cleanup pass, not a refactoring exercise
- Keep changes minimal and focused
- Test after each change to catch regressions early
- If unsure whether a change is safe, skip it
