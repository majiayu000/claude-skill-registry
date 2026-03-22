---
name: plan-review
version: 1.0.0
description: '[Planning] Auto-review plan for validity, correctness, and best practices before implementation'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

- `.claude/skills/shared/double-round-trip-review-protocol.md` — Mandatory two-round review enforcement

> **Critical Purpose:** Ensure quality — no flaws, no bugs, no missing updates, no stale content. Verify both code AND documentation.

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

> **OOP & DRY Enforcement:** MANDATORY IMPORTANT MUST — flag duplicated patterns that should be extracted to a base class, generic, or helper. Classes in the same group or suffix (ex *Entity, *Dto, \*Service, etc...) MUST inherit a common base (even if empty now — enables future shared logic and child overrides). Verify project has code linting/analyzer configured for the stack.

## Quick Summary

**Goal:** Auto-review implementation plans for validity, correctness, and best practices before proceeding (AI self-review, not user interview).

**Workflow:**

1. **Resolve Plan** — Use $ARGUMENTS path or active plan from `## Plan Context`
2. **Read Files** — plan.md + all phase-\*.md files, extract requirements/steps/files/risks
3. **Evaluate Checklist** — Validity (summary, requirements, steps, files), Correctness (specific, paths, no conflicts), Best Practices (YAGNI/KISS/DRY, architecture), Completeness (risks, testing, success, security)
4. **Score & Classify** — PASS (all Required + ≥50% Recommended), WARN (all Required + <50% Recommended), FAIL (any Required fails)
5. **Output Result** — Status, checks passed, issues, recommendations, verdict

**Key Rules:**

- **PASS**: Proceed to implementation
- **WARN**: Proceed with caution, note gaps
- **FAIL**: STOP - must fix before proceeding, list specific issues
- **Constructive**: Focus on implementation-blocking issues, not pedantic details

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Your mission

Perform automatic self-review of an implementation plan to ensure it's valid, correct, follows best practices, and identify anything needing fixes before proceeding.

**Key distinction**: This is AI self-review (automatic), NOT user interview like `/plan-validate`.

## Plan Resolution

1. If `$ARGUMENTS` provided -> Use that path
2. Else check `## Plan Context` section -> Use active plan path
3. If no plan found -> Error: "No plan to review. Run /plan first."

## Workflow

### Step 1: Read Plan Files

Read the plan directory:

- `plan.md` - Overview, phases list, frontmatter
- `phase-*.md` - All phase files
- Extract: requirements, implementation steps, file listings, risks

### Step 2: Evaluate Against Checklist

#### Validity (Required - all must pass)

- [ ] Has executive summary (clear 1-2 sentence description)
- [ ] Has defined requirements section
- [ ] Has implementation steps (actionable tasks)
- [ ] Has files to create/modify listing

#### Correctness (Required - all must pass)

- [ ] Steps are specific and actionable (not vague)
- [ ] File paths follow project patterns
- [ ] No conflicting or duplicate steps
- [ ] Dependencies between steps are clear
- [ ] **New Tech/Lib Gate:** If plan introduces new packages/libraries/frameworks not in the project, verify alternatives were evaluated (top 3 compared) and user confirmed the choice. FAIL if new tech is added without evaluation.

#### Best Practices (Required - all must pass)

- [ ] YAGNI: No unnecessary features or over-engineering
- [ ] KISS: Simplest viable solution chosen
- [ ] DRY: No planned duplication of logic
- [ ] Architecture: Follows project patterns from `.claude/docs/`

#### Completeness (Recommended - ≥50% should pass)

- [ ] Risk assessment present with mitigations
- [ ] Testing strategy defined
- [ ] Success criteria per phase
- [ ] Security considerations addressed

### Step 3: Score and Classify

| Status   | Criteria                            | Action                            |
| -------- | ----------------------------------- | --------------------------------- |
| **PASS** | All Required pass, ≥50% Recommended | Proceed to implementation         |
| **WARN** | All Required pass, <50% Recommended | Proceed with caution, note gaps   |
| **FAIL** | Any Required check fails            | STOP - must fix before proceeding |

### Step 4: Output Result

```markdown
## Plan Review Result

**Status:** PASS | WARN | FAIL
**Reviewed:** {plan-path}
**Date:** {current-date}

### Summary

{1-2 sentence summary of plan quality}

### Checks Passed ({X}/{Y})

#### Required ({X}/{Y})

- ✅ Check 1
- ✅ Check 2
- ❌ Check 3 (if failed)

#### Recommended ({X}/{Y})

- ✅ Check 1
- ⚠️ Check 2 (missing)

### Issues Found

- ❌ FAIL: {critical issue requiring fix}
- ⚠️ WARN: {minor issue, can proceed}

### Recommendations

1. {specific fix 1}
2. {specific fix 2}

### Verdict

{PROCEED | REVISE_FIRST | BLOCKED}
```

## Round 2: Focused Re-Review (MANDATORY)

> **Protocol:** `.claude/skills/shared/double-round-trip-review-protocol.md`

After completing Round 1 checklist evaluation, execute a **second full review round**:

1. **Re-read** the Round 1 verdict and checklist results
2. **Re-evaluate** ALL checklist items — do NOT rely on Round 1 memory
3. **Challenge** Round 1 PASS items: "Is this really PASS? Did I verify with evidence?"
4. **Focus on** what Round 1 typically misses:
    - Implicit assumptions that weren't validated
    - Missing acceptance criteria coverage
    - Edge cases not addressed in the artifact
    - Cross-references that weren't verified
5. **Update verdict** if Round 2 found new issues
6. **Final verdict** must incorporate findings from BOTH rounds

## Next Steps

- **If PASS**: Announce "Plan review complete. Proceeding with next workflow step."
- **If WARN**: Announce "Plan review complete with warnings. Proceeding - consider addressing gaps."
- **If FAIL**: List specific issues. Do NOT proceed. Ask user to fix or regenerate plan.

## **IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
- **MANDATORY FINAL TASKS:** After creating all planning todo tasks, ALWAYS add these two final tasks:
    1. **Task: "Run /plan-validate"** — Trigger `/plan-validate` skill to interview the user with critical questions and validate plan assumptions
    2. **Task: "Run /plan-review"** — Trigger `/plan-review` skill to auto-review plan for validity, correctness, and best practices

## Important Notes

- Be constructive, not pedantic - focus on issues that would cause implementation problems
- WARN is acceptable for missing optional sections
- FAIL only for genuinely missing required content
- If plan is simple and valid, quick review is fine

---

## Skill Interconnection (MANDATORY — ask user)

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/plan-validate (Recommended)"** — Interview user to confirm plan assumptions
- **"/cook" or "/code"** — If plan is approved and ready for implementation
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
