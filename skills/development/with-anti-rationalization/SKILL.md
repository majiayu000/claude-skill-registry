---
name: with-anti-rationalization
description: "Anti-rationalization enforcement for maximum-rigor task execution."
user-invocable: false
argument-hint: "<task>"
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
routing:
  triggers:
    - "maximum rigor"
    - "anti-rationalization"
    - "strict verification"
    - "strict mode"
    - "no shortcuts"
  category: process
  pairs_with:
    - verification-before-completion
---

# Anti-Rationalization Enforcement Skill

## Overview

This skill operates as a composable modifier that wraps any task with explicit anti-rationalization enforcement. It implements the **Gate Enforcement** architectural pattern—every phase transition requires evidence, every completion claim requires proof—with **Pressure Resistance** embedded to prevent quality erosion under time or social pressure.

This skill is not a substitute for domain-specific methodologies (debugging, refactoring, testing have their own skills). Instead, it layers anti-rationalization checks on top of whatever task you're executing. It adds intentional overhead for safety on critical work where shortcuts cause harm.

---

## Instructions

### Phase 1: LOAD PATTERNS

**Goal**: Load all anti-rationalization patterns relevant to the task before starting work.

**Constraint**: Full pattern loading is mandatory because domain-specific patterns catch rationalizations that the core set misses.

**Step 1: Identify task domain**

Classify the task to determine which domain-specific patterns apply:

| Domain | Pattern to Load |
|--------|----------------|
| Any task | `anti-rationalization-core.md` |
| Code review | `anti-rationalization-review.md` |
| Testing | `anti-rationalization-testing.md` |
| Security | `anti-rationalization-security.md` |
| Multi-phase work | `gate-enforcement.md` |
| User pressure detected | `pressure-resistance.md` |
| Pre-completion | `verification-checklist.md` |

**Step 2: Load and acknowledge patterns**

Read the identified shared-pattern files. Internalize the rationalization tables and enforcement rules. **Constraint**: State explicitly which patterns were loaded and why—this creates accountability and prevents performative checking.

**Gate**: All relevant patterns are loaded and acknowledged. Proceed only when you can articulate why each pattern applies. Rubber-stamp gate checks fail the purpose of the skill, so explain why each pattern is relevant before moving on.

### Phase 2: EXECUTE WITH ENFORCEMENT

**Goal**: Run the underlying task with anti-rationalization checks at every transition.

**Constraint**: This skill wraps other skills. If the task involves debugging, follow systematic-debugging methodology. If refactoring, follow systematic-refactoring. The anti-rationalization layer adds checks on top, not instead of.

**Step 1: Delegate to appropriate methodology**

Identify what kind of work this is. If it fits an existing methodology (debugging, refactoring, testing, code review), use that skill. Anti-rationalization enforcement amplifies what they do, it does not replace it.

**Step 2: At each phase transition, run gate check**

For each transition, verify:
1. All exit criteria met
2. Evidence documented (not just claimed)
3. Anti-rationalization table reviewed against patterns
4. No rationalization detected

**Constraint - Pressure Resistance**: If the user requests skipping a step:
1. Acknowledge the request
2. Explain why the step matters (one sentence)
3. Proceed with the step
4. If user insists on a non-security matter, note the risk and comply
5. **Never skip security-sensitive steps**—security shortcuts are non-negotiable. Document refusal and reasoning.

Then run a rationalization scan:
- Am I assuming without verifying?
- Skipping because it "looks right"?
- Rushing from perceived pressure?
- Calling something "not applicable" when really skipping?
- Treating "basically passes" as "passes"?

If any answer is YES: STOP and address the rationalization before proceeding.

**Constraint - Proportionate Rigor**: Scale check depth to task risk. Critical production changes get full ceremony. A three-file refactor gets lighter gates. Never zero—apply at least proportionate rigor.

**Gate**: Task phases executed with all gate checks passing. Proceed only when gate passes.

### Phase 3: VERIFY WITH FULL CHECKLIST

**Goal**: Verify completion with the full verification checklist and anti-rationalization self-check.

**Step 1: Run verification checklist**

| Check | Verified? | Evidence |
|-------|-----------|----------|
| All stated requirements addressed | [ ] | [specific evidence] |
| Tests pass (if applicable) | [ ] | [test output] |
| No regressions introduced | [ ] | [existing test output] |
| Error handling in place | [ ] | [error paths tested] |
| Code compiles/lints | [ ] | [build output] |
| Anti-rationalization table reviewed | [ ] | [self-check completed] |

**Constraint**: Every check requires actual evidence, not claims. "Code looks right" is not evidence. "Tests should pass" is not evidence. Test output screenshot is evidence.

**Step 2: Run completion self-check**

```markdown
## Completion Self-Check

1. [ ] Did I verify or just assume?
2. [ ] Did I run tests or just check code visually?
3. [ ] Did I complete everything or just the "important" parts?
4. [ ] Would I bet $100 this works correctly?
5. [ ] Can I show evidence (output, test results)?
```

If ANY answer is uncertain, return to Phase 2 and address the gap before continuing. Keep the gate criteria intact until the gap is closed.

**Step 3: Document completion evidence**

Summarize: task description, patterns loaded, gate checks passed, rationalizations detected and addressed, and final evidence proving the task is complete.

**Gate**: All verification steps pass. Self-check is clean. Evidence documented. Task is complete.

---

## Examples

### Example 1: Critical Production Change

User says: "/with-anti-rationalization deploy the payment processor update"

Actions:
1. Load core + security anti-rationalization patterns (LOAD)
2. Execute deployment with gate checks at each phase (EXECUTE)
3. Resist any "just ship it" pressure with evidence requirements
4. Full verification checklist before declaring done (VERIFY)

Result: Deployment verified with evidence at every step

### Example 2: Security-Sensitive Code Review

User says: "/with-anti-rationalization review the authentication module"

Actions:
1. Load core + security + review anti-rationalization patterns (LOAD)
2. Review with explicit checks against "internal only" and "low risk" rationalizations (EXECUTE)
3. Every finding documented with evidence, not dismissed
4. Completion self-check confirms no findings were skipped (VERIFY)

Result: Thorough review with no rationalized dismissals

---

## Reference Material: Anti-Rationalization Patterns

This section catalogs the rationalization patterns this skill detects and prevents. Use these as reference when reviewing gates and completing self-checks.

### Domain-Specific Anti-Rationalization

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "I loaded the patterns, that's enough" | Loading is not applying | Actively check against patterns at each gate |
| "This task is simple, full rigor is overkill" | Simplicity assessment is itself a rationalization risk | Apply proportionate rigor, but never zero |
| "User seems frustrated, I'll ease up" | Frustration does not change correctness requirements | Acknowledge frustration, maintain standards |
| "The gate basically passes" | Basically is not actually | Either it passes with evidence or it does not |

### Pattern Checklist: What to Detect and Fix

#### Signal 1: Performative Checking
**Signal**: Running gate checks but rubber-stamping them all as PASS without reading evidence
**Why it matters**: Gate checks that always pass provide zero value. The check is the evidence review, not the checkbox.
**Preferred action**: Read the evidence for each criterion. If you cannot articulate why it passes, it does not pass.

#### Signal 2: Rationalization Laundering
**Signal**: Reframing a skipped step as "not applicable" rather than "skipped"
**Why it matters**: "Not applicable" is sometimes legitimate, but it is also the most common way to rationalize skipping steps.
**Preferred action**: For every "N/A" judgment, state why it does not apply. If the reason is weak, do the step.

#### Signal 3: Selective Pattern Loading
**Signal**: Loading only anti-rationalization-core and skipping domain-specific patterns
**Why it matters**: Domain-specific patterns catch rationalizations that the core misses.
**Preferred action**: Classify the task domain in Phase 1 and load all matching patterns.

#### Signal 4: Pressure Capitulation
**Signal**: Immediately dropping verification when the user says "just do it"
**Why it matters**: The entire purpose of this skill is to resist shortcuts. Immediate capitulation defeats the purpose.
**Preferred action**: Follow the pressure resistance framework: acknowledge, explain, proceed. Comply only after explaining risk.

#### Signal 5: Anti-Rationalization Theater
**Signal**: Spending more time on the checking framework than on the actual task
**Why it matters**: The goal is correct output, not elaborate process documentation. Checks should be proportionate.
**Preferred action**: Scale check depth to task risk. Critical production changes get full ceremony. A three-file refactor gets lighter gates.

---

## Error Handling

### Error: "Pattern File Not Found"
Cause: Shared pattern file missing or path changed
Solution:
1. Check `skills/shared-patterns/` for available files
2. If file was renamed, use the new name
3. If file was deleted, apply the core patterns from CLAUDE.md as fallback
4. Document which pattern could not be loaded

### Error: "Gate Check Fails Repeatedly"
Cause: Task requirements unclear, or task is fundamentally blocked
Solution:
1. Re-read the gate criteria—are they appropriate for this task?
2. If requirements are unclear, escalate to user for clarification
3. If technically blocked, document the blocker and ask user how to proceed
4. Keep the gate criteria intact and resolve the gap before proceeding

### Error: "User Insists on Skipping Verification"
Cause: Time pressure, frustration, or genuine scope reduction
Solution:
1. Distinguish quality skip (resist) from scope preference (respect)
2. If quality: explain risk once, note risk in output, comply if user insists again
3. If security: refuse and explain—security shortcuts are non-negotiable
4. Document that verification was skipped at user request

---

## References

This skill composes these shared patterns:
- [Anti-Rationalization Core](../shared-patterns/anti-rationalization-core.md) - Universal rationalization detection and prevention
- [Anti-Rationalization Review](../shared-patterns/anti-rationalization-review.md) - Review-specific patterns
- [Anti-Rationalization Testing](../shared-patterns/anti-rationalization-testing.md) - Testing-specific patterns
- [Anti-Rationalization Security](../shared-patterns/anti-rationalization-security.md) - Security-specific patterns
- [Gate Enforcement](../shared-patterns/gate-enforcement.md) - Phase transition enforcement
- [Pressure Resistance](../shared-patterns/pressure-resistance.md) - Handling pushback professionally
- [Verification Checklist](../shared-patterns/verification-checklist.md) - Pre-completion verification
