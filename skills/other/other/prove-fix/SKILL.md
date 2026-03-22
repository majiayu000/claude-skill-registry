---
name: prove-fix
version: 1.0.0
description: '[Code Quality] Prove fix correctness with code proof traces, confidence scoring, and stack-trace-style evidence chains. Use after /fix in bugfix workflows.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`
- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

## Quick Summary

**Goal:** Prove (or disprove) that each fix change is correct by building a code proof trace — like a debugger stack trace — with confidence percentages per change.

**Workflow:**

1. **Inventory** — List every code change made by the fix (file:line, before/after)
2. **Trace** — For each change, build a proof chain tracing from symptom → root cause → fix
3. **Score** — Assign confidence percentage per change with evidence
4. **Verify** — Cross-check fix against edge cases and side effects
5. **Verdict** — Overall fix confidence and any remaining risks

**Key Rules:**

- Every claim MUST have `file:line` evidence — no exceptions
- Each change gets its OWN proof trace and confidence score
- If ANY change scores below 80%, flag it and recommend additional investigation
- This step is **non-negotiable** after `/fix` — never skip it

### Frontend/UI Context (if applicable)

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Prove Fix

Post-fix verification skill that builds evidence-based proof chains for every code change. Think of it as a code debugger's stack trace, but for proving WHY a fix is correct.

---

## When to Use

- **After `/fix`** in bugfix, hotfix, or any fix workflow
- After applying code changes that fix a reported bug
- When you need to verify fix correctness before review/commit

## When NOT to Use

- Before the fix is applied (use `/debug` instead)
- For new feature verification (use `/test` instead)
- For code quality review (use `/code-review` instead)

---

## Step 1: Change Inventory

List ALL changes made by the fix. For each change, document:

```
CHANGE #N: [short description]
  File: [path/to/file.ext]
  Lines: [start-end]
  Before: [code snippet — the broken version]
  After:  [code snippet — the fixed version]
  Type:   [root-cause-fix | secondary-fix | defensive-fix | cleanup]
```

**Change types:**

- **root-cause-fix** — Directly addresses the root cause of the bug
- **secondary-fix** — Fixes a related issue discovered during investigation
- **defensive-fix** — Prevents the same class of bug from recurring
- **cleanup** — Removed dead code or simplified logic (no behavior change)

---

## Step 2: Proof Trace (per change)

For EACH change, build a **stack-trace-style proof chain**. This is the core of the skill.

### Proof Trace Format

```
PROOF TRACE — Change #N: [description]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYMPTOM (what the user sees):
  → [Observable behavior, e.g., "UI doesn't refresh after assigning PIC"]

TRIGGER PATH (how the symptom occurs):
  1. [file:line] User action → [method/event]
  2. [file:line] → calls [method]
  3. [file:line] → dispatches [action/event]
  4. [file:line] → handler/effect [name]
  5. [file:line] ← BUG HERE: [exact broken behavior]

ROOT CAUSE (proven):
  → [One sentence: what exactly is wrong and why]
  → Evidence: [file:line] shows [specific code proving the bug]

FIX MECHANISM (how the change fixes it):
  → [One sentence: what the fix does differently]
  → Before: [broken code path with file:line]
  → After:  [fixed code path with file:line]

WHY THIS FIX IS CORRECT:
  → [Reasoning backed by code evidence]
  → Pattern precedent: [file:line] shows same pattern working elsewhere
  → Framework behavior: [file:line or doc reference] confirms expected behavior

EDGE CASES CHECKED:
  → [edge case 1]: [verified/not-verified] — [evidence]
  → [edge case 2]: [verified/not-verified] — [evidence]

SIDE EFFECTS:
  → [None / List of potential side effects with evidence]

CONFIDENCE: [X%]
  Verified: [list of verified items]
  Not verified: [list of unverified items, if any]
```

### Proof Trace Rules

1. **Every arrow (→) MUST have a `file:line` reference** — no exceptions
2. **TRIGGER PATH must be traceable** — someone should be able to follow it step-by-step in the code
3. **Pattern precedent is REQUIRED** — find at least 1 working example of the same pattern elsewhere in the codebase
4. **Edge cases MUST be enumerated** — at minimum: error path, null/empty input, concurrent access
5. **Side effects MUST be assessed** — what else could this change affect?

---

## Step 3: Confidence Scoring

Each change gets an individual confidence score:

| Score       | Meaning                                                                     | Action Required                                    |
| ----------- | --------------------------------------------------------------------------- | -------------------------------------------------- |
| **95-100%** | Full proof trace complete, all edge cases verified, pattern precedent found | Ship it                                            |
| **80-94%**  | Main proof trace complete, some edge cases unverified                       | Ship with caveats noted                            |
| **60-79%**  | Proof trace partial, some links unverified                                  | Flag to user — recommend additional investigation  |
| **<60%**    | Insufficient evidence                                                       | **BLOCK** — do not proceed until evidence gathered |

### Scoring Criteria

Award points for each verified item:

| Criterion                                 | Points  | Evidence Required             |
| ----------------------------------------- | ------- | ----------------------------- |
| Root cause identified with file:line      | +25     | Code reference                |
| Fix mechanism explained with before/after | +20     | Code diff                     |
| Pattern precedent found in codebase       | +15     | Working example at file:line  |
| Framework behavior confirmed              | +10     | Framework source or docs      |
| Edge cases checked (per case)             | +5 each | Verification result           |
| Side effects assessed                     | +10     | Impact analysis               |
| No regressions identified                 | +5      | Test results or code analysis |

**Total possible: 100+** (normalize to percentage)

---

## Step 4: Cross-Verification

After individual proof traces, perform cross-change verification:

1. **Interaction check** — Do the changes interact with each other? Could one change break another?
2. **Completeness check** — Does the combined fix address ALL reported symptoms?
3. **Regression check** — Could the combined changes introduce new bugs?
4. **Dependency check** — Are there other code paths that depend on the changed behavior?
5. **Performance regression check** — Does the fix introduce performance issues?

> **[IMPORTANT] Database Performance Protocol (MANDATORY):**
>
> 1. **Paging Required** — ALL list/collection queries MUST use pagination. NEVER load all records into memory. Verify: no unbounded `GetAll()`, `ToList()`, or `Find()` without `Skip/Take` or cursor-based paging.
> 2. **Index Required** — ALL query filter fields, foreign keys, and sort columns MUST have database indexes configured. Verify: entity expressions match index field order, database collections have index management methods, migrations include indexes for WHERE/JOIN/ORDER BY columns.

---

## Step 5: Final Verdict

Produce a summary verdict:

```
FIX VERIFICATION VERDICT
━━━━━━━━━━━━━━━━━━━━━━━

Overall Confidence: [X%]

Changes Summary:
  #1: [description] — [X%] ✅/⚠️/❌
  #2: [description] — [X%] ✅/⚠️/❌
  #N: [description] — [X%] ✅/⚠️/❌

Symbols: ✅ ≥80% (ship) | ⚠️ 60-79% (flag) | ❌ <60% (block)

Remaining Risks:
  - [risk 1]: [likelihood] × [impact] — [mitigation]
  - [risk 2]: [likelihood] × [impact] — [mitigation]

Verification Method:
  - [Manual testing required? Which scenarios?]
  - [Automated tests cover this? Which tests?]
  - [Additional monitoring needed post-deploy?]

Recommendation: [SHIP / SHIP WITH CAVEATS / INVESTIGATE FURTHER / BLOCK]
```

---

## Example: Proof Trace for NgRx Effect Fix

```
PROOF TRACE — Change #1: Move catchError inside switchMap
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYMPTOM:
  → UI doesn't refresh after assigning PIC, Job Opening, or changing stage

TRIGGER PATH:
  1. candidate-quick-card-v2.component.ts:445 — User clicks "Assign PIC"
  2. candidate-card.container.component.ts:892 — onPersonInChargeChange($event)
  3. candidate-card.effect.ts:275 — SavePersonInCharge effect
  4. candidate-card.effect.ts:284 — dispatches LoadCandidateDetailsAction
  5. candidate-card.effect.ts:48 ← EFFECT IS DEAD — never processes the action

ROOT CAUSE:
  → catchError at outer pipe level (effect.ts:64) causes effect completion on ANY error
  → Evidence: effect.ts:43-69 shows catchError OUTSIDE switchMap
  → Evidence: ngrx-effects.js:156-165 confirms defaultEffectsErrorHandler
     only catches errors, not completions

FIX MECHANISM:
  → Move catchError INSIDE switchMap so errors are caught per-request
  → Before: effect.ts:64 — catchError at outer pipe → effect COMPLETES → DEAD
  → After:  effect.ts:52 — catchError inside switchMap → inner obs completes → outer SURVIVES

WHY THIS FIX IS CORRECT:
  → RxJS: catchError inside switchMap catches per-emission, outer stream continues
  → Pattern precedent: effect.ts:120 (moveApplicationToNextState) uses same inner pattern
  → Framework: NgRx effects auto-resubscribe on ERROR but NOT on COMPLETION

EDGE CASES:
  → 403 Forbidden: verified — returns SetCandidateDetails with isAllowDisplayed=false
  → Network timeout: verified — returns EMPTY, effect survives
  → Multiple rapid requests: verified — switchMap cancels previous (unchanged)

SIDE EFFECTS:
  → None — same error handling logic, only scope changed

CONFIDENCE: 95%
  Verified: root cause, fix mechanism, pattern precedent, framework source, all edge cases
  Not verified: behavior under specific proxy/auth middleware errors (very unlikely)
```

---

## Integration with Other Skills

This skill is the **mandatory verification gate** between `/fix` and `/code-simplifier` in fix workflows.

**Workflow position:**

```
... → /fix → /prove-fix → /code-simplifier → /review-changes → ...
```

**If proof trace reveals issues:**

- Score ≥80%: proceed to next step
- Score 60-79%: ask user whether to proceed or investigate further
- Score <60%: BLOCK — return to `/debug` or `/fix` step

---

<prove-context>$ARGUMENTS</prove-context>

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using TaskCreate
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `bugfix` workflow** (Recommended) — scout → investigate → debug → plan → fix → prove-fix → review → test
> 2. **Execute `/prove-fix` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/code-simplifier (Recommended)"** — Clean up fix implementation
- **"/review-changes"** — Review all changes before commit
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
