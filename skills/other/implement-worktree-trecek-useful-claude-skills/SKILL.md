---
name: implement-worktree
description: Implement a plan in an isolated git worktree. Use when user says "implement in worktree", "worktree implement", or "isolated implementation". Creates a worktree from current branch, explores affected systems with subagents, then implements phase by phase.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '🌳 [SKILL: implement-worktree] Setting up isolated worktree implementation...'"
          once: true
---

# Implement in Worktree Skill

Implement a provided plan in an isolated git worktree branched from the current branch.

## When to Use

- User says "implement in worktree", "worktree implement", "isolated implementation"
- User provides a plan and wants it executed in a fresh worktree

## Arguments

`{plan_path}`   — Absolute path to the implementation plan file (required)

## Critical Constraints

**NEVER:**
- Implement without first exploring affected systems with subagents
- Implement in the main working directory (always use the worktree)
- Force push or perform destructive git operations
- Consider implementation complete if ANY test fails
- Blame test failures on "pre-existing issues" — ALL tests must pass
- Re-run tests just to see failures — grep the saved output file instead

**ALWAYS:**
- Create a new worktree from the current branch
- Use subagents to deeply understand affected systems BEFORE implementing
- Implement one phase at a time
- Run the project's test suite after implementation
- Rebase onto base branch before completion (ready for squash-and-merge)

## Workflow

### Step 0: Validate Prerequisites

1. Verify plan exists (file path or pasted content)
2. **Check for dry-walkthrough verification:** Read the first line of the plan file. If it does not contain exactly `Dry-walkthrough verified = TRUE`:
   - Display warning: "⚠️ WARNING: This plan has NOT been validated with a dry-walkthrough. Implementation may encounter issues that could have been caught beforehand."
   - Use `AskUserQuestion` to prompt: "Do you want to continue without dry-walkthrough validation?"
   - If user declines, abort and suggest running `/dry-walkthrough` first
3. Check `git status --porcelain` — if dirty, warn user
4. Parse plan: phases, files per phase, verification commands
5. **Multi-Part Plan Detection:** Examine the plan filename. If it contains `_part_` (e.g., `_part_a`, `_part_b`, `_part_1`):
   - Extract the part identifier (A, B, C… or number) from the suffix.
   - **SCOPE FENCE — MANDATORY:** Before any exploration or implementation begins, output the following constraint:
     > "🚧 SCOPE FENCE ACTIVE: I am implementing PART {X} ONLY. I MUST NOT open, read, or execute any other part files, regardless of what I encounter in temp/ or any other directory. Sibling part files are out of scope for this entire session."
   - When launching subagents in Step 2, include this fence instruction explicitly in each subagent prompt so that the subagents do not open, read, or reference sibling part files.

### Step 1: Create Git Worktree

```bash
WORKTREE_NAME="impl-{plan_name}-$(date +%Y%m%d-%H%M%S)"
WORKTREE_PATH="../worktrees/${WORKTREE_NAME}"
git worktree add -b "${WORKTREE_NAME}" "${WORKTREE_PATH}"
WORKTREE_PATH="$(cd "${WORKTREE_PATH}" && pwd)"
```

### Step 2: Deep System Understanding (Subagents)

Before implementing ANY code, launch parallel Explore subagents to understand affected systems:
- **Affected files** — current implementation, dependencies, consumers
- **Test coverage** — existing tests, patterns, fixtures for affected code
- **Integration points** — entry/exit points, contracts that must be maintained
- **Data flow** — state management, source of truth

### Step 3: Set Up Worktree Environment

Set up the project environment in the worktree following the project's standard setup procedure.

**Why isolated environment matters:** Running setup without proper isolation can overwrite global configuration files. When the worktree is deleted, commands may break with missing module errors.

**All commands in Steps 4–6 must run from the worktree directory.** Use absolute paths to avoid CWD drift across tool calls.

### Step 4: Implement Phase by Phase

For each phase:
1. Announce phase objective and files to modify
2. Implement changes guided by understanding from Step 2
3. Run per-phase verification if plan specifies it
4. Commit per phase if possible
5. Report phase completion

Where practical, delegate test updates to subagents to keep main conversation context lean.

### Step 4.5: Pre-Implementation Checklist

Before running the test suite, confirm the following to prevent avoidable test-fix cycles:

- [ ] **Architecture documentation** — if new modules, sub-packages, or files were added,
  any architecture sections in project documentation (e.g., CLAUDE.md) reflect them
- [ ] **Registration checks** — if the project maintains a registry of components
  (e.g., a plugin manifest, a module index, a command registry), verify any
  newly added components are registered. Missing registrations cause cascading test failures.
- [ ] **Documentation consistency** — if the project maintains architecture documentation
  or component counts, update them to reflect new components added during implementation.
- [ ] **Count-based test assertions** — if component counts have changed, update any
  `assert len(...) ==` or similar count assertions in the test suite before running tests

This checklist exists because these categories produce avoidable test-fix cycles: a single
missed registration generates 5–30 cascading test failures that require a second commit to fix.

### Step 5: Final Verification

Run linting and formatting checks, then run the project's test suite.

If tests fail: grep the saved output file (if the project captures output), fix the issue, then re-run.
Delete the exact test output file path when finished (no glob patterns).

### Step 6: Rebase for Squash-and-Merge

```bash
git fetch origin
git rebase origin/{base_branch}
```

If conflicts occur, resolve them, `git rebase --continue`, then re-run tests. Report rebase status.

### Step 7: Completion Report

Output to terminal: worktree path, branch name, base branch, status, summary of changes, and next steps (fast-forward merge then clean up).
Change directory before removing worktree to prevent deleting the cwd.
Always confirm the merge went through before removing work tree.
Do not merge until user confirms first!

## Error Handling

- **Worktree creation fails** — check `git worktree list`, suggest `git worktree prune`
- **Phase fails** — report which phase and why, offer to fix/retry, skip (if optional), or abort and clean up
- **Tests fail** — implementation is NOT complete. Fix the issue. If truly unfixable, report to user and ask for guidance. Do NOT proceed or mark as complete.
- **Rebase conflicts** — resolve keeping implementation intent intact, re-run full test suite after
