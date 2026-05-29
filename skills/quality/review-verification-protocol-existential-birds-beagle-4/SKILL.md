---
name: review-verification-protocol
description: Mandatory verification steps for all code reviews to reduce false positives. Load this skill before reporting ANY code review findings.
user-invocable: false
---

# Review Verification Protocol

This protocol MUST be followed before reporting any code review finding. Skipping these steps leads to false positives that waste developer time and erode trust in reviews.

For Elixir/OTP/Phoenix/LiveView files, apply the gates below first; the issue-type and cross-stack sections apply when the reviewed code uses those stacks or patterns.

## Hard gates (execute in order)

Do not report a finding until each relevant gate passes for **that** finding. A gate passes only when the pass condition is objectively satisfied (tool output, cited path:line), not when it “feels” verified.

1. **Read gate** — *Pass if:* you opened the full defining function, module section, or template region (or equivalent scoped read), not only the PR diff hunk for that symbol.
2. **Evidence gate** — *Pass if:* the finding cites `path:line` (or line range) that you can tie to actual file content from a read/search tool in this session.
3. **Usage gate** (before “unused”, “dead code”, “unreachable”) — *Pass if:* you ran a repo-wide reference search and can state the result (e.g. zero matches vs matches at listed paths); if the symbol may be invoked dynamically, *Pass if:* you checked reflection-like mechanisms (macros, `apply`, MFA strings, config) or explicitly mark uncertainty as a question, not a defect.
4. **Cross-cutting gate** (before “missing validation/error handling”) — *Pass if:* you checked at least one of caller, plug/pipeline, context, supervision, or framework guarantees, or you document that none apply.
5. **Severity gate** (before Critical/Major) — *Pass if:* you can name a concrete failure mode (what breaks, who is affected), not a style preference or hypothetical edge case.

If you cannot pass a gate, **omit the finding**, **downgrade** per [Severity Calibration](#severity-calibration), or **ask a question** instead of asserting a defect.

## Pre-Report Verification Checklist

Before flagging ANY issue, verify (maps to [Hard gates](#hard-gates-execute-in-order)):

- [ ] **Read gate** — Full symbol/region read, not diff-only
- [ ] **Evidence gate** — Citable `path:line` from tool-backed content
- [ ] **Usage gate** — Reference search (or dynamic-call check) before “unused”
- [ ] **Cross-cutting gate** — Validation/handling checked at other layers where relevant
- [ ] **Docs/syntax** — Verified against current framework/docs for the file’s stack (e.g. Tailwind v4, TS 5.x, React 19 when reviewing those files)
- [ ] **Style vs wrong** — Both approaches may be valid; distinguish
- [ ] **Intentional design** — Comments, CLAUDE.md, AGENTS.md, architectural context considered

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
```elixir
# Pattern matching, NOT type casting
%UserData{} = data = load_user()

# Guard clauses narrow the type safely
def process(%User{name: name} = user) do
  name  # Elixir knows this is a User struct
end
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

### Elixir

| Pattern | Why It's Valid |
|---------|----------------|
| `case` with multiple clauses | Standard pattern matching, not excessive branching |
| `with` chains | Idiomatic for sequential operations that may fail |
| Pipe operator (`\|>`) chains | Elixir's core composition pattern |
| `@spec` without Dialyzer enforcement | Documentation value even without static analysis |
| `defp` private functions | Proper encapsulation, not hidden complexity |

### Phoenix/LiveView

| Pattern | Why It's Valid |
|---------|----------------|
| `assign/2` in `mount/3` | Standard LiveView state initialization |
| `handle_event/3` returning `{:noreply, socket}` | Correct for UI-triggered state updates |
| `~H` sigil for inline templates | Valid for small components |
| `on_mount` hooks | Correct lifecycle pattern for auth/setup |
| PubSub broadcasts in handle_info | Standard real-time communication pattern |

### Testing

| Pattern | Why It's Valid |
|---------|----------------|
| `assert` without message | ExUnit provides clear diff output |
| `setup` block for test context | Standard ExUnit fixture pattern |
| `describe` blocks for grouping | Idiomatic test organization |
| `conn` pipeline in controller tests | Phoenix test helper convention |

### General

| Pattern | Why It's Valid |
|---------|----------------|
| `+?` lazy quantifier in regex | Prevents over-matching, correct for many patterns |
| Direct string concatenation | Simpler than template literals for simple cases |
| Multiple returns in function | Can improve readability |
| Comments explaining "why" | Better than no comments |

## Context-Sensitive Rules

### Pattern Matching

Flag missing pattern match **ONLY IF ALL** of these are true:
- [ ] Function receives structured data that should be destructured
- [ ] Not a pass-through function that forwards data unchanged
- [ ] Pattern match would prevent actual runtime errors
- [ ] Not a GenServer callback with standard signature

### Process Architecture

Flag missing supervision **ONLY IF**:
- [ ] Process is long-lived (not a Task)
- [ ] Crash would affect system stability
- [ ] No supervisor already manages this process
- [ ] Not a test-only process

### Error Handling

Flag missing error handling **ONLY IF**:
- [ ] No `with` clause handles the error case
- [ ] No supervision tree restarts the process
- [ ] The error would cascade beyond the current process
- [ ] User needs specific feedback for this error type

## Before Submitting Review

Final verification:
0. For each finding, confirm the [Hard gates](#hard-gates-execute-in-order) that apply to its type were passed (or the finding was downgraded/removed).
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
