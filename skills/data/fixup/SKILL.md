---
name: fixup
description: Create a fixup commit and autosquash rebase
allowed-tools: Bash(git status:*), Bash(git fetch:*), Bash(git log:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git rebase:*), Read, Glob
---

# Fixup

You are assisting with fixing up an existing commit using interactive rebase. Follow these steps:

## 1. Initial Assessment

- Run `git status` to see if there are uncommitted changes
- Run `git fetch origin` to get latest remote updates
- Display existing commits with `git log origin/main..HEAD --oneline`

## 2. Create Fixup Commit

If there are uncommitted changes:

1. Show the commit history
2. Ask user which commit hash to fixup (or identify it based on context)
3. Stage changes with `git add .` or ask which files to stage
4. Create a fixup commit:

   ```bash
   git commit --fixup=<commit-hash>
   ```

## 3. Autosquash Rebase

Run non-interactive rebase with autosquash:

```bash
git rebase --autosquash origin/main
```

## 4. Commit Message Review

After rebase completes, verify the commit message matches the changes:

1. Display the rebased commit:

   ```bash
   git show HEAD --stat
   ```

2. Compare the commit message body with the actual changes

3. If the message is inaccurate or incomplete:
   - Draft a corrected commit message following the `commit-message` rule
   - Explain what needs to be updated and why
   - Update with `git commit --amend`

## 5. Post-Rebase Actions

After message review:

1. Display the final commit history:

   ```bash
   git log origin/main..HEAD --oneline
   ```

2. Inform the user to run `/publish` to push changes and update the PR

## Key Principles

- Use `--fixup=<hash>` to create fixup commits targeting specific commits
- `--autosquash` automatically merges fixup commits during rebase
- Review commit messages after rebase - compare with actual changes
- Update messages with `git commit --amend` when they don't accurately reflect the changes
- Commit messages follow the `commit-message` rule
