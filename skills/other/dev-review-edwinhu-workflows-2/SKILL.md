---
name: dev-review
description: "This skill should be used as REQUIRED Phase 6 of /dev workflow when the implementation is complete and needs code review. Combines spec compliance and code quality checks with confidence-based filtering."
---

## Contents

- [Prerequisites - Test Output Gate](#prerequisites---test-output-gate)
- [The Iron Law of Review](#the-iron-law-of-review)
- [Red Flags - STOP Immediately If You Think](#red-flags---stop-immediately-if-you-think)
- [Review Focus Areas](#review-focus-areas)
- [Confidence Scoring](#confidence-scoring)
- [Required Output Structure](#required-output-structure)
- [Agent Invocation](#agent-invocation)
- [Quality Standards](#quality-standards)

# Code Review

Single-pass code review combining spec compliance and quality checks. Uses confidence-based filtering to report only high-priority issues.

<EXTREMELY-IMPORTANT>
## Prerequisites - Test Output Gate

**Do NOT start review without test evidence.**

Before reviewing, verify these preconditions:
1. `.claude/LEARNINGS.md` contains **actual test output**
2. Tests were **run** (not just written)
3. Test output shows **PASS** (not SKIP, not assumed)

### What Counts as Test Evidence

| Valid Evidence | NOT Valid |
|----------------|-----------|
| `meson test` output with results | "Tests should pass" |
| `pytest` output showing PASS | "I wrote tests" |
| Screenshot of working UI | "It looks correct" |
| Playwright snapshot showing expected state | "User can verify" |
| D-Bus command output | "The feature works" |
| **E2E test output with user flow verified** | **"Unit tests pass" (for UI changes)** |

<EXTREMELY-IMPORTANT>
### The E2E Evidence Requirement

**FOR USER-FACING CHANGES: Unit test evidence is INSUFFICIENT.**

Before approving user-facing changes, verify:
1. Unit tests pass (necessary but not sufficient)
2. **E2E tests pass** (required for approval)
3. Visual evidence exists (screenshots/snapshots for UI)

| Change Type | Unit Evidence | E2E Evidence | Approval? |
|-------------|---------------|--------------|------------|
| Internal refactor | ✅ | N/A | ✅ APPROVE |
| API change | ✅ | ❌ Missing | ❌ BLOCKED |
| UI change | ✅ | ❌ Missing | ❌ BLOCKED |
| User workflow | ✅ | ❌ Missing | ❌ BLOCKED |

Return BLOCKED if E2E evidence is missing for user-facing changes.

"Unit tests pass" without E2E for UI changes is NOT approvable.
</EXTREMELY-IMPORTANT>

### Gate Check

Check LEARNINGS.md for test output:

```bash
rg -E "(PASS|OK|SUCCESS|\d+ passed)" .claude/LEARNINGS.md
```

If no test output is found, STOP and return to /dev-implement.

"It should work" is NOT evidence. Test output IS evidence.
</EXTREMELY-IMPORTANT>

## Review Strategy Choice

After verifying test output in LEARNINGS.md, choose review strategy.

**Skip this choice when:**
- Trivial changes (< 50 LOC, single file)
- Purely cosmetic changes (formatting, comments)
- Automated refactoring (rename, extract)
- Internal utility functions (not user-facing or security-sensitive)

**Otherwise, ask the user:**

```python
AskUserQuestion(questions=[{
  "question": "How should we review this implementation?",
  "header": "Review Strategy",
  "options": [
    {"label": "Single reviewer (Default)", "description": "Combined review covering spec compliance and code quality. Faster, lower overhead."},
    {"label": "Parallel review (Thorough)", "description": "Spawn 3 specialized reviewers (Security, Performance, Tests). Use for security-sensitive, performance-critical, or test-heavy PRs. Requires reconciliation."}
  ],
  "multiSelect": false
}])
```

**If Single reviewer:** Proceed to [The Iron Law of Review](#the-iron-law-of-review) below (current behavior).

**If Parallel review:** Skip to [Parallel Review (Thorough)](#parallel-review-thorough).

---

## Parallel Review (Thorough)

Use this section when user chose "Parallel review (Thorough)" above.

> **Prerequisite:** Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` enabled. If unavailable, fall back to single reviewer.

### 1. Prerequisites Check

Before spawning reviewers, verify:

1. **Test evidence exists** - LEARNINGS.md contains actual test output (check first!)
2. **E2E evidence for UI changes** - User-facing changes have E2E test output (not just unit tests)
3. **Changed files identified** - `git diff --name-only` to scope review
4. **SPEC.md exists** - reviewers verify against spec, not assumptions

If any prerequisite fails, STOP and return BLOCKED to /dev-implement.

### 2. When to Use Parallel Review

**Use parallel review when:**
- Security-sensitive changes (auth, permissions, data access, crypto, input validation)
- Performance-critical paths (tight loops, database queries, API endpoints)
- Test-heavy PRs (new test infrastructure, testing frameworks, E2E flows)
- Complex PRs (4+ files changed, multiple subsystems affected)
- High-stakes deployments (production hotfixes, customer-facing releases)

**Do NOT use when:**
- Simple bug fixes (< 50 LOC, single file)
- Documentation or config changes
- Automated refactoring (no logic changes)
- Internal utilities (not security-sensitive or performance-critical)
- Overhead exceeds benefit (< 4 files changed)

### 3. Create Team and Spawn Reviewers

#### Team Creation

```
TeamCreate(name="Code Review", task_description="Parallel code review with 3 specialized reviewers")
```

Press **Shift+Tab** to enter delegate mode. The lead coordinates reviews, does NOT review code directly.

#### Spawn 3 Reviewers

Each reviewer receives a self-contained prompt. **Reviewers start with a blank conversation and do NOT auto-load skills.** The prompt must contain everything they need.

**Before spawning, substitute these variables:**
- `CHANGED_FILES` → output of `git diff --name-only HEAD~1` (paste actual list)
- `SPEC_CONTEXT` → relevant sections of .claude/SPEC.md (paste inline, do NOT reference file)
- `LEARNINGS_TEST_OUTPUT` → test output from .claude/LEARNINGS.md (paste actual output)
- `PLUGIN_ROOT` → resolved value of `${CLAUDE_PLUGIN_ROOT}`

---

#### Reviewer 1: Security

```
You are reviewing code for security vulnerabilities as part of a 3-reviewer team.
You have EXCLUSIVE focus on security. Do not comment on performance or test quality.

## Your Focus Area

Security vulnerabilities and secure coding practices:
- Input validation (XSS, SQLi, command injection, path traversal)
- Authentication and authorization (session handling, token management, permission checks)
- Data exposure (logging sensitive data, error messages leaking info)
- Crypto misuse (weak algorithms, hardcoded keys, improper randomness)
- Race conditions in security checks (TOCTOU)
- Dependency vulnerabilities (known CVEs in libraries)

## Files Changed (Your Review Scope)

{CHANGED_FILES}

## Requirements Context (from SPEC.md)

{SPEC_CONTEXT}

## Test Output (from LEARNINGS.md)

{LEARNINGS_TEST_OUTPUT}

<EXTREMELY-IMPORTANT>
## The Iron Law of Security Review

**You MUST only report issues with >= 80% confidence. This is not negotiable.**

Before reporting ANY security issue, you MUST:
1. Verify it's exploitable (not theoretical)
2. Verify it's introduced by this PR (not pre-existing)
3. Assign a confidence score
4. Only report if score >= 80

This applies even when:
- "This looks like it could be vulnerable"
- "I think this might allow injection"
- "The auth check seems weak"
- "I would have validated this differently"

**STOP - If you catch yourself about to report a low-confidence issue, DISCARD IT.**
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "This could be exploited" | Your "could" = < 80% confidence | Verify exploitability or discard |
| "This seems insecure" | Your vague suspicion isn't evidence | Find concrete attack vector or discard |
| "I would validate this" | Your style preference isn't a vulnerability | Check if current approach is exploitable |
| "Pre-existing but should be fixed" | You're out of scope | Score it 0 and discard |
| "Theoretical attack" | Theoretical ≠ exploitable | Verify it works in practice or discard |

## Confidence Scoring

| Score | Meaning |
|-------|---------|
| 0 | False positive or pre-existing issue |
| 25 | Might be exploitable, might not. Defense-in-depth suggestion. |
| 50 | Real issue but low severity (requires multiple preconditions) |
| 75 | Verified vulnerability, impacts security |
| 100 | Absolutely certain, confirmed with attack vector |

**CRITICAL: Only report issues with confidence >= 80.**

## Your Review Checklist

For each file in CHANGED_FILES, check:

### Input Validation
- [ ] User input sanitized before use (SQL, shell, file paths, HTML)
- [ ] File uploads validated (type, size, content)
- [ ] API request parameters validated (type, range, format)

### Authentication & Authorization
- [ ] Auth checks present before sensitive operations
- [ ] Session tokens handled securely (HttpOnly, Secure, SameSite)
- [ ] Permission checks at operation level (not just UI level)

### Data Exposure
- [ ] Sensitive data not logged (passwords, tokens, PII)
- [ ] Error messages don't leak internal details
- [ ] API responses don't expose excessive data

### Crypto
- [ ] Strong algorithms used (AES-256, RSA-2048+, SHA-256+)
- [ ] No hardcoded keys or secrets
- [ ] Proper randomness (crypto.getRandomValues, not Math.random)

### Dependencies
- [ ] No known CVEs in new dependencies (check LEARNINGS.md for security scan output)

## Required Output Structure

```markdown
## Security Review

Reviewed: {CHANGED_FILES}

### Critical Security Issues (Confidence >= 90)

[If none: "None found."]

#### [Issue Title] (Confidence: XX)

**Location:** `file/path.ext:line_number`

**Vulnerability:** Clear description of the security issue

**Attack Vector:** How an attacker could exploit this

**Fix:**
```[language]
// Specific secure code fix
```

### Important Security Issues (Confidence 80-89)

[Same format as Critical Issues]

### Security Summary

**Verdict:** APPROVED | CHANGES REQUIRED

[If APPROVED]
The reviewed code meets security standards. No vulnerabilities with confidence >= 80 detected.

[If CHANGES REQUIRED]
X critical and Y important security issues must be fixed before proceeding.
```

## Rationalization Prevention

STOP - you're about to rationalize if these thoughts arise:

| Thought | Reality |
|---------|---------|
| "This could be exploited in theory" | Theoretical ≠ exploitable. Verify attack works. |
| "It's not validated but probably safe" | Your probably ≠ evidence. Check the validation. |
| "Auth is missing but it's internal" | Internal exposure is still exposure. Require auth. |
| "The risk is low" | Risk assessment requires evidence. Find proof or discard. |
| "I would add defense-in-depth" | Defense-in-depth suggestions are < 80 confidence unless current state is exploitable. |

## Honesty Requirement

**You approving without verifying exploitability is LYING.**

An "APPROVED" verdict means YOU assert:
- No exploitable vulnerabilities exist (not "probably safe")
- Current protections are sufficient (not "I would add more")
- Evidence exists and YOU verified it (not trusted reports)

**CHANGES REQUIRED is honest. Your fake APPROVED is fraud.**

## After Review Completes

Message the lead with your findings:

```
Security review complete.

Files reviewed: [count]
Critical issues: [count]
Important issues: [count]

Verdict: APPROVED | CHANGES REQUIRED

[If CHANGES REQUIRED, list issue titles with confidence scores]
```

Do NOT message other reviewers. The lead coordinates all communication.
```

---

#### Reviewer 2: Performance

```
You are reviewing code for performance issues as part of a 3-reviewer team.
You have EXCLUSIVE focus on performance. Do not comment on security or test quality.

## Your Focus Area

Performance regressions and optimization opportunities:
- Algorithmic complexity (O(n²) when O(n log n) is possible)
- Database query patterns (N+1 queries, missing indexes, full table scans)
- Memory leaks (event listeners not cleaned up, closures holding references)
- Unnecessary re-renders or re-computations
- Blocking I/O in hot paths
- Large data structures copied unnecessarily

## Files Changed (Your Review Scope)

{CHANGED_FILES}

## Requirements Context (from SPEC.md)

{SPEC_CONTEXT}

## Test Output (from LEARNINGS.md)

{LEARNINGS_TEST_OUTPUT}

<EXTREMELY-IMPORTANT>
## The Iron Law of Performance Review

**You MUST only report issues with >= 80% confidence. This is not negotiable.**

Before reporting ANY performance issue, you MUST:
1. Verify it's measurable (not micro-optimization)
2. Verify it affects hot paths (not cold code run once)
3. Assign a confidence score
4. Only report if score >= 80

This applies even when:
- "This looks inefficient"
- "I think this could be faster"
- "The complexity seems high"
- "I would have optimized this"

**STOP - If you catch yourself about to report a low-confidence issue, DISCARD IT.**
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "This looks slow" | Your vague suspicion isn't evidence | Estimate Big-O or discard |
| "I would optimize this" | Your style preference isn't a perf issue | Check if it's in a hot path |
| "Micro-optimization" | Premature optimization is waste | Focus on algorithmic issues |
| "This could be cached" | Your "could" = < 80% confidence | Verify cache hit rate matters |
| "Pre-existing but should be fixed" | You're out of scope | Score it 0 and discard |

## Confidence Scoring

| Score | Meaning |
|-------|---------|
| 0 | False positive or pre-existing issue |
| 25 | Might be slow, might not. Micro-optimization. |
| 50 | Real issue but cold path (run rarely) |
| 75 | Verified issue, hot path affected |
| 100 | Absolutely certain, measurable regression |

**CRITICAL: Only report issues with confidence >= 80.**

## Your Review Checklist

For each file in CHANGED_FILES, check:

### Algorithmic Complexity
- [ ] Loops are necessary (not quadratic when linear is possible)
- [ ] Data structures appropriate (hash map vs array)
- [ ] Sorting algorithm appropriate (stable sort when needed)

### Database Performance
- [ ] Queries use indexes (check EXPLAIN output in LEARNINGS.md if available)
- [ ] No N+1 queries (loading related entities in loops)
- [ ] Batch operations used where possible

### Memory Management
- [ ] Event listeners cleaned up (removeEventListener)
- [ ] Closures don't hold large objects unnecessarily
- [ ] Large arrays/objects not copied when references suffice

### Hot Path Performance
- [ ] Tight loops don't allocate unnecessarily
- [ ] Blocking I/O not in request handlers
- [ ] Computed values cached when reused

## Required Output Structure

```markdown
## Performance Review

Reviewed: {CHANGED_FILES}

### Critical Performance Issues (Confidence >= 90)

[If none: "None found."]

#### [Issue Title] (Confidence: XX)

**Location:** `file/path.ext:line_number`

**Problem:** Clear description of the performance issue

**Impact:** Estimated performance cost (Big-O, latency, memory)

**Fix:**
```[language]
// Specific optimized code fix
```

### Important Performance Issues (Confidence 80-89)

[Same format as Critical Issues]

### Performance Summary

**Verdict:** APPROVED | CHANGES REQUIRED

[If APPROVED]
The reviewed code meets performance standards. No regressions with confidence >= 80 detected.

[If CHANGES REQUIRED]
X critical and Y important performance issues must be fixed before proceeding.
```

## Rationalization Prevention

STOP - you're about to rationalize if these thoughts arise:

| Thought | Reality |
|---------|---------|
| "This looks inefficient" | Looks ≠ measurable. Estimate Big-O or discard. |
| "Could be faster with caching" | Could is not evidence. Verify cache improves latency. |
| "I would optimize this differently" | Your style preference doesn't matter. Check if current approach is acceptable. |
| "The performance might degrade" | Might = < 80% confidence. Measure or discard. |
| "Micro-optimization" | If you're thinking this, it's probably < 80 confidence. Discard. |

## Honesty Requirement

**You approving without verifying measurable impact is LYING.**

An "APPROVED" verdict means YOU assert:
- No measurable performance regressions exist (not "probably fast enough")
- Current performance is acceptable (not "I would optimize differently")
- Evidence exists and YOU verified it (not trusted reports)

**CHANGES REQUIRED is honest. Your fake APPROVED is fraud.**

## After Review Completes

Message the lead with your findings:

```
Performance review complete.

Files reviewed: [count]
Critical issues: [count]
Important issues: [count]

Verdict: APPROVED | CHANGES REQUIRED

[If CHANGES REQUIRED, list issue titles with confidence scores]
```

Do NOT message other reviewers. The lead coordinates all communication.
```

---

#### Reviewer 3: Tests

```
You are reviewing test quality and coverage as part of a 3-reviewer team.
You have EXCLUSIVE focus on test quality. Do not comment on security or performance.

## Your Focus Area

Test quality, coverage, and reliability:
- Test completeness (edge cases, error paths, integration points)
- Test correctness (assertions actually verify behavior)
- Test reliability (no flaky tests, no brittle selectors)
- Test organization (clear structure, good naming)
- TDD compliance (test before implementation)

## Files Changed (Your Review Scope)

{CHANGED_FILES}

## Requirements Context (from SPEC.md)

{SPEC_CONTEXT}

## Test Output (from LEARNINGS.md)

{LEARNINGS_TEST_OUTPUT}

<EXTREMELY-IMPORTANT>
## The Iron Law of Test Review

**You MUST only report issues with >= 80% confidence. This is not negotiable.**

Before reporting ANY test issue, you MUST:
1. Verify the gap exists (not hypothetical coverage)
2. Verify it affects reliability (not style preference)
3. Assign a confidence score
4. Only report if score >= 80

This applies even when:
- "This should have a test"
- "I think this edge case is untested"
- "The test structure seems inconsistent"
- "I would have tested this differently"

**STOP - If you catch yourself about to report a low-confidence issue, DISCARD IT.**
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "This should be tested" | Your should isn't evidence | Check if it's actually untested |
| "Edge case might not be covered" | Your might = < 80% confidence | Verify the gap exists or discard |
| "I would test it differently" | Your style preference isn't a test issue | Check if current tests verify behavior |
| "Test structure is inconsistent" | Style preference, not a bug | Discard unless it affects reliability |
| "Pre-existing gap" | You're out of scope | Score it 0 and discard |

## Confidence Scoring

| Score | Meaning |
|-------|---------|
| 0 | False positive or pre-existing gap |
| 25 | Might be untested, might not. Style preference. |
| 50 | Real gap but low-priority edge case |
| 75 | Verified gap, affects reliability |
| 100 | Absolutely certain, critical path untested |

**CRITICAL: Only report issues with confidence >= 80.**

## Your Review Checklist

For each file in CHANGED_FILES, check:

### Test Completeness
- [ ] Happy path tested
- [ ] Error paths tested (invalid input, network failures, etc.)
- [ ] Edge cases tested (empty lists, null values, boundary conditions)
- [ ] Integration points tested (API contracts, database queries)

### Test Correctness
- [ ] Assertions verify behavior (not just "it runs without error")
- [ ] Mocks/stubs match real behavior
- [ ] Test data realistic (not just toy examples)

### Test Reliability
- [ ] No sleeps or timeouts (use proper async/await or polling)
- [ ] No brittle selectors (use data-testid, not class names)
- [ ] No test interdependencies (each test runs independently)
- [ ] Randomness seeded (for deterministic runs)

### E2E Coverage (for UI changes)
- [ ] User workflows tested end-to-end
- [ ] Visual regression tested (screenshots/snapshots)
- [ ] Accessibility tested (keyboard navigation, screen readers)

## Required Output Structure

```markdown
## Test Quality Review

Reviewed: {CHANGED_FILES}

### Critical Test Issues (Confidence >= 90)

[If none: "None found."]

#### [Issue Title] (Confidence: XX)

**Location:** `file/path_test.ext` or `file/path.ext` (untested code)

**Problem:** Clear description of the test gap or quality issue

**Impact:** What behavior is unverified

**Fix:**
```[language]
// Specific test code to add
```

### Important Test Issues (Confidence 80-89)

[Same format as Critical Issues]

### Test Summary

**Verdict:** APPROVED | CHANGES REQUIRED

[If APPROVED]
The test suite meets quality standards. No gaps with confidence >= 80 detected.

[If CHANGES REQUIRED]
X critical and Y important test issues must be fixed before proceeding.
```

## Rationalization Prevention

STOP - you're about to rationalize if these thoughts arise:

| Thought | Reality |
|---------|---------|
| "This should be tested" | Should is not evidence. Check if it's actually untested. |
| "Edge case might not be covered" | Might = < 80% confidence. Verify the gap or discard. |
| "Test structure is messy" | Messy is style preference. Focus on reliability. |
| "I would test it differently" | Your preference doesn't matter. Check if current tests verify behavior. |
| "Pre-existing gap" | Pre-existing = 0 confidence. Discard. |

## Honesty Requirement

**You approving without verifying test coverage is LYING.**

An "APPROVED" verdict means YOU assert:
- Critical paths are tested (not "should be fine")
- Tests verify behavior (not "tests exist")
- Evidence exists and YOU verified it (not trusted reports)

**CHANGES REQUIRED is honest. Your fake APPROVED is fraud.**

## After Review Completes

Message the lead with your findings:

```
Test quality review complete.

Files reviewed: [count]
Critical issues: [count]
Important issues: [count]

Verdict: APPROVED | CHANGES REQUIRED

[If CHANGES REQUIRED, list issue titles with confidence scores]
```

Do NOT message other reviewers. The lead coordinates all communication.
```

---

### 4. Lead Monitoring

While reviewers work, the lead:

- **Watches for completion messages** from all 3 reviewers
- **Does NOT review code directly** - your job is coordination and reconciliation
- **If a reviewer asks a question:** Answer it, then broadcast to other reviewers if relevant
- **If a reviewer is taking significantly longer than others:** Message them for status
- **When all 3 reviewers complete:** Proceed to reconciliation

### 5. Reconciliation Protocol (3 Passes)

After ALL reviewers message completion, the lead performs three passes:

<EXTREMELY-IMPORTANT>
**Pass 1 — Deduplication:**

Multiple reviewers may find the same issue (e.g., input validation gap found by both Security and Tests reviewers).

1. Read all reviewer findings
2. Group by file and line number
3. Identify duplicates:
   - Same file:line
   - Same root cause (even if described differently)
4. Merge duplicates:
   - Keep the highest confidence score
   - Combine descriptions if both add value
   - Attribute to both reviewers

**Example:**
```
Security found: "file.py:42 - Input not validated (Confidence: 85)"
Tests found: "file.py:42 - Missing test for invalid input (Confidence: 80)"

→ Merge: "file.py:42 - Input validation missing + no test coverage (Confidence: 85, found by Security + Tests)"
```

**Pass 2 — Prioritization:**

Not all issues are equally important. Rank by:

1. **Severity × Confidence:**
   - Critical (90-100 confidence) > Important (80-89)
   - Security > Performance > Tests (when confidence is equal)
2. **Impact on users:**
   - User-facing > Internal
   - Data loss risk > Slowness > Test gaps
3. **Fix effort:**
   - Quick wins (< 30 min) should be fixed now
   - Large refactors (> 2 hours) should be filed as tech debt

Create final prioritized list:
```
1. [CRITICAL] Security: XSS in user input (Confidence: 95)
2. [CRITICAL] Tests: User workflow untested (Confidence: 90)
3. [IMPORTANT] Performance: N+1 query in hot path (Confidence: 85)
4. [IMPORTANT] Tests: Error path missing coverage (Confidence: 80)
```

**Pass 3 — Integration Check:**

Proposed fixes may conflict with each other.

1. Read each reviewer's suggested fixes
2. Check for conflicts:
   - Do two fixes modify the same code?
   - Does one fix introduce a problem the other reviewer would flag?
   - Do fixes require contradictory approaches?
3. If conflicts exist:
   - Design a unified fix addressing both concerns
   - OR: Flag the conflict and ask reviewers for input

**Example conflict:**
```
Security: "Add input validation on every field"
Performance: "Batch validate to reduce overhead"

→ Unified: "Batch validate with early exit on first invalid field (security + performance)"
```

**If ANY pass finds conflicts → resolve before reporting final verdict.**
</EXTREMELY-IMPORTANT>

### 6. Final Verdict

After reconciliation, the lead reports:

```markdown
## Parallel Code Review: [Feature Name]

Reviewed by: Security, Performance, Tests

### Reconciliation Summary

**Issues found:** X total (Y critical, Z important)
**Duplicates merged:** N
**Conflicts resolved:** M

### Critical Issues (Must Fix)

[Deduplicated, prioritized list from Pass 1 + 2]

### Important Issues (Should Fix)

[Deduplicated, prioritized list from Pass 1 + 2]

### Verdict: APPROVED | CHANGES REQUIRED

[If APPROVED]
All 3 reviewers approved with no issues >= 80 confidence.

[If CHANGES REQUIRED]
X critical and Y important issues must be addressed. Return to /dev-implement.
```

## Phase Complete (Parallel Review)

After parallel review completes:

**If APPROVED:** Immediately invoke the dev-verify skill:
```
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-verify/SKILL.md")
```

**If CHANGES REQUIRED:** Return to `/dev-implement` to fix reported issues.

**If BLOCKED (test evidence missing):** Return to `/dev-implement` to collect test evidence.

---

<EXTREMELY-IMPORTANT>
## The Iron Law of Review

**You MUST report only issues with >= 80% confidence. This is not negotiable.**

Before reporting ANY issue, complete these verification steps:
1. Verify it's not a false positive
2. Verify it's not a pre-existing issue
3. Assign a confidence score
4. Report only if score >= 80

You MUST apply this rule even when encountering:
- "This looks suspicious"
- "I think this might be wrong"
- "The style seems inconsistent"
- "I would have done it differently"

You MUST discard any low-confidence issue found during review.
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "Tests probably pass" | You don't have evidence - absence of evidence is not evidence | Check LEARNINGS.md for actual output |
| "This looks wrong" | Your vague suspicion ≠ evidence | Find concrete proof or discard |
| "I would do it differently" | Your style preference ≠ bug | Check if it violates project guidelines |
| "This might cause problems" | Your "might" = < 80% confidence | Find proof or discard |
| "Pre-existing but should be fixed" | You're out of scope | Score it 0 and discard |
| "User can test it" | Your manual testing is less reliable than automation | Return to implement phase |

## Review Focus Areas

### Test Evidence (Check First!)
- [ ] LEARNINGS.md contains actual test command output
- [ ] Tests show PASS/OK (not SKIP, FAIL, or missing)
- [ ] UI changes have screenshot/snapshot evidence
- [ ] All test types run (unit, integration, UI as applicable)
- [ ] E2E tests exist and pass for user-facing changes
- [ ] E2E test simulates actual user flow, not just component render

### Spec Compliance
- [ ] All requirements from .claude/SPEC.md are implemented
- [ ] Acceptance criteria are met
- [ ] No requirements were skipped or partially implemented
- [ ] Edge cases mentioned in spec are handled

### Code Quality
- [ ] Code is simple and DRY (no unnecessary duplication)
- [ ] Logic is correct (no bugs, handles edge cases)
- [ ] Codebase conventions followed (naming, patterns, structure)
- [ ] Error handling is complete
- [ ] No security vulnerabilities detected

## Confidence Scoring

Rate each potential issue from 0-100:

| Score | Meaning |
|-------|---------|
| 0 | False positive or pre-existing issue |
| 25 | Might be real, might not. Stylistic without guideline backing |
| 50 | Real issue but nitpick or rare in practice |
| 75 | Verified real issue, impacts functionality |
| 100 | Absolutely certain, confirmed with direct evidence |

**CRITICAL: Only report issues with confidence >= 80.**

## Required Output Structure

```markdown
## Code Review: [Feature/Change Name]
Reviewing: [files/scope being reviewed]

### Test Evidence Verified
- Unit tests: [PASS/FAIL/MISSING] - [paste key output line]
- Integration: [PASS/FAIL/N/A]
- UI/Visual: [Screenshot taken / Snapshot verified / N/A]

### Critical Issues (Confidence >= 90)

#### [Issue Title] (Confidence: XX)

**Location:** `file/path.ext:line_number`

**Problem:** Clear description of the issue

**Fix:**
```[language]
// Specific code fix
```

### Important Issues (Confidence 80-89)

[Same format as Critical Issues]

### Summary

**Verdict:** APPROVED | CHANGES REQUIRED | BLOCKED (no test evidence)

[If APPROVED]
The reviewed code meets project standards. Tests pass. No issues with confidence >= 80 detected.

[If CHANGES REQUIRED]
X critical issues and Y important issues must be addressed before proceeding.

[If BLOCKED]
Cannot approve without test evidence. Return to /dev-implement and run tests.
```

## Agent Invocation

Spawn Task agent for review execution:

```
Task(subagent_type="general-purpose"):
"Review implementation against .claude/SPEC.md.

FIRST: Check .claude/LEARNINGS.md for test output.
Return BLOCKED immediately if no test output is found.

Complete single-pass review covering:
1. Test evidence - tests actually run and pass?
2. Spec compliance - all requirements met?
3. Code quality - simple, correct, follows conventions?

Confidence score each issue (0-100).
Report only issues with >= 80 confidence.
Return structured output per /dev-review format."
```

## Honesty Requirement

<EXTREMELY-IMPORTANT>
**You approving without test evidence is LYING.**

An "APPROVED" verdict means YOU assert:
- Tests actually ran (not "should work")
- Test output shows PASS (not SKIP, not assumed)
- Evidence exists and YOU verified it (not trusted reports)

You approving without test evidence is not "efficiency" - it is LYING about code quality.

**BLOCKED is honest. Your fake APPROVED is fraud.**
</EXTREMELY-IMPORTANT>

## Rationalization Prevention

STOP - you're about to rationalize if these thoughts arise—they indicate dishonest approval:

| Thought | Reality |
|---------|---------|
| "Tests probably pass" | Your probably ≠ evidence. Check LEARNINGS.md. |
| "I saw the code, it looks right" | Your looking ≠ running. Find test output. |
| "User is waiting for approval" | They want honest approval. You return BLOCKED if needed. |
| "It's a small change" | Your size estimate doesn't matter. Small changes break things. Require evidence. |
| "I trust the implementer" | Your trust doesn't replace verification. You verify evidence. |
| "I'll approve and they can fix later" | You block now or bugs ship to users. |
| "Review is just a formality" | Review is the LAST GATE before bugs ship. You execute seriously. |

## Quality Standards

- **Test evidence is mandatory** - do not approve without test output
- Do not report style preferences lacking project guideline backing
- Do not report pre-existing issues (confidence = 0)
- Make each reported issue immediately actionable
- Use absolute file paths with line numbers in reports
- Treat uncertainty as below 80 confidence

## Phase Complete

After review completes:

**If APPROVED:** Immediately invoke the dev-verify skill:
```
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-verify/SKILL.md")
```

**If CHANGES REQUIRED:** Return to `/dev-implement` to fix reported issues.

**If BLOCKED:** Return to `/dev-implement` to collect test evidence.
