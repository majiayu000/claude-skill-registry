---
name: review-changes
description: '[Code Quality] Review all uncommitted changes before commit'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`

> **Critical Purpose:** Ensure quality — no flaws, no bugs, no missing updates, no stale content. Verify both code AND documentation.

## Quick Summary

**Goal:** Comprehensive code review of all uncommitted changes following project standards.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `project-structure-reference.md` — service list, directory tree, conventions
>
> If file not found, search for: project documentation, coding standards, architecture docs.

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

**Be skeptical. Apply critical thinking. Every claim needs traced proof.**

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

| Changed file pattern   | Docs to check for staleness                                                                                    |
| ---------------------- | -------------------------------------------------------------------------------------------------------------- |
| `.claude/hooks/**`     | `docs/claude/hooks/README.md`, `docs/claude/hooks-reference.md`, hook count tables in `docs/claude/hooks/*.md` |
| `.claude/skills/**`    | `docs/claude/skills/README.md`, skill count/catalog tables                                                     |
| `.claude/workflows/**` | `CLAUDE.md` workflow catalog table, `docs/claude/` workflow references                                         |
| Service code `**`      | `docs/business-features/` doc for the affected service                                                         |
| Frontend code `**`     | `docs/frontend-patterns-reference.md`, relevant business-feature docs                                          |
| Frontend legacy `**`   | `docs/frontend-patterns-reference.md`, relevant business-feature docs                                          |
| `CLAUDE.md`            | `docs/claude/README.md` (navigation hub must stay in sync)                                                     |
| Framework code `**`    | `docs/backend-patterns-reference.md`, `docs/claude/advanced-patterns.md`                                       |
| `docs/templates/**`    | Any docs generated from those templates                                                                        |

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

## Review Checklist

### 1. Architecture Compliance

- [ ] Follows Clean Architecture layers (Domain, Application, Persistence, Service)
- [ ] Uses correct repository pattern (search for: service-specific repository interface)
- [ ] CQRS pattern: Command/Query + Handler + Result in ONE file (search for: existing command patterns)
- [ ] No cross-service direct database access

### 2. Code Quality & Clean Code

- [ ] Single Responsibility Principle — each function/class does ONE thing
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

### 3. Platform Patterns

- [ ] Uses platform validation fluent API (.And(), .AndAsync())
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

### 8. Frontend-Specific Checks

- [ ] Component base class inheritance correct (search for: project base component classes)
- [ ] State management patterns (search for: project store base class)
- [ ] Memory leaks (search for: subscription cleanup pattern)
- [ ] Template binding issues
- [ ] BEM class naming on all elements

### 9. Documentation Staleness

- [ ] Changed service code → check `docs/business-features/` for affected service
- [ ] Changed frontend code → check `docs/frontend-patterns-reference.md` + business-feature docs
- [ ] Changed framework code → check `docs/backend-patterns-reference.md`, `docs/claude/advanced-patterns.md`
- [ ] Changed `.claude/hooks/**` → check `docs/claude/hooks/README.md`, `docs/claude/hooks-reference.md`
- [ ] Changed `.claude/skills/**` → check `docs/claude/skills/README.md`, skill catalogs
- [ ] Changed `.claude/workflows/**` → check `CLAUDE.md` workflow catalog, `docs/claude/` references
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
