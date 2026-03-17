---
name: implement-batch
description: Multi-ticket batch workflow. Takes a batch of tickets, plans execution order, implements each via /implement in autonomous mode, runs cross-cutting quality passes, and presents results for final review.
model: opus
---

# Implement-Batch - Multi-Ticket Orchestration Workflow

Orchestrates a batch of tickets as a cohesive unit. Creates a project branch, implements each ticket sequentially using the `/implement` workflow in autonomous mode, runs cross-cutting quality passes, and presents results for final human review.

## Philosophy

**Maximize autonomy, minimize accumulated error.** The goal is to complete an entire batch of tickets without user intervention — but not at the cost of letting problems compound. When something goes wrong, pull the andon cord immediately rather than pressing forward and hoping later steps will compensate.

**The project branch is the integration point.** Each ticket gets its own topic branch. Work flows from topic branches into the project branch, never directly into main. This keeps main clean and gives the user a single decision point at the end: merge the project branch or don't.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                   BATCH WORKFLOW                     │
├──────────────────────────────────────────────────────┤
│  1. Receive ticket specification                     │
│  2. Detect issue tracker & fetch tickets             │
│  3. Batch planning (present to user)                 │
│  4. Create project branch                            │
│  5. Per-ticket loop:                                 │
│     ├─ 5a. Create topic branch                       │
│     ├─ 5b. Run /implement (autonomous mode)            │
│     ├─ 5c. Merge topic branch → project branch       │
│     ├─ 5d. Post-merge verification gate              │
│     └─ 5e. Delete topic branch                       │
│  6. Cross-cutting quality passes                     │
│     ├─ 6a. /refactor (SAFE aggression)               │
│     └─ 6b. /review-doc                               │
│  7. Final review (present to user)                   │
└──────────────────────────────────────────────────────┘
```

## Andon Cord Protocol

**This protocol applies throughout the entire workflow.** When the andon cord is pulled:

1. **Stop all work immediately** — do not attempt to continue with other tickets or steps
2. Present to user:
   - Which ticket and which step failed
   - What was attempted and what went wrong
   - Current state of all branches (what's merged, what's in-progress)
3. Wait for user guidance before resuming

**Andon cord triggers:**
- Acceptance verification fails 3 times (step 5b, `/implement` step 4)
- Unresolvable critical/high security findings (step 5b, `/implement` step 5a)
- Post-merge test suite failure (step 5d)
- Merge conflict (step 5c)
- Issue tracker unavailable or tickets can't be fetched (step 2)
- Empty ticket with no description (step 5b)
- Project branch already exists (step 4)
- Any unexpected failure not covered above

## Workflow Details

### 1. Receive Ticket Specification

Accept tickets from the user in any of these forms:
- Explicit list of ticket IDs (e.g., `#12, #15, #18`)
- Tag/label query (e.g., "all tickets tagged `v2.0`")
- Milestone (e.g., "milestone: Sprint 4")
- User-provided description to search for

### 2. Detect Issue Tracker & Fetch Tickets

**Detect platform:**
- Run `git remote -v` and inspect the URL
- GitHub: `github.com` → use `gh` CLI
- Gitea: other git hosting → use `mcp__gitea__*` MCP tools if available, otherwise API
- GitLab: `gitlab.com` or GitLab instances → use `glab` CLI if available

**Fetch each ticket:**
- Title
- Description/body
- Acceptance criteria (if explicitly present)
- Labels/tags
- Dependencies (referenced issues, "depends on" links)

**Andon cord** if tracker is unavailable or tickets can't be fetched.

### 3. Batch Planning

Analyze all fetched tickets and produce an execution plan:

**Dependency analysis:**
- Check for explicit "depends on" or "blocks" relationships between tickets
- Check for tickets referencing the same files or subsystems (implicit dependencies)
- Identify any tickets that must come before others

**Execution ordering:**
- Dependencies first (blocked tickets come after their blockers)
- Among independent tickets: simpler tickets first (builds momentum, establishes patterns)
- Flag any ambiguous tickets (missing description, no clear acceptance criteria)

**Present the plan to user:**
- Proposed execution order with rationale
- Any concerns about ambiguous or under-specified tickets
- Estimated scope (brief, qualitative — "3 small tickets, 1 medium")

**Wait for user approval** before proceeding. This is the one planned user interaction point.

### 4. Create Project Branch

- Identify the main branch (`main` or `master`)
- Create project branch from current HEAD: `feat/batch-<descriptive-name>`
- Branch name derived from the tag, milestone, or a brief summary of the ticket batch
- **Andon cord** if branch already exists — ask user whether to resume or start fresh

### 5. Per-Ticket Execution Loop

For each ticket in the planned order:

#### 5a. Create Topic Branch

- Checkout project branch (ensure it's current)
- Create topic branch: `feat/issue-<number>-<brief-slug>`
- The slug is derived from the ticket title (lowercase, hyphens, truncated to ~40 chars)

#### 5b. Run `/implement` Workflow (Autonomous Mode)

Follow the `/implement` workflow with these overrides for autonomous operation:

| `/implement` Step                             | Autonomous Override                                                                                                                                                                                              |
|---------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Step 1** (requirements)                   | Pre-loaded from ticket body. Do not prompt user for requirements. If the ticket lacks explicit acceptance criteria, derive them from the description. If the description is empty or incoherent, **andon cord**. |
| **Step 2** (planning)                       | Follow normal conditional logic — invoke `swe-planner` for complex tasks, skip for simple ones.                                                                                                                  |
| **Steps 3-4** (implementation + acceptance) | Follow normal logic. If acceptance verification fails 3 times, **andon cord** (do not escalate to user within `/implement` — escalate here at the batch level).                                                    |
| **Step 5a** (security review)               | Follow normal logic. If critical/high findings cannot be resolved by the implementation agent, **andon cord**.                                                                                                   |
| **Steps 5b-5c** (refactoring/perf review)   | Follow normal logic — these are advisory.                                                                                                                                                                        |
| **Step 6** (implement review feedback)      | Follow normal logic.                                                                                                                                                                                             |
| **Step 7** (peer review)                    | Follow normal logic. Handle deep issues autonomously — trust agents. If peer review breaks tests, revert peer review changes per standard `/implement` logic.                                                      |
| **Step 8** (coverage/quality verification)  | Follow normal logic. Handle autonomously — if tests pass, proceed. Do not prompt user for approval of minor issues.                                                                                              |
| **Step 9** (documentation)                  | Follow normal logic.                                                                                                                                                                                             |
| **Step 10** (final verification)            | Follow normal logic.                                                                                                                                                                                             |
| **Step 11a** (commit)                       | Auto-commit with ticket reference. Use `Fixes #<number>` in the commit message.                                                                                                                                  |
| **Step 11b** (ticket update/close)          | Post a comment on the ticket summarizing changes made. **Do not close** the ticket — leave that for the user after final review.                                                                                 |
| **Step 11c** (rebase on main)               | **Skip entirely.** We're on topic branches off the project branch, not main.                                                                                                                                     |

#### 5c. Merge Topic Branch into Project Branch

- Checkout project branch
- Merge: `git merge --no-ff feat/issue-<number>-<brief-slug>`
- The `--no-ff` preserves topic branch history for clarity
- **Andon cord** on merge conflict — do not attempt auto-resolution

#### 5d. Post-Merge Verification Gate

- Run the full test suite on the project branch
- Run linters/formatters
- **Andon cord** if tests fail — the merge introduced a regression

#### 5e. Clean Up Topic Branch

- Delete the merged topic branch: `git branch -d feat/issue-<number>-<brief-slug>`
- Update orchestrator state: mark ticket as done

### 6. Cross-Cutting Quality Passes

After all tickets are implemented and merged into the project branch:

#### 6a. Refactoring

Run the `/refactor` workflow with these parameters:
- **Aggression ceiling:** SAFE (conservative — only SAFEST and SAFE changes)
- **Custom QA instructions:** None (standard test suite verification)
- **Scope:** Entire codebase
- The `/refactor` workflow handles its own iteration loop, commits, and QA verification

#### 6b. Documentation Review

Run the `/review-doc` workflow:
- Full documentation audit (not git-diff scoped)
- Fixes committed separately

### 7. Final Review

Present comprehensive summary to user:

```
## Batch Complete

### Tickets Implemented
- #12: <title> — <brief outcome>
- #15: <title> — <brief outcome>
- #18: <title> — <brief outcome>

### Statistics
- Total commits: N
- Net lines changed: +/-N
- Tests added/modified: N
- Documentation files updated: N

### Quality Passes
- Refactoring: N improvements, net -N lines
- Documentation: N updates

### Branch Status
- Project branch: feat/batch-<name>
- Base branch: <main branch>
- Ready to merge
```

User decides next steps: merge to main, further work, or discard.

## State Management

The orchestrator maintains:
- **Ticket list**: all tickets with status (pending / in-progress / done / failed)
- **Current ticket**: which ticket is being worked on
- **Execution order**: from the planning step
- **Summary log**: brief notes on each completed ticket (avoid context bloat — just ticket number, title, outcome, and commit count)
- **Branch names**: project branch and any active topic branches (for cleanup if needed)

## Agent Coordination

**Sequential execution:**
- One ticket at a time, one agent at a time
- Each agent completes before the next begins
- No parallel agent execution

**Context management:**
- The `/implement` workflow within each ticket manages its own agent lifecycle
- The batch orchestrator tracks only summary-level state across tickets
- Keep per-ticket summaries brief to avoid context window bloat across a large batch

**Fresh state per ticket:**
- Each ticket starts with a fresh topic branch
- The `/implement` workflow starts from scratch for each ticket
- No state leaks between tickets except the cumulative project branch

## Integration with Other Skills

**Relationship to `/implement`:**
- `/implement-batch` is a higher-level orchestrator that runs `/implement` for each ticket
- `/implement` handles the full development cycle for a single ticket
- `/implement-batch` adds: batching, ordering, branching strategy, cross-cutting quality passes

**Relationship to `/scope`:**
- `/scope` creates tickets; `/implement-batch` consumes them
- Typical flow: `/scope` to plan and create tickets, then `/implement-batch` to implement the batch

**Relationship to `/refactor`, `/review-doc`:**
- These run as cross-cutting quality passes after all tickets are implemented
- They catch issues that span multiple tickets or emerge from their interaction
