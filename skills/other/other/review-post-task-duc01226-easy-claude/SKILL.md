---
name: review-post-task
version: 1.0.0
description: '[Code Quality] Two-pass code review for task completion'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`
- `.claude/skills/shared/design-patterns-quality-checklist.md` — Design pattern opportunities, anti-pattern detection, DRY/abstraction enforcement
- `.claude/skills/shared/double-round-trip-review-protocol.md` — Mandatory two-round review enforcement

> **Critical Purpose:** Ensure quality — no flaws, no bugs, no missing updates, no stale content. Verify both code AND documentation.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference docs:
>
> - `docs/project-reference/code-review-rules.md` — anti-patterns, review checklists, quality standards **(READ FIRST)**
> - `project-structure-reference.md` — service list, directory tree, conventions
>
> If files not found, search for: project documentation, coding standards, architecture docs.

> **OOP & DRY Enforcement:** MANDATORY IMPORTANT MUST — flag duplicated patterns that should be extracted to a base class, generic, or helper. Classes in the same group or suffix (ex *Entity, *Dto, \*Service, etc...) MUST inherit a common base (even if empty now — enables future shared logic and child overrides). Verify project has code linting/analyzer configured for the stack.

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

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

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

## Readability Checklist (MUST evaluate)

Before approving, verify the code is **easy to read, easy to maintain, easy to understand**:

- **Schema visibility** — If a function computes a data structure (object, map, config), a comment should show the output shape so readers don't have to trace the code
- **Non-obvious data flows** — If data transforms through multiple steps (A → B → C), a brief comment should explain the pipeline
- **Self-documenting signatures** — Function params should explain their role; flag unused params
- **Magic values** — Unexplained numbers/strings should be named constants or have inline rationale
- **Naming clarity** — Variables/functions should reveal intent without reading the implementation

## Protocol

**Pass 1:** Gather changes (`git diff`), apply project review checklist:

- Backend: platform repos, validation, events, DTOs
- Backend: seed data in data seeders (not migrations) — if data must exist after DB reset, it's a seeder
- Frontend: base classes, stores, untilDestroyed, BEM
- Architecture: layer placement, service boundaries
- **Convention:** grep for 3+ similar patterns to verify code follows codebase conventions
- **Correctness:** trace logic paths, check edge cases (null, empty, boundary values)
- **DRY:** grep for duplicate/similar code across codebase
- **YAGNI/KISS:** flag over-engineering, unnecessary abstractions, speculative features
- **Doc staleness:** cross-reference changed files against `docs/business-features/`, test specs, READMEs — flag stale docs

> **[IMPORTANT] Database Performance Protocol (MANDATORY):**
>
> 1. **Paging Required** — ALL list/collection queries MUST use pagination. NEVER load all records into memory. Verify: no unbounded `GetAll()`, `ToList()`, or `Find()` without `Skip/Take` or cursor-based paging.
> 2. **Index Required** — ALL query filter fields, foreign keys, and sort columns MUST have database indexes configured. Verify: entity expressions match index field order, database collections have index management methods, migrations include indexes for WHERE/JOIN/ORDER BY columns.

Fix issues found.

**Pass 2 (MANDATORY — Round 2):** Re-review ALL changes (original + corrections) with fresh eyes. Do NOT skip even if Pass 1 made no changes. Focus on what Pass 1 missed: cross-cutting concerns, subtle edge cases, naming inconsistencies, missing pieces, convention drift, over-engineering. Update report with Round 2 findings. See `.claude/skills/shared/double-round-trip-review-protocol.md`.

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

---

## Systematic Review Protocol (for 10+ changed files)

> **When the changeset is large (10+ files), categorize files by concern, fire parallel `code-reviewer` sub-agents per category, then synchronize findings into a holistic report.** See `review-changes/SKILL.md` § "Systematic Review Protocol" for the full 4-step protocol (Categorize → Parallel Sub-Agents → Synchronize → Holistic Assessment).
