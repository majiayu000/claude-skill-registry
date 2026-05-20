---
name: fix-ci
version: 1.0.0
description: '[Implementation] Analyze Github Actions logs and fix issues'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` AND `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

> **Skill Variant:** Variant of `/fix` — specialized for CI/GitHub Actions log analysis.

## Quick Summary

**Goal:** Analyze GitHub Actions CI logs to identify and fix build/test failures in the pipeline.

**Workflow:**
1. **Fetch** — Download CI logs from GitHub Actions
2. **Analyze** — Identify root cause from log output (build errors, test failures, env issues)
3. **Fix** — Apply targeted fix based on traced root cause

**Key Rules:**
- Debug Mindset: every claim needs `file:line` evidence
- Focus on CI-specific issues (env vars, Docker, dependencies, build order)
- Verify fix doesn't break local development

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

## Github Actions URL

<url>$ARGUMENTS</url>

## Workflow

1. Use `debugger` subagent to read the github actions logs with `gh` command, analyze and find the root cause of the issues and report back to main agent.
   1.5. Write analysis findings to `.ai/workspace/analysis/{ci-issue}.analysis.md`. Re-read before implementing fix.
2. Start implementing the fix based the reports and solutions.
3. Use `tester` agent to test the fix and make sure it works, then report back to main agent.
4. If there are issues or failed tests, repeat from step 2.
5. After finishing, respond back to user with a summary of the changes and explain everything briefly, guide user to get started and suggest the next steps.

## Notes

- If `gh` command is not available, instruct the user to install and authorize GitHub CLI first.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
