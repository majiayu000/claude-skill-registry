---
skill: refactor
description: Refactor code while preserving behavior and tests
arguments: file path or component name, and refactoring goal
---

# Refactor: $ARGUMENTS

Safely refactor code while ensuring tests continue to pass.

## Process

### 1. Understand Current State

- Read the target file(s)
- Identify existing tests
- Run tests to confirm they pass before changes:
  ```bash
  npm test -- --testPathPattern="[target]"
  ```

### 2. Plan Refactoring

Common refactoring types:
- **Extract**: Pull code into separate function/component
- **Rename**: Change names for clarity
- **Simplify**: Reduce complexity, remove duplication
- **Restructure**: Change file/folder organization

Document what will change and why.

### 3. Apply Changes Incrementally

Make small, focused changes:
1. One logical change at a time
2. Run tests after each change
3. If tests fail, fix immediately before continuing

### 4. Update Tests if Needed

If refactoring changes the API:
- Update test imports
- Update test assertions
- Add tests for new extracted functions

### 5. Validate

```bash
npm run build
npm run lint
npm test
```

### 6. Report Changes

Summarize:
- Files modified
- What was refactored and why
- Any API changes
- Test status

## Refactoring Patterns

**Extract Component:**
```tsx
// Before: Large component with embedded logic
// After: Smaller component + extracted sub-component
```

**Extract Hook:**
```tsx
// Before: useState + useEffect logic in component
// After: Custom hook encapsulating the logic
```

**Extract Utility:**
```tsx
// Before: Inline data transformation
// After: Pure function in lib/utils.ts
```

## Safety Rules

- Never change behavior, only structure
- Tests must pass before AND after
- If unsure, add tests first
- Preserve public API unless explicitly requested
