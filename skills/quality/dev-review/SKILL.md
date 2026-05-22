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
Skill(skill="workflows:dev-verify")
```

**If CHANGES REQUIRED:** Return to `/dev-implement` to fix reported issues.

**If BLOCKED:** Return to `/dev-implement` to collect test evidence.
