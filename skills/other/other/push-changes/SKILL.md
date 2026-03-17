---
name: push-changes
description: Push git changes to remote with full workflow including status check, staging, committing, and pushing. Use when the user asks to push changes, push up code, or sync with remote. Includes safety check to prevent pushing directly to main branch.
---

# Push Changes

Push local changes to the remote repository with safety checks.

## Workflow

1. **Check current branch**

   ```bash
   git branch --show-current
   ```

   **STOP if on `main` or `master`**: Warn the user they forgot to create a branch. **ALWAYS use the AskQuestion tool:**
   - Title: "Branch Required"
   - Question: "You're currently on the main branch. What branch name would you like to use?"
   - Options:
     - id: "custom", label: "Let me specify a branch name"
     - id: "abort", label: "Abort, I'll create it myself"

   If the user selects "custom", ask them conversationally for the branch name, then create and switch to it:

   ```bash
   git checkout -b <branch-name>
   ```

2. **Check status**

   ```bash
   git status
   ```

   Review untracked files and modifications.

3. **Stage changes**

   ```bash
   git add -A
   ```

   Or selectively add specific files if the user prefers.

4. **Review staged changes**

   ```bash
   git diff --staged --stat
   ```

5. **Commit with descriptive message**
   Analyze the changes and create a commit message following conventional commits format:

   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <description>

   <optional body>
   EOF
   )"
   ```

   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

6. **Push to remote**

   ```bash
   git push -u origin HEAD
   ```

7. **Verify push succeeded**
   ```bash
   git status
   ```
   Confirm the branch is up to date with remote.

## Safety Rules

- **Never push to `main` or `master`** - always create a feature branch first
- **Never force push** unless explicitly requested by the user
- **Review changes** before committing to avoid committing secrets or unwanted files
