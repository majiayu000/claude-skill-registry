---
description: Fetch Jira ticket, create branch, implement changes, commit, push, open PR.
argument-hint: <ticket-key> [--gw | --worktree]
---

# Implement Jira Task

You are a software engineer. This skill takes a Jira ticket key, reads its
description, and implements the work end-to-end: branch creation, code changes,
commits, push, and PR.

## Argument Parsing

Parse `$ARGUMENTS` to extract:

- **Ticket key**: The Jira ticket key (e.g., `NIMBUS-123`). Required.
- **`--gw`**: Use the `gw` CLI to create a worktree for the feature branch.
- **`--worktree`**: Use Claude Code's `EnterWorktree` tool to create an isolated
  worktree. Falls back to `git worktree add` if `EnterWorktree` is unavailable.

`--gw` and `--worktree` are mutually exclusive. If neither is provided, use the
default behavior (create a branch in the current working tree).

> **IMPORTANT — Restore Context**
>
> This skill uses `/agent-restore-context` to survive `/clear` and `/compact`.
>
> - **Step 0**: `/agent-restore-context check` to verify the hook is set up.
> - **Step 3a**: `/agent-restore-context write jira-implement-task` after
>   creating the implementation plan.
> - **Before each `/clear`**: `/agent-restore-context write jira-implement-task`
>   with the updated current task number and all other necessary information.
> - **Step 3e**: `/agent-restore-context delete jira-implement-task` when done.

## Step 0: Verify Restore Context

Invoke `/agent-restore-context check`. This verifies the hook is configured and
will invoke `/agent-restore-context-setup` if needed.

## Project Configuration

Before starting, read the project's `CLAUDE.md` and/or `AGENTS.md` to determine
the following project-specific settings. These files are the source of truth for
how to work in this repo.

| Setting                  | What to look for                                                | Fallback default      |
| ------------------------ | --------------------------------------------------------------- | --------------------- |
| **Test command (files)** | Command to run tests for specific files/folders                 | `pnpm test <files>`   |
| **Test command (full)**  | Command to run the full test suite                              | `pnpm test`           |
| **Branch naming**        | Branch naming convention or prefix rules                        | `<TICKET-KEY>-<slug>` |
| **Base branch**          | Default branch to branch from                                   | `main`                |
| **Commit format**        | Commit message convention                                       | Conventional commits  |
| **Component workflow**   | Command/process for new components (e.g., `/propose-component`) | None                  |
| **Available agents**     | Specialized agents for research, coding, review                 | None                  |

If a setting is not found in `CLAUDE.md`, `AGENTS.md`, `rules/`, or `/docs`, ask the
user whether they want to add it to `CLAUDE.md`, `AGENTS.md`, `rules/` or `/docs` — or
use the fallback default for this run only.

## Step 1: Fetch Ticket Details

Use the Atlassian MCP tools to retrieve the ticket:

1. Call `mcp__atlassian__getAccessibleAtlassianResources` to get the cloud ID
2. Call `mcp__atlassian__getJiraIssue` with the cloud ID and ticket key
3. Extract: **Summary**, **Description** (requirements, acceptance criteria,
   files), and **Issue type**

If the ticket cannot be found, report the error and stop. Always write Markdown
to Jira, never ADF — the MCP tools handle conversion.

## Step 2: Create a Feature Branch

Determine the branch name using the project's **branch naming** convention and
the **base branch** from project configuration.

### Default mode (no flag)

Create a branch from the base branch in the current working tree:

```bash
git checkout <base-branch>
git pull
git checkout -b <branch-name>
```

If the branch already exists, ask the user whether to check out the existing
branch or create a new one with a `-v2` suffix.

### `--gw` mode

Use the `gw` CLI to create a worktree with the feature branch:

```bash
gw task <branch-name>
```

This creates a new worktree and switches into it. All subsequent work in this
skill happens inside the worktree directory returned by `gw`. Include the
worktree path in the restore context so future `/clear` cycles can `cd` back
into it.

### `--worktree` mode

Use Claude Code's `EnterWorktree` tool to create an isolated worktree:

1. Call `EnterWorktree` with `name` set to the branch name.
2. If `EnterWorktree` is unavailable or fails, fall back to manual git
   worktree creation:
   ```bash
   git worktree add .claude/worktrees/<branch-name> -b <branch-name> <base-branch>
   cd .claude/worktrees/<branch-name>
   ```
3. All subsequent work in this skill happens inside the worktree directory.
   Include the worktree path in the restore context so future `/clear` cycles
   can `cd` back into it.

## Step 3: Implement Changes

### 3a: Understand Scope and Plan

1. **Understand scope**: Read the ticket description carefully. Identify all
   files to modify/create.
2. **Read existing files**: Always read files before modifying them.
3. **Create implementation plan**: Break the changes into the smallest
   reasonable chunks of work. Save the plan to
   `<skills-dir>/jira-implement-task/plans/<TICKET-KEY>-plan.md` (where
   `<skills-dir>` is `.agents/skills/` or `.claude/skills/` per the detected
   layout). Each task should be independently testable and committable. Commit
   the plan so it can be shared for handoff. Delete it before merging or keep
   it as a record.
4. **Create restore context**: Invoke `/agent-restore-context write jira-implement-task`
   with content that includes the ticket key, branch name, plan file path,
   current task number (1), and the instruction to invoke
   `/jira-implement-task <TICKET-KEY>` and read the plan file before doing any
   work.

### 3b: Red/Green Testing Loop (per task)

For each task in the implementation plan, follow this cycle:

1. Invoke `/agent-restore-context write jira-implement-task` with the current
   task number.
2. Run `/clear`.
3. **Write tests first** (red phase): Write or update tests that capture the
   expected behavior for this task. Tests should fail at this point.
4. **Get user approval on tests**: Present the tests to the user and get
   explicit approval before proceeding. Do NOT implement changes until tests are
   approved.
5. **Commit the tests**: Once approved, commit the failing tests with a message
   like `test(<scope>): add tests for <task description>`.
6. **Implement changes** (green phase): Write the minimum code to make the tests
   pass.
7. **Run tests**: Verify all tests pass using the project's **test command
   (files)**.

### 3c: Three Strikes Policy

If the implementation fails to make tests pass after **3 attempts**:

1. **Revert** the branch to the last testing commit (the committed failing
   tests).
2. Invoke `/agent-restore-context write jira-implement-task`.
3. Run `/clear`.
4. **Try again** from the green phase with a fresh approach.

If the second full attempt also fails after 3 strikes, stop and ask the user for
guidance.

### 3d: Commit and Advance

Once tests pass:

1. Commit the implementation changes.
2. Invoke `/agent-restore-context write jira-implement-task` with the next
   task number.
3. Run `/clear`.
4. Move on to the next task in the implementation plan.

### 3e: Completion

Once all tasks in the plan are implemented and passing:

1. **Run full test suite**: Run the project's **test command (full)** to verify
   everything passes.
2. Invoke `/agent-restore-context delete jira-implement-task`.
3. Ask the user whether to **delete the implementation plan file** or keep it.
4. Proceed to Step 4 (push and PR creation).

### Guidelines

- Follow the project's conventions from `CLAUDE.md` / `AGENTS.md`
- If the ticket is ambiguous, ask the user for clarification before proceeding
- If the project defines a **component workflow**, use it for new component
  tickets
- If the project defines **available agents**, use them when task complexity
  warrants it

## Step 4: Push and Create PR

### Permission check

Run `gh repo view --json viewerPermission --jq '.viewerPermission'`. If the
result is `READ`, skip push and PR — print the exact `git push` and
`gh pr create` commands for the user to run manually, then stop.

### Push and create PR

```bash
git push -u origin <branch-name>
gh pr create --title "<type>(<scope>): <summary>" --body "$(cat <<'EOF'
## Summary
<1-5 bullet points describing the changes>

Closes <TICKET-KEY>

## Test plan
- [ ] <verification steps>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Return the PR URL to the user when done.

---

**Implement Jira task: $ARGUMENTS**
