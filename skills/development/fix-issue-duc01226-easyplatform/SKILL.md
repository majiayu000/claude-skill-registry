---
name: fix-issue
version: 1.0.0
description: '[Implementation] Debug and fix GitHub issues with systematic investigation'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` AND `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

> **Skill Variant:** Variant of `/fix` — debug and fix GitHub issues with systematic investigation.

## Quick Summary

**Goal:** Investigate and fix bugs reported as GitHub issues with full traceability.

**Workflow:**
1. **Fetch** — Read GitHub issue details (title, description, reproduction steps)
2. **Reproduce** — Trace the reported behavior in code
3. **Fix** — Apply fix with root cause evidence

**Key Rules:**
- Debug Mindset: every claim needs `file:line` evidence
- Link fix back to the GitHub issue for traceability
- Verify fix addresses the specific reproduction steps from the issue

<issue-number>$ARGUMENTS</issue-number>

## Debug Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking. Every claim needs traced proof.**

- Do NOT assume the first hypothesis is correct — verify with actual code traces
- Every root cause claim must include `file:line` evidence
- If you cannot prove a root cause with a code trace, state "hypothesis, not confirmed"
- Question assumptions: "Is this really the cause?" → trace the actual execution path
- Challenge completeness: "Are there other contributing factors?" → check related code paths
- No "should fix it" without proof — verify the fix addresses the traced root cause

## ⚠️ MANDATORY: Confidence & Evidence Gate

**MUST** declare `Confidence: X%` with evidence list + `file:line` proof for EVERY claim.
**95%+** recommend freely | **80-94%** with caveats | **60-79%** list unknowns | **<60% STOP — gather more evidence.**

Activate `debug` skill and follow its workflow.

**IMPORTANT**: Always use external memory at `.ai/workspace/analysis/issue-[number].analysis.md` for structured analysis. **Re-read ENTIRE analysis file before proposing any fix** — this prevents knowledge loss.

**DO NOT** make any code changes without explicit user approval. Present analysis and proposed fix, then wait for approval before implementing.

See `.ai/docs/AI-DEBUGGING-PROTOCOL.md` for comprehensive guidelines.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
