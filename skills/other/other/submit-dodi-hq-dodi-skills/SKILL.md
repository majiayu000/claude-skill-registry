---
name: submit
description: Use after review passes — creates PR, waits for CI, and merges only after CI is green
---

# Submit

Create a PR, wait for CI to pass, then merge.

## Process

1. **Pre-flight:**
   - Verify you're on a feature branch (not main/master)
   - Check for uncommitted changes — commit or warn
   - Ensure branch is pushed to remote
   - **Run `/quality-gate`** — this is mandatory. Invoke the quality-gate skill to run compliance checks, create tests, and run the test suite. Do NOT skip this step.

2. **Create PR:**
   ```bash
   git push -u origin <branch>
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   ## Summary
   <2-3 bullets>

   ## Test Plan
   - [ ] <verification steps>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

3. **Enable auto-merge:**
   GitHub will automatically squash-merge once CI passes and delete the remote branch.

   ```bash
   gh pr merge <pr-number> --squash --delete-branch --auto
   ```

   - Report the PR URL to the user
   - Update ticket status if tracker tools available
   - **Do NOT poll or wait** — auto-merge handles it asynchronously

   Note: Local worktree and branch cleanup happens automatically at the next `pickup`.

## Key Rules

- **Never force-merge or use --admin** without explicit user approval
- **Always squash-merge** (clean history)
- **Always use --auto** — let GitHub merge when CI passes, don't block the conversation
- **Delete branch after merge** (keep repo clean)
