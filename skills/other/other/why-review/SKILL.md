---
name: why-review
version: 1.0.0
description: '[Code Quality] Validate design rationale completeness in plan files before implementation'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

- `.claude/skills/shared/double-round-trip-review-protocol.md` — Mandatory two-round review enforcement

> **Critical Purpose:** Ensure quality — no flaws, no bugs, no missing updates, no stale content. Verify both code AND documentation.

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

> **OOP & DRY Enforcement:** MANDATORY IMPORTANT MUST — flag duplicated patterns that should be extracted to a base class, generic, or helper. Classes in the same group or suffix (ex *Entity, *Dto, \*Service, etc...) MUST inherit a common base (even if empty now — enables future shared logic and child overrides). Verify project has code linting/analyzer configured for the stack.

## Quick Summary

**Goal:** Validate that a plan contains sufficient design rationale (WHY, not just WHAT) before implementation begins.

**Applies to:** Features and refactors only — bugfixes and trivial changes exempt.

**Why this exists:** AI code generation optimizes mechanics but misses conceptual quality. This skill ensures the human thinking happened before the mechanical coding starts.

## Your Mission

<task>
$ARGUMENTS
</task>

## Review Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

- Do NOT accept plan rationale at face value — verify alternatives were genuinely considered
- Every pass/fail must include evidence (section reference, specific text quoted)
- If rationale is vague or hand-wavy, flag it — "we chose X" without WHY is a fail
- Question assumptions: "Is this really the best approach?" → check if alternatives have real trade-offs listed
- Challenge completeness: "Are all risks identified?" → think about what could go wrong that isn't mentioned
- No "looks fine" without proof — state what you verified and how

## Plan Resolution

1. If arguments contain a path → use that plan directory
2. Else check `## Plan Context` in injected context → use active plan path
3. If no plan found → tell user: "No active plan found. Run `/plan` or `/plan-hard` first."

## Validation Checklist

Read the plan's `plan.md` and all `phase-*.md` files. Check each item below. Report pass/fail for each.

### Required Sections (in plan.md or phase files)

| #   | Section                     | What to Check                                  | Pass Criteria                                     |
| --- | --------------------------- | ---------------------------------------------- | ------------------------------------------------- |
| 1   | **Problem Statement**       | Clearly states WHAT problem is being solved    | 2-3 sentences describing the problem              |
| 2   | **Alternatives Considered** | 2+ approaches with pros/cons                   | Minimum 2 alternatives with trade-offs            |
| 3   | **Design Rationale**        | Explains WHY chosen approach over alternatives | Explicit reasoning linking decision to trade-offs |
| 4   | **Risk Assessment**         | Risks identified with likelihood and impact    | At least 1 risk per phase                         |
| 5   | **Ownership**               | Clear who maintains code post-merge            | Implicit OK (author owns), explicit better        |

### Optional (Flag if Missing, Don't Fail)

| #   | Section                  | When Required                           |
| --- | ------------------------ | --------------------------------------- |
| 6   | **Operational Impact**   | Service-layer or API changes            |
| 7   | **Cross-Service Impact** | Changes touching multiple microservices |
| 8   | **Migration Strategy**   | Database schema or data changes         |

## Output Format

```markdown
## Why-Review Results

**Plan:** {plan path}
**Date:** {date}
**Verdict:** PASS / NEEDS WORK

### Checklist

| #   | Check                   | Status | Notes     |
| --- | ----------------------- | ------ | --------- |
| 1   | Problem Statement       | ✅/❌  | {details} |
| 2   | Alternatives Considered | ✅/❌  | {details} |
| 3   | Design Rationale        | ✅/❌  | {details} |
| 4   | Risk Assessment         | ✅/❌  | {details} |
| 5   | Ownership               | ✅/❌  | {details} |

### Missing Items (if any)

- {specific item to add before implementation}

### Recommendation

{Proceed to /cook | Add missing sections first}
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

## Scope

- **Applies to:** Features, refactors, architectural changes
- **Exempt:** Bugfixes, config changes, single-file tweaks, documentation-only
- **Enforcement:** Advisory (soft warning) — does not block implementation

## Important Notes

- Review only — do NOT modify plan files or implement changes
- Keep output concise — actionable in <2 minutes
- If plan is simple and clear, a short "PASS" is sufficient

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/cook (Recommended)"** — Begin implementation after design rationale is validated
- **"/code"** — If implementing a simpler change
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
