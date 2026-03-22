---
name: review-changes
description: '[Code Quality] Review all uncommitted changes before commit'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`
- `.claude/skills/shared/design-patterns-quality-checklist.md` — Design pattern opportunities, anti-pattern detection, DRY/abstraction enforcement
- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

> **Critical Purpose:** Ensure quality — no flaws, no bugs, no missing updates, no stale content. Verify both code AND documentation.

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

> **OOP & DRY Enforcement:** MANDATORY IMPORTANT MUST — flag duplicated patterns that should be extracted to a base class, generic, or helper. Classes in the same group or suffix (ex *Entity, *Dto, \*Service, etc...) MUST inherit a common base (even if empty now — enables future shared logic and child overrides). Verify project has code linting/analyzer configured for the stack.

## Quick Summary

**Goal:** Comprehensive code review of all uncommitted changes following project standards.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference docs:
>
> - `docs/project-reference/code-review-rules.md` — anti-patterns, review checklists, quality standards **(READ FIRST)**
> - `project-structure-reference.md` — service list, directory tree, conventions
> - `docs/project-reference/scss-styling-guide.md` — BEM methodology, SCSS variables, mixins
> - `docs/project-reference/design-system/README.md` — design tokens, component inventory, icons
>
> If files not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Phase 0: Collect** — Run git status/diff, create report file
2. **Phase 1: File Review** — Review each changed file, update report incrementally
3. **Phase 2: Holistic** — Re-read report for big-picture architecture and responsibility checks
4. **Phase 3: Finalize** — Generate critical issues, recommendations, and suggested commit message

**Key Rules:**

- Report-driven: always write findings to `plans/reports/code-review-{date}-{slug}.md`
- Check logic placement (lowest layer: Entity > Service > Component)
- Must create todo tasks for all 4 phases before starting
- Be skeptical — every claim needs `file:line` proof
- Verify convention by grepping 3+ existing examples before flagging violations
- Actively check for DRY violations, YAGNI/KISS over-engineering, and correctness bugs
- Cross-reference changed files against related docs — flag stale feature docs, test specs, READMEs

# Code Review: Uncommitted Changes

Perform a comprehensive code review of all uncommitted changes following project standards.

## Review Scope

Target: All uncommitted changes (staged and unstaged) in the current working directory.

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

**YAGNI** — Flag code that solves problems that don't exist yet (unused parameters, speculative interfaces, premature abstractions)
**KISS** — Flag unnecessarily complex solutions. Ask: "Is there a simpler way that meets the same requirement?"
**DRY** — Actively grep for similar/duplicate code across the codebase before accepting new code. If 3+ similar patterns exist, flag for extraction.
**Clean Code** — Readable > clever. Names reveal intent. Functions do one thing. No deep nesting.
**Follow Convention** — Before flagging ANY pattern violation, grep for 3+ existing examples in the codebase. The codebase convention wins over textbook rules.
**No Flaws/No Bugs** — Trace logic paths. Verify edge cases (null, empty, boundary values). Check error handling covers failure modes.
**Proof Required** — Every claim backed by `file:line` evidence or grep results. Speculation is forbidden.
**Doc Staleness** — Cross-reference changed files against related docs (feature docs, test specs, READMEs). Flag any doc that is stale or missing updates to reflect current code changes.

## Review Approach (Report-Driven Two-Phase - CRITICAL)

**⛔ MANDATORY FIRST: Create Todo Tasks for Review Phases**
Before starting, call TaskCreate with:

- [ ] `[Review Phase 0] Get changes and create report file` - in_progress
- [ ] `[Review Phase 1] Review file-by-file and update report` - pending
- [ ] `[Review Phase 2] Re-read report for holistic assessment` - pending
- [ ] `[Review Phase 3] Generate final review findings` - pending
      Update todo status as each phase completes. This ensures review is tracked.

> **Note:** If Phase 0 reveals 20+ changed files, replace Phase 1-3 tasks with Systematic Review Protocol tasks:
> `[Review Phase 1] Categorize and fire parallel sub-agents`, `[Review Phase 2] Synchronize and cross-reference`, `[Review Phase 3] Generate consolidated report`

**Phase 0: Get Changes and Create Report File**

- [ ] Run `git status` to see all changed files
- [ ] Run `git diff` to see actual changes (staged and unstaged)
- [ ] Create `plans/reports/code-review-{date}-{slug}.md`
- [ ] Initialize with Scope, Files to Review sections

**Phase 1: File-by-File Review (Build Report Incrementally)**
For EACH changed file, read and **immediately update report** with:

- [ ] File path and change type (added/modified/deleted)
- [ ] Change Summary: what was modified/added
- [ ] Purpose: why this change exists
- [ ] **Convention check:** Grep for 3+ similar patterns in codebase — does new code follow existing convention?
- [ ] **Correctness check:** Trace logic paths — does the code handle null, empty, boundary values, error cases?
- [ ] **DRY check:** Grep for similar/duplicate code — does this logic already exist elsewhere?
- [ ] Issues Found: naming, typing, responsibility, patterns, bugs, over-engineering
- [ ] Continue to next file, repeat

**Phase 2: Holistic Review (Review the Accumulated Report)**
After ALL files reviewed, **re-read the report** to see big picture:

- [ ] Overall technical approach makes sense?
- [ ] Solution architecture coherent as unified plan?
- [ ] New files in correct layers (Domain/Application/Presentation)?
- [ ] Logic in LOWEST appropriate layer?
- [ ] Backend: mapping in Command/DTO (not Handler)?
- [ ] Frontend: constants/columns in Model (not Component)?
- [ ] No duplicated logic across changes?
- [ ] Service boundaries respected?
- [ ] No circular dependencies?

**Clean Code & Over-engineering Checks:**

- [ ] **YAGNI:** Any code solving hypothetical future problems? Unused params, speculative interfaces, config for one-time ops?
- [ ] **KISS:** Any unnecessarily complex solution? Could this be simpler while meeting same requirement?
- [ ] **Function complexity:** Methods >30 lines? Nesting >3 levels? Multiple responsibilities in one function?
- [ ] **Over-engineering:** Abstractions for single-use cases? Generic where specific suffices? Feature flags for things that could just be changed?
- [ ] **Readability:** Would a new team member understand this in <2 minutes? Are names self-documenting?

**Documentation Staleness Check (REQUIRED):**

Cross-reference changed files against related documentation using this mapping:

| Changed file pattern   | Docs to check for staleness                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------------------------- |
| `.claude/hooks/**`     | `.claude/docs/hooks/README.md`, hook count tables in `.claude/docs/hooks/*.md`                                |
| `.claude/skills/**`    | `.claude/docs/skills/README.md`, skill count/catalog tables                                                   |
| `.claude/workflows/**` | `CLAUDE.md` workflow catalog table, `.claude/docs/` workflow references                                       |
| Service code `**`      | `docs/business-features/` doc for the affected service                                                        |
| Frontend code `**`     | `docs/project-reference/frontend-patterns-reference.md`, relevant business-feature docs                       |
| Frontend legacy `**`   | `docs/project-reference/frontend-patterns-reference.md`, relevant business-feature docs                       |
| `CLAUDE.md`            | `.claude/docs/README.md` (navigation hub must stay in sync)                                                   |
| Backend code `**`      | `docs/project-reference/backend-patterns-reference.md`, `docs/project-reference/domain-entities-reference.md` |
| `docs/templates/**`    | Any docs generated from those templates                                                                       |

- [ ] For each changed file, check if matching docs exist and are still accurate
- [ ] Flag docs where counts, tables, examples, or descriptions no longer match the code
- [ ] Flag missing docs for new features/components that should be documented
- [ ] Check test specs (`docs/business-features/**/test-*`) reflect current behavior
- [ ] **Do NOT auto-fix** — flag in report with specific stale section and what changed

**Correctness & Bug Detection:**

- [ ] **Edge cases:** Null/undefined inputs handled? Empty collections? Boundary values (0, -1, max)?
- [ ] **Error paths:** What happens when this fails? Are errors caught, logged, and propagated correctly?
- [ ] **Race conditions:** Any async code with shared state? Concurrent access patterns safe?
- [ ] **Business logic:** Does the logic match the requirement? Trace one complete happy path + one error path through the code.

**Phase 3: Generate Final Review Result**
Update report with final sections:

- [ ] Overall Assessment (big picture summary)
- [ ] Critical Issues (must fix before merge)
- [ ] High Priority (should fix)
- [ ] Architecture Recommendations
- [ ] Documentation Staleness (list stale docs with what changed, or "No doc updates needed")
- [ ] Positive Observations
- [ ] Suggested commit message (based on changes)

## Readability Checklist (MUST evaluate)

Before approving, verify the code is **easy to read, easy to maintain, easy to understand**:

- **Schema visibility** — If a function computes a data structure (object, map, config), a comment should show the output shape so readers don't have to trace the code
- **Non-obvious data flows** — If data transforms through multiple steps (A → B → C), a brief comment should explain the pipeline
- **Self-documenting signatures** — Function params should explain their role; flag unused params
- **Magic values** — Unexplained numbers/strings should be named constants or have inline rationale
- **Naming clarity** — Variables/functions should reveal intent without reading the implementation

## Review Checklist

### 1. Architecture Compliance

- [ ] Follows Clean Architecture layers (Domain, Application, Persistence, Service)
- [ ] Uses correct repository pattern (search for: service-specific repository interface)
- [ ] CQRS pattern: Command/Query + Handler + Result in ONE file (search for: existing command patterns)
- [ ] No cross-service direct database access

### 2. Code Quality & Clean Code

- [ ] Single Responsibility Principle — each function/class does ONE thing. Event handlers/consumers/jobs: one handler = one independent concern (failures don't cascade)
- [ ] No code duplication (DRY) — grep for similar code, extract if 3+ occurrences
- [ ] Appropriate error handling with project validation patterns (search for: validation result pattern)
- [ ] No magic numbers/strings (extract to named constants)
- [ ] Type annotations on all functions
- [ ] No implicit any types
- [ ] Early returns/guard clauses used
- [ ] YAGNI — no speculative features, unused parameters, premature abstractions
- [ ] KISS — simplest solution that meets the requirement
- [ ] Function length <30 lines, nesting depth ≤3 levels
- [ ] Follows existing codebase conventions (verify with grep for 3+ examples)

### 2.5. Naming Conventions

- [ ] Names reveal intent (WHAT not HOW)
- [ ] Specific names, not generic (`employeeRecords` not `data`)
- [ ] Methods: Verb + Noun (`getEmployee`, `validateInput`)
- [ ] Booleans: is/has/can/should prefix (`isActive`, `hasPermission`)
- [ ] No cryptic abbreviations (`employeeCount` not `empCnt`)

### 3. Project Patterns (see docs/project-reference/backend-patterns-reference.md)

- [ ] Uses project validation fluent API (.And(), .AndAsync())
- [ ] No direct side effects in command handlers (use entity events)
- [ ] DTO mapping in DTO classes, not handlers
- [ ] Static expressions for entity queries

### 4. Security

- [ ] No hardcoded credentials
- [ ] Proper authorization checks
- [ ] Input validation at boundaries
- [ ] No SQL injection risks

### 5. Performance

- [ ] No O(n²) complexity (use dictionary for lookups)
- [ ] No N+1 query patterns (batch load related entities)
- [ ] Project only needed properties (don't load all then select one)
- [ ] Pagination for all list queries (never get all without paging)
- [ ] Parallel queries for independent operations
- [ ] Appropriate use of async/await
- [ ] Entity query expressions have database indexes configured
- [ ] Database collections have index management methods (search for: index setup pattern)
- [ ] Database migrations include indexes for WHERE clause columns

### 6. Common Issues to Check

- [ ] Unused imports or variables
- [ ] Console.log/Debug.WriteLine statements left in
- [ ] Hardcoded values that should be configuration
- [ ] Missing async/await keywords
- [ ] Incorrect exception handling
- [ ] Missing validation

### 7. Backend-Specific Checks

- [ ] CQRS patterns followed correctly
- [ ] Repository usage (no direct DbContext access)
- [ ] Entity DTO mapping patterns
- [ ] Validation using project validation patterns
- [ ] Seed data in data seeders, NOT in migration executors (if data must exist after DB reset → seeder)

### 8. Frontend-Specific Checks

- [ ] Component base class inheritance correct (search for: project base component classes)
- [ ] State management patterns (search for: project store base class)
- [ ] Memory leaks (search for: subscription cleanup pattern)
- [ ] Template binding issues
- [ ] BEM class naming on all elements

### 9. Documentation Staleness

- [ ] Changed service code → check `docs/business-features/` for affected service
- [ ] Changed frontend code → check `docs/project-reference/frontend-patterns-reference.md` + business-feature docs
- [ ] Changed backend code → check `docs/project-reference/backend-patterns-reference.md`
- [ ] Changed `.claude/hooks/**` → check `.claude/docs/hooks/README.md`
- [ ] Changed `.claude/skills/**` → check `.claude/docs/skills/README.md`, skill catalogs
- [ ] Changed `.claude/workflows/**` → check `CLAUDE.md` workflow catalog, `.claude/docs/` references
- [ ] New feature/component added → verify corresponding doc exists or flag as missing
- [ ] Test specs in `docs/business-features/**/` reflect current behavior after changes
- [ ] API changes reflected in relevant API docs or Swagger annotations

## Output Format

Provide feedback in this format:

**Summary:** Brief overall assessment

**Critical Issues:** (Must fix before commit)

- Issue 1: Description and suggested fix
- Issue 2: Description and suggested fix

**High Priority:** (Should fix)

- Issue 1: Description
- Issue 2: Description

**Suggestions:** (Nice to have)

- Suggestion 1
- Suggestion 2

**Documentation Staleness:** (Docs that may need updating)

- Doc 1: What is stale and why
- `No doc updates needed` — if no changed file maps to a doc

**Positive Notes:**

- What was done well

**Suggested Commit Message:**

```
type(scope): description

- Detail 1
- Detail 2
```

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Systematic Review Protocol (for 10+ changed files)

> **NON-NEGOTIABLE: When the changeset is large (10+ files), you MUST use this systematic protocol instead of reviewing files one-by-one sequentially.**
>
> **Principle:** Review carefully and systematically — break into groups, fire multiple agents to review in parallel. Ensure no flaws, no bugs, no stale info, and best practices in every aspect.

### Auto-Activation

In Phase 0, after running `git status`, count the changed files. If **10 or more files** changed:

1. **STOP** the sequential Phase 1-3 approach
2. **SWITCH** to this Systematic Review Protocol automatically
3. **ANNOUNCE** to user: `"Detected {N} changed files. Switching to systematic parallel review protocol."`

The sequential Phase 1-3 approach is ONLY for small changesets (<20 files). For large changesets, the parallel protocol produces better results with fewer missed issues.

### Step 1: Categorize Changes

Group all changed files into logical categories (e.g., by directory, concern, or layer):

| Category                        | Example Groupings                                             |
| ------------------------------- | ------------------------------------------------------------- |
| **Claude tooling**              | `.claude/hooks/`, `.claude/skills/`, `.claude/workflows.json` |
| **Root docs & instructions**    | `CLAUDE.md`, `README.md`, `.github/`                          |
| **System docs**                 | `.claude/docs/**`                                             |
| **Project docs & biz features** | `docs/business-features/`, `docs/*-reference.md`              |
| **Backend code**                | `src/Services/**/*.cs`                                        |
| **Frontend code**               | `src/{frontend}/**/*.ts`, `src/{legacy-frontend}/**/*.ts`     |

### Step 2: Fire Parallel Sub-Agents

Launch one `code-reviewer` sub-agent per category using the `Agent` tool with `run_in_background: true`. Each sub-agent receives:

- Full list of files in its category
- Category-specific review checklist
- Cross-reference verification instructions (counts, tables, links)

**All sub-agents run in parallel** to maximize speed and coverage.

### Step 3: Synchronize & Cross-Reference

After all sub-agents complete:

1. **Collect findings** from each agent's report
2. **Cross-reference** — verify counts, keyword tables, and references are consistent ACROSS categories
3. **Detect gaps** — issues that only appear when looking across categories (e.g., a workflow added in `.claude/` but missing from `CLAUDE.md` keyword table)
4. **Consolidate** into single holistic report with categorized findings

### Step 4: Holistic Big-Picture Assessment

With all category findings combined, assess:

- Overall coherence of changes as a unified plan
- Cross-category synchronization (do docs match code? do counts match reality?)
- Risk areas where categories interact
- Missing documentation updates for changed code

### Why This Protocol Matters

Sequential file-by-file review of 50+ files causes:

- Context window exhaustion before completing review
- Missed cross-file inconsistencies
- Shallow review of later files due to attention fatigue
- No big-picture assessment

Parallel categorized review ensures thorough coverage with holistic synthesis.

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `review-changes` workflow** (Recommended) — review-changes → code-review → watzup
> 2. **Execute `/review-changes` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/code-review (Recommended)"** — Deeper code quality review
- **"/watzup"** — Wrap up session and review all changes
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
