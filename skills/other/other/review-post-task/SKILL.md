---
name: review-post-task
version: 1.0.0
description: '[Code Quality] Two-pass code review for task completion'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`

> **Critical Purpose:** Ensure quality — no flaws, no bugs, no missing updates, no stale content. Verify both code AND documentation.

## Quick Summary

**Goal:** Two-pass code review after task completion to catch issues before commit.

**Workflow:**
1. **Pass 1: File-by-File** — Review each changed file individually
2. **Pass 2: Holistic** — Assess overall approach, architecture, consistency
3. **Report** — Summarize critical issues and recommendations

**Key Rules:**
- Ensure quality: no flaws, no bugs, no missing updates, no stale content
- Check both code AND documentation for completeness
- Evidence-based findings with `file:line` references

Execute mandatory two-pass review protocol after completing code changes.
Focus: $ARGUMENTS

Activate `code-review` skill and follow its workflow with **post-task two-pass** protocol:

## Review Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking. Every claim needs traced proof.**

- Do NOT accept code correctness at face value — verify by reading actual implementations
- Every finding must include `file:line` evidence (grep results, read confirmations)
- If you cannot prove a claim with a code trace, do NOT include it in the report
- Question assumptions: "Does this actually work?" → trace the call path to confirm
- Challenge completeness: "Is this all?" → grep for related usages across services
- Verify side effects: "What else does this change break?" → check consumers and dependents
- No "looks fine" without proof — state what you verified and how

## Core Principles (ENFORCE ALL)

**YAGNI** — Flag code solving hypothetical future problems (unused params, speculative interfaces, premature abstractions)
**KISS** — Flag unnecessarily complex solutions. Ask: "Is there a simpler way?"
**DRY** — Grep for similar/duplicate code across the codebase. If 3+ similar patterns exist, flag for extraction.
**Clean Code** — Readable > clever. Names reveal intent. Functions do one thing. No deep nesting (≤3 levels). Methods <30 lines.
**Follow Convention** — Before flagging ANY pattern violation, grep for 3+ existing examples. Codebase convention wins.
**No Flaws/No Bugs** — Trace logic paths. Verify edge cases (null, empty, boundary). Check error handling.
**Proof Required** — Every claim backed by `file:line` evidence or grep results. Speculation is forbidden.
**Doc Staleness** — Cross-reference changed files against related docs (feature docs, test specs, READMEs). Flag any doc that is stale or missing updates to reflect current code changes.

## Protocol

**Pass 1:** Gather changes (`git diff`), apply project review checklist:
- Backend: platform repos, validation, events, DTOs
- Frontend: base classes, stores, untilDestroyed, BEM
- Architecture: layer placement, service boundaries
- **Convention:** grep for 3+ similar patterns to verify code follows codebase conventions
- **Correctness:** trace logic paths, check edge cases (null, empty, boundary values)
- **DRY:** grep for duplicate/similar code across codebase
- **YAGNI/KISS:** flag over-engineering, unnecessary abstractions, speculative features
- **Doc staleness:** cross-reference changed files against `docs/business-features/`, test specs, READMEs — flag stale docs
Fix issues found.

**Pass 2 (conditional):** Only if Pass 1 made changes. Re-review ALL changes (original + corrections). Verify no new issues introduced.

**Final Report:** Task description, Pass 1/2 results, changes summary, issues fixed, remaining concerns.

## Integration Notes

- Auto-triggered by workflow orchestration after `/cook`, `/fix`, `/code`
- Can be manually invoked with `/review-post-task`
- For PR reviews, use `/code-review` instead
- Use `code-reviewer` subagent for complex reviews

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
