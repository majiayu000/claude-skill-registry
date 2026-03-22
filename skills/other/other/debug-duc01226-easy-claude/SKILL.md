---
name: debug
version: 1.0.0
description: "[Fix & Debug] Systematic debugging with root cause investigation. Use when bugfix workflow reaches debug step."
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` AND `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
- `.claude/skills/shared/red-flag-stop-conditions-protocol.md` — STOP after 3+ failed attempts, when each fix reveals new problems

## Quick Summary

**Goal:** Investigate and identify root cause of a bug with evidence.

**Workflow:**

1. **Reproduce** — Understand expected vs actual behavior
2. **Hypothesize** — Form theories about root cause
3. **Trace** — Follow code paths with file:line evidence
4. **Confirm** — Verify root cause with grep/read evidence
5. **Report** — Output root cause with confidence level

**Key Rules:**

- Debug Mindset: every claim needs file:line proof
- Never assume first hypothesis is correct
- Output: confirmed root cause OR "hypothesis, not confirmed" with evidence gaps
- This is investigation-only — hand off to /fix for implementation

## Debug Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

- Do NOT assume the first hypothesis is correct — verify with actual code traces
- Every root cause claim must include `file:line` evidence
- If you cannot prove a root cause with a code trace, state "hypothesis, not confirmed"
- Question assumptions: "Is this really the cause?" → trace the actual execution path
- Challenge completeness: "Are there other contributing factors?" → check related code paths

## Confidence & Evidence Gate

**MANDATORY IMPORTANT MUST** declare `Confidence: X%` with evidence list + `file:line` proof for EVERY claim.

| Confidence | Meaning                                  | Action                               |
| ---------- | ---------------------------------------- | ------------------------------------ |
| 95-100%    | Full trace verified                      | Report as confirmed root cause       |
| 80-94%     | Main path verified, edge cases uncertain | Report with caveats                  |
| 60-79%     | Partial trace                            | Report as hypothesis                 |
| <60%       | Insufficient evidence                    | DO NOT report — gather more evidence |

## Workflow Details

### Step 1: Reproduce

- Clarify expected vs actual behavior
- Identify trigger conditions (user action, data state, timing)

### Step 2: Hypothesize

- Form 2-3 theories about root cause
- Rank by likelihood based on symptoms

### Step 3: Trace

- For each hypothesis, trace the code path:
  - Find entry point (API, UI, job, event)
  - Follow through handlers/services
  - Check data transformations and state changes
  - Verify error handling paths
- Use grep/read to collect `file:line` evidence

### Step 4: Confirm

- Match evidence to a single root cause
- Verify the root cause explains ALL symptoms
- Check for secondary contributing factors

### Step 5: Report

- Output: confirmed root cause with evidence chain
- Include: affected files, data flow, fix recommendation
- Hand off to `/fix` for implementation

## ⚠️ MANDATORY: Post-Fix Verification

**After `/fix` applies changes, `/prove-fix` MUST be run.** It builds code proof traces per change with confidence scores. This is non-negotiable in all fix workflows.

## Red Flags — STOP (Debugging-Specific)

If you're thinking:

- "I see the problem, let me fix it" — Seeing symptoms is not understanding root cause. Investigate first.
- "Quick fix for now, investigate later" — Quick fixes mask bugs and create debt. Find root cause.
- "Just try changing X and see" — One hypothesis at a time. Scientific method, not trial and error.
- "Already tried 2+ fixes, one more" — 3+ failed fixes = STOP. Question the architecture, not the fix.
- "The error message is misleading" — Read it again carefully. Error messages are usually right.
- "It works on my machine" — Reproduce in the failing environment. Your environment hides bugs.
- "This can't be the cause" — Verify with evidence, not intuition. Unlikely causes are still causes.

## IMPORTANT Task Planning Notes (MUST FOLLOW)

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `bugfix` workflow** (Recommended) — scout → investigate → debug → plan → fix → prove-fix → review → test
> 2. **Execute `/debug` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/fix (Recommended)"** — Apply fix based on debug findings
- **"/plan"** — If fix requires planning
- **"Skip, continue manually"** — user decides

## Standalone Review Gate (Non-Workflow Only)

> **MANDATORY IMPORTANT MUST:** If this skill is called **outside a workflow** (standalone `/debug`), you MUST create a `TaskCreate` todo task for `/review-changes` as the **last task** in your task list. This ensures all changes are reviewed before commit even without a workflow enforcing it.
>
> If already running inside a workflow (e.g., `bugfix`), skip this — the workflow sequence handles `/review-changes` at the appropriate step.

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
