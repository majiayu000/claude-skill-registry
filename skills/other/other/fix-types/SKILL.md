---
name: fix-types
description: '[Implementation] Fix type errors'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` AND `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

> **Skill Variant:** Variant of `/fix` — TypeScript/type error resolution.

## Quick Summary

**Goal:** Fix TypeScript compilation errors and type mismatches across the codebase.

**Workflow:**

1. **Collect** — Run `tsc --noEmit` or `nx build` to gather type errors
2. **Analyze** — Classify errors (missing types, wrong signatures, import issues)
3. **Fix** — Apply type-safe fixes without `any` casts where possible

**Key Rules:**

- Debug Mindset: every claim needs `file:line` evidence
- Prefer proper typing over `any` or type assertions
- Fix root cause (wrong interface, missing export) not symptoms

Run `bun run typecheck` or `tsc` or `npx tsc` and fix all type errors.

## Debug Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

- Do NOT assume the first hypothesis is correct — verify with actual code traces
- Every root cause claim must include `file:line` evidence
- If you cannot prove a root cause with a code trace, state "hypothesis, not confirmed"
- Question assumptions: "Is this really the cause?" → trace the actual execution path
- Challenge completeness: "Are there other contributing factors?" → check related code paths
- No "should fix it" without proof — verify the fix addresses the traced root cause

## ⚠️ MANDATORY: Confidence & Evidence Gate

**MANDATORY IMPORTANT MUST** declare `Confidence: X%` with evidence list + `file:line` proof for EVERY claim.
**95%+** recommend freely | **80-94%** with caveats | **60-79%** list unknowns | **<60% STOP — gather more evidence.**

## Rules

- Fix all of type errors and repeat the process until there are no more type errors.
- Do not use `any` just to pass the type check.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
- **After fixing, MUST run `/prove-fix`** — build code proof traces per change with confidence scores. Never skip.
