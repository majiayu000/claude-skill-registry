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
- Use `model: "sonnet"` when spawning all subagents via the Task tool
- Implement one phase at a time
- Run the project's test suite after implementation
- Rebase onto base branch before completion (ready for squash-and-merge)

## Context Limit Behavior

If this skill hits the Claude context limit mid-execution, the headless session
terminates with `needs_retry=true` in the tool response. The worktree remains
intact on disk with all commits made up to that point.

The orchestrator **must not** retry this skill when `needs_retry=true`. Retrying
creates a brand-new timestamped worktree, discarding all partial progress.

Correct orchestration on `needs_retry=true`:
- Route immediately to `/autoskillit:retry-worktree` (via `retry.on_exhausted`)
- Pass `worktree_path` from `context.worktree_path` (captured from this step's output)
- Use `max_attempts: 0` on this step's `retry` block to ensure immediate escalation

## Workflow

### Step 0: Validate Prerequisites

1. Extract and verify the plan path using **path detection**: scan the tokens
   after the skill name for the first one that starts with `/`, `./`, `temp/`,
   or `.autoskillit/` — that token is the plan path. Ignore any non-path words
   that appear before it. If no path-like token is found, treat the entire
   argument string as pasted plan content. Verify the resolved file exists before
   proceeding; if it does not, abort with:
   `"Plan file not found: {path}. Correct format: /autoskillit:implement-worktree <plan_path>"`
2. **Check for dry-walkthrough verification:** Read the first line of the plan file. If it does not contain exactly `Dry-walkthrough verified = TRUE`:
   - Display warning: "⚠️ WARNING: This plan has NOT been validated with a dry-walkthrough. Implementation may encounter issues that could have been caught beforehand."
   - Use `AskUserQuestion` to prompt: "Do you want to continue without dry-walkthrough validation?"
   - If user declines, abort and suggest running `/autoskillit:dry-walkthrough` first
3. Check `git status --porcelain` — if dirty, warn user
4. Parse plan: phases, files per phase, verification commands
5. **Multi-Part Plan Detection:** Examine the plan filename. If it contains `_part_` (e.g., `_part_a`, `_part_b`, `_part_1`):
   - Extract the part identifier (A, B, C… or number) from the suffix.
   - **SCOPE FENCE — MANDATORY:** Before any exploration or implementation begins, output the following constraint:
     > "🚧 SCOPE FENCE ACTIVE: I am implementing PART {X} ONLY. I MUST NOT open, read, or execute any other part files, regardless of what I encounter in temp/ or any other directory. Sibling part files are out of scope for this entire session."
   - When launching subagents in Step 2, include this fence instruction explicitly in each subagent prompt so that the subagents do not open, read, or reference sibling part files.

### Step 1: Create Git Worktree

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
WORKTREE_NAME="impl-{plan_name}-$(date +%Y%m%d-%H%M%S)"
WORKTREE_PATH="../worktrees/${WORKTREE_NAME}"
git worktree add -b "${WORKTREE_NAME}" "${WORKTREE_PATH}"
WORKTREE_PATH="$(cd "${WORKTREE_PATH}" && pwd)"
mkdir -p ".autoskillit/temp/worktrees/${WORKTREE_NAME}"
echo "${CURRENT_BRANCH}" > ".autoskillit/temp/worktrees/${WORKTREE_NAME}/base-branch"
```

### Step 1.5: Initialize Code Index for Original Project

Set the MCP code-index project path to the **original project directory** so Explore subagents can use code search tools:

```
mcp__code-index__set_project_path(path="{ORIGINAL_PROJECT_PATH}")
```

This must happen before Step 2 or any code-index search tools will fail with "Project path not set."

### Step 2: Deep System Understanding (Subagents)

Before implementing ANY code, launch parallel Explore subagents to understand affected systems:
- **Affected files** — current implementation, dependencies, consumers
- **Test coverage** — existing tests, patterns, fixtures for affected code
- **Integration points** — entry/exit points, contracts that must be maintained
- **Data flow** — state management, source of truth

### Step 3: Set Up Worktree Environment

Set up the project's development environment in the worktree. Use the project's configured `worktree_setup.command` from `.autoskillit/config.yaml` if available. If not configured, check for a Taskfile with `install-worktree` task, or detect the project type and run appropriate setup.

```bash
cd "${WORKTREE_PATH}"
# If worktree_setup.command is configured, run it. Otherwise:
task install-worktree   # or equivalent for the project type
```

**Why isolated env matters:** Installing packages without isolation overwrites the global state. When the worktree is deleted, CLI commands break with import errors.

**All commands in Steps 4–6 must run from `${WORKTREE_PATH}`.** Use absolute paths to avoid CWD drift across Bash tool calls.

### Step 3.5: Re-point Code Index to Worktree (REQUIRED)

**CRITICAL:** After setting up the worktree environment, you **MUST** update the MCP code-index project path to the worktree. This ensures all subsequent code searches operate on the worktree's files (which will diverge from the original as implementation proceeds):

```
mcp__code-index__set_project_path(path="${WORKTREE_PATH}")
```

**Failure to do this means code-index searches will return results from the original project, not your worktree — leading to confusion and incorrect file reads.**

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

- [ ] **CLAUDE.md architecture section** — if new modules, sub-packages, or files were added,
  the `## Architecture` section in CLAUDE.md reflects them
- [ ] **Recipe diagrams** — if any recipe YAML file was added or modified, either regenerate
  diagrams (`task diagrams`) or confirm new diagram files are listed in `.gitignore`
- [ ] **Project-specific registration checks** — if the project maintains a registry of
  components (e.g., a tool registry, a plugin manifest, a module index), verify any
  newly added components are registered. This prevents cascading test failures caused
  by missing registrations rather than implementation bugs.
- [ ] **Documentation consistency** — if the project maintains architecture documentation
  or a component count (e.g., in CLAUDE.md, README, or API docs), update it to reflect
  new components added during this implementation.
- [ ] **Count-based test assertions** — if tool, skill, or rule counts have changed, update any
  `assert len(...) ==` assertions in the test suite before running `{test_command}`

This checklist exists because these categories produce avoidable test-fix cycles: a single
missed registration generates 5–30 cascading test failures that require a second commit to fix.

### Step 5: Final Verification

Read the configured test command from `.autoskillit/config.yaml` (key: `test_check.command`). Use this command wherever `{test_command}` appears below. If no config exists, use `task test-check` as the default.

Run the project's code quality checks and test suite from the worktree.

```bash
cd "${WORKTREE_PATH}" && pre-commit run --all-files
cd "${WORKTREE_PATH}" && {test_command}
```

If tests fail, fix the issue and re-run.

### Step 6: Rebase for Squash-and-Merge

```bash
CURRENT_BRANCH=$(cat ".autoskillit/temp/worktrees/${WORKTREE_NAME}/base-branch")
git fetch origin
git rebase origin/${CURRENT_BRANCH}
```

If conflicts occur, resolve them, `git rebase --continue`, then re-run tests. Report rebase status.

### Step 7: Completion Report

Output to terminal: worktree path, branch name, base branch, status, summary of changes, and next steps (fast-forward merge then clean up).
Change directory before removing worktree to prevent deleting the cwd.
Always confirm the merge went through before removing work tree.
Do not merge until user confirms first!

Then emit these structured output tokens on their own lines so recipe capture blocks can extract them:

```bash
CURRENT_BRANCH=$(cat ".autoskillit/temp/worktrees/${WORKTREE_NAME}/base-branch")
```

```
worktree_path = ${WORKTREE_PATH}
branch_name = ${WORKTREE_NAME}
base_branch = ${CURRENT_BRANCH}
```

### Step 7.5: Reset Code Index to Original Project (REQUIRED)

**CRITICAL:** After worktree cleanup, you **MUST** reset the MCP code-index project path back to the original project directory:

```
mcp__code-index__set_project_path(path="{ORIGINAL_PROJECT_PATH}")
```

**Failure to do this leaves code-index pointing at a deleted worktree path, breaking all subsequent code searches in any session.**

## Error Handling

- **Worktree creation fails** — check `git worktree list`, suggest `git worktree prune`
- **Phase fails** — report which phase and why, offer to fix/retry, skip (if optional), or abort and clean up
- **Tests fail** — implementation is NOT complete. Fix the issue. If truly unfixable, report to user and ask for guidance. Do NOT proceed or mark as complete.
- **Rebase conflicts** — resolve keeping implementation intent intact, re-run full test suite after
