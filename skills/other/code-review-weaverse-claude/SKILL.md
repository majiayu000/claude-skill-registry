---
name: code-review
description: "[Skill] Perform thorough code reviews focusing on unused code, duplications, coding patterns, bugs, and optimizations. Use when user wants code reviewed or audited. Read-only - outputs findings without making changes."
argument-hint: [file, directory, or scope]
allowed-tools: Read, Grep, Glob
---

Perform a comprehensive code review on $ARGUMENTS. This is a **read-only** review - do NOT modify any files. Only output findings.

## Review Categories

### 1. Dead Code Detection
- Unused imports
- Unused variables, functions, components, hooks
- Unreachable code paths
- Commented-out code that should be removed
- Unused type definitions / interfaces

### 2. Code Duplication
- Duplicated logic that could be extracted to a shared utility
- Similar components that could be consolidated
- Repeated patterns that warrant a custom hook
- Copy-pasted code blocks across files

### 3. Coding Pattern Violations
Check against these rules:
- **Collocation > Distribution**: Related code should live together, not scattered
- **`let` > `const`**: Prefer `let` over `const` for variable declarations
- **Named exports > Default exports**: Use `export function Foo` not `export default`
- **Function declarations > Function expressions**: Use `function foo()` not `const foo = () =>`
- **No `useMemo`**: Flag any usage of `useMemo`
- **No `useCallback`**: Flag any usage of `useCallback`
- **`ALL_CAPS` for constants**: Constants should be `SCREAMING_SNAKE_CASE`

### 4. Bugs & Memory Leaks
- Missing cleanup in useEffect
- Event listeners not removed
- Subscriptions not unsubscribed
- Stale closures
- Race conditions in async code
- Missing error handling
- Null/undefined access risks
- Incorrect dependency arrays

### 5. Optimization Opportunities
- Unnecessary re-renders
- Heavy computations in render path
- Missing keys in lists
- Inefficient data structures
- N+1 query patterns
- Bundle size concerns (large imports)

## Output Format

For each finding, output with **numbered indexes** wrapped in brackets for easy reference:

```
CATEGORY NAME

[1] `file:line` - Short description
    Brief explanation if needed (4-space indent)

[2] `file:line` - Short description
    Explanation with 4-space indent

```

**Important formatting rules:**
- Use ALL CAPS for category names
- Use sequential numbering wrapped in brackets `[1]`, `[2]`, etc. across ALL categories
- Highlight file references with backticks: `filename:line`
- Indent explanations with 4 spaces for readability
- For **Coding Pattern Violations**: If multiple items with the same problem occur in the same file, list only ONCE (e.g., "5 usages of `const`" instead of listing each). No fix suggestions needed - these are easy fixes.

Example:
```
DEAD CODE

[1] `src/utils/helpers.ts:42` - Unused function `formatDate`
    Not imported anywhere in the codebase

[2] `src/components/Modal.tsx:3` - Unused import `useEffect`

CODING PATTERN VIOLATIONS

[3] `src/hooks/useAuth.ts` - Using `const` instead of `let` (7 occurrences)

[4] `src/components/Button.tsx:1` - Default export used

[5] `src/api/client.ts` - Function expressions instead of declarations (3 occurrences)

```

## End of Review

After listing all findings, ask the user:

```
Found [N] items. Which would you like me to address?
- Enter number(s) to fix specific items (e.g., "1, 3, 5" or "1-5")
- "all" to fix everything
- "none" to skip
- Or describe what you'd like to do
```

## Instructions

1. Thoroughly explore the target files/directory
2. Cross-reference imports and usages across the codebase
3. Check for pattern violations against the coding rules
4. Look for subtle bugs and memory leak patterns
5. Identify optimization opportunities
6. Output ALL findings grouped by category
7. Be specific: always include `filename:line` references
8. Be concise: short descriptions, no lengthy explanations
9. **DO NOT** make any changes - this is review only
