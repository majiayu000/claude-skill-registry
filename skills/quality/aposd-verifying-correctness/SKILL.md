---
name: aposd-verifying-correctness
description: "Verify code correctness before claiming done or committing. Run 6-dimension checklist: requirements coverage, concurrency safety, error handling, resource management, boundary conditions, and security. Output PASS/FAIL per dimension with final DONE/NOT DONE verdict. Use after implementation as pre-commit gate. Triggers on: is it done, ready to commit, verify correctness, did I miss anything, pre-commit check."
---

# Skill: aposd-verifying-correctness

## STOP - Before "Done"

**Design quality ≠ correctness.** Well-designed code can still have bugs, missing requirements, or safety issues.

**Run ALL dimension checks before claiming done.** "I think I covered everything" without explicit mapping is a red flag.

---

## Dimension Detection & Checks

For each dimension: detect if it applies, then verify.

---

### 1. Requirements Coverage

**Detect:** Were requirements stated? (explicit list, user request, spec)

**If YES, verify:**
- [ ] List each requirement explicitly
- [ ] For each: point to code that implements it
- [ ] Any requirement without code? → **Not done**
- [ ] Any code without requirement? → Scope creep or missing requirement

**Red flag:** "I think I covered everything" without explicit mapping

---

### 2. Concurrency Safety

**Detect:** Any of these present?
- Multiple threads/processes accessing same data
- Async/await patterns
- Shared mutable state (class attributes, globals)
- "Thread-safe" in requirements or docstring
- Web handlers, queue workers, background tasks

**If YES, verify:**
- [ ] All shared mutable state identified
- [ ] Each access point protected (lock, atomic, queue, immutable)
- [ ] No time-of-check to time-of-use (TOCTOU) gaps
- [ ] Lock ordering consistent (if multiple locks)

**Red flag:** "It's probably fine" or "Python GIL handles it"

---

### 3. Error Handling

**Detect:** Can any operation fail?
- I/O (file, network, database)
- External calls (APIs, subprocesses)
- Resource acquisition (memory, connections)
- User input processing
- Parsing/deserialization

**If YES, verify:**
- [ ] Each failure point has explicit handling OR propagates
- [ ] No bare `except:` or `except Exception: pass`
- [ ] Error messages actionable (what failed, why, how to fix)
- [ ] Partial failures handled (rollback, cleanup, consistent state)

**Red flag:** "Errors are rare" or "caller handles it" without checking caller

---

### 4. Resource Management

**Detect:** Does code acquire resources?
- File handles, sockets, connections
- Locks, semaphores
- Memory allocations (large buffers, caches)
- External service handles
- Background threads/processes

**If YES, verify:**
- [ ] Every acquire has corresponding release
- [ ] Release happens in finally/context manager/destructor
- [ ] Release happens on error paths too
- [ ] No resource leaks on repeated calls
- [ ] Bounded growth (caches have limits, queues have limits)

**Red flag:** "It cleans up eventually" or daemon threads without shutdown

---

### 5. Boundary Conditions

**Detect:** Does code handle variable-size input?
- Collections (lists, dicts, sets)
- Strings, byte arrays
- Numeric ranges
- Optional/nullable values

**If YES, verify:**
- [ ] Empty input: What happens with `[]`, `""`, `None`, `0`?
- [ ] Single item: Edge case often different from N items
- [ ] Maximum size: What if input is huge? Memory? Time?
- [ ] Invalid values: Negative numbers, NaN, special characters?
- [ ] Type boundaries: int overflow, float precision?

**Red flag:** "Nobody would pass that" or "that's an edge case"

---

### 6. Security (if applicable)

**Detect:** Does code handle untrusted input?
- User-provided data (forms, API requests)
- File contents from external sources
- URLs, paths, identifiers from users
- Data that becomes SQL, shell, HTML, or code

**If YES, verify:**
- [ ] Input validated before use
- [ ] No string concatenation for SQL/shell/HTML (use parameterized)
- [ ] Path traversal prevented (no `../` exploitation)
- [ ] Secrets not logged or exposed in errors
- [ ] Auth/authz checked before action, not after

**Red flag:** "It's internal only" (internals get exposed)

---

## Quick Checklist (Minimum)

Before "done", answer YES to all that apply:

| Dimension | Detection Trigger | Verified? |
|-----------|-------------------|-----------|
| Requirements | Requirements were stated | [ ] Each mapped to code |
| Concurrency | Shared state exists | [ ] All access protected |
| Errors | Operations can fail | [ ] All failures handled |
| Resources | Resources acquired | [ ] All released (incl. errors) |
| Boundaries | Variable-size input | [ ] Edge cases handled |
| Security | Untrusted input | [ ] Input validated |

---

## Anti-Rationalization Table

| Thought | Reality |
|---------|---------|
| "Design is good, so it works" | Design ≠ correctness. Check anyway. |
| "It's simple code" | Simple code has bugs too. Check anyway. |
| "I'll add error handling later" | Later = never. Check now. |
| "Edge cases are rare" | Edge cases cause production incidents. |
| "It's not user-facing" | Internal code gets exposed. Check anyway. |
| "Tests will catch it" | Tests check what you wrote, not what you missed. |

---

## Output Format

When verifying, output:

```
## Correctness Verification

### Requirements: [PASS/FAIL/N/A]
- Requirement 1 → implemented in X
- Requirement 2 → implemented in Y

### Concurrency: [PASS/FAIL/N/A]
- Shared state: [list]
- Protection: [how]

### Errors: [PASS/FAIL/N/A]
- Failure points: [list]
- Handling: [approach]

### Resources: [PASS/FAIL/N/A]
- Acquired: [list]
- Released: [how]

### Boundaries: [PASS/FAIL/N/A]
- Edge cases: [list]
- Handling: [approach]

### Security: [PASS/FAIL/N/A]
- Untrusted input: [list]
- Validation: [approach]

**Verdict:** [DONE / NOT DONE - list blockers]
```

---

## Relationship to Other Skills

| Skill | Focus | When |
|-------|-------|------|
| **aposd-designing-deep-modules** | Design quality | FIRST—during design |
| **aposd-maintaining-design-quality** | Design philosophy | During modification |
| **aposd-verifying-correctness** | Actual correctness | BEFORE "done" |
| **cc-quality-practices** | Testing/debugging | Throughout |

**Order:** Design → Implement → Verify (this skill) → Done


---

## Chain

| After | Next |
|-------|------|
| All dimensions pass | Done (pre-commit gate) |
