---
name: review-verification-protocol
description: Mandatory verification steps for all code reviews to reduce false positives. Load this skill before reporting ANY code review findings.
---

# Review Verification Protocol

This protocol MUST be followed before reporting any code review finding. Skipping these steps leads to false positives that waste developer time and erode trust in reviews.

## Pre-Report Verification Checklist

Before flagging ANY issue, verify:

- [ ] **I read the actual code** - Not just the diff context, but the full function/class
- [ ] **I searched for usages** - Before claiming "unused", searched all references
- [ ] **I checked surrounding code** - The issue may be handled elsewhere (guards, earlier checks)
- [ ] **I verified syntax against current docs** - Framework syntax evolves (Tailwind v4, TS 5.x, React 19)
- [ ] **I distinguished "wrong" from "different style"** - Both approaches may be valid
- [ ] **I considered intentional design** - Checked comments, CLAUDE.md, architectural context

## Verification by Issue Type

### "Unused Variable/Function"

**Before flagging**, you MUST:
1. Search for ALL references in the codebase (grep/find)
2. Check if it's exported and used by external consumers
3. Check if it's used via reflection, decorators, or dynamic dispatch
4. Verify it's not a callback passed to a framework

**Common false positives:**
- State setters in React (may trigger re-renders even if value appears unused)
- Variables used in templates/JSX
- Exports used by consuming packages

### "Missing Validation/Error Handling"

**Before flagging**, you MUST:
1. Check if validation exists at a higher level (caller, middleware, route handler)
2. Check if the framework provides validation (Pydantic, Zod, TypeScript)
3. Verify the "missing" check isn't present in a different form

**Common false positives:**
- Framework already validates (FastAPI + Pydantic, React Hook Form)
- Parent component validates before passing props
- Error boundary catches at higher level

### "Type Assertion/Unsafe Cast"

**Before flagging**, you MUST:
1. Confirm it's actually an assertion, not an annotation
2. Check if the type is narrowed by runtime checks before the point
3. Verify if framework guarantees the type (loader data, form data)

**Valid patterns often flagged incorrectly:**
```typescript
// Type annotation, NOT assertion
const data: UserData = await loader()

// Type narrowing makes this safe
if (isUser(data)) {
  data.name  // TypeScript knows this is User
}
```

### "Potential Memory Leak/Race Condition"

**Before flagging**, you MUST:
1. Verify cleanup function is actually missing (not just in a different location)
2. Check if AbortController signal is checked after awaits
3. Confirm the component can actually unmount during the async operation

**Common false positives:**
- Cleanup exists in useEffect return
- Signal is checked (code reviewer missed it)
- Operation completes before unmount is possible

### "Performance Issue"

**Before flagging**, you MUST:
1. Confirm the code runs frequently enough to matter (render vs click handler)
2. Verify the optimization would have measurable impact
3. Check if the framework already optimizes this (React compiler, memoization)

**Do NOT flag:**
- Functions created in click handlers (runs once per click)
- Array methods on small arrays (< 100 items)
- Object creation in event handlers

## Severity Calibration

### Critical (Block Merge)

**ONLY use for:**
- Security vulnerabilities (injection, auth bypass, data exposure)
- Data corruption bugs
- Crash-causing bugs in happy path
- Breaking changes to public APIs

### Major (Should Fix)

**Use for:**
- Logic bugs that affect functionality
- Missing error handling that causes poor UX
- Performance issues with measurable impact
- Accessibility violations

### Minor (Consider Fixing)

**Use for:**
- Code clarity improvements
- Documentation gaps
- Inconsistent style (within reason)
- Non-critical test coverage gaps

### Informational (No Action Required)

**Use for:**
- Improvements that require adding new dependencies or modules
- Suggestions for net-new code that didn't exist in the codebase before (new modules, test suites, abstractions)
- Architectural ideas for future consideration
- Test infrastructure suggestions (new mock libraries, behaviour extraction)
- Optimizations without measurable impact in the current context

**These are NOT review blockers.** They should be noted for the author's awareness but must not appear in the actionable issue count. The Verdict should ignore informational items entirely.

### Do NOT Flag At All

- Style preferences where both approaches are valid
- Optimizations with no measurable benefit
- Test code not meeting production standards (intentionally simpler)
- Library/framework internal code (shadcn components, generated code)
- Hypothetical issues that require unlikely conditions

## Valid Patterns (Do NOT Flag)

### TypeScript

| Pattern | Why It's Valid |
|---------|----------------|
| `map.get(key) \|\| []` | `Map.get()` returns `T \| undefined`, fallback is correct |
| Class exports without separate type export | Classes work as both value and type |
| `as const` on literal arrays | Creates readonly tuple types |
| Type annotation on variable declaration | Not a type assertion |
| `satisfies` instead of `as` | Type checking without assertion |

### React

| Pattern | Why It's Valid |
|---------|----------------|
| Array index as key (static list) | Valid when: items don't reorder, list is static, no item identity needed |
| Inline arrow in onClick | Valid for non-performance-critical handlers (runs once per click) |
| State that appears unused | May be set via refs, external callbacks, or triggers re-renders |
| Empty dependency array with refs | Refs are stable, don't need to be dependencies |
| Non-null assertion after check | TypeScript narrowing may not track through all patterns |

### Testing

| Pattern | Why It's Valid |
|---------|----------------|
| `toHaveTextContent` without regex | Handles nested text correctly |
| Mock at module level | Defined once, not duplicated |
| Index-based test data | Tests don't need stable identity |
| Simplified error messages | Test clarity over production polish |

### General

| Pattern | Why It's Valid |
|---------|----------------|
| `+?` lazy quantifier in regex | Prevents over-matching, correct for many patterns |
| Direct string concatenation | Simpler than template literals for simple cases |
| Multiple returns in function | Can improve readability |
| Comments explaining "why" | Better than no comments |

## Context-Sensitive Rules

### React Keys

Flag array index as key **ONLY IF ALL** of these are true:
- [ ] Items CAN be reordered (sortable list, drag-drop)
- [ ] Items CAN be inserted/removed from middle
- [ ] Items HAVE stable identifiers available (id, uuid)
- [ ] The list is NOT completely replaced atomically

### useEffect Dependencies

Flag missing dependency **ONLY IF**:
- [ ] The value actually changes during component lifetime
- [ ] Stale closure would cause incorrect behavior
- [ ] The value is NOT a ref (refs are stable)
- [ ] The value is NOT a stable callback (useCallback with empty deps)

### Error Handling

Flag missing try/catch **ONLY IF**:
- [ ] No error boundary catches this at a higher level
- [ ] The framework doesn't handle errors (loader errorElement)
- [ ] The error would cause a crash, not just a failed operation
- [ ] User needs specific feedback for this error type

## Before Submitting Review

Final verification:
1. Re-read each finding and ask: "Did I verify this is actually an issue?"
2. For each finding, can you point to the specific line that proves the issue exists?
3. Would a domain expert agree this is a problem, or is it a style preference?
4. Does fixing this provide real value, or is it busywork?
5. Format every finding as: `[FILE:LINE] ISSUE_TITLE`
6. For each finding, ask: "Does this fix existing code, or does it request entirely new code that didn't exist before?" If the latter, downgrade to Informational.
7. If this is a re-review: ONLY verify previous fixes. Do not introduce new findings.

If uncertain about any finding, either:
- Remove it from the review
- Mark it as a question rather than an issue
- Verify by reading more code context
