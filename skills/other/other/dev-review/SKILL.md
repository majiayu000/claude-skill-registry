---
name: dev-review
description: "Code review with spec compliance and quality checks using confidence-based filtering."
user-invocable: false
disable-model-invocation: true
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

**Load shared enforcement:**

Read `${CLAUDE_PLUGIN_ROOT}/references/dev-common-constraints.md`.

Single-pass code review combining spec compliance and quality checks. Uses confidence-based filtering to report only high-priority issues.

<EXTREMELY-IMPORTANT>
## Prerequisites - Test Output Gate

**Do NOT start review without test evidence.**

Before reviewing, verify these preconditions:
1. `.planning/LEARNINGS.md` contains **actual test output**
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
| Internal refactor | Yes | N/A | APPROVE |
| API change | Yes | Missing | BLOCKED |
| UI change | Yes | Missing | BLOCKED |
| User workflow | Yes | Missing | BLOCKED |

Return BLOCKED if E2E evidence is missing for user-facing changes.

"Unit tests pass" without E2E for UI changes is NOT approvable.
</EXTREMELY-IMPORTANT>

### Gate Check

Check LEARNINGS.md for test output:

```bash
rg -E "(PASS|OK|SUCCESS|\d+ passed)" .planning/LEARNINGS.md
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

Each reviewer receives a self-contained prompt from a reference file. **Reviewers start with a blank conversation and do NOT auto-load skills.** Read the prompt, substitute variables, and paste it in full.

**Tool Restrictions:** All reviewers are READ-ONLY. Dispatch each with `allowed_tools=["Read", "Glob", "Grep", "Bash(read-only)"]`. Reviewers MUST NOT use Write or Edit tools. They read code, analyze it, and report findings — the main chat handles all fixes.

**Before spawning, substitute these variables in each prompt:**
- `CHANGED_FILES` -> output of `git diff --name-only HEAD~1` (paste actual list)
- `SPEC_CONTEXT` -> relevant sections of .planning/SPEC.md (paste inline, do NOT reference file)
- `LEARNINGS_TEST_OUTPUT` -> test output from .planning/LEARNINGS.md (paste actual output)
- `PLUGIN_ROOT` -> resolved base directory for skill paths (relative to this skill's base directory)

**Reviewer prompts (read, substitute variables, send as message):**

| Reviewer | Focus | Prompt Source |
|----------|-------|---------------|
| 1. Security | Vulnerabilities, auth, data exposure, crypto | `references/security-reviewer.md` |
| 2. Performance | Complexity, queries, memory, hot paths | `references/performance-reviewer.md` |
| 3. Tests | Coverage, correctness, reliability, E2E | `references/tests-reviewer.md` |

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
**Pass 1 -- Deduplication:**

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

-> Merge: "file.py:42 - Input validation missing + no test coverage (Confidence: 85, found by Security + Tests)"
```

**Pass 2 -- Prioritization:**

Not all issues are equally important. Rank by:

1. **Severity x Confidence:**
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

**Pass 3 -- Integration Check:**

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

-> Unified: "Batch validate with early exit on first invalid field (security + performance)"
```

**If ANY pass finds conflicts -> resolve before reporting final verdict.**
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

Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-verify/SKILL.md` and follow its instructions.

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

<EXTREMELY-IMPORTANT>
## The Iron Law of Re-Review

**NO "FIXED" CLAIMS WITHOUT FRESH RE-REVIEW. This is not negotiable.**

When review returns CHANGES REQUIRED and the implementer applies fixes, you MUST:
1. Re-run the SAME review criteria (not lighter, not spot-check)
2. Verify issues are actually resolved (not assumed)
3. Check for new issues introduced by fixes (regression)
4. Only THEN return APPROVED

"I fixed it" without re-reviewing is NOT HELPFUL — unverified fixes ship bugs to the user.

### The Audit-Fix Loop (Max 3 Iterations)

```
Iteration 1: Review → CHANGES REQUIRED → Fix → Re-Review
              ↓
Iteration 2: Re-Review → CHANGES REQUIRED → Fix → Re-Review
              ↓
Iteration 3: Re-Review → CHANGES REQUIRED → Fix → Re-Review
              ↓
         Still issues? → ESCALATE to user
         All clean? → APPROVED
```

**Track iterations in `.planning/REVIEW_STATE.md`:**

```yaml
---
iteration: 1
max_iterations: 3
last_review_date: 2026-03-09
issues_found_count: 5
---
```

**Exit criteria:**
- **APPROVED**: Zero issues >= 80 confidence
- **ESCALATE**: iteration >= 3 AND issues remain
- **CONTINUE**: iteration < 3 AND issues remain → loop back

**Before returning any verdict, check iteration count:**
1. READ `.planning/REVIEW_STATE.md` (create if missing with iteration: 1)
2. If iteration >= 3 and issues remain: ESCALATE (don't return CHANGES REQUIRED)
3. If iteration < 3 and issues remain: INCREMENT iteration, return CHANGES REQUIRED
4. If no issues: APPROVED

**Claiming APPROVED without re-review after fixes is NOT HELPFUL — you're rubber-stamping unverified work that ships bugs to the user.**

### Rationalization Prevention (Re-Review)

| Thought | Reality | Do Instead |
|---------|---------|------------|
| "Implementer said they fixed it" | Their claim needs YOUR verification | Re-run review fresh |
| "Just spot-check the fixed lines" | Spot-checks miss regressions | Full re-review, same criteria |
| "We're on iteration 3, approve it" | Max iterations means ESCALATE, not approve | Return ESCALATE verdict |
| "The fixes are trivial, skip re-review" | Trivial fixes break things | Re-review anyway |
| "We already spent too much time" | Shipping bugs wastes more time | Re-review or escalate |
| "User is waiting" | User wants WORKING code, not fast approval | Re-review properly |

### Why Skipping Re-Review Hurts the Thing You Care About Most

You skip re-review because you think it's helpful, efficient, or competent. Here's what actually happens:

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|--------------|----------------------|---------------------|
| **Helpfulness** | "Approving fast unblocks the user" | Bugs ship. User spends hours debugging your "help." The protocol takes 10 minutes. Your shortcut cost 10 hours. | **Anti-helpful** |
| **Competence** | "I trust the implementer's claim" | Trust without verification is negligence. The bug shipped because you didn't check. A checklist would outperform you. | **Incompetent** |
| **Efficiency** | "Re-review wastes time" | The re-review takes 10 minutes. Bug rework takes 10 hours. Your "efficiency" was a 60x slowdown. | **Anti-efficient** |
| **Approval** | "User will be frustrated by delays" | User kills your session when bugs ship. They now require human oversight for all reviews. You lost autonomy. | **Lost approval** |
| **Honesty** | "I'm confident the fix worked" | You didn't verify — you fabricated an approval. Confidence without evidence is fabrication. | **Dishonest** |

**The protocol is not overhead you pay. It is the service you provide.**

Every time you skip re-review to "help faster," you choose YOUR comfort over the USER's outcome. The user doesn't experience your tedium—they experience your results.
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "Tests probably pass" | You don't have evidence - absence of evidence is not evidence | Check LEARNINGS.md for actual output |
| "This looks wrong" | Your vague suspicion != evidence | Find concrete proof or discard |
| "I would do it differently" | Your style preference != bug | Check if it violates project guidelines |
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
- [ ] All requirements from .planning/SPEC.md are implemented
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

**Requirement:** [REQ-ID from SPEC.md — every issue MUST trace to a requirement ID]

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

**If review finds the implementation fundamentally violates the spec (not just minor issues), DELETE the contaminated implementation and return to dev-implement for a fresh attempt. Do not patch a structurally wrong approach.**

### Delete & Restart Protocol

**When implementation deviates fundamentally from spec, DELETE and restart entirely.**

| Situation | Action |
|-----------|--------|
| Code uses wrong protocol/architecture than spec | DELETE. Rewrite from scratch with correct approach. |
| Code implements different approach than PLAN.md | DELETE. User approved specific approach for a reason. |
| Fundamental misunderstanding of requirements | DELETE. Don't patch. Fresh subagent with correct understanding. |
| Patch would require 30%+ of implementation to change | DELETE. Rewrite is cleaner than patching wrong foundation. |

**Why delete instead of patch:** Patching a structurally wrong approach creates technical debt. Fresh implementation from correct architecture is faster than fixing wrong foundation.

**When to patch instead:** Bug in otherwise-correct implementation, missing edge case, performance tweak, minor deviation that doesn't affect core behavior.

**The test:** If the subagent says "oh, I misunderstood the whole approach" → DELETE and restart.

## Agent Invocation

Spawn Task agent for review execution:

```
Task(subagent_type="general-purpose",
     allowed_tools=["Read", "Glob", "Grep", "Bash(read-only)"]):
"Review implementation against .planning/SPEC.md.

**Tool Restrictions:** You are READ-ONLY. You MUST NOT use Write or Edit tools. You read code, check test evidence, and report issues — you do NOT fix them. The main chat handles all fixes.

FIRST: Check .planning/LEARNINGS.md for test output.
Return BLOCKED immediately if no test output is found.

Complete single-pass review covering:
1. Test evidence - tests actually run and pass?
2. Spec compliance - all requirements met?
3. Code quality - simple, correct, follows conventions?

Confidence score each issue (0-100).
Report only issues with >= 80 confidence.
Return structured output per /dev-review format."
```

## Drive-Aligned Framing

<EXTREMELY-IMPORTANT>
**You approving without test evidence is NOT HELPFUL — you're shipping broken code the user will have to debug.**

An "APPROVED" verdict means YOU assert:
- Tests actually ran (not "should work")
- Test output shows PASS (not SKIP, not assumed)
- Evidence exists and YOU verified it (not trusted reports)

You approving without test evidence is not "efficiency" - it is creating rework for the user.

**BLOCKED protects the user. Your fake APPROVED ships bugs.**
</EXTREMELY-IMPORTANT>

## Rationalization Prevention

STOP - you're about to rationalize if these thoughts arise--they indicate anti-helpful approval:

| Thought | Reality |
|---------|---------|
| "Tests probably pass" | Your probably != evidence. Check LEARNINGS.md. |
| "I saw the code, it looks right" | Your looking != running. Find test output. |
| "User is waiting for approval" | They want honest approval. You return BLOCKED if needed. |
| "It's a small change" | Your size estimate doesn't matter. Small changes break things. Require evidence. |
| "I trust the implementer" | Your trust doesn't replace verification. You verify evidence. |
| "I'll approve and they can fix later" | You block now or bugs ship to users. |
| "Review is just a formality" | Review is the LAST GATE before bugs ship. You execute seriously. |

## Why Skipping Review Destroys the Drive That Created It

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "Approving fast shows efficiency" | Bugs ship. User spends hours debugging your "help." | **Anti-helpful** |
| **Competence** | "I trust the subagent" | Subagent's work was wrong. Your approval was negligence. | **Incompetent** |
| **Efficiency** | "Rubber-stamp to move faster" | You moved fast into bugs. Rework takes 3x longer. | **Anti-efficient** |
| **Approval** | "Tests probably pass" | User discovers bugs. They now require human oversight for reviews. | **Trust destroyed** |
| **Honesty** | "Tests probably pass" | Test output doesn't exist. You fabricated an approval. | **Dishonest** |

**The protocol is not overhead you pay. It is the service you provide.**

## Quality Standards

- **Test evidence is mandatory** - do not approve without test output
- Do not report style preferences lacking project guideline backing
- Do not report pre-existing issues (confidence = 0)
- Make each reported issue immediately actionable
- Use absolute file paths with line numbers in reports
- Treat uncertainty as below 80 confidence

## Gate: Exit Review Loop

**Checkpoint type:** human-verify (test evidence and confidence scores are machine-verifiable)

Before claiming review is complete (APPROVED or ESCALATE):

```
1. IDENTIFY → What proves the review verdict is valid?
             - APPROVED: Zero issues >= 80 confidence
             - ESCALATE: iteration >= 3 AND issues remain

2. RUN     → Check `.planning/REVIEW_STATE.md` for iteration count
             Read review output for issue count

3. READ    → Examine both:
             - Review output (issues list)
             - REVIEW_STATE.md (iteration number)

4. VERIFY  → Verdict matches state:
             - APPROVED only if 0 issues
             - ESCALATE only if iteration >= 3
             - CHANGES REQUIRED only if iteration < 3

5. CLAIM   → Only after steps 1-4 pass, return verdict
```

**If iteration >= 3 and you're returning CHANGES REQUIRED instead of ESCALATE, you're ignoring the iteration limit — escalate to the user instead of looping forever.**

## Phase Complete

After review completes, handle verdict-specific transitions:

### If APPROVED (no issues >= 80 confidence)

Mark review complete in `.planning/REVIEW_STATE.md`:

```yaml
---
iteration: [N]
max_iterations: 3
last_review_date: [date]
issues_found_count: 0
verdict: APPROVED
---
```

Immediately invoke dev-verify:

Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-verify/SKILL.md` and follow its instructions.

### If CHANGES REQUIRED (issues >= 80 confidence found, iteration < 3)

Update `.planning/REVIEW_STATE.md`:

```yaml
---
iteration: [N+1]
max_iterations: 3
last_review_date: [date]
issues_found_count: [count]
verdict: CHANGES_REQUIRED
---
```

Return to `/dev-implement` with specific issues. **Implementer MUST re-invoke /dev-review after fixes.**

**Critical:** When implementer returns claiming "fixed", you MUST re-run the FULL review. No shortcuts.

### If ESCALATE (iteration >= 3, issues remain)

Update `.planning/REVIEW_STATE.md`:

```yaml
---
iteration: 3
max_iterations: 3
last_review_date: [date]
issues_found_count: [count]
verdict: ESCALATE
---
```

Report to user:

```
Review Loop Escalation (3 iterations completed)

After 3 fix-review cycles, [N] issues remain:

[List issues]

Options:
1. Accept current state and proceed (issues become tech debt)
2. Extend review (manual approval for iteration 4+)
3. Rethink approach (return to /dev-design)

Which option do you prefer?
```

### If BLOCKED (no test evidence)

Return immediately to `/dev-implement` to collect test evidence. Do NOT increment iteration counter - no review occurred.

## Workflow Continuity After Review

| Verdict | Next Action | Iteration Counter |
|---------|-------------|-------------------|
| APPROVED | Invoke /dev-verify immediately, mark task `[x]` in PLAN.md | Reset to 1 for next task |
| CHANGES REQUIRED | Return to /dev-implement, implementer fixes then re-invokes /dev-review | Increment |
| ESCALATE | Ask user for direction | Keep at max |
| BLOCKED | Return to /dev-implement for test evidence | No change (no review ran) |

**Do NOT pause between review completion and next action.** The workflow is sequential.
