---
name: worktree-spawn
description: Spawn an independent Claude instance in a git worktree to work on a task in parallel. Use when the user wants to delegate a task to run independently while continuing the current conversation.
argument-hint: <task description>
---

# Worktree Spawn

Spawn an independent Claude instance in a separate git worktree to work on a task in parallel.

## When to Use

- User wants to delegate a task to run independently
- Task can be completed without further interaction
- User wants to continue working on something else in the current session

## Workflow

1. Determine branch name using author initials (from `git config user.initials` or `git config user.name`) and task description
2. Choose a worktree directory name (typically `../aztec-<feature-name>`)
3. Create the worktree with a new branch
4. Spawn Claude in the worktree with a detailed task prompt

## Command Template

```bash
cd $(git rev-parse --show-toplevel) && \
git worktree add -b <author>/<branch-name> ../<worktree-dir-name> && \
cd ../<worktree-dir-name>/yarn-project && \
claude "$(cat <<'EOF'
Task: [Brief task description]

Steps:
1. [Step 1]
2. [Step 2]
...

IMPORTANT: Read CLAUDE.md first to understand the project structure and workflow.

[Any additional context or requirements]
- Working directory: yarn-project in the worktree
- Branch: <author>/<branch-name>
- PR target: next (unless specified otherwise)
EOF
)"
```

## Example

For a task "Fix bug #123 in the sequencer":

```bash
cd $(git rev-parse --show-toplevel) && \
git worktree add -b jd/fix-bug-123 ../aztec-fix-bug && \
cd ../aztec-fix-bug/yarn-project && \
claude "$(cat <<'EOF'
Task: Fix bug #123 in the sequencer

Steps:
1. Investigate the issue in sequencer package
2. Implement fix
3. Add tests
4. Compile and run tests
5. Commit and create PR

IMPORTANT: Read CLAUDE.md first to understand the project structure and workflow.
EOF
)"
```

## Key Points

- Always go to git root first before creating worktree
- Use `-b` flag to create a new branch
- Navigate to `yarn-project` within the worktree
- Always include "Read CLAUDE.md first" in the prompt
- Worktree directories are typically named `../aztec-<feature-name>`
- The spawned Claude instance works independently from the current session
- PR target is `next` unless specified otherwise
