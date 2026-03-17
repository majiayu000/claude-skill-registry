---
name: task-complete
description: Complete a beads task — mark done, create PR, merge, and clean up worktree. Use after all tests pass and verification is complete.
disable-model-invocation: true
---

# Task Completion Workflow

## Steps

1. **Mark task done**: `bd close <id>`
2. **Create PR**: `gh pr create --base develop` with descriptive title and summary
3. **Code review**: `/code-review` → address any findings
4. **Watch CI**: `gh pr checks --watch`
5. **Merge PR**: `gh pr merge --squash`
6. **Remove worktree**:
   ```bash
   cd "$CLAUDE_PROJECT_DIR"
   git worktree remove ~/worktrees/property-tracker/<name>
   ```
7. **Next task**: `/compact` → `bd ready`

## When Ready to Release

1. Verify staging (`staging.bricktrack.au`) works correctly
2. Create PR: `develop` → `main`
3. Merge after CI passes
4. Production deploys automatically to `bricktrack.au`
