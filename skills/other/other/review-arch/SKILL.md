---
name: review-arch
description: Interactive architectural review workflow. Analyzes codebase organization via noun analysis, produces a target blueprint, then collaborates with the user to decide what to implement. Changes are made through SMEs, verified with QA, and committed atomically.
model: opus
---

# Arch Review - Blueprint-Driven Architectural Improvement

Interactive workflow that analyzes codebase architecture, produces a target blueprint via noun analysis, and collaborates with the user to review, refine, and implement it.

## Philosophy

**Clarity through organization is the goal.** Every module should have a clear identity - a domain noun it owns. Functions should live where a reader expects to find them. DRY and Prune serve this organizational goal, not the other way around.

**Recommend boldly, implement collaboratively.** The analysis agent should surface every opportunity it finds, even uncertain ones — the user can always reject a recommendation. But the decision to implement is the user's. Present findings clearly, iterate on the plan together, and let the user direct what happens next.

**Red diffs are good within modules.** Once a function is in the right place, simplify its implementation. Less code is better when it doesn't sacrifice comprehensibility. But don't let line-count savings override architectural decisions.

## Workflow Overview

```
┌─────────────────────────────────────────────────────┐
│           ARCH REVIEW WORKFLOW                      │
├─────────────────────────────────────────────────────┤
│  1. Determine scope                                 │
│  2. Gather QA instructions                          │
│  3. Spawn swe-arch-reviewer agent (full analysis)    │
│     → returns dead code list + target blueprint     │
│  4. Present analysis to user                        │
│  5. Iterate on plan with user                       │
│  6. Ask user how to proceed                         │
│  7. Implement dead code removal                     │
│  8. Implement blueprint items iteratively           │
│     ├─ For each item: SME → QA → commit             │
│     └─ On persistent failure: skip item             │
│  9. Completion summary                              │
│ 10. Update documentation (/review-doc)              │
└─────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope

**Default:** Entire codebase.

**If user specifies scope:** Respect that scope (directory, files, module). Pass scope constraint to all spawned agents.

### 2. Gather QA Instructions

**Ask the user:** "Are there any special verification steps for the QA agent? For example: visual checks, manual testing commands, specific scenarios to validate."

**If provided:** Pass these instructions to the QA agent on every verification cycle, in addition to standard test suite execution.

**Examples of custom QA instructions:**
- "After each change, start the app, take a screenshot, and verify it renders correctly"
- "Run `make demo` and check that output matches expected behavior"
- "Hit the `/health` endpoint and verify 200 response"
- "Verify the CLI still produces valid output for `./tool --help`"

**If none provided:** QA agent runs standard verification (test suite, linters, formatters).

### 3. Analyze Codebase

**Spawn fresh `swe-arch-reviewer` agent:**

The agent performs four sequential analysis steps:
1. Catalogs dead code for removal
2. Builds a domain model via noun analysis
3. Catalogs repetition patterns
4. Produces a target architecture blueprint

**Prompt the agent with:**
```
Perform a full architectural analysis of this codebase.
Scope: [entire codebase | user-specified scope]
Produce a comprehensive target architecture blueprint showing where
everything should live. Cover every module — existing and proposed.
```

The agent returns:
- A noun frequency table (the primary analytical artifact)
- A per-noun namespace evaluation
- A dead code list (to implement first)
- A repetition catalog (DRY candidates, resolved in the blueprint)
- A target architecture blueprint (existing modules + proposed new modules)
- Any linter/formatter issues
- Any behavior-altering changes requiring approval

**If the agent reports "No refactoring needed":** Workflow complete.

### 4. Present Analysis to User

After the analysis agent returns, present its findings to the user. The user needs to see the full picture before deciding what to do.

**Present three things:**

**a) Noun analysis.** Show the noun frequency table and the per-noun namespace evaluations. This is the analytical foundation — the user should understand what nouns the agent identified, how frequently they appear, and why they do or don't deserve their own namespace.

**b) Proposed changes.** Show the blueprint items — modules to change, absorb, dissolve, or rename, plus proposed new modules. For each item, include the agent's rationale. Group by category (dead code removal, renames, moves, absorptions, dissolutions, new modules).

**c) No-change items.** Show the modules the agent evaluated and explicitly decided to leave alone, with their domain justifications. This is important context — the user may disagree and want to add items, or may spot a module the agent missed entirely.

### 5. Iterate on Plan with User

The user now has the full analysis. Give them the opportunity to shape the plan before anything is implemented.

**The user may want to:**
- Remove items they disagree with
- Add items the agent missed
- Modify proposed changes (e.g., "move that function to module X instead of Y")
- Ask questions about specific recommendations ("why did you flag this as dead code?")
- Adjust the scope based on what they see
- Reprioritize items

**Continue iterating until the user is satisfied with the plan.** Don't rush this — architectural decisions are consequential and benefit from deliberation.

### 6. Ask User How to Proceed

Once the plan is finalized, ask the user how they'd like to proceed. Don't assume implementation is the goal — the user may have other intentions.

The user will tell you what they want. Follow their direction.

### 7. Implement Dead Code Removal

If the finalized plan includes dead code removal and the user chose to proceed with implementation, implement removal first. This simplifies everything that follows.

- Batch all dead code removals together
- Spawn appropriate SME (or implement directly for mechanical deletions)
- Verify with QA
- Commit atomically

If no dead code removal is in the plan, skip to step 8.

### 8. Implement Blueprint

Work through the finalized blueprint iteratively. Each blueprint item describes a module's target state - what it owns, what it absorbs, what gets renamed or simplified.

#### 8a. Order Blueprint Items

Sequence items for safety:
1. Linter/formatter fixes
2. Renames and stutter fixes (lowest risk)
3. File splits within existing modules
4. Function moves within existing modules
5. Module absorptions (A absorbs functions from B)
6. Module dissolutions (all of C's functions distributed elsewhere)
7. New module creation

Within each category, prefer items that don't depend on other items.

#### 8b. For Each Blueprint Item

**Detect appropriate SME and spawn based on primary file type:**
- Go: `swe-sme-golang`
- Dockerfile: `swe-sme-docker`
- Makefile: `swe-sme-makefile`
- GraphQL: `swe-sme-graphql`
- Ansible: `swe-sme-ansible`
- Zig: `swe-sme-zig`
- TypeScript: `swe-sme-typescript`
- JavaScript: `swe-sme-javascript`
- HTML: `swe-sme-html`
- CSS: `swe-sme-css`

**For languages without a dedicated SME** (Python, Rust, Lua, etc.): implement directly as orchestrator, following language idioms and project conventions.

**For mixed-language items**: split into per-language batches, or implement directly if changes are mechanical.

**Prompt the SME with:**
```
Implement the following architectural change:

Target state for [module]:
[paste the blueprint item]

This is part of a larger reorganization. Move the listed functions/code
into this module, update all references, and simplify implementations
where possible.

Follow existing project conventions. Maintain all existing behavior.
Report when complete.
```

**SME implements and reports back.**

#### 8c. Verify Changes

**Spawn `qa-engineer` agent:**
- Run test suite
- Run linters/formatters
- Execute any custom QA instructions gathered in step 2
- Verify no regressions introduced
- Report pass/fail with specifics

**On PASS:** Proceed to commit.

**On FAIL:**
1. Return failure details to SME for repair
2. SME attempts fix
3. Re-verify with QA
4. Track failure count for this item

**After 3 consecutive failures for an item:**
- Revert all changes for that item (`git checkout -- .`)
- Log the failure (what was attempted, why it failed)
- Continue with next blueprint item
- Include in final summary as "skipped item"

#### 8d. Commit Changes

**Create atomic commit for successful item:**

```bash
git add [specific files modified]
git diff --staged  # verify only intended changes
git commit -m "$(cat <<'EOF'
refactor: [brief description of changes]

[Details of what was refactored and why]
EOF
)"
```

**Commit guidelines:**
- Stage only files modified by the current item (not `git add -A`)
- Verify staged changes before committing
- Use `refactor:` prefix in commit message
- Keep items atomic (one logical change per commit)

#### 8e. Next Item

Proceed to the next blueprint item. Continue until all items are implemented or skipped.

### 9. Completion Summary

When workflow completes, present summary:

```
## Arch Review Complete

### Statistics
- Commits made: N
- Net lines changed: -XXX (target: negative in source)
- Blueprint items completed: N
- Blueprint items skipped: N

### Blueprint Status
- [module]: completed / skipped (reason)

### Skipped Items (if any)
- [Item description]: [reason for failure]
```

### 10. Update Documentation

After the summary, run the `/review-doc` workflow to bring project documentation up to date. Architectural changes often rename modules, move functions, and change the project structure — documentation that references the old structure becomes stale.

Invoke the skill directly:
```
/review-doc
```

This spawns a doc-maintainer agent that audits all project documentation and fixes issues it finds. Any changes are committed separately from the refactoring commits.

## Agent Coordination

**Sequential execution:**
- One agent at a time
- Wait for completion before spawning next
- No parallel agent execution

**State to maintain (as orchestrator):**
- Current blueprint and progress through it
- Completed items (brief log)
- Skipped items (with reasons)
- Failure count per active item
- Running totals for summary

## Abort Conditions

**Abort current item:**
- 3 consecutive QA failures
- Revert changes, log failure, continue with next item

**Abort entire workflow:**
- User interrupts
- Git repository in unclean state that can't be resolved
- Critical system error

**Agent failures:**
- Spawn failure: retry once, then abort workflow with error
- Malformed output: log issue, skip item, continue
- Timeout: treat as failure, apply retry logic

**Do NOT abort for:**
- Individual item failures (skip and continue)
- Warnings from linters (fix or note, don't abort)

## Integration with Other Skills

**Relationship to `/refactor`:**
- `/refactor` is a tactical workflow for code quality improvements within existing architecture (DRY, dead code, naming, complexity)
- `/review-arch` is a strategic workflow that questions and restructures the architecture itself (noun analysis, module boundaries, blueprints)
- Use `/refactor` for routine cleanup; use `/review-arch` when the module structure itself needs rethinking

**Relationship to `/implement`:**
- `/implement` is a feature development workflow that optionally invokes `swe-code-reviewer` (tactical) for code review after implementation
- `/review-arch` is a dedicated architectural improvement workflow

**Relationship to `/scope`:**
- `/scope` explores and creates tickets
- `/review-arch` analyzes architecture and collaborates with the user on what to change
- Could use `/scope` first to plan a large restructuring, then `/review-arch` to execute

## Example Session

```
> /review-arch

Scope: entire codebase

Any special QA instructions?
> Run `make test && make lint` after each change

Starting analysis...

Spawning swe-arch-reviewer agent...

Analysis complete. Here's what I found:

## Noun Frequency

| Noun     | Count | Has Namespace? | Modules Where It Appears |
|----------|-------|----------------|--------------------------|
| request  | 14    | No             | Server, App, Middleware  |
| config   | 9     | No             | Widget, App, Server      |
| response | 7     | No             | Server, App, Middleware  |
| plugins  | 5     | No             | App                      |
| helper   | 4     | Yes (helpers)  | helpers                  |

## Noun Evaluation

request  — has namespace: no
           should have namespace: yes
           justification: highest frequency noun, spread across 3 modules.
           action: create namespace

config   — has namespace: no
           should have namespace: no change needed
           justification: already well-scoped within each module.
           action: no change

response — has namespace: no
           should have namespace: yes
           justification: response construction scattered across 3 modules.
           action: create namespace

[...]

## Proposed Changes

1. **Dead code removal** (4 instances across 3 files)
   - `helpers.go:42` unused `formatDate()` function
   - `server.go:118` commented-out legacy handler
   - ...

2. **Rename** `parser.go` → `request.go` (domain noun)

3. **request.go absorbs** `validate()` from `server.go`
   Rationale: validation is a request concept, not a server concept.

4. **Dissolve** `helpers.go`
   Rationale: no cohesive domain identity. Distribute functions to owners.

5. **Create** `response.go`
   Rationale: response construction logic scattered across 3 modules.

## No-Change Items

- **config.go** — domain noun: config. Clear identity, well-scoped. No change.
- **middleware.go** — domain noun: middleware. Cohesive, correctly placed. No change.
- **logger.go** — domain noun: logger. Single responsibility. No change.

What would you like to change about this plan?

> I agree with 1-4, but let's hold off on creating response.go for now.
  Also, can you explain why you want to dissolve helpers.go? I think
  some of those functions are genuinely shared utilities.

Good question. helpers.go contains 6 functions:
- `formatDate()` — dead code (already flagged for removal)
- `parseURL()` — only used by request handling → belongs in request.go
- `sanitizeInput()` — only used by request validation → belongs in request.go
- `truncateString()` — used by 3 modules for display formatting
- `pluralize()` — used by 2 modules for display formatting
- `retryWithBackoff()` — used by server.go and client.go

You're right that truncateString, pluralize, and retryWithBackoff are
genuinely shared. I'd suggest keeping a focused `display.go` for the
formatting helpers and moving retryWithBackoff to a `retry.go` module.
That dissolves the grab-bag while preserving shared utilities.

> That works. Let's do that instead. How should we proceed?

Updated plan:
1. Remove dead code (4 instances)
2. Rename parser.go → request.go
3. request.go absorbs validate() from server.go
4. Dissolve helpers.go:
   - parseURL, sanitizeInput → request.go
   - truncateString, pluralize → display.go (new)
   - retryWithBackoff → retry.go (new)

How would you like to proceed?

> Let's implement these changes now.

Implementing dead code removal...
  QA verification: PASS
  Committed: "refactor: remove dead code (4 instances)"

Implementing item 1/3: rename parser.go → request.go
  Spawning swe-sme-golang...
  QA verification: PASS
  Committed: "refactor: rename parser to request (domain noun)"

Implementing item 2/3: request.go absorbs validate() from server.go
  Spawning swe-sme-golang...
  QA verification: FAIL - TestServerValidate broken
  Returning to swe-sme-golang for repair (attempt 1/3)...
  QA verification: PASS
  Committed: "refactor: move validation into request module"

Implementing item 3/3: dissolve helpers.go
  Spawning swe-sme-golang...
  QA verification: PASS
  Committed: "refactor: dissolve helpers; distribute to domain owners"

## Arch Review Complete

### Statistics
- Commits made: 4
- Net lines changed: -128
- Blueprint items completed: 3/3

Running /review-doc to update documentation...
```
