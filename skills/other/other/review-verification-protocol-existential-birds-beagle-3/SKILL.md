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
```python
# Type annotation, NOT cast
data: UserData = await load_user()

# Type narrowing with isinstance
if isinstance(data, User):
    data.name  # Mypy knows this is User
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

### Python

| Pattern | Why It's Valid |
|---------|----------------|
| `dict.get(key, [])` | Returns default for missing keys, not error suppression |
| `Optional[T]` return type | Standard way to express nullable in Python typing |
| `assert` in test code | pytest uses assertions, not try/except |
| Type annotation on variable | Not a cast, just a hint for type checkers |
| `typing.cast()` with prior validation | Valid after runtime check confirms type |

### FastAPI

| Pattern | Why It's Valid |
|---------|----------------|
| `Depends()` without explicit type | FastAPI infers dependency type from function signature |
| `async def` endpoint without await | May use sync DB calls or simple returns |
| Response model different from DB model | Separation of concerns between API and persistence |
| `BackgroundTasks` parameter | Valid for fire-and-forget operations |
| Direct `request.state` access | Standard pattern for middleware-injected data |

### Testing

| Pattern | Why It's Valid |
|---------|----------------|
| `assert` without message | pytest rewrites assertions to show detailed diffs |
| `@pytest.fixture` without explicit scope | Default `function` scope is correct for most fixtures |
| `monkeypatch` over `unittest.mock` | Simpler API, pytest-native |
| Fixture returning mutable state | Each test gets fresh fixture invocation by default |

### General

| Pattern | Why It's Valid |
|---------|----------------|
| `+?` lazy quantifier in regex | Prevents over-matching, correct for many patterns |
| Direct string concatenation | Simpler than template literals for simple cases |
| Multiple returns in function | Can improve readability |
| Comments explaining "why" | Better than no comments |

## Context-Sensitive Rules

### Type Annotations

Flag missing type annotation **ONLY IF ALL** of these are true:
- [ ] Function is public API (not prefixed with `_`)
- [ ] Types are not obvious from context (e.g., `x = 5` is clearly `int`)
- [ ] Not a test function or fixture
- [ ] Codebase has existing typing conventions

### Exception Handling

Flag bare `except` **ONLY IF**:
- [ ] Not in a top-level error boundary / middleware
- [ ] The caught exception is actually swallowed (not logged/re-raised)
- [ ] Specific exception types are known and available
- [ ] Not in cleanup/teardown code where any error should be caught

### Error Handling

Flag missing try/except **ONLY IF**:
- [ ] No middleware or error handler catches this at a higher level
- [ ] The framework doesn't handle errors (FastAPI exception handlers)
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
