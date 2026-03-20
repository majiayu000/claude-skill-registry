---
name: refactor
description: Autonomous iterative refactoring workflow. Scans for tactical code quality improvements (DRY, dead code, naming, complexity), implements through SMEs, verifies with QA, commits atomically, and loops until no improvements remain.
model: opus
---

# Refactor - Iterative Code Quality Improvement

Autonomous refactoring workflow that iteratively improves code quality within the existing architecture, always preferring the least aggressive change available, until no further opportunities exist.

## Philosophy

**Clarity is the goal.** Every iteration should make the codebase easier to form a correct mental model of. Red diffs are the strongest signal - less code almost always means clearer code, and every iteration should delete more than it adds. But when reducing lines would hurt comprehensibility, clarity wins.

**Err on the side of trying.** When uncertain whether a refactoring is worthwhile, attempt it anyway. Git makes failed experiments free - the workflow will revert changes that don't pass QA. Missed opportunities are invisible; failed attempts teach you something. Be bold, knowing that version control provides the safety net.

**Work within the existing architecture.** This workflow improves code quality - DRY, dead code, naming, complexity - without questioning module boundaries or reorganizing the system. For architectural analysis (noun extraction, module dissolution, blueprint-driven restructuring), use `/review-arch` instead.

## Workflow Overview

```
┌─────────────────────────────────────────────────────┐
│                  REFACTORING LOOP                   │
├─────────────────────────────────────────────────────┤
│  1. Determine scope                                 │
│  2. Select aggression ceiling                       │
│  3. Gather QA instructions                          │
│  4. Spawn fresh swe-code-reviewer agent (full scan)      │
│  5. Select least aggressive changes available       │
│  6. If none remain → exit to summary                │
│  7. Spawn SME agent (implement batch)               │
│  8. Spawn QA agent (verify)                         │
│     ├─ PASS → commit, goto 4                        │
│     └─ FAIL → retry (max 3), then abort batch       │
│  9. Completion summary                              │
│ 10. Update documentation (/review-doc)              │
└─────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope

**Default:** Entire codebase.

**Boundary: version-controlled files only.** The refactoring workflow operates exclusively on files tracked by git. Untracked files and directories must never be modified or deleted — their loss could be irreversible. This boundary is non-negotiable regardless of scope setting.

**If user specifies scope:** Respect that scope (directory, files, module). Pass scope constraint to all spawned agents.

### 2. Select Aggression Ceiling

**Ask the user:** "How aggressive should refactoring be?"

Present these options:
- **Maximum**: Attempt all improvements, including aggressive changes (removing legacy code with unclear purpose, consolidating similar-but-not-identical behavior)
- **High**: Go up to MODERATE changes (cross-module DRY, removing abstraction layers, splitting files into focused modules) but skip aggressive changes
- **Low**: Only SAFEST and SAFE changes (formatters, linters, dead code, simple DRY, pruning single-use indirection, reducing stutter)
- **Let's discuss**: Talk through the situation to determine the right level

The workflow still proceeds from least aggressive to more aggressive - this setting determines how far up the ladder to climb before stopping.

### 3. Gather QA Instructions

**Ask the user:** "Are there any special verification steps for the QA agent? For example: visual checks, manual testing commands, specific scenarios to validate."

**If provided:** Pass these instructions to the QA agent on every verification cycle, in addition to standard test suite execution.

**Examples of custom QA instructions:**
- "After each change, start the app, take a screenshot, and verify it renders correctly"
- "Run `make demo` and check that output matches expected behavior"
- "Hit the `/health` endpoint and verify 200 response"
- "Verify the CLI still produces valid output for `./tool --help`"

**If none provided:** QA agent runs standard verification (test suite, linters, formatters).

### 4. Aggression Philosophy

**Always make the least aggressive change available, up to the user's chosen ceiling (step 2).**

The `swe-code-reviewer` agent returns recommendations organized by risk level: **SAFEST → SAFE → MODERATE → AGGRESSIVE**. These aren't gates to pass through sequentially. Instead:
- Each pass, prefer the least aggressive changes available
- More aggressive changes naturally "bubble up" as gentler options are exhausted
- Stop when reaching the user's ceiling (e.g., if ceiling is High/MODERATE, skip AGGRESSIVE recommendations)
- Earlier refactorings may unlock new gentle changes (rescan catches these)

### 5. Iterative Refactoring Loop

For each iteration:

#### 5a. Scan for Opportunities

**Spawn fresh `swe-code-reviewer` agent:**
- Agent performs FULL scan across all aggression levels
- Pass scope if user specified one
- Agent returns structured recommendations organized by risk level
- Fresh instance each pass (context management)

**Why full scan every time:**
- Refactoring creates new opportunities (consolidating duplicates may reveal higher-order patterns)
- Cascading improvements are the goal
- Fresh scan catches what previous changes unlocked

**Prompt the agent with:**
```
Scan for ALL refactoring opportunities across all aggression levels.
Scope: [entire codebase | user-specified scope]
Return recommendations organized by risk level (SAFEST → AGGRESSIVE).
Prioritize changes that produce RED diffs (net code reduction) while improving clarity.
```

**Orchestrator selects least aggressive changes:**
- From the full scan, select the LEAST aggressive recommendations available
- Batch and implement those
- Rescan - previous changes may have unlocked new gentle options
- Aggressive changes naturally surface as gentler ones are exhausted
- If no recommendations at any level: workflow complete

**Set aside user-decision items:**
- **Commented-out code**: Do not implement. Collect findings across all passes.
- **Informational findings** (unused public APIs): Do not implement. Collect across all passes.
- Present both to the user in the completion summary (step 6).

#### 5b. Plan Implementation

Review recommendations from scan. Group related changes into atomic batches.

**Batching criteria:**
- Changes to the same module/package
- Logically related refactorings (e.g., all DRY violations of the same pattern)
- Changes that must be done together to maintain consistency

**For each batch, prepare:**
- Clear list of changes to make
- Files affected
- Expected outcome (lines removed, patterns eliminated)
- Which SME agent is appropriate (based on language/framework)

#### 5c. Implement Changes

**Detect appropriate SME and spawn based on primary file type in batch:**
- Go: `swe-sme-golang`
- Dockerfile: `swe-sme-docker`
- Makefile: `swe-sme-makefile`
- GraphQL: `swe-sme-graphql`
- Ansible: `swe-sme-ansible`
- Zig: `swe-sme-zig`

**For languages without a dedicated SME** (Python, JavaScript, Rust, etc.): implement directly as orchestrator, following language idioms and project conventions.

**For mixed-language batches**: split into per-language batches, or implement directly if changes are mechanical (e.g., dead code removal across file types).

**Prompt the SME with:**
```
Implement the following refactorings:
[List of specific changes from batch]

These changes should:
- Follow existing project conventions
- Maintain all existing behavior
- Result in net code reduction where possible

Report when complete.
```

**SME implements and reports back.**

#### 5d. Verify Changes

**Spawn `qa-engineer` agent:**
- Run test suite
- Run linters/formatters
- Execute any custom QA instructions gathered in step 3
- Verify no regressions introduced
- Report pass/fail with specifics

**On PASS:** Proceed to commit.

**On FAIL:**
1. Return failure details to SME for repair
2. SME attempts fix
3. Re-verify with QA
4. Track failure count for this batch

**After 3 consecutive failures for a batch:**
- Revert all changes for that batch (`git checkout -- .`)
- Log the failure (what was attempted, why it failed)
- Continue with next batch
- Include in final summary as "aborted batch"

#### 5e. Commit Changes

**Create atomic commit for successful batch:**

```bash
git add [specific files modified in this batch]
git diff --staged  # verify only intended changes
git commit -m "$(cat <<'EOF'
refactor: [brief description of changes]

[Details of what was refactored and why]

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Commit guidelines:**
- Stage only files modified by the current batch (not `git add -A`)
- Verify staged changes before committing
- Use `refactor:` prefix in commit message
- Keep batches atomic (one logical change per commit)

#### 5f. Loop

Return to step 5a with fresh agent instance.

**Loop continues until:**
- No opportunities found at any aggression level (success)
- User interrupts
- Critical error

### 6. Completion Summary

When workflow completes, present summary:

```
## Refactoring Complete

### Statistics
- Commits made: N
- Net lines changed: -XXX (target: negative)
- Batches completed: N
- Batches aborted: N

### Changes by Category
- Dead code removal: N instances
- DRY consolidation: N instances
- [etc.]

### Aborted Batches (if any)
- [Batch description]: [reason for failure]
```

**Then present user-decision items** collected across all passes:

**Commented-out code:** List each location and what the code appears to be (debugging helper, disabled feature, TODO, etc.). Ask the user which, if any, should be deleted. Implement deletions for the items the user selects.

**Apparently-unused public APIs:** List each symbol and location. Note that these may be consumed by external users of the package. These are informational only — do not offer to delete them.

### 7. Update Documentation

After the refactoring summary, run the `/review-doc` workflow to bring project documentation up to date. Even tactical refactoring can rename functions, move code between files, and change APIs — documentation that references the old state becomes stale.

Invoke the skill directly:
```
/review-doc
```

This spawns a doc-maintainer agent that audits all project documentation and fixes issues it finds. Any changes are committed separately from the refactoring commits.

## Agent Coordination

**Fresh instances for context management:**
- Spawn NEW `swe-code-reviewer` agent for each scan pass
- This prevents context accumulation in the scanner
- Orchestrator (you) maintains only summary state

**Sequential execution:**
- One agent at a time
- Wait for completion before spawning next
- No parallel agent execution

**State to maintain (as orchestrator):**
- Completed batches (brief log)
- Aborted batches (with reasons)
- Failure count per active batch
- Running totals for summary
- Commented-out code findings (accumulated across passes, for user review)
- Informational findings (unused public APIs, accumulated across passes)

## Abort Conditions

**Abort current batch:**
- 3 consecutive QA failures
- Revert changes, log failure, continue with next batch

**Abort entire workflow:**
- User interrupts
- Git repository in unclean state that can't be resolved
- Critical system error

**Agent failures:**
- Spawn failure: retry once, then abort workflow with error
- Malformed output: log issue, skip batch, continue
- Timeout: treat as failure, apply retry logic

**Do NOT abort for:**
- Individual batch failures (skip and continue)
- Warnings from linters (fix or note, don't abort)

## Integration with Other Skills

**Relationship to `/review-arch`:**
- `/refactor` is a tactical workflow for code quality improvements within existing architecture
- `/review-arch` is a strategic workflow that questions and restructures the architecture itself (noun analysis, module boundaries, blueprints)
- Use `/refactor` for routine cleanup; use `/review-arch` when the module structure itself needs rethinking

**Relationship to `/implement`:**
- `/implement` is a feature development workflow that optionally invokes `swe-code-reviewer` for code review after implementation
- `/refactor` is a dedicated refactoring workflow that uses `swe-code-reviewer` as its core scanner in an autonomous loop
- Same agent, different workflows: one-shot review vs. iterative improvement

**Relationship to `/scope`:**
- `/scope` explores and creates tickets
- `/refactor` implements improvements autonomously
- Could use `/scope` first to plan a large refactoring, then `/refactor` to execute

## Example Session

```
> /refactor

Scope: entire codebase

How aggressive should refactoring be?
> High (up to MODERATE changes)

Any special QA instructions?
> Run `make test && make lint` after each change

Starting iterative refactoring...

[Pass 1]
Spawning swe-code-reviewer agent for scan...
Found opportunities across levels:
  SAFEST: 8 dead code blocks (Prune), 2 lint failures
  SAFE: 3 DRY violations
  MODERATE: 1 cross-module DRY opportunity
Selecting least aggressive: dead code + lint (SAFEST)
Spawning swe-sme-golang for implementation...
Implementation complete.
Spawning qa-engineer for verification...
All tests pass.
Committed: "refactor: remove dead code and fix lint issues"

[Pass 2]
Spawning swe-code-reviewer agent for scan...
Found opportunities across levels:
  SAFEST: (none)
  SAFE: 3 DRY violations, 1 single-use wrapper (Prune)
  MODERATE: 1 cross-module DRY opportunity
Selecting least aggressive: DRY + prune (SAFE)
Spawning swe-sme-golang for implementation...
Implementation complete.
Spawning qa-engineer for verification...
Test failure: TestParseConfig
Returning to swe-sme-golang for repair (attempt 1/3)...
Repair complete.
Spawning qa-engineer for verification...
All tests pass.
Committed: "refactor: consolidate duplicate parsing logic"

[Pass 3]
Spawning swe-code-reviewer agent for scan...
Found opportunities across levels:
  SAFEST: 1 new dead code block exposed by DRY consolidation (Prune)
  SAFE: (none)
  MODERATE: 1 cross-module DRY opportunity
Selecting least aggressive: dead code (SAFEST)
...

[Passes 4-7...]

[Pass 8]
Spawning swe-code-reviewer agent for scan...
No opportunities found at any level.

## Refactoring Complete

### Statistics
- Commits made: 7
- Net lines changed: -312
- Batches completed: 7
- Batches aborted: 0

### Changes by Category
- Prune (dead code, unused indirection): 11 instances
- DRY consolidation: 5 instances
- Lint fixes: 2 instances

Running /review-doc to update documentation...

Spawning doc-maintainer agent...
  No documentation changes needed.
```
