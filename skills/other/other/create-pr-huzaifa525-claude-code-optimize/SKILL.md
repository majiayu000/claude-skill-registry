---
name: create-pr
description: Use when the user wants to create a pull request, open a PR, or submit changes for review.
disable-model-invocation: true
allowed-tools: Bash
argument-hint: "[base-branch]"
---

Create a pull request for the current branch.

## Steps

1. **Gather context**
   ```
   git branch --show-current
   git log main..HEAD --oneline
   git diff main..HEAD --stat
   git diff main..HEAD
   ```

2. **Analyze ALL commits** on this branch (not just the latest)

3. **Generate PR**

   - **Title**: Under 70 characters, describes the change
   - **Body**: Summary bullets + test plan

4. **Push and create PR**
   ```
   git push -u origin $(git branch --show-current)
   ```

   Then create PR:
   ```
   gh pr create --title "title" --body "$(cat <<'EOF'
   ## Summary
   - Bullet point 1
   - Bullet point 2
   - Bullet point 3

   ## Changes
   - [file] — [what changed and why]

   ## Test Plan
   - [ ] Test step 1
   - [ ] Test step 2
   - [ ] Test step 3
   EOF
   )"
   ```

5. **Return the PR URL**

## If $ARGUMENTS is provided

Use it as the base branch instead of `main`.

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
