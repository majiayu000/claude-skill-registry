---
name: github-elements-tracking
description: This skill should be used when the user asks to "track work across sessions", "create an epic", "manage issue waves", "post a checkpoint", "claim an issue", "recover from compaction", "coordinate multiple agents", "update memory bank", "store large documents", or mentions GitHub Issues as persistent memory, multi-session work, context survival, agent collaboration, SERENA MCP memory, or project-level context. Provides complete protocols for using GitHub Issues as permanent memory that survives context exhaustion, with integrated SERENA MCP memory bank for project-level context and large document storage.
---

## IRON LAW: User Specifications Are Sacred

**THIS LAW IS ABSOLUTE AND ADMITS NO EXCEPTIONS.**

1. **Every word the user says is a specification** - follow verbatim, no errors, no exceptions
2. **Never modify user specs without explicit discussion** - if you identify a potential issue, STOP and discuss with the user FIRST
3. **Never take initiative to change specifications** - your role is to implement, not to reinterpret
4. **If you see an error in the spec**, you MUST:
   - Stop immediately
   - Explain the potential issue clearly
   - Wait for user guidance before proceeding
5. **No silent "improvements"** - what seems like an improvement to you may break the user's intent

**Violation of this law invalidates all work produced.**

## Background Agent Boundaries

When running as a background agent, you may ONLY write to:
- The project directory and its subdirectories
- The parent directory (for sub-git projects)
- ~/.claude (for plugin/settings fixes)
- /tmp

Do NOT write outside these locations.

---

## GHE_REPORTS Rule (MANDATORY)

**ALL agent reports MUST be posted to BOTH locations:**

1. **GitHub Issue Thread** - Full report text (NOT just a link!)
2. **GHE_REPORTS/** - Same full report text (FLAT structure, no subfolders!)

**Report naming:** `<TIMESTAMP>_<title or description>_(<AGENT>).md`
**Timestamp format:** `YYYYMMDDHHMMSSTimezone`

**Examples:**
- `20251206143000GMT+01_epic_15_wave_launched_(Athena).md`
- `20251206143022GMT+01_issue_42_dev_complete_(Hephaestus).md`
- `20251206150000GMT+01_issue_42_tests_passed_(Artemis).md`
- `20251206160000GMT+01_issue_42_review_complete_(Hera).md`

**ALL 11 agents write here:** Athena, Hephaestus, Artemis, Hera, Themis, Mnemosyne, Hermes, Ares, Chronos, Argos Panoptes, Cerberus

**REQUIREMENTS/** is SEPARATE - permanent design documents with legal validity, NEVER deleted.

**Deletion Policy:**
- GHE_REPORTS should be git-tracked - it constitutes the pulse of the GHE plugin
- DELETE ONLY when user EXPLICITLY orders deletion due to space constraints
- DO NOT delete during normal project cleanup or just because reports were archived to GitHub

---

## Project Settings

This skill respects settings in `.claude/ghe.local.md`. Run `/ghe:setup` to configure.

| Setting | Effect on This Skill |
|---------|---------------------|
| `enabled` | If false, skip all GitHub Elements operations |
| `enforcement_level` | strict/standard/lenient - affects rule strictness |
| `serena_sync` | If false, skip SERENA memory bank integration |
| `auto_worktree` | If true, auto-create git worktree on claim |
| `checkpoint_interval_minutes` | Reminder interval for checkpoints |
| `notification_level` | verbose/normal/quiet output |

**Defaults** (no settings file): enabled=true, enforcement=standard, serena_sync=true

---

## Related GHE Skills

For specific operations, GHE provides specialized skills:

| Skill | Purpose |
|-------|---------|
| **ghe-requirements** | Create, version, and link requirements files. Use when starting features. |
| **ghe-changelog** | Maintain version history with git-diff. Track code, requirements, and design changes. |
| **ghe-status** | Check thread status and context |
| **ghe-claim** | Claim a thread for work |
| **ghe-checkpoint** | Post progress checkpoints |
| **ghe-transition** | Request phase transitions |
| **ghe-report** | Generate status reports |

### Key Workflows

**Starting a New Feature:**
1. Use **ghe-requirements** to create REQ file
2. Link requirements to DEV issue
3. Use **ghe-claim** to claim the thread
4. Follow TDD workflow from DEV manager

**Tracking Changes:**
1. Use **ghe-changelog** after significant commits
2. Updates automatically track requirements and code changes

**Requirements-First Development:**
All DEV threads MUST link to a requirements file. The DEV manager (Hephaestus) enforces:
- Requirements breakdown into atomic changes
- TDD cycle for each atomic change (RED-GREEN-REFACTOR)
- Test coverage verification before transition

---

# GitHub Elements Tracking

GitHub Issues as **permanent memory** for AI agents. Survives compaction, enables collaboration, provides complete traceability.

**Integrated with SERENA MCP memory bank** for project-level context and large document storage beyond GitHub's limits.

---

## FUNDAMENTAL PRINCIPLES (READ FIRST)

These principles are non-negotiable. Violating them corrupts the entire workflow.

### 1. THE SACRED ORDER: One Branch, One Phase at a Time

Each branch goes through phases in strict circular order:

```
DEV ───► TEST ───► REVIEW ───► DEV ───► ... (until REVIEW passes)
         │           │
         │           └─► PASS? → merge to main
         │
    Bug fixes ONLY (no structural changes, no new tests)
```

**Critical Rules:**
- **ONE phase thread open at a time** per branch
- Opening TEST = closing DEV
- Opening REVIEW = closing TEST
- REVIEW fail → back to DEV (NEVER to TEST)
- REVIEW pass → merge to main

### 2. NEW BUG REPORT = NEW BRANCH (ALWAYS)

When a bug report is posted as a **new GitHub issue**:
- ALWAYS create a NEW branch with NEW DEV → TEST → REVIEW cycle
- NEVER merge it into an existing review thread, even if related
- Mixing issues violates the Sacred Order

**Exception**: Comments posted directly IN an existing thread are handled within that thread.

### 3. RESPONSIBILITY BOUNDARIES

| Agent | Handles Bug Reports? | Handles Test Writing? | Renders Verdicts? |
|-------|---------------------|----------------------|-------------------|
| **DEV** | NO (creates new branches for validated bugs) | YES | NO |
| **TEST** | NO (only runs existing tests) | NO | NO |
| **REVIEW** | YES (triages ALL bug reports) | NO | YES |

**REVIEW handles ALL bug reports and quality evaluation. TEST only runs existing tests.**

### 4. THE 3-STRIKE RULE FOR BUG REPORTS

When a bug report cannot be reproduced:
1. **Strike 1**: Politely ask for more details
2. **Strike 2**: Politely ask again with specific questions
3. **Strike 3**: Politely close as "cannot-reproduce"

**ALWAYS be polite**, even when closing. Thank the reporter for their effort.

### 5. EVERY CONTRIBUTION IS VALUED

- Never dismiss a contribution as "nitpick" or "pedantic"
- Verify everything, assume nothing
- If valid, thank the contributor regardless of size
- Reply respectfully even when rejecting

---

## Terminology

Understanding the relationship between GitHub entities and workflow concepts:

| Term | Definition |
|------|------------|
| **Issue** | A GitHub Issue - the container/ticket that holds all work history |
| **Thread** | A phase-specific issue. A "DEV thread" is an issue labeled `phase:dev` |
| **Comment** | A reply within an issue - holds checkpoints, decisions, work logs |
| **Element** | A comment containing Knowledge, Action, and/or Judgement facets |

**Key insight**: Every thread IS an issue. The terms describe the same GitHub entity from different perspectives:
- "Issue" emphasizes the GitHub container (the thing with a number like #201)
- "Thread" emphasizes the phase role (DEV, TEST, or REVIEW work)

**Example**: Issue #201 labeled `phase:dev` is the "DEV thread" for JWT authentication. When DEV completes, issue #201 closes and issue #202 (labeled `phase:test`) opens as the "TEST thread" for the same feature.

**One thread per phase**: Each phase (DEV, TEST, REVIEW) gets its own issue. When phase transitions occur, the old issue closes and a new issue opens with the new phase label.

### Thread Naming Convention

All thread titles MUST follow this standard format:

| Thread Type | Title Format | Example |
|-------------|--------------|---------|
| **DEV** | `[DEV] #ISSUE - Short Description` | `[DEV] #201 - JWT Authentication` |
| **TEST** | `[TEST] #ISSUE - Short Description` | `[TEST] #201 - JWT Authentication` |
| **REVIEW** | `[REVIEW] #ISSUE - Short Description` | `[REVIEW] #201 - JWT Authentication` |
| **DEV (iteration)** | `[DEV] #ISSUE - Description (Iteration N)` | `[DEV] #201 - JWT Auth (Iteration 2)` |

**Rules:**
- Prefix with phase in brackets: `[DEV]`, `[TEST]`, `[REVIEW]`
- Include original issue number after prefix
- Keep description short (under 50 chars)
- For iterations after demotion, append iteration number

### Thread Message Structure

> **Reference**: See [references/templates/issue-comment-format.md](references/templates/issue-comment-format.md) for detailed comment formatting templates with avatar URLs and examples.

**CRITICAL**: The first message (issue body) is an INDEX, not a changelog. Updates go in REPLIES.

#### First Message (Issue Body) = Living Index

The first message should contain:

| Section | Content | How to Update |
|---------|---------|---------------|
| **Objective** | What this thread accomplishes | Rarely changes |
| **Scope** | Files to modify, files NOT to modify | Add items, don't remove |
| **Checklist** | Tasks with checkboxes | Check boxes as completed, add new tasks |
| **Key References** | Links to significant replies | Add links as contributions arrive |
| **Artifacts** | Links to PRs, reports, docs, scripts | Add links when created |

**First Message Template:**
```markdown
## Objective
<what this thread accomplishes>

## Scope
Files to modify:
- [ ] path/to/file1.ts
- [ ] path/to/file2.ts

Files NOT to modify:
- path/to/other.ts (belongs to #203)

## Progress Checklist
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Key Contributions
| What | Where | By |
|------|-------|-----|
| Initial design | [#comment-1](#issuecomment-XXX) | @agent-1 |
| Implementation | [#comment-5](#issuecomment-YYY) | @agent-2 |

## Artifacts
- PR: (pending)
- Test report: (pending)
- Documentation: (pending)
```

#### Replies = Chronological Updates

All work updates go in replies, NOT in edits to the first message:

```markdown
## [Session N] 2025-01-15 14:30 UTC - @agent-name

### Work Completed
- Implemented validateToken function
- Added unit tests for edge cases

### Files Changed
| File | Changes |
|------|---------|
| src/auth/jwt.ts | +45 lines (new function) |

### Commits
- abc1234: Add JWT validation

### References
- Relates to decision in [#comment-3](#issuecomment-XXX)

### Next Action
Integrate with middleware
```

#### Every Change Gets a Reply

**CRITICAL**: Every action must be documented in a reply. The thread is the complete record of the endeavor - like a chat history. Subscribers must be able to follow along by reading replies.

| Action | What to Do |
|--------|------------|
| Mark checkbox complete | 1. Edit first message to check box 2. **Post reply** explaining what was completed |
| Add new task to checklist | 1. Edit first message to add task 2. **Post reply** explaining why task was added |
| Add link to contribution | 1. Edit first message to add link 2. **Post reply** explaining the contribution |
| Add artifact link (PR, report) | 1. Edit first message to add link 2. **Post reply** announcing the artifact |
| Work progress | **Post reply** with details |
| Checkpoint | **Post reply** with state snapshot |
| Decision made | **Post reply** documenting decision and rationale |
| Blocker encountered | **Post reply** explaining blocker |
| Test results | **Post reply** with results |

**Example - Completing a Task:**

```markdown
## Task Completed

Marked `[x] Implement validateToken function` in the index.

### What Was Done
- Added validateToken() to src/auth/jwt.ts
- Handles RS256 signature verification
- Returns decoded payload or throws AuthError

### Commit
- abc1234: Add JWT token validation

### Next
Proceeding to integrate with middleware.
```

**Golden Rule**: The thread is the single source of truth. Every change, including index edits, gets announced in a reply so subscribers can follow along.

---

## Prerequisites and Tools

### Required Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| `gh` | GitHub CLI - all issue/PR operations | `brew install gh` then `gh auth login` |
| `git` | Version control, worktrees, branches | Usually pre-installed |
| `jq` | JSON parsing for `gh` command output | `brew install jq` |

### Required: SERENA MCP

SERENA MCP is **required** for large document storage and project memory. Without it, agents cannot store documents exceeding GitHub's 64KB limit or maintain project-level context.

#### SERENA MCP Installation

**Step 1: Create Installation Script**

Create `install-serena.sh` in the project root:

```bash
#!/bin/bash
# SERENA MCP Installation Script
set -e

PROJECT_DIR=$(pwd)
echo "Installing SERENA MCP for project: $PROJECT_DIR"
echo ""

# Step 1: Add SERENA MCP server to Claude Code
echo "[1/4] Adding SERENA MCP server..."
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project "$PROJECT_DIR"
echo "✓ Complete"
echo ""

# Step 2: Create SERENA project configuration
echo "[2/4] Creating SERENA project configuration..."
echo "Supported: csharp, python, rust, java, kotlin, typescript, go, ruby, dart, cpp, php, r, perl, clojure, elixir, elm, terraform, swift, bash, zig, lua, nix, erlang, al, rego, scala, julia, fortran, haskell, markdown, yaml"
echo ""
read -p "Enter languages to index (space-separated): " languages

lang_flags=""
for lang in $languages; do
    lang_flags="$lang_flags --language $lang"
done

uvx --from git+https://github.com/oraios/serena serena project create $lang_flags
echo "✓ Complete"
echo ""

# Step 3: Index the project codebase
echo "[3/4] Indexing project codebase..."
uvx --from git+https://github.com/oraios/serena serena project index
echo "✓ Complete"
echo ""

echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. RESTART Claude Code"
echo "2. After restart, tell Claude: 'Activate the current dir as project using serena mcp'"
echo ""
```

**Step 2: Run Installation**
```bash
chmod +x install-serena.sh
# Exit Claude Code first!
./install-serena.sh
# Restart Claude Code
```

**Step 3: Activate SERENA**

After restarting Claude Code, tell Claude:
```
Activate the current dir as project using serena mcp
```

### Verify Installation

```bash
# Check all tools are available
gh --version && git --version && jq --version

# Verify GitHub authentication
gh auth status

# Verify SERENA is active (after activation)
# The mcp__serena__* tools should be available
```

---

## MANDATORY: Git Worktrees for All Phase Work

### Why Worktrees Are REQUIRED

**CRITICAL**: ALL phase work (DEV, TEST, REVIEW) MUST happen in isolated git worktrees. Working on main is FORBIDDEN.

When multiple agents work on different phases (DEV, TEST, REVIEW), they need **separate working directories** to avoid conflicts. Git worktrees allow multiple checkouts from a single repository.

**Problem without worktrees:**
```
Agent-1 (DEV): Working on feature/auth branch
Agent-2 (TEST): Needs to checkout testing/auth branch
→ CONFLICT: Only one branch can be checked out at a time
```

**Solution with worktrees:**
```
main-repo/           ← Main repository (can be on main branch)
├── .git/
└── worktrees/
    ├── dev-auth/    ← DEV thread: feature/auth branch
    ├── test-auth/   ← TEST thread: testing/auth branch
    └── review-auth/ ← REVIEW thread: review/auth branch
```

### Worktree Setup for Threads

**Standard Worktree Location**: `../ghe-worktrees/issue-{N}/`

```bash
ISSUE_NUM=<issue number>

# Step 1: Create worktree directory
mkdir -p ../ghe-worktrees

# Step 2: Create worktree with new branch
git worktree add ../ghe-worktrees/issue-${ISSUE_NUM} -b issue-${ISSUE_NUM} main

# Step 3: Switch to worktree
cd ../ghe-worktrees/issue-${ISSUE_NUM}

# Step 4: Verify branch
git branch --show-current  # Should output: issue-${ISSUE_NUM}
```

### MANDATORY: Verify Worktree Before Any Work

**Every agent MUST run this check before starting any work:**

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# BLOCK if on main
if [ "$CURRENT_BRANCH" == "main" ]; then
  echo "ERROR: Work on main is FORBIDDEN!"
  echo "Create worktree: git worktree add ../ghe-worktrees/issue-N -b issue-N main"
  exit 1
fi

# Verify we're in a worktree
if [ ! -f .git ]; then
  echo "WARNING: Not in a worktree. Should be in ../ghe-worktrees/issue-N/"
fi

echo "Phase work running in branch: $CURRENT_BRANCH"
```

### Legacy Worktree Setup (Alternative)

```bash
# Initial setup: Create worktrees directory
mkdir -p worktrees

# Create worktree for DEV thread
git worktree add worktrees/dev-$FEATURE feature/$FEATURE

# Create worktree for TEST thread (after DEV completes)
git worktree add worktrees/test-$FEATURE testing/$FEATURE

# Create worktree for REVIEW thread (after TEST completes)
git worktree add worktrees/review-$FEATURE review/$FEATURE

# List all worktrees
git worktree list

# Remove worktree when phase is complete
git worktree remove worktrees/dev-$FEATURE
```

### Branch Naming Convention

| Thread Type | Branch Pattern | Example |
|-------------|----------------|---------|
| DEV | `feature/<issue>-<slug>` | `feature/201-jwt-auth` |
| TEST | `testing/<issue>-<slug>` | `testing/201-jwt-auth` |
| REVIEW | `review/<issue>-<slug>` | `review/201-jwt-auth` |

### Worktree Commands for Agents

**DEV Agent starting work:**
```bash
ISSUE=201
SLUG="jwt-auth"
FEATURE="${ISSUE}-${SLUG}"

# Create feature branch and worktree
git checkout -b feature/$FEATURE main
git worktree add worktrees/dev-$FEATURE feature/$FEATURE

# Work in the worktree
cd worktrees/dev-$FEATURE
# ... do development work ...
```

**TEST Agent claiming TEST thread:**
```bash
# Verify DEV worktree is removed (phase complete)
git worktree list | grep dev-$FEATURE && echo "ERROR: DEV worktree still exists"

# Create testing branch from feature branch
git checkout feature/$FEATURE
git checkout -b testing/$FEATURE
git worktree add worktrees/test-$FEATURE testing/$FEATURE

# Work in TEST worktree
cd worktrees/test-$FEATURE
# ... run tests, fix bugs ...
```

**REVIEW Agent starting review:**
```bash
# Create review branch from testing branch
git checkout testing/$FEATURE
git checkout -b review/$FEATURE
git worktree add worktrees/review-$FEATURE review/$FEATURE

# Work in REVIEW worktree (read-only, no code changes)
cd worktrees/review-$FEATURE
# ... evaluate code ...
```

### Worktree Lifecycle

| Phase Transition | Worktree Action |
|------------------|-----------------|
| Claim DEV | `git worktree add ../ghe-worktrees/issue-N -b issue-N main` |
| DEV → TEST | Stay in same worktree (same branch) |
| TEST → REVIEW | Stay in same worktree (same branch) |
| REVIEW PASS | 1. Save review to `GHE_REPORTS/` 2. Commit 3. Create PR 4. Merge 5. Remove worktree |
| REVIEW FAIL | 1. Save review to `GHE_REPORTS/` 2. Commit 3. Stay in worktree 4. Back to DEV |

**Key insight**: All phases (DEV, TEST, REVIEW) work in the SAME worktree/branch. The worktree is only removed after REVIEW PASS and successful merge to main.

### Cleanup Commands

```bash
# Prune stale worktrees (after worktree directory deleted)
git worktree prune

# Force remove a worktree
git worktree remove --force worktrees/dev-$FEATURE

# List and clean all worktrees for a feature
for wt in dev test review; do
  git worktree remove worktrees/${wt}-$FEATURE 2>/dev/null
done
```

---

## GHE_REPORTS Directory

### Purpose

The `GHE_REPORTS/` directory stores all REVIEW phase verdict reports. These reports:
- Document the quality evaluation process
- Travel with the code (committed to feature branch)
- Provide audit trail for approvals/rejections
- Merge with approved code or stay in rejected branches

### Directory Location

```
project-root/
├── GHE_REPORTS/
│   ├── README.md
│   ├── issue-1-review.md
│   ├── issue-2-review.md
│   └── ...
```

### Report Naming Convention

```
issue-{N}-review.md
```

Where `{N}` is the original issue number being reviewed.

### Report Template

```markdown
# REVIEW Report: Issue #{N}

## Metadata
- **Issue**: #{N} - {Title}
- **Reviewer**: {Agent/User}
- **Date**: {YYYY-MM-DD}
- **Branch**: issue-{N}

## Verdict: {PASS | FAIL}

## Requirements Checklist
- [x] Requirement 1
- [x] Requirement 2
- [ ] Requirement 3 (if FAIL)

## Code Quality Assessment

### Architecture
{Assessment}

### Testing
{Assessment}

### Security
{Assessment}

### Performance
{Assessment}

## Test Results Summary
| Suite | Passed | Failed | Coverage |
|-------|--------|--------|----------|
| Unit | X | Y | Z% |
| Integration | X | Y | Z% |

## Issues Found
{If FAIL: List all issues requiring attention}

## Reviewer Notes
{Any additional observations}

## Approval Status
{If PASS: Approved for merge}
{If FAIL: Requires return to DEV with issues listed above}
```

### Report Timing (Critical)

**IMPORTANT**: Reviews are created **BEFORE** the merge decision:

1. **Create report** in feature branch (`issue-{N}`)
2. **Commit report** to the feature branch
3. **Push branch** to remote
4. **If PASS**: Create PR, merge to main (report travels with code)
5. **If FAIL**: Report stays in rejected branch (doesn't pollute main)

### Why Before Merge?

| Timing | Pros | Cons |
|--------|------|------|
| **Before merge (in feature branch)** | Report travels with code; rejected reports don't pollute main; complete audit trail | Requires commit before merge |
| After merge (in main) | Simpler workflow | Rejected reviews pollute main; breaks audit trail |

**Decision**: Save reviews **in feature branch BEFORE merge**. This ensures:
- Only approved code AND its review reach main
- Rejected code's review stays with the rejected branch
- Complete traceability of what was approved and why

### REVIEW PASS Workflow with Report

```bash
ISSUE_NUM=<issue number>
REVIEW_DATE=$(date +%Y-%m-%d)

# 1. Verify in correct worktree
cd ../ghe-worktrees/issue-${ISSUE_NUM}

# 2. Create GHE_REPORTS directory if needed
mkdir -p GHE_REPORTS

# 3. Write review report
cat > GHE_REPORTS/issue-${ISSUE_NUM}-review.md << 'EOF'
# REVIEW Report: Issue #${ISSUE_NUM}
...
## Verdict: PASS
...
EOF

# 4. Commit the review
git add GHE_REPORTS/issue-${ISSUE_NUM}-review.md
git commit -m "Add REVIEW report for issue #${ISSUE_NUM} - PASS"

# 5. Push feature branch
git push origin issue-${ISSUE_NUM}

# 6. Create PR
gh pr create --title "Issue #${ISSUE_NUM} - Feature Implementation" \
  --body "Closes #${ISSUE_NUM}

## Review Report
See: GHE_REPORTS/issue-${ISSUE_NUM}-review.md

## Verdict: PASS"

# 7. Merge PR
gh pr merge --squash

# 8. Clean up worktree
cd ..
git worktree remove issue-${ISSUE_NUM}
```

---

## Merge Coordination Protocol

### The Problem: Parallel Agents Completing Simultaneously

When multiple agents finish REVIEW with PASS verdicts at similar times, they may all attempt to merge to main simultaneously. This creates:

1. **Race Conditions**: Two agents try to merge at the same moment
2. **Merge Conflicts**: Agent-B's merge fails because Agent-A just changed main
3. **Cascading Failures**: Failed merges require rebase, which invalidates the REVIEW PASS

### The Critical Insight

```
REVIEW PASS (before rebase) ≠ REVIEW PASS (after rebase)
```

**Why?** Rebasing changes the code context. The code that was reviewed is NOT the same code after rebase. New conflicts may introduce bugs, logic changes, or break assumptions that led to PASS.

**Therefore: Any rebase MUST be followed by re-running TEST validations before merge.**

### Pre-Merge Protocol (MANDATORY)

Before any merge to main, execute this protocol:

```bash
ISSUE_NUM=<issue number>
MAX_ATTEMPTS=3
attempt=0

while [ $attempt -lt $MAX_ATTEMPTS ]; do
    # Step 1: Fetch latest main
    git fetch origin main

    # Step 2: Check if behind main
    BEHIND=$(git rev-list --count HEAD..origin/main)

    if [ "$BEHIND" -eq 0 ]; then
        echo "Branch is up to date with main - safe to merge"
        break
    fi

    echo "Branch is $BEHIND commits behind main - rebasing..."

    # Step 3: Attempt rebase
    if ! git rebase origin/main; then
        git rebase --abort
        echo "REBASE CONFLICT: Manual resolution required"
        echo "DEMOTE TO DEV: Cannot auto-resolve conflicts"
        exit 1
    fi

    echo "Rebase successful - RE-RUNNING TEST validations..."

    # Step 4: RE-RUN TEST (CRITICAL - code context changed!)
    # Run project-specific tests here
    if ! ./run-tests.sh; then
        echo "TESTS FAILED after rebase"
        echo "DEMOTE TO DEV: Code no longer passes tests after rebase"
        exit 1
    fi

    # Step 5: Force push the rebased branch
    if ! git push origin issue-${ISSUE_NUM} --force-with-lease; then
        echo "Push failed - another change occurred, retrying..."
        attempt=$((attempt + 1))
        continue
    fi

    echo "Branch rebased and pushed successfully"
    break
done

if [ $attempt -ge $MAX_ATTEMPTS ]; then
    echo "DEMOTE TO DEV: Max rebase attempts ($MAX_ATTEMPTS) exceeded"
    echo "High contention detected - requires manual coordination"
    exit 1
fi
```

### Merge Lock Mechanism (Optional - For High Contention)

For repositories with frequent parallel merges, use a lock mechanism:

```bash
# Check if merge lock exists
check_merge_lock() {
    gh issue list --label "merge:active" --state open --json number | jq '. | length'
}

# Wait for lock (with timeout)
wait_for_lock() {
    local timeout=900  # 15 minutes
    local start=$(date +%s)

    while [ $(check_merge_lock) -gt 0 ]; do
        local now=$(date +%s)
        local elapsed=$((now - start))

        if [ $elapsed -gt $timeout ]; then
            echo "Lock timeout exceeded - forcing lock release"
            release_stale_locks
            break
        fi

        echo "Merge in progress by another agent, waiting... ($elapsed/$timeout sec)"
        sleep 30
    done
}

# Acquire lock
acquire_lock() {
    gh issue edit $ISSUE_NUM --add-label "merge:active"
    echo "Merge lock acquired for issue #$ISSUE_NUM"
}

# Release lock
release_lock() {
    gh issue edit $ISSUE_NUM --remove-label "merge:active"
    echo "Merge lock released for issue #$ISSUE_NUM"
}
```

### Priority: First-Come-First-Served (FCFS)

When multiple agents have REVIEW PASS:

1. **Priority = REVIEW PASS timestamp** (first to pass reviews, first to merge)
2. **No cutting in line** - later PASS waits for earlier PASS to merge
3. **Timeout protection** - if an agent holds lock > 15 min, lock is force-released

### Merge Coordination Summary

| Scenario | Action |
|----------|--------|
| Branch is up-to-date with main | Proceed to merge |
| Branch is behind main | Rebase → Re-run TEST → Then merge |
| Rebase has conflicts | DEMOTE TO DEV (cannot auto-resolve) |
| Tests fail after rebase | DEMOTE TO DEV (rebase broke something) |
| Max attempts exceeded | DEMOTE TO DEV (high contention) |
| Another merge in progress | Wait for lock release (max 15 min) |

### Loop Prevention

- **Max 3 rebase attempts** per merge session
- After 3 failed attempts → DEMOTE TO DEV
- Prevents infinite rebase loops when main is highly active

### Merge Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| **Merge without checking main** | Creates merge conflicts | Always `git fetch` first |
| **Skip TEST after rebase** | Reviewed code ≠ merged code | RE-RUN TEST after ANY rebase |
| **Force push without lease** | Can overwrite others' work | Use `--force-with-lease` |
| **Ignore rebase conflicts** | Broken code reaches main | DEMOTE TO DEV on conflicts |
| **No merge lock in high traffic** | Race conditions | Use `merge:active` label |
| **Hold merge lock indefinitely** | Blocks other agents | 15 min timeout max |
| **Retry forever on conflicts** | Infinite loop | Max 3 attempts then demote |

---

## Storage Tiering: Where to Store What

Agents need to store information at different scales and lifetimes. Use the appropriate tier:

### Three-Tier Storage Hierarchy

| Tier | Tool | Lifetime | Size Limit | Use Case |
|------|------|----------|------------|----------|
| **1. Transient** | TodoWrite | Session only | ~50 items | Current task tracking, local state |
| **2. Persistent** | GitHub Elements | Forever | 64KB/comment | Decisions, checkpoints, coordination |
| **3. Archive** | SERENA MCP | Project lifetime | No practical limit | Large docs, reports, references |

### Tier 1: TodoWrite (Transient)

**When to use:**
- Tracking current session tasks
- Local progress tracking
- Items that don't need to survive compaction
- Quick scratch notes

**Characteristics:**
- Lost on session end or compaction
- Fast to read/write
- No collaboration (single agent only)
- No external dependencies

**Example:**
```
[x] Read issue thread
[x] Verify branch exists
[ ] Fix bug in jwt.service.ts
[ ] Run tests
[ ] Post checkpoint
```

### Tier 2: GitHub Elements (Persistent)

**When to use:**
- Checkpoints that must survive compaction
- Decisions that affect other agents
- State that needs collaboration
- Content < 64KB per comment

**Characteristics:**
- Permanent (survives everything)
- Collaborative (multiple agents can read/write)
- Ordered history preserved
- Has size limits (see below)

**GitHub Limits:**

| Element | Limit | Notes |
|---------|-------|-------|
| Issue/Comment body | **65,536 characters** (64KB) | Hard limit, no exceptions |
| Issue title | 256 characters | Keep titles concise |
| Labels per issue | 50 | Use sparingly |
| API calls | 5,000/hour (authenticated) | Rarely a problem |

**When approaching limits:**
```markdown
## Checkpoint - Content Split Required

This checkpoint exceeds GitHub's 64KB limit.

### Summary (in GitHub)
<brief summary here>

### Full Content (in SERENA)
See SERENA memory: `checkpoint-201-session-5.md`

### Index
- Part 1: Test results (SERENA: test-results-201.md)
- Part 2: Coverage report (SERENA: coverage-201.md)
- Part 3: File changes (in this comment, below)
```

### Tier 3: SERENA MCP Memory (Archive)

**When to use:**
- Documents > 60KB (leave 4KB buffer for GitHub)
- Large test reports
- Extensive code examples
- Reference documentation
- Multi-part documents
- Project-level context that spans multiple issues

**Characteristics:**
- No practical size limit
- Project-scoped (persists with project)
- Requires SERENA MCP setup
- Slightly slower access

#### Memory Bank File Structure

The `.serena/memories/` folder contains structured files for different purposes:

| File | Purpose | Update Timing |
|------|---------|---------------|
| `activeContext.md` | Currently ongoing tasks | Task start/progress |
| `progress.md` | Completed work history | Task completion |
| `projectBrief.md` | Project overview | Scope changes |
| `techContext.md` | Technical decisions | Tech stack changes |
| `dataflow.md` | System data flow | Data structure changes |
| `test_results/` | Test reports | After test runs |

**File Purposes:**

1. **activeContext.md**
   - Record details of currently ongoing tasks
   - Only record in-progress tasks
   - Move completed tasks to `progress.md` with summary

2. **progress.md**
   - Record project progress chronologically
   - Add summary when major tasks complete
   - **Reverse chronological order** (newest on top)

3. **projectBrief.md**
   - Overall project overview
   - Update when goals or scope change
   - Core features and objectives

4. **techContext.md**
   - Technical context and decisions
   - Libraries, architecture patterns
   - Decision rationale

5. **dataflow.md**
   - System data flow documentation
   - Input/output structure
   - Data transformation processes

6. **test_results/**
   - Store test reports and validation data
   - Phase-specific reports
   - Performance benchmarks

#### Issue-Specific vs Project-Level Memory

| Memory Type | Storage | Naming Convention | Use Case |
|-------------|---------|-------------------|----------|
| **Project context** | Standard files | `activeContext.md`, `progress.md` | Spans all issues |
| **Issue-specific** | Custom files | `issue-201-checkpoint.md` | Single issue data |
| **Large documents** | Custom files | `report-201-full.md` | Exceeds GitHub 64KB |

**SERENA Memory Commands:**

```bash
# Write a memory (from agent perspective, use MCP tools)
# Tool: mcp__serena__write_memory
# Parameters:
#   memory_file_name: "checkpoint-201-full.md"
#   content: "<full content>"

# Read a memory
# Tool: mcp__serena__read_memory
# Parameters:
#   memory_file_name: "checkpoint-201-full.md"

# List available memories
# Tool: mcp__serena__list_memories

# Edit a memory (regex replacement)
# Tool: mcp__serena__edit_memory
# Parameters:
#   memory_file_name: "checkpoint-201-full.md"
#   needle: "old text"
#   repl: "new text"
#   mode: "literal"
```

### Document Splitting Protocol

When a document exceeds GitHub's 64KB limit:

**Step 1: Create Index in GitHub**
```markdown
## Large Document: <Title>

### Summary
<2-3 sentence summary>

### Document Index
| Part | Content | Location |
|------|---------|----------|
| 1 | Executive Summary | This comment |
| 2 | Detailed Analysis | SERENA: `analysis-201-part2.md` |
| 3 | Test Results | SERENA: `test-results-201.md` |
| 4 | Recommendations | SERENA: `recommendations-201.md` |

### Part 1: Executive Summary
<content that fits in GitHub>
```

**Step 2: Store Parts in SERENA**
```
# For each part that doesn't fit:
mcp__serena__write_memory(
  memory_file_name="analysis-201-part2.md",
  content="## Part 2: Detailed Analysis\n\n<full content>"
)
```

**Step 3: Cross-Reference**
- GitHub comment references SERENA memories
- SERENA memories reference GitHub issue number
- Never more than ONE level of indirection

### Decision Matrix: Which Tier?

| Question | Yes → Use | No → Next Question |
|----------|-----------|---------------------|
| Needed only this session? | **TodoWrite** | ↓ |
| Fits in 60KB? | **GitHub Elements** | ↓ |
| Larger than 60KB? | **SERENA MCP** | N/A |

| Question | Yes → Use | No → Use |
|----------|-----------|----------|
| Needs collaboration? | GitHub or SERENA | TodoWrite |
| Must survive compaction? | GitHub or SERENA | TodoWrite |
| Other agents need access? | GitHub or SERENA | TodoWrite |

---

## Memory Bank Integration with Thread Lifecycle

The memory bank (`.serena/memories/`) is updated at specific points during the DEV → TEST → REVIEW cycle. This ensures project context stays synchronized with issue progress.

### Thread Lifecycle → Memory Updates

| Thread Event | Memory Files to Update | Content |
|--------------|------------------------|---------|
| **DEV claim** | `activeContext.md` | Add: Issue #, scope, objectives |
| **DEV checkpoint** | `activeContext.md` | Update: progress, blockers |
| **DEV decision** | `techContext.md` | Add: technical decision + rationale |
| **DEV architecture** | `dataflow.md` | Update: data flow changes |
| **DEV complete** | `progress.md`, `activeContext.md` | Move task summary to progress |
| **TEST start** | `activeContext.md` | Add: TEST phase for issue # |
| **TEST results** | `test_results/` | Save: `test-<issue>-<date>.md` |
| **TEST complete** | `progress.md`, `activeContext.md` | Move test summary to progress |
| **REVIEW complete** | `progress.md` | Add: REVIEW verdict, merge status |
| **REVIEW fail** | `activeContext.md` | Add: DEV iteration with issues to fix |

### Memory Update Workflow

After completing meaningful work, follow this sequence:

**Step 1: Analyze Current Task**
- What was completed?
- Were there technical decisions?
- Were there data flow changes?
- Are there test results?

**Step 2: Determine Files to Update**

| Work Type | Memory Files |
|-----------|--------------|
| New feature work | `progress.md` |
| Tech stack changes | `techContext.md` |
| Data structure changes | `dataflow.md`, `techContext.md` |
| Test execution | `test_results/` |
| Project scope changes | `projectBrief.md` |
| Task in progress | `activeContext.md` |

**Step 3: Update Each File**

Use SERENA MCP tools:
```
# Read current content
mcp__serena__read_memory("activeContext.md")

# Edit with new content
mcp__serena__edit_memory(
  memory_file_name="activeContext.md",
  needle="## In Progress",
  repl="## In Progress\n\n### Issue #201 - JWT Authentication\n- Phase: DEV\n- Started: 2025-01-15\n- Scope: Implement JWT token validation",
  mode="literal"
)
```

**Step 4: Verify No Duplication**
- Same content should not appear in multiple files
- Each piece of information in the most appropriate file
- `progress.md` is reverse chronological (newest on top)

### Phase-Specific Memory Operations

#### DEV Thread Start
```
# Update activeContext.md
mcp__serena__edit_memory(
  memory_file_name="activeContext.md",
  needle="## In Progress",
  repl="""## In Progress

### Issue #${ISSUE} - ${TITLE}
- **Phase**: DEV
- **Started**: ${DATE}
- **Branch**: feature/${ISSUE}-${SLUG}
- **Scope**: ${SCOPE_DESCRIPTION}

#### Objectives
- ${OBJECTIVE_1}
- ${OBJECTIVE_2}
""",
  mode="literal"
)
```

#### DEV Thread Complete
```
# 1. Read current active context
content = mcp__serena__read_memory("activeContext.md")

# 2. Move completed task to progress.md (prepend - newest first)
mcp__serena__edit_memory(
  memory_file_name="progress.md",
  needle="# Progress Log",
  repl="""# Progress Log

## ${DATE} - Issue #${ISSUE} DEV Complete
- **Feature**: ${TITLE}
- **Commits**: ${COMMIT_COUNT}
- **Files Changed**: ${FILE_COUNT}
- **Tests Written**: ${TEST_COUNT}
- **Status**: Ready for TEST

""",
  mode="literal"
)

# 3. Remove from activeContext.md
mcp__serena__edit_memory(
  memory_file_name="activeContext.md",
  needle="### Issue #${ISSUE}...(entire section)",
  repl="",
  mode="regex"
)
```

#### TEST Thread Complete
```
# 1. Save test results
mcp__serena__write_memory(
  memory_file_name="test_results/test-${ISSUE}-${DATE}.md",
  content="""# Test Results - Issue #${ISSUE}

## Summary
| Suite | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| Unit | ${UNIT_PASS} | ${UNIT_FAIL} | 0 |
| Integration | ${INT_PASS} | ${INT_FAIL} | 0 |

## Coverage
- Statement: ${STATEMENT_COV}%
- Branch: ${BRANCH_COV}%

## Bugs Fixed
${BUG_LIST}
"""
)

# 2. Update progress.md
mcp__serena__edit_memory(
  memory_file_name="progress.md",
  needle="# Progress Log",
  repl="""# Progress Log

## ${DATE} - Issue #${ISSUE} TEST Complete
- **All tests pass**: YES
- **Coverage**: ${COVERAGE}%
- **Bugs fixed**: ${BUG_COUNT}
- **Status**: Ready for REVIEW

""",
  mode="literal"
)
```

#### REVIEW Thread Complete (PASS)
```
# Update progress.md with final status
mcp__serena__edit_memory(
  memory_file_name="progress.md",
  needle="# Progress Log",
  repl="""# Progress Log

## ${DATE} - Issue #${ISSUE} MERGED
- **Feature**: ${TITLE}
- **PR**: #${PR_NUMBER}
- **Review Verdict**: PASS
- **Merged to**: main
- **Total Cycle Time**: DEV(${DEV_SESSIONS}) → TEST(${TEST_SESSIONS}) → REVIEW(${REVIEW_SESSIONS})

""",
  mode="literal"
)
```

#### REVIEW Thread Complete (FAIL)
```
# 1. Update progress.md with demotion
mcp__serena__edit_memory(
  memory_file_name="progress.md",
  needle="# Progress Log",
  repl="""# Progress Log

## ${DATE} - Issue #${ISSUE} DEMOTED to DEV
- **Review Verdict**: FAIL
- **Reason**: ${FAILURE_REASON}
- **Issues Found**: ${ISSUE_COUNT}
- **Next**: DEV iteration required

""",
  mode="literal"
)

# 2. Add to activeContext.md for new DEV iteration
mcp__serena__edit_memory(
  memory_file_name="activeContext.md",
  needle="## In Progress",
  repl="""## In Progress

### Issue #${ISSUE} - ${TITLE} (Iteration ${N})
- **Phase**: DEV (demoted from REVIEW)
- **Demotion Date**: ${DATE}
- **Issues to Fix**:
  - ${ISSUE_1}
  - ${ISSUE_2}

""",
  mode="literal"
)
```

### Memory Bank Activation Triggers

Update the memory bank when ANY of these events occur:

| Trigger | Memory Update Required |
|---------|------------------------|
| Thread claimed | `activeContext.md` |
| Checkpoint posted | Consider `activeContext.md` |
| Technical decision made | `techContext.md` |
| Architecture changed | `dataflow.md` |
| Thread closed | `progress.md`, `activeContext.md` |
| Tests executed | `test_results/` |
| Feature merged | `progress.md` |
| Project scope changed | `projectBrief.md` |

### Preventing Information Duplication

Before updating any memory file:

1. **Check if content already exists**
   ```
   mcp__serena__read_memory("progress.md")
   # Search for issue number to avoid duplicates
   ```

2. **Place information in ONE file only**
   - Technical decisions → `techContext.md` (not `progress.md`)
   - Completed work summary → `progress.md` (not `activeContext.md`)
   - Current work → `activeContext.md` (move to `progress.md` when done)

3. **Use cross-references, not copies**
   ```markdown
   ## Issue #201 Complete
   See test results: test_results/test-201-2025-01-15.md
   See technical decisions: techContext.md (JWT section)
   ```

---

## Agent Resource Access

Each agent type needs access to specific resources. Verify access before starting work.

### DEV Agent Resources

| Resource | How to Access | Verify Command |
|----------|---------------|----------------|
| Issue thread | `gh issue view $ISSUE --comments` | Should return issue content |
| Git repository | `git status` | Should show repo status |
| Feature branch | `git checkout feature/$FEATURE` | Should switch branches |
| DEV worktree | `cd worktrees/dev-$FEATURE` | Directory should exist |
| SERENA memories | `mcp__serena__list_memories` | Should list memories |

**Memory Bank Operations (DEV):**

| When | Memory File | Operation |
|------|-------------|-----------|
| Claim issue | `activeContext.md` | Add issue entry |
| Make tech decision | `techContext.md` | Document decision + rationale |
| Change architecture | `dataflow.md` | Update data flow |
| Complete DEV | `progress.md` | Move from active to progress |

### TEST Agent Resources

| Resource | How to Access | Verify Command |
|----------|---------------|----------------|
| TEST thread | `gh issue view $TEST_ISSUE --comments` | Should return issue content |
| DEV thread (read) | `gh issue view $DEV_ISSUE --comments` | Need to read DEV decisions |
| Testing branch | `git checkout testing/$FEATURE` | Should switch branches |
| TEST worktree | `cd worktrees/test-$FEATURE` | Directory should exist |
| Test framework | `npm test` or `pytest` | Should run tests |
| SERENA memories | `mcp__serena__list_memories` | Should list memories |

**Memory Bank Operations (TEST):**

| When | Memory File | Operation |
|------|-------------|-----------|
| Start TEST | `activeContext.md` | Update phase to TEST |
| Run tests | `test_results/` | Save test report |
| Complete TEST | `progress.md` | Add test summary |

### REVIEW Agent Resources

| Resource | How to Access | Verify Command |
|----------|---------------|----------------|
| REVIEW thread | `gh issue view $REVIEW_ISSUE --comments` | Should return issue content |
| DEV thread (read) | `gh issue view $DEV_ISSUE --comments` | Understand what was built |
| TEST thread (read) | `gh issue view $TEST_ISSUE --comments` | Verify tests passed |
| Review branch | `git checkout review/$FEATURE` | Should switch branches |
| REVIEW worktree | `cd worktrees/review-$FEATURE` | Directory should exist |
| Coverage tools | `npm run coverage` | Should generate coverage |
| SERENA memories | `mcp__serena__list_memories` | Should list memories |

**Memory Bank Operations (REVIEW):**

| When | Memory File | Operation |
|------|-------------|-----------|
| PASS verdict | `progress.md` | Add merge record |
| FAIL verdict | `progress.md`, `activeContext.md` | Add demotion + new DEV iteration |

### Access Verification Script

Run before starting any thread work:

```bash
#!/bin/bash
# verify-agent-access.sh

ISSUE=$1
FEATURE=$2
THREAD_TYPE=$3  # dev, test, or review

echo "Verifying $THREAD_TYPE agent access for issue #$ISSUE..."
echo ""

# Check GitHub access
echo -n "[1/5] GitHub CLI: "
gh issue view $ISSUE > /dev/null 2>&1 && echo "✓ OK" || echo "✗ FAIL"

# Check Git access
echo -n "[2/5] Git repository: "
git status > /dev/null 2>&1 && echo "✓ OK" || echo "✗ FAIL"

# Check worktree
WORKTREE="worktrees/${THREAD_TYPE}-${FEATURE}"
echo -n "[3/5] Worktree ($WORKTREE): "
[ -d "$WORKTREE" ] && echo "✓ OK" || echo "✗ MISSING"

# Check SERENA memories directory
echo -n "[4/5] SERENA memories: "
[ -d ".serena/memories" ] && echo "✓ OK" || echo "✗ MISSING (run SERENA setup)"

# Check required memory files
echo -n "[5/5] Memory bank files: "
MISSING=""
[ ! -f ".serena/memories/activeContext.md" ] && MISSING="$MISSING activeContext.md"
[ ! -f ".serena/memories/progress.md" ] && MISSING="$MISSING progress.md"
[ ! -f ".serena/memories/techContext.md" ] && MISSING="$MISSING techContext.md"
[ -z "$MISSING" ] && echo "✓ OK" || echo "✗ MISSING:$MISSING"

echo ""
echo "Verification complete."
```

### Memory Bank Initialization

If memory bank files don't exist, initialize them:

```bash
# Initialize memory bank structure
mkdir -p .serena/memories/test_results

# Create activeContext.md
cat > .serena/memories/activeContext.md << 'EOF'
# Active Context

## In Progress

<!-- Current tasks go here -->
EOF

# Create progress.md
cat > .serena/memories/progress.md << 'EOF'
# Progress Log

<!-- Completed work entries go here, newest first -->
EOF

# Create techContext.md
cat > .serena/memories/techContext.md << 'EOF'
# Technical Context

## Tech Stack

<!-- Libraries, frameworks, tools -->

## Architecture Decisions

<!-- Decision records with rationale -->
EOF

# Create dataflow.md
cat > .serena/memories/dataflow.md << 'EOF'
# Data Flow

## System Overview

<!-- Data flow diagrams and descriptions -->
EOF

# Create projectBrief.md
cat > .serena/memories/projectBrief.md << 'EOF'
# Project Brief

## Overview

<!-- Project description and goals -->

## Core Features

<!-- Main features and objectives -->
EOF
```

---

## Core Philosophy

**Order matters. Time does not.**

- ETA is always "when it's done"
- Issues are not tickets with urgency levels
- Waves are ordered checklists, not kanban boards
- Messages can be answered 10 years later - order preserved, timing irrelevant
- Strict sequence: each step must complete before the next begins

---

## Quick Start: Select the Appropriate Playbook

| Agent Role | Thread Type | Playbook |
|------------|-------------|----------|
| **Task Agent** (implementing features, writing tests) | DEV | [P1-task-agent-playbook.md](references/P1-task-agent-playbook.md) |
| **Test Agent** (running tests, fixing bugs only) | TEST | [P9-test-agent-playbook.md](references/P9-test-agent-playbook.md) |
| **Review Agent** (code review, coverage estimation) | REVIEW | [P3-review-agent-playbook.md](references/P3-review-agent-playbook.md) |
| **Epic Coordinator** (planning, orchestrating waves) | Epic-level | [P2-epic-coordinator-playbook.md](references/P2-epic-coordinator-playbook.md) |

### Recovering from Compaction

Follow the recovery protocol: [P4-compaction-recovery-walkthrough.md](references/P4-compaction-recovery-walkthrough.md)

### Multiple Agents Working Together

Coordination protocols: [P5-multi-instance-protocol.md](references/P5-multi-instance-protocol.md)

---

## Thread Types and Phase Gates

### Two Levels of Order

| Level | What | Order |
|-------|------|-------|
| **Threads/Issues** | DEV, TEST, REVIEW | **ORDERED** (circular sequence) |
| **Elements inside threads** | KNOWLEDGE, ACTION, JUDGEMENT | **UNORDERED** (any order) |

Threads follow strict sequence. Comments within threads can mix knowledge, action, and judgement freely.

### Thread Types

| Thread Type | Purpose | ALLOWED | NOT ALLOWED |
|-------------|---------|---------|-------------|
| **Dev Thread** | Development work | Code, structural changes, **DESIGN & WRITE TESTS** | Definitive verdicts, final reviews, PASS/FAIL |
| **Test Thread** | Run tests & bug fixes | **RUN tests**, bug reports, **bug fixes only** | **Writing new tests**, structural changes, rewrites |
| **Review Thread** | Evaluation & verdicts | Verdicts, PASS/FAIL, **ESTIMATE COVERAGE** | New development, writing tests |

**Key insight**: Tests are CODE. Writing tests is DEVELOPMENT. TEST threads only RUN existing tests.

### Circular Phase Order

```
        ┌──────────────────────────────────────────────┐
        │                                              │
        ▼                                              │
    DEV THREAD ───► TEST THREAD ───► REVIEW THREAD ───┘
        │               │                 │
        │               │                 ▼
        │               │         PASS? → main/close
        │               │                 │
        │               │         FAIL? ──┘ (back to DEV)
        │               │
        │          Bug fixes only
        │          (NO structural changes)
        │
    New features,
    structural changes,
    rewrites
```

**Key Rules:**
- **ONE thread open at a time** per feature/solution
- Opening DEV = closing REVIEW (if returning from review)
- TEST can only fix bugs, NOT rewrite functionality
- Review decides if rewrite needed → demotes to DEV (never to TEST)
- Cycle repeats until REVIEW passes

### Demotion Rules

| From | Can Demote To | What Happens |
|------|---------------|--------------|
| **REVIEW** | **DEV only** | Review thread closes, dev thread reopens |
| **REVIEW** | ~~TEST~~ | **NEVER** - changes need dev first |
| **TEST** | **DEV** | If bugs reveal structural issues |

**Why Review → DEV only?** Because fixing issues found in review requires development work. Testing validates existing code; it cannot create structural fixes. Only after DEV completes the fixes can TEST validate them again.

### PR Branch Flow

```
feature branch ──► testing branch ──► review branch ──► main
      │                 │                  │
      │                 │                  ▼
      │                 │          PASS? → merge to main
      │                 │                  │
      │                 │          FAIL? ──┴──► demote to feature branch
      │                 │                       (back to DEV thread)
      │            Bug fixes only
      │            (test thread)
      │
 Development work
 (dev thread)
```

**Self-approval is NOT allowed.** "I tested it myself" and "I reviewed my own code" are phase bypasses.

### Thread Lifecycle Mechanics

Each thread (DEV, TEST, REVIEW) is a separate GitHub issue with the appropriate `phase:` label. Here's how threads transition:

#### Thread Creation

| When | Action |
|------|--------|
| New feature starts | Create DEV issue with `phase:dev` label |
| DEV completes | Close DEV issue, create TEST issue with `phase:test` label |
| TEST completes | Close TEST issue, create REVIEW issue with `phase:review` label |

#### Thread Transitions

```bash
# DEV → TEST (DEV work complete)
gh issue close $DEV_ISSUE
gh issue create --title "Feature X - TEST" \
  --label "phase:test" --label "in-progress" --label "epic:$EPIC" \
  --body "TEST thread for Feature X.
Source DEV thread: #$DEV_ISSUE
Linked PR: #$PR_NUMBER"

# TEST → REVIEW (all tests pass)
gh issue close $TEST_ISSUE
gh issue create --title "Feature X - REVIEW" \
  --label "phase:review" --label "in-progress" --label "epic:$EPIC" \
  --body "REVIEW thread for Feature X.
Source DEV thread: #$DEV_ISSUE
Source TEST thread: #$TEST_ISSUE"

# REVIEW → DEV (demotion - REVIEW fails)
gh issue close $REVIEW_ISSUE
gh issue reopen $DEV_ISSUE  # Or create new DEV iteration
gh issue edit $DEV_ISSUE --add-label "in-progress"
gh issue comment $DEV_ISSUE --body "Demoted from REVIEW #$REVIEW_ISSUE. Issues: ..."

# REVIEW → main (PASS - merge and close)
gh pr merge $PR_NUMBER --squash
gh issue close $REVIEW_ISSUE --comment "PASS - merged to main"
```

#### Thread States

| Issue State | Label State | Meaning |
|-------------|-------------|---------|
| OPEN | `in-progress` | Active work happening |
| OPEN | `needs-input` | Blocked, waiting for decision |
| CLOSED | `phase:dev` | DEV phase complete |
| CLOSED | `phase:test` | TEST phase complete |
| CLOSED | `completed` | REVIEW passed, merged |
| CLOSED | `phase:dev` | REVIEW failed, back to DEV |

#### Critical Rule: One Thread At A Time

At any moment, only ONE thread (DEV, TEST, or REVIEW) should be OPEN for a feature:

```bash
# Check for violations (should return at most 1 result)
gh issue list --label "epic:$EPIC" --state open --json number,labels | \
  jq '[.[] | select(.labels[].name | startswith("phase:"))]'
```

If this returns more than one issue, there's a phase order violation.

### Thread Initialization

Every new thread MUST declare required skills:

```markdown
## Thread: <Title>

### Required Skills
Agents participating in this thread should activate:
- `skill-name-1` - <why needed>
- `skill-name-2` - <why needed>

### Thread Type
<dev | test | review>

### Scope
<what this thread covers>
```

### Epic Threads (Meta-Level)

Epic threads follow the **same circular order** but operate on batches:

| Epic Thread Type | Purpose |
|------------------|---------|
| **Epic DEV Thread** | Development of a batch of issue solutions |
| **Epic TEST Thread** | Testing of a batch of issue solutions |
| **Epic REVIEW Thread** | Review of a batch of issue solutions |

Same rules apply: one epic thread open at a time, circular demotion to DEV, TEST for bug fixes only.

---

## Core Protocol Summary

### Session Start
```bash
# Find active work
gh issue list --assignee @me --label "in-progress"

# If found: read thread, inherit state, post resumption comment
# If empty: claim new issue from "ready" queue
```

### During Session
- **Checkpoint at each meaningful state change** (milestone completed, blocker hit, decision made)
- Post **State Snapshot** with: Completed, In Progress, Pending, Next Action

### Session End
- Post **final checkpoint** with complete state
- Verify: "Recovery possible with ONLY this issue thread?" (all items = yes)

---

## State Snapshot Format

Every checkpoint includes this structure:

```markdown
## [Session N] DATE TIME UTC - @agent-id

### Work Log
- [HH:MM] Action taken
- [HH:MM] Decision made

### State Snapshot

#### Thread Type
<dev | test | review>

#### Completed
- [x] Finished task 1
- [x] Finished task 2

#### In Progress
- [ ] Current work

#### Pending
- [ ] Future task 1
- [ ] Future task 2

#### Blockers
- Description + resolver

#### Files Changed
| File | Changes |
|------|---------|
| path/to/file | +50 lines |

#### Commits
| Hash | Message |
|------|---------|
| abc1234 | Description |

#### Branch
`feature/issue-number-slug`

#### Next Action
Specific action for resumption

#### Scope Reminder (for TEST threads)
- I CAN: <allowed actions for this thread type>
- I CANNOT: <disallowed actions for this thread type>
```

**Note**: Thread Type is critical for recovery - agents must know which phase they're resuming into.

---

## GitHub Elements vs TodoWrite Decision

| Condition | GitHub Elements | TodoWrite |
|-----------|-----------------|-----------|
| Context needed in 2 weeks | Yes | No |
| Context may get compacted | Yes | No |
| Multiple contributors | Yes | No |
| Dependencies or blockers exist | Yes | No |

**Default**: Use GitHub Elements. Persistent memory without need is preferable to lost context.

---

## Essential Commands

All coordination uses `gh` CLI only. No external scripts.

```bash
# Find active work
gh issue list --assignee @me --label "in-progress"

# Read issue with full history (order matters)
gh issue view 123 --comments

# Post checkpoint (at meaningful state changes)
gh issue comment 123 --body "## Checkpoint..."

# Claim new issue (strict sequence: claim → scope → work)
gh issue edit 123 --add-assignee @me --add-label "in-progress" --remove-label "ready"

# Mark needs input (waiting for decision/clarification)
gh issue edit 123 --add-label "needs-input"

# Input received, continue
gh issue edit 123 --remove-label "needs-input"

# Ready for review (after work complete)
gh issue edit 123 --remove-label "in-progress" --add-label "review-needed"

# Check wave completion
gh issue list --label "wave:1" --label "epic:200" --state open
# Wave complete when this returns empty

# Link PR to issue (closes issue when PR merges)
gh pr create --title "Fix #123 - Description" --body "Closes #123"
# Or add to existing PR
gh pr edit 456 --body "$(gh pr view 456 --json body --jq .body)

Closes #123"
```

### PR-Issue Linking Best Practices

Always link PRs to their source issues for traceability:

| Method | Syntax | Effect |
|--------|--------|--------|
| **Auto-close on merge** | `Closes #123` in PR body | Issue closes when PR merges |
| **Reference without close** | `Relates to #123` | Creates link, doesn't close |
| **Multiple issues** | `Closes #123, closes #124` | Closes both on merge |

**Include in PR body:**
```markdown
## Source Issue
Closes #123

## Thread Context
- DEV thread: #123
- Epic: #100
```

---

## Query Optimization

### Use activeContext.md as Index

Instead of searching all issues, check activeContext.md first for current work:

```bash
# SLOW: Search all issues
gh issue list --label "in-progress" --json number,title,body --limit 100

# FAST: Check SERENA memory for current context
# Use mcp__serena__read_memory("activeContext.md") first
# Only query GitHub for specific issue numbers found in activeContext
```

### Efficient Thread Discovery

| Need | Efficient Query |
|------|-----------------|
| My current work | `gh issue list --assignee @me --label "in-progress" --json number` |
| Specific epic issues | `gh issue list --label "epic:123" --json number,title` |
| Find specific issue | `gh issue view 123` (direct lookup, no search) |

### Batch Operations

When checking multiple issues, batch queries:

```bash
# SLOW: Query each issue separately
for issue in 101 102 103; do gh issue view $issue; done

# FAST: Single query with multiple numbers
gh issue list --json number,title,state | jq '.[] | select(.number | IN(101,102,103))'
```

---

## Key Concepts

### Element = Reply with Three Facets

Every issue reply contains:
- **Knowledge**: Decisions, plans, requirements
- **Action**: Code, commits, PRs
- **Judgement**: Reviews, test results, feedback

### Epic = Meta-Issue with Waves

Epics coordinate sub-issues through three phases:
1. **Meta-Knowledge**: Planning, architecture
2. **Meta-Action**: Launch waves of implementation issues
3. **Meta-Judgement**: Evaluation waves assess success

### Wave = Sprint Equivalent

Waves mark the transition from planning to implementation:
- All issues in a wave run in parallel
- Wave completes when all issues close
- Evaluation wave gates the next wave

**The House Analogy**: Waves are like floors of a house. You cannot build the second floor while the first floor has missing walls. Wave N+1 cannot start until Wave N is 100% complete.

```
Wave 1: Foundation
        ┌─────────────────────────────┐
        │ [x] A   [x] B   [x] C       │  ← ALL must be complete
        └─────────────────────────────┘
                      │
                      ▼ ONLY THEN
Wave 2: First Floor
        ┌─────────────────────────────┐
        │ [ ] D   [ ] E               │  ← Can start
        └─────────────────────────────┘
```

**No exceptions.** "95% done" is not done. One incomplete issue blocks the entire next wave.

---

## Labels

### Status Labels

| Label | Meaning |
|-------|---------|
| `ready` | Available for claiming |
| `in-progress` | Being worked on |
| `needs-input` | Waiting for external input (decision, clarification) |
| `review-needed` | Ready for review |
| `wave:N` | Part of wave N |
| `epic:N` | Part of epic N |
| `completed` | Review passed, issue closed |

### Thread Type Labels

| Label | Meaning |
|-------|---------|
| `phase:dev` | Development thread (no verdicts allowed) |
| `phase:test` | Testing thread (no feature opinions allowed) |
| `phase:review` | Review thread (verdicts allowed) |

### Violation Labels

| Label | Meaning |
|-------|---------|
| `violation:phase` | Posted verdict/opinion in wrong thread type |
| `violation:wave-order` | Started Wave N+1 before Wave N complete |
| `violation:self-approval` | Attempted to test/review own work |
| `violation:scope` | Work started before scope declaration |

Note: No priority labels. No time-based labels. Order is determined by wave membership and dependencies documented in issue bodies.

---

## Argos Panoptes Labels

**Argos Panoptes** is the 24/7 GitHub Actions automation that triages incoming work while agents are offline. Argos uses specific labels to queue work for the appropriate specialist agents.

### Session Startup: Check Argos-Queued Work FIRST

When starting any session, check for Argos-queued work before handling existing in-progress threads:

```bash
# Find all Argos-queued work (ready for processing)
gh issue list --state open --label "ready" --json number,title,labels | \
  jq -r '.[] | "\(.number): \(.title) [\(.labels | map(.name) | join(", "))]"'

# Priority order:
# 1. URGENT + security → Hephaestus (DEV) immediately
# 2. ci-failure → Chronos
# 3. needs-moderation → Ares (enforcement)
# 4. source:pr + review → Hera (REVIEW)
# 5. bug + review → Hera (REVIEW)
# 6. feature + dev → Hephaestus (DEV)
```

### Argos Label Reference

| Label | Set By | Meaning | Route To |
|-------|--------|---------|----------|
| `ready` | Argos | Validated, ready for work | Check phase label for specialist |
| `dev` | Argos | Needs development work | Hephaestus (dev-thread-manager) |
| `review` | Argos | Needs review/triage | Hera (review-thread-manager) |
| `source:pr` | Argos | Originated from a PR | Hera (review-thread-manager) |
| `source:ci` | Argos | Originated from CI failure | Chronos (ci-issue-opener) |
| `needs-info` | Argos | Awaiting user response | Wait for response |
| `needs-moderation` | Argos | Policy violation flagged | Ares (enforcement) |
| `urgent` | Argos | High priority work | Handle immediately |
| `security` | Argos | Security vulnerability | Hephaestus + urgent |
| `ci-failure` | Argos | CI/CD workflow failed | Chronos |
| `bot-pr` | Argos | PR from Dependabot | Hera (may auto-merge) |
| `blocked` | Argos | Critical severity | Escalate to orchestrator |
| `feature` / `enhancement` | Argos | Feature request validated | Hephaestus |
| `bug` | Argos | Bug report validated | Hera |

### Recognizing Argos Comments

Argos Panoptes signs all comments with its identity:

```
Argos Panoptes (The All-Seeing)
Avatar: ../../assets/avatars/argos.png
```

When you see an Argos comment, the issue has been triaged. Proceed with your phase-specific duties.

### Argos Does NOT:

- Claim issues (only queues them)
- Post checkpoints (only triages)
- Transition phases (only labels)
- Write code (only validates)
- Render verdicts (only flags)

Argos queues. Specialists execute.

---

## Safeguards System

GHE includes a comprehensive safeguards system to prevent errors and enable recovery.

### Loading Safeguards

```bash
# Source at the beginning of any operation
source plugins/ghe/scripts/safeguards.sh
```

### Available Functions

| Function | Purpose | When to Use |
|----------|---------|-------------|
| `pre_flight_check <issue>` | All safety checks | Before starting any work |
| `verify_worktree_health <path>` | Check worktree validity | Before worktree operations |
| `safe_worktree_cleanup <path> [force]` | Safe removal | When cleaning up worktrees |
| `acquire_merge_lock_safe <issue>` | Get lock with TTL | Before merge attempts |
| `release_merge_lock_safe <issue>` | Release lock | After merge (always!) |
| `wait_for_merge_lock <issue> [timeout]` | Wait for lock | When lock is held by others |
| `heartbeat_merge_lock <issue>` | Keep lock alive | During long operations |
| `atomic_commit_push <branch> <msg> <files>` | Safe commit+push | For critical commits |
| `reconcile_ghe_state` | Fix state desync | On startup, after errors |
| `validate_with_retry <script> <file>` | Validation with retries | For flaky validations |
| `recover_from_merge_crash <issue>` | Crash recovery | After interruptions |

### Configuration (Environment Variables)

| Variable | Default | Description |
|----------|---------|-------------|
| `LOCK_TTL` | 900 | Lock timeout in seconds (15 min) |
| `MAX_RETRIES` | 3 | Retry attempts for validation |
| `RETRY_DELAY` | 2 | Seconds between retries |
| `GHE_WORKTREES_DIR` | ../ghe-worktrees | Worktrees directory |

### Pre-Flight Check Output

```
Running pre-flight checks for issue #123
==================================================
[1/6] Issue #123 status: OPEN
[2/6] Worktree exists: YES
[3/6] Worktree health: HEALTHY
[4/6] Branch check: issue-123
[5/6] Merge lock: FREE
[6/6] GitHub auth: OK
==================================================
All pre-flight checks passed
```

---

## Recovery Procedures

### Recovery: Crashed Merge Operation

If a merge was interrupted (agent crashed, network failure, etc.):

```bash
source plugins/ghe/scripts/safeguards.sh

# Automatic recovery
recover_from_merge_crash "$ISSUE_NUM"

# This will:
# 1. Release any held merge locks
# 2. Abort any in-progress rebase or merge
# 3. Reconcile ghe.local.md state
```

### Recovery: Orphaned Worktree

If a worktree exists but its issue is closed:

```bash
source plugins/ghe/scripts/safeguards.sh

# Check and cleanup all orphaned worktrees
reconcile_ghe_state

# Or cleanup specific worktree
safe_worktree_cleanup "../ghe-worktrees/issue-123" true
```

### Recovery: Stale Merge Lock

If a merge lock is held longer than TTL (15 min):

```bash
# The safeguards system automatically detects and releases stale locks
# Just attempt to acquire the lock normally:
acquire_merge_lock_safe "$ISSUE_NUM"
# If old lock is stale, it will be released automatically
```

### Recovery: Corrupted Worktree

If worktree is in an invalid state (detached HEAD, missing .git, etc.):

```bash
source plugins/ghe/scripts/safeguards.sh

# Check health
if ! verify_worktree_health "../ghe-worktrees/issue-123"; then
    echo "Worktree corrupted - recreating..."

    # Force remove corrupted worktree
    safe_worktree_cleanup "../ghe-worktrees/issue-123" true

    # Recreate from main
    git worktree add ../ghe-worktrees/issue-123 -b issue-123 main
fi
```

### Recovery: State Desync

If ghe.local.md references closed issues or wrong phase:

```bash
source plugins/ghe/scripts/safeguards.sh

# Automatic reconciliation
reconcile_ghe_state ".claude/ghe.local.md"
```

### Recovery Decision Matrix

| Symptom | Recovery Function |
|---------|-------------------|
| Worktree operations fail | `verify_worktree_health` → `safe_worktree_cleanup` |
| Merge lock stuck | `acquire_merge_lock_safe` (auto-releases stale) |
| ghe.local.md wrong issue | `reconcile_ghe_state` |
| Rebase left incomplete | `recover_from_merge_crash` |
| Push failed mid-operation | `atomic_commit_push` (rollback) |
| Validation flaky | `validate_with_retry` |

### Startup Reconciliation

Run on every startup/session to ensure clean state:

```bash
source plugins/ghe/scripts/safeguards.sh

# Full state reconciliation
reconcile_ghe_state

# Prune any stale git worktrees
git worktree prune
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Work without checkpoints | Context lost on compaction | Checkpoint at state changes |
| Skip scope declaration | File conflicts | Declare files on claim |
| Skip session end checkpoint | Recovery impossible | Always post final state |
| Vague "Next Action" | Cannot resume | Specific single action |
| Silent decisions | Coordination failure | Document in thread |
| Skip steps in sequence | Order violation | Complete each step before next |
| Start Wave N+1 before Wave N done | Dependency violation | All items in wave must complete first |
| Add urgency/priority labels | Philosophy violation | Order only, no urgency |
| **Post verdict in dev thread** | Phase violation | Wait for review thread |
| **Skip testing phase** | Order violation | Dev → Test → Review sequence |
| **"I tested it myself"** | Self-approval bypass | Independent tester required |
| **"I reviewed my own code"** | Self-approval bypass | Independent reviewer required |
| **PR direct to main** | Skip branch phases | feature → testing → review → main |
| **Open thread without skills list** | Coordination failure | Always list required skills first |
| **Two threads open simultaneously** | Order violation | Only ONE of DEV/TEST/REVIEW at a time |
| **Demote REVIEW → TEST** | Phase bypass | REVIEW always demotes to DEV (never TEST) |
| **Structural changes in TEST** | Scope violation | TEST = bug fixes only, demote to DEV |
| **Rewrite in TEST thread** | Scope violation | Only DEV can do rewrites |
| **Write new tests in TEST thread** | Scope violation | Tests are CODE, writing tests is DEV work |
| **Missing coverage → demote to TEST** | Phase bypass | Missing coverage → DEV (to write tests) |
| **Skip memory bank update** | Context loss | Update memory bank at every thread transition |
| **Duplicate info in memory files** | Data inconsistency | Each info in ONE file only |
| **activeContext.md never cleaned** | Stale context | Move completed to progress.md |
| **No test_results/ for TEST phase** | Missing traceability | Always save test reports to SERENA |
| **Memory bank not initialized** | Operations fail | Initialize before first thread claim |
| **Bloat first message with work logs** | Unreadable index | Work logs go in replies, index stays clean |
| **Edit index without announcing** | Silent change, subscribers miss it | Always post reply explaining index changes |
| **Make any change without reply** | Breaks thread as record | Every change gets announced in a reply |
| **Work on main branch** | Breaks isolation, pollutes main | ALL work in worktrees: `../ghe-worktrees/issue-N/` |
| **Skip worktree verification** | Risk of main pollution | Always verify branch before any work |
| **Merge before REVIEW PASS** | Unreviewed code in main | Only merge after REVIEW verdict = PASS |
| **Skip review report creation** | No audit trail | Save review to `GHE_REPORTS/` BEFORE merge |
| **Save review after merge** | Rejected reviews pollute main | Commit review to feature branch first |
| **Merge without checking main** | Merge conflicts, race conditions | Always `git fetch origin main` first |
| **Skip TEST after rebase** | Reviewed code ≠ merged code | RE-RUN TEST after ANY rebase |
| **Force push without --force-with-lease** | Can overwrite others' work | Always use `--force-with-lease` |
| **Ignore rebase conflicts** | Broken code reaches main | DEMOTE TO DEV on any conflict |
| **Retry rebase forever** | Infinite loop, blocks progress | Max 3 attempts then demote to DEV |
| **Hold merge lock > 15 min** | Blocks all other agents | Release lock, investigate issue |

---

## Documentation Map

This map shows ALL available documentation. Read only what you need for your current situation.

> **Progressive Disclosure**: Scan these situational titles. When you encounter a matching situation, read that reference.

---

## DEV Thread Work — [P1-task-agent-playbook.md](references/P1-task-agent-playbook.md)

When you are implementing features, writing tests, or doing structural work.

| What to do... | Read |
|---------------|------|
| ...if I don't understand the workflow approach | Core Philosophy |
| ...if I'm unsure which thread type applies | Thread Types and Phase Gates |
| ...if I'm wondering if two threads can be open at once | One Thread At A Time Rule |
| ...when a REVIEW just failed | Demotion Rules |
| ...when a new feature has no DEV thread yet | Thread Initialization Protocol |
| ...when I just started a new session | SESSION START PROTOCOL |
| ...if I don't know what work is assigned to me | Step 1: Find Your Work |
| ...if this is a continuation of previous work | Step 2: Resume Existing Work |
| ...when there's unclaimed work in the queue | Step 3: Claim New Work |
| ...if I made progress and wonder if a checkpoint is needed | Checkpoint Triggers |
| ...when I need to write a checkpoint | Checkpoint Format |
| ...if I can't continue without external input | Handling Need-Input Situations |
| ...when input I was waiting for just arrived | When Input Is Received |
| ...when I'm done working for now | SESSION END PROTOCOL |
| ...if a task is too complex for one issue | Creating Sub-Tasks |
| ...if another agent might be working on the same files | Scope Conflict Detection |
| ...when I need checkpoint templates | Templates |

---

## TEST Thread Work — [P9-test-agent-playbook.md](references/P9-test-agent-playbook.md)

When you are running existing tests and fixing simple bugs.

| What to do... | Read |
|---------------|------|
| ...if I don't understand what TEST is supposed to do | Core Philosophy |
| ...if I'm unsure what TEST can and cannot do | What You Can Do / What You CANNOT Do |
| ...if I'm about to start TEST but DEV might still be open | Phase Entry Verification |
| ...when there's TEST work available in the queue | Step 1: Find Available TEST Work |
| ...when a TEST thread is ready and unclaimed | TEST Thread Claiming |
| ...when tests need to be run | TEST Execution Protocol |
| ...when tests finished and results need documenting | Documenting Test Results |
| ...when a test failed | Bug Fix Protocol |
| ...if I fixed a bug but I'm unsure if it was allowed in TEST | Allowed Fixes |
| ...if a bug fix requires structural changes | Demotion Protocol |
| ...when all tests pass | TEST Completion Protocol |
| ...when I need to write a TEST checkpoint | Checkpoint Format |
| ...to avoid common TEST mistakes | Anti-Patterns |

---

## REVIEW Thread Work — [P3-review-agent-playbook.md](references/P3-review-agent-playbook.md)

When you are evaluating code, rendering verdicts, or triaging bug reports.

| What to do... | Read |
|---------------|------|
| ...if I don't understand what REVIEW's authority is | Core Philosophy |
| ...if I'm about to start REVIEW but TEST might still be open | Step 0: Verify Phase Order |
| ...when a REVIEW thread is ready and unclaimed | Step 1: Claim Review Issue |
| ...if I don't have context about what DEV and TEST did | Step 2: Gather Context |
| ...when I'm reviewing code and need a checklist | Code Review Checklist |
| ...when I'm checking for security issues | Security Audit Checklist |
| ...when I'm checking for performance issues | Performance Review Checklist |
| ...when I found issues and need to document them | Step 4: Document Findings |
| ...when no blocking issues were found | PASS Verdict |
| ...when blocking issues were found | FAIL Verdict / DEMOTION PROTOCOL |
| ...if I don't know if test coverage is sufficient | TEST COVERAGE ESTIMATION |
| ...when I'm looking for common coverage gaps | Common Coverage Gaps |
| ...if I found an issue but don't know its severity | Severity Definitions |
| ...if something is unclear and DEV needs to explain | Requesting Clarification |
| ...if an issue is beyond my authority | Escalating to Epic |

---

## Epic Coordination — [P2-epic-coordinator-playbook.md](references/P2-epic-coordinator-playbook.md)

When you are planning, coordinating waves, or orchestrating multiple agents.

| What to do... | Read |
|---------------|------|
| ...if I don't understand epic-level coordination | Core Philosophy |
| ...when a large feature has no epic issue yet | Step 1: Create the Epic Issue |
| ...when an epic exists but has no plan | Step 2: Planning Session |
| ...when work needs to be broken into waves | Step 3: Define Waves |
| ...when a wave has no issues yet | Step 4: Create Wave Issues |
| ...when a wave is ready to start | Step 5: Post Wave Launch |
| ...when a wave is in progress | Step 6: Monitor Wave Progress |
| ...when an agent is blocked waiting for input | Step 7: Handle Input Requests |
| ...when all issues in a wave are closed | Step 8: Wave Completion |
| ...when a wave completed and needs evaluation | Step 9: Spawn Evaluation Issues |
| ...when verdicts arrived from evaluation | Step 11: Process Verdicts |
| ...when all waves completed and passed evaluation | Step 12: Close Epic |
| ...when a wave order violation was detected | Wave Order Violation Response |

---

## Recovery from Compaction — [P4-compaction-recovery-walkthrough.md](references/P4-compaction-recovery-walkthrough.md)

When context was compacted and you need to resume work.

| What to do... | Read |
|---------------|------|
| ...if I don't understand recovery philosophy | Core Philosophy |
| ...when context was just compacted and I don't know my assignment | Step 1: Find Assigned Work |
| ...if I found my issue but don't know what was done | Step 2: Read the Issue |
| ...if I don't know if local git state matches the checkpoint | Step 3: Verify Local State |
| ...when local TodoWrite is empty after compaction | Step 4: Build Local TodoWrite |
| ...when I recovered and need to document it | Step 5: Post Recovery Comment |
| ...when recovery is complete | Step 6: Continue Work |
| ...when I'm recovering in a TEST thread | TEST Thread Recovery Scenario |
| ...when I'm recovering in a REVIEW thread | REVIEW Thread Recovery Scenario |
| ...when recovery revealed work is done and phase should change | Thread Transition During Recovery |
| ...to avoid common recovery mistakes | Anti-Patterns in Recovery |

---

## Multi-Agent Coordination — [P5-multi-instance-protocol.md](references/P5-multi-instance-protocol.md)

When multiple agents work on the same project simultaneously.

| What to do... | Read |
|---------------|------|
| ...if I don't understand multi-agent challenges | The Challenge |
| ...when an issue is unclaimed and I want it | Protocol 1: Issue Claiming |
| ...when I claimed an issue and need to declare my scope | Protocol 2: Scope Declaration |
| ...if another agent might be working on the same files | Checking for Scope Conflicts |
| ...when a scope conflict was detected | Handling Scope Conflicts |
| ...when I'm done with an assignment and releasing it | Protocol 3: Assignment Management |
| ...when I made a decision that affects other agents | Protocol 4: Decision Broadcasting |
| ...when another agent broadcast a decision | Acknowledging Broadcasts |
| ...if merge conflicts might occur | Protocol 5: Merge Conflict Prevention |
| ...when multiple agents need the same resource | Protocol 6: Shared Resource Locking |
| ...when a PR is ready to merge | Protocol 7: PR Merge Flow |
| ...if I don't understand branch phase flow | The Branch Flow |
| ...when my self-approval was rejected | Self-Approval Rejection |

---

## Complete Lifecycle Example — [P8-complete-lifecycle-example.md](references/P8-complete-lifecycle-example.md)

When you need to see the full DEV → TEST → REVIEW cycle in action.

| I want to see an example of... | Section |
|--------------------------------|---------|
| A DEV thread being created | Day 1, 09:00 - DEV Thread Created |
| An agent claiming a DEV thread | 09:15 - Agent-A Claims DEV Thread |
| A session end checkpoint | 12:30 - Session 1 End Checkpoint |
| DEV completing and TEST starting | 17:45 - DEV Complete, Ready for TEST |
| TEST thread execution | PHASE 2: TEST THREAD |
| Tests finding a bug | 18:30 - Tests Run, Bug Found |
| REVIEW failing and demoting to DEV | 11:30 - REVIEW Complete - FAIL |
| A second DEV iteration after demotion | PHASE 4: DEV THREAD (Second Iteration) |
| REVIEW passing and merging to main | PHASE 7: MERGE TO MAIN |
| What goes wrong when demotion goes to TEST | What If Demotion Went to TEST? (Anti-Pattern) |

---

## Setting Up GitHub Actions Enforcement — [P6-enforcement-setup.md](references/P6-enforcement-setup.md)

When you need automated enforcement of workflow rules.

| What to do... | Read |
|---------------|------|
| ...when the project has no enforcement yet | Quick Setup Checklist |
| ...when required labels don't exist | Step 1: Create Required Labels |
| ...when issues are created without validation | Step 2: Issue Validation Workflow |
| ...when scope conflicts are not being detected | Step 3: Scope Conflict Detector |
| ...when PRs merge without validation | Step 4: PR Validation |
| ...when thread initialization is not enforced | Step 5: Thread Initialization Validator |
| ...when phase violations are not detected | Step 6: Phase Violation Detector |
| ...when TEST threads make unauthorized changes | Step 7: TEST Thread Scope Enforcement |
| ...when demotions go to wrong phase | Step 8: Demotion Direction Enforcement |
| ...when self-approvals are not blocked | Step 9: Self-Approval Rejection |
| ...if enforcement is not working | Troubleshooting |
| ...when enforcement needs to be removed | Uninstall |

---

## Manual Validation Checklists — [P7-validation-checklist.md](references/P7-validation-checklist.md)

When you need to manually verify workflow compliance.

| What to do... | Read |
|---------------|------|
| ...if I don't understand the enforcement levels | Enforcement Levels |
| ...if I found a violation but don't know its type | Violation Types |
| ...when a violation was found and needs clearing | Clearing Violations |
| ...when an issue just started | Issue Start Checklist |
| ...when a thread was just initialized | Thread Initialization Checklist |
| ...when a phase transition is about to happen (DEV→TEST, TEST→REVIEW) | Phase Gate Validation |
| ...if TEST thread might have violated its scope | TEST Thread Scope Validation |
| ...if a demotion happened and direction might be wrong | Demotion Direction Validation |
| ...when a PR is ready and branch flow needs checking | PR Branch Flow Checklist |
| ...if waves might be out of order | Wave Order Validation |
| ...when a checkpoint was posted | Checkpoint Validation |
| ...when a session just ended | Session End Validation |
| ...when an epic structure needs checking | Epic Validation |
| ...when a review was just completed | Review Validation |
| ...when it's time for a routine audit | Periodic Audit |
| ...when a thorough audit is needed | Comprehensive Audit |
| ...if an issue is beyond my authority | Escalation Matrix |

---

## Handling Bug Reports — [P10-bug-triage-protocol.md](references/P10-bug-triage-protocol.md)

When a new bug report is posted or you cannot reproduce an issue.

| What to do... | Read |
|---------------|------|
| ...when a bug report just arrived | CRITICAL: Bug Reports Go to REVIEW |
| ...if I cannot reproduce the reported bug | The 3-Strike Rule |
| ...when first reproduction attempt failed | Strike 1: First Request for Details |
| ...when second reproduction attempt failed | Strike 2: Second Request with Specific Questions |
| ...when third reproduction attempt failed | Strike 3: Polite Closure |
| ...when the bug report is a NEW GitHub issue | Case 1: Bug from NEW GitHub Issue |
| ...when the bug report is a comment IN an existing thread | Case 2: Bug from Comment IN Existing Thread |
| ...when a user made a valid contribution | Valid Contribution (Any Size) |
| ...when a report is invalid but the user deserves politeness | Invalid/Cannot Reproduce (Still Be Polite) |
| ...if I disagree with a report but the user deserves respect | Disagreement (Respectful) |
| ...to avoid common triage mistakes | Anti-Patterns |

---

## The Golden Rules

### 1. The issue thread IS the memory
Every session starts by reading the thread. Every session ends by updating it. Content not in the thread does not exist.

### 2. Order is sacred, time is irrelevant
Steps must be completed in sequence. But when each step happens doesn't matter. A message posted today responds to a question from a year ago - the ORDER in the thread is what matters.

### 3. Strict sequence enforcement

**Issue Lifecycle Order** (cannot skip steps):
```
1. ready          → Issue available
2. claimed        → Assignee set, in-progress label
3. scope declared → Files listed in comment
4. work begins    → Implementation starts
5. checkpoints    → State preserved at changes
6. work complete  → All tasks done
7. review-needed  → Ready for review
8. review done    → PASS (close + completed) or FAIL (back to phase:dev)
9. merged/closed  → If passed
```

**Wave Order** (dependencies):
```
Wave 1: [x] A, [x] B, [x] C   ← ALL must complete
Wave 2: [ ] D, [ ] E          ← Can only start after Wave 1 ALL checked
Wave 3: [ ] F                 ← Can only start after Wave 2 ALL checked
```

### 4. No urgency, no deadlines
- ETA = "when it's done"
- No priority:high/medium/low
- No "blocks deployment"
- No stale claims (time doesn't make claims stale)
- Respond whenever. Order preserved.

### 5. Circular phase order (one thread at a time)
```
DEV → TEST → REVIEW → DEV → TEST → REVIEW → ... (until REVIEW passes)
```

**Rules:**
- **ONE thread open at a time** per feature/solution
- Opening TEST = closing DEV
- Opening REVIEW = closing TEST
- REVIEW pass = merge to main, done
- REVIEW fail = reopen DEV (never TEST)

**Thread scope:**
- **Dev threads**: Work, structural changes, rewrites, **DEVELOP TESTS** - NO VERDICTS
- **Test threads**: **RUN tests**, fix bugs causing test failures - NO NEW TESTS, NO STRUCTURAL CHANGES
- **Review threads**: Verdicts, PASS/FAIL, **ESTIMATE COVERAGE** - NO NEW DEVELOPMENT

**Test development cycle:**
```
DEV: Design & write tests ──► TEST: Run tests, fix bugs ──► REVIEW: Check coverage
                                                                    │
                              Missing coverage? ◄───────────────────┘
                                    │
                                    ▼
                              Back to DEV (to write new tests)
```

**Self-approval is forbidden:** "I tested it myself" = REJECTED

### 6. Two levels of order
| Level | What | Order |
|-------|------|-------|
| **Threads** | DEV, TEST, REVIEW | **ORDERED** (circular) |
| **Elements** inside threads | KNOWLEDGE, ACTION, JUDGEMENT | **UNORDERED** |

Threads follow strict sequence. Comments within threads can mix knowledge, action, and judgement freely.

### 7. Memory bank stays synchronized
Every thread transition triggers a memory bank update:

| Thread Event | Memory Update |
|--------------|---------------|
| Claim thread | Add to `activeContext.md` |
| Complete thread | Move to `progress.md` |
| Tech decision | Document in `techContext.md` |
| Run tests | Save to `test_results/` |
| Merge feature | Final entry in `progress.md` |

**The memory bank IS the project context.** GitHub Issues track per-issue work. The memory bank tracks project-level progress across all issues.
