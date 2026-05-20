---
name: code-review
version: 2.1.0
description: '[Code Quality] Use when receiving code review feedback (especially if unclear or technically questionable), when completing tasks or major features requiring review before proceeding, or before making any completion/success claims. Covers three practices - receiving feedback with technical rigor over performative agreement, requesting reviews via code-reviewer subagent, and verification gates requiring evidence before any status claims. Essential for subagent-driven development, pull requests, and preventing false completion claims.'
allowed-tools: NONE
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

> **Critical Purpose:** Ensure quality — no flaws, no bugs, no missing updates, no stale content. Verify both code AND documentation.

## Quick Summary

**Goal:** Ensure technical correctness through three practices: receiving feedback with verification over performative agreement, requesting systematic reviews via code-reviewer subagent, and enforcing verification gates before completion claims.

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference docs:
>
> - `backend-patterns-reference.md` — backend CQRS, validation, entity patterns
> - `frontend-patterns-reference.md` — component hierarchy, store, forms patterns
>
> If files not found, search for: project coding standards, architecture documentation.

**Workflow:**

1. **Create Review Report** — Initialize report file in `plans/reports/code-review-{date}-{slug}.md`
2. **Phase 1: File-by-File** — Review each file, update report with issues (naming, typing, magic numbers, responsibility)
3. **Phase 2: Holistic Review** — Re-read accumulated report, assess overall approach, architecture, duplication
4. **Phase 3: Final Result** — Update report with overall assessment, critical issues, recommendations

**Key Rules:**

- **Report-Driven**: Build report incrementally, re-read for big picture
- **Two-Phase**: Individual file review → holistic assessment of accumulated findings
- **No Performative Agreement**: Technical evaluation, not social comfort ("You're right!" banned)
- **Verification Gates**: Evidence required before any completion claims (tests pass, build succeeds)

# Code Review

Guide proper code review practices emphasizing technical rigor, evidence-based claims, and verification over performative responses.

## Overview

Code review requires three distinct practices:

1. **Receiving feedback** - Technical evaluation over performative agreement
2. **Requesting reviews** - Systematic review via code-reviewer subagent
3. **Verification gates** - Evidence before any completion claims

Each practice has specific triggers and protocols detailed in reference files.

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
**KISS** — Flag unnecessarily complex solutions. Ask: "Is there a simpler way that meets the same requirement?"
**DRY** — Actively grep for similar/duplicate code across the codebase before accepting new code. If 3+ similar patterns exist, flag for extraction.
**Clean Code** — Readable > clever. Names reveal intent. Functions do one thing. No deep nesting (≤3 levels). Methods <30 lines.
**Follow Convention** — Before flagging ANY pattern violation, grep for 3+ existing examples in the codebase. The codebase convention wins over textbook rules.
**No Flaws/No Bugs** — Trace logic paths. Verify edge cases (null, empty, boundary values). Check error handling covers failure modes.
**Proof Required** — Every claim backed by `file:line` evidence or grep results. Speculation is forbidden.
**Doc Staleness** — Cross-reference changed files against related docs (feature docs, test specs, READMEs). Flag any doc that is stale or missing updates to reflect current code changes.

**Be honest, be brutal, straight to the point, and be concise.**
**Technical correctness over social comfort.** Verify before implementing. Ask before assuming. Evidence before claims.

## Review Approach (Report-Driven Two-Phase - CRITICAL)

**⛔ MANDATORY FIRST: Create Todo Tasks**
Before starting, call TaskCreate with review phase tasks:

- `[Review Phase 1] Create report file` - in_progress
- `[Review Phase 1] Review file-by-file and update report` - pending
- `[Review Phase 2] Re-read report for holistic assessment` - pending
- `[Review Phase 3] Generate final review findings` - pending
  Update todo status as each phase completes.

**Step 0: Create Report File**

- Create `plans/reports/code-review-{date}-{slug}.md`
- Initialize with Scope, Files to Review sections

**Phase 1: File-by-File Review (Build Report)**
For EACH file, **immediately update report** with:

- File path, Change Summary, Purpose, Issues Found
- Check naming, typing, magic numbers, responsibility placement
- **Convention check:** Grep for 3+ similar patterns in codebase — does new code follow existing convention?
- **Correctness check:** Trace logic paths — does the code handle null, empty, boundary values, error cases?
- **DRY check:** Grep for similar/duplicate code — does this logic already exist elsewhere?

**Phase 2: Holistic Review (Review the Report)**
After ALL files reviewed, **re-read accumulated report** to see big picture:

- **Technical Solution**: Does overall approach make sense as unified plan?
- **Responsibility**: New files in correct layers? Logic in LOWEST layer?
- **Backend**: Mapping in Command/DTO (not Handler)?
- **Frontend**: Constants/columns in Model (not Component)?
- **Duplication**: Any duplicated logic across changes? Similar code elsewhere? (grep to verify)
- **Architecture**: Clean Architecture followed? Service boundaries respected?

**Clean Code & Over-engineering Checks:**

- **YAGNI:** Any code solving hypothetical future problems? Unused params, speculative interfaces, config for one-time ops?
- **KISS:** Any unnecessarily complex solution? Could this be simpler while meeting same requirement?
- **Function complexity:** Methods >30 lines? Nesting >3 levels? Multiple responsibilities in one function?
- **Over-engineering:** Abstractions for single-use cases? Generic where specific suffices?

**Correctness & Bug Detection:**

- **Edge cases:** Null/undefined inputs handled? Empty collections? Boundary values (0, -1, max)?
- **Error paths:** What happens when this fails? Are errors caught, logged, and propagated correctly?
- **Race conditions:** Any async code with shared state? Concurrent access patterns safe?
- **Business logic:** Does the logic match the requirement? Trace one complete happy path + one error path.

**Documentation Staleness Check:**

Cross-reference changed files against related documentation:

| Changed file pattern   | Docs to check                                                   |
| ---------------------- | --------------------------------------------------------------- |
| Service code `**`      | Business feature docs for affected service                      |
| Frontend code `**`     | Frontend patterns doc, relevant business-feature docs           |
| Framework code `**`    | Backend patterns doc, advanced patterns doc                     |
| `.claude/hooks/**`     | `docs/claude/hooks/README.md`, `docs/claude/hooks-reference.md` |
| `.claude/skills/**`    | `docs/claude/skills/README.md`, skill catalogs                  |
| `.claude/workflows/**` | `CLAUDE.md` workflow catalog, `docs/claude/` references         |

- Flag docs where counts, tables, examples, or descriptions no longer match the code
- Flag missing docs for new features/components
- Check test specs reflect current behavior
- **Do NOT auto-fix** — flag in report with specific stale section and what changed

**Phase 3: Final Review Result**
Update report with: Overall Assessment, Critical Issues, High Priority, Architecture Recommendations, Documentation Staleness, Positive Observations

## Clean Code Rules (MUST CHECK)

1. **No Magic Numbers/Strings** - All literal values must be named constants
2. **Type Annotations** - All functions must have explicit parameter and return types
3. **Single Responsibility** - One reason to change per method/class
4. **DRY** - No code duplication; extract shared logic
5. **Naming** - Clear, specific names that reveal intent:
    - Specific not generic: `employeeRecords` not `data`
    - Methods: Verb+Noun: `getEmployee()`, `validateInput()`
    - Booleans: is/has/can/should prefix: `isActive`, `hasPermission`
    - No cryptic abbreviations: `employeeCount` not `empCnt`
6. **Performance** - Efficient data access patterns:
    - No O(n²): use dictionary lookup instead of nested loops
    - Project in query: don't load all then `.Select(x.Id)`
    - Always paginate: never get all data without `.PageBy()`
    - Batch load: use `GetByIdsAsync()` not N+1 queries
7. **Entity Indexes** - Database queries have matching indexes:
    - Database collections: index management methods (search for: index setup pattern)
    - EF Core: Composite indexes in migrations for filter columns
    - Expression fields match index field order (leftmost prefix)
    - Text search queries have text indexes configured

## WebV1 Platform Compliance (`src/Web/**`)

When reviewing files in `src/Web/**`, verify these MANDATORY patterns.
**⚠️ MUST READ:** CLAUDE.md "Component Hierarchy" and "Frontend (TypeScript)" sections for full pattern reference.

### Review Checklist

- [ ] Component extends project's base component class (search for: app base component hierarchy)
- [ ] Constructor includes required DI and calls `super(...)`
- [ ] Uses `this.untilDestroyed()` for RxJS subscriptions (NO manual `Subject` destroy pattern)
- [ ] Services extend `PlatformApiService` (NO direct `HttpClient`)
- [ ] Store API calls use `effectSimple()` (NOT `observerLoadingErrorState` in store)

### Anti-Patterns to Flag as CRITICAL

```typescript
// ❌ Manual destroy Subject / takeUntil pattern
private destroy$ = new Subject<void>();
.pipe(takeUntil(this.destroy$))

// ❌ Raw Component without base class
export class MyComponent implements OnInit, OnDestroy { }
```

## When to Use This Skill

### Receiving Feedback

Trigger when:

- Receiving code review comments from any source
- Feedback seems unclear or technically questionable
- Multiple review items need prioritization
- External reviewer lacks full context
- Suggestion conflicts with existing decisions

**⚠️ MUST READ:** `references/code-review-reception.md`

### Requesting Review

Trigger when:

- Completing tasks in subagent-driven development (after EACH task)
- Finishing major features or refactors
- Before merging to main branch
- Stuck and need fresh perspective
- After fixing complex bugs

**⚠️ MUST READ:** `references/requesting-code-review.md`

### Verification Gates

Trigger when:

- About to claim tests pass, build succeeds, or work is complete
- Before committing, pushing, or creating PRs
- Moving to next task
- Any statement suggesting success/completion
- Expressing satisfaction with work

**⚠️ MUST READ:** `references/verification-before-completion.md`

## Quick Decision Tree

```
SITUATION?
│
├─ Received feedback
│  ├─ Unclear items? → STOP, ask for clarification first
│  ├─ From human partner? → Understand, then implement
│  └─ From external reviewer? → Verify technically before implementing
│
├─ Completed work
│  ├─ Major feature/task? → Request code-reviewer subagent review
│  └─ Before merge? → Request code-reviewer subagent review
│
└─ About to claim status
   ├─ Have fresh verification? → State claim WITH evidence
   └─ No fresh verification? → RUN verification command first
```

## Receiving Feedback Protocol

### Response Pattern

READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT

### Key Rules

- ❌ No performative agreement: "You're absolutely right!", "Great point!", "Thanks for [anything]"
- ❌ No implementation before verification
- ✅ Restate requirement, ask questions, push back with technical reasoning, or just start working
- ✅ If unclear: STOP and ask for clarification on ALL unclear items first
- ✅ YAGNI check: grep for usage before implementing suggested "proper" features

### Source Handling

- **Human partner:** Trusted - implement after understanding, no performative agreement
- **External reviewers:** Verify technically correct, check for breakage, push back if wrong

**Full protocol:** `references/code-review-reception.md`

## Requesting Review Protocol

### When to Request

- After each task in subagent-driven development
- After major feature completion
- Before merge to main

### Process

1. Get git SHAs: `BASE_SHA=$(git rev-parse HEAD~1)` and `HEAD_SHA=$(git rev-parse HEAD)`
2. Dispatch code-reviewer subagent via Task tool with: WHAT_WAS_IMPLEMENTED, PLAN_OR_REQUIREMENTS, BASE_SHA, HEAD_SHA, DESCRIPTION
3. Act on feedback: Fix Critical immediately, Important before proceeding, note Minor for later

**Full protocol:** `references/requesting-code-review.md`

## Verification Gates Protocol

### The Iron Law

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE**

### Gate Function

IDENTIFY command → RUN full command → READ output → VERIFY confirms claim → THEN claim

Skip any step = lying, not verifying

### Requirements

- Tests pass: Test output shows 0 failures
- Build succeeds: Build command exit 0
- Bug fixed: Test original symptom passes
- Requirements met: Line-by-line checklist verified

### Red Flags - STOP

Using "should"/"probably"/"seems to", expressing satisfaction before verification, committing without verification, trusting agent reports, ANY wording implying success without running verification

**Full protocol:** `references/verification-before-completion.md`

## Integration with Workflows

- **Subagent-Driven:** Review after EACH task, verify before moving to next
- **Pull Requests:** Verify tests pass, request code-reviewer review before merge
- **General:** Apply verification gates before any status claims, push back on invalid feedback

## Bottom Line

1. Technical rigor over social performance - No performative agreement
2. Systematic review processes - Use code-reviewer subagent
3. Evidence before claims - Verification gates always

Verify. Question. Then implement. Evidence. Then claim.

## Related

- `code-simplifier`
- `debug`
- `refactoring`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
