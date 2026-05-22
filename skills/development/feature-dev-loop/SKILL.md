---
name: feature-dev-loop
description: Execute feature lifecycle from beads issue to GitHub push without git locks or JSONL corruption. Triggers on "start feature", "implement issue", "feature workflow", "new feature".
---

# Feature Dev Loop

Execute a complete feature lifecycle: issue → code → sync.

## Prerequisites

- [ ] `bd` CLI available
- [ ] Git repository initialized
- [ ] `.beads/` directory exists
- [ ] No `.git/index.lock` file

Run `scripts/validate.sh` to verify.

## Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| title | string | yes | - | Feature title for beads issue |
| type | feature\|bugfix\|chore | no | feature | Issue type |
| priority | P0\|P1\|P2\|P3\|P4 | no | P2 | Issue priority |
| scope | string | no | core | Commit scope |
| use_worktree | boolean | no | false | Create isolated worktree |

## Procedure

### Step 1: Create Issue

@check: No existing issue with same title

@command:
```bash
ISSUE_ID=$(bd create --title="<title>" --type=<type> --priority=<priority> --json 2>/dev/null | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Created: $ISSUE_ID"
```

@output: Issue ID (e.g., `superpowers-abc`)

@on-error: Check `bd list` for duplicate titles

---

### Step 2: Worktree Isolation (Optional)

@check: `use_worktree` is true AND branch does not exist

@command:
```bash
sp wt create feature/<slug> ../sp-<slug> --base=main
cd $(sp wt switch feature/<slug>)
```

@output: Working directory is isolated worktree

@on-error: If branch exists, use existing worktree or choose different name

---

### Step 3: Mark In Progress

@check: Issue exists and is open

@command:
```bash
bd update $ISSUE_ID --status=in_progress
```

@output: Issue status changed to `in_progress`

---

### Step 4: Implement

@check: Issue is in_progress

Execute coding task:
- Write code changes
- Add tests if applicable

@command:
```bash
pnpm --filter @sp/<package> build
pnpm --filter @sp/<package> test
```

@output: Build succeeds, tests pass

@on-error: Fix errors before proceeding

---

### Step 5: Finish (Atomic)

@check: Implementation complete, tests pass

Use the finish script for atomic close → sync → commit → push:

@command:
```bash
npx tsx .claude/skills/feature-dev-loop/scripts/finish.ts $ISSUE_ID "<type>(<scope>): <title>"
```

@output: Issue closed, JSONL synced, commit pushed

@on-error: Script provides recovery hints for each failure mode

The finish script (TypeScript):
1. **Pre-flight checks**: Validates git repo, bd CLI, issue exists, issue status
2. **Closes issue** with commit message as reason
3. **Syncs beads** (full sync, not just flush)
4. **Commits** with `BD_SKIP_AUTO_CREATE=1` to prevent auto-issue loop
5. **Handles "nothing to commit"** gracefully
6. **Pushes with retry** (auto-rebase on rejection, up to 3 attempts)
7. **Provides recovery hints** on failure with step-specific guidance

## Success Criteria

- [ ] `bd show $ISSUE_ID` returns `status: closed`
- [ ] `.beads/issues.jsonl` contains closed issue
- [ ] `git log -1` shows commit with issue ID
- [ ] `git status` shows clean working directory
- [ ] Remote branch updated (check with `git fetch && git status`)

## Error Recovery

The finish.ts script handles most errors automatically. Manual recovery only needed for:

| Error | Recovery Action |
|-------|-----------------|
| Rebase conflicts | Resolve conflicts, `git rebase --continue && git push` |
| Branch exists | Use `--force` or choose different worktree name |
| Tests fail | Fix code, re-run tests before Step 5 |
| Issue already closed | Manual commit: `git add . && git commit -m "..."` |

**Auto-handled by finish.ts:**
- `index.lock` cleanup
- Push rejection (auto-rebase retry)
- Nothing to commit (graceful skip)
- JSONL sync issues

## Output Schema

```json
{
  "status": "complete",
  "issue_id": "<beads-issue-id>",
  "commit": "<git-commit-hash>",
  "branch": "<branch-name>"
}
```
