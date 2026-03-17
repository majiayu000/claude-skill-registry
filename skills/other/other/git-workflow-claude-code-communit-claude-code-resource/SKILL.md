---
name: git-workflow
description: Git best practices including commit message conventions, interactive rebase, conflict resolution, and repository hygiene. Reference for all git operations.
---

# Git Workflow

## Conventional Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type       | Purpose                                      | Example                                      |
|------------|----------------------------------------------|----------------------------------------------|
| `feat`     | New feature for the user                     | `feat(auth): add OAuth2 login flow`          |
| `fix`      | Bug fix for the user                         | `fix(cart): correct quantity calculation`     |
| `refactor` | Code change that neither fixes nor adds      | `refactor(api): simplify request middleware`  |
| `docs`     | Documentation only changes                   | `docs(readme): add setup instructions`       |
| `test`     | Adding or correcting tests                   | `test(auth): add login failure scenarios`    |
| `chore`    | Maintenance tasks, dependencies              | `chore(deps): upgrade lodash to 4.17.21`    |
| `perf`     | Performance improvement                      | `perf(query): add index for user lookup`     |
| `style`    | Formatting, whitespace, semicolons           | `style(lint): fix indentation in models`     |
| `ci`       | CI configuration and scripts                 | `ci(actions): add Node 20 to test matrix`    |
| `revert`   | Reverts a previous commit                    | `revert: revert feat(auth) commit abc123`    |

### Commit Message Rules

- Subject line: max 72 characters, imperative mood, no trailing period
- Body: wrap at 80 characters, explain what and why (not how)
- Footer: reference issues with `Closes #123` or `Refs #456`
- Breaking changes: add `BREAKING CHANGE:` in the footer or `!` after type

```
feat(api)!: change authentication endpoint response shape

The /auth/login endpoint now returns a nested token object instead
of a flat structure. This aligns with our OAuth2 token standard.

BREAKING CHANGE: response.token is now response.auth.access_token
Closes #892
```

## Commit Atomicity

Each commit must represent exactly one logical change.

- [ ] Address a single concern (one bug fix, one feature slice, one refactor)
- [ ] Leave the codebase in a working state (tests pass, code compiles)
- [ ] Be revertable without side effects on unrelated code
- [ ] Include related test changes alongside the code change
- [ ] Never mix formatting with logic changes
- [ ] Never bundle unrelated bug fixes together

```bash
# Stage specific hunks, specific files, then verify
git add -p
git add src/auth/login.ts src/auth/login.test.ts
git diff --cached
```

## Interactive Rebase

```bash
git rebase -i HEAD~5      # Rebase last N commits
git rebase -i main        # Rebase onto a branch
```

### Rebase Commands

| Command    | Short | Effect                                          |
|------------|-------|-------------------------------------------------|
| `pick`     | `p`   | Keep the commit as-is                           |
| `reword`   | `r`   | Keep the commit but edit the message            |
| `edit`     | `e`   | Pause to amend the commit (add files, split)    |
| `squash`   | `s`   | Merge into the previous commit, keep message    |
| `fixup`    | `f`   | Merge into previous commit, discard message     |
| `drop`     | `d`   | Remove the commit entirely                      |

**Squash WIP commits:**
```
pick   a1b2c3d feat(auth): add login endpoint
fixup  e4f5g6h wip
fixup  i7j8k9l fix tests
```

**Fixup a commit further back:**
```bash
git commit --fixup=<target-sha>
git rebase -i --autosquash main
```

**Split a commit (mark as "edit"):**
```bash
git reset HEAD~1
git add src/models/user.ts
git commit -m "refactor(models): extract user validation"
git add src/routes/auth.ts
git commit -m "feat(auth): add login route"
git rebase --continue
```

## Merge vs Rebase

| Use Rebase                                   | Use Merge                                         |
|----------------------------------------------|---------------------------------------------------|
| Updating feature branch from main            | Integrating feature branch into main (`--no-ff`)  |
| Cleaning up local commits before pushing     | Shared branches others have based work on         |
| Maintaining linear history on personal branch | Preserving context of parallel development        |

- Never rebase commits pushed to a shared branch
- Always rebase local work before pushing
- Use `git pull --rebase` to avoid unnecessary merge commits

```bash
git checkout feature/login && git rebase main          # Update feature
git checkout main && git merge --no-ff feature/login   # Merge feature
```

## Conflict Resolution

1. **Identify:** `git status` -- look for "both modified" entries
2. **Understand both sides:**
   ```bash
   git show :1:path/to/file    # base version
   git show :2:path/to/file    # ours (current branch)
   git show :3:path/to/file    # theirs (incoming branch)
   ```
3. **Resolve each conflict block**, then mark resolved:
   ```bash
   git add path/to/file
   git rebase --continue    # or git merge --continue
   ```

| Strategy       | When to Use                                    |
|----------------|------------------------------------------------|
| Accept ours    | Their change is outdated or wrong              |
| Accept theirs  | Our change was superseded                      |
| Manual merge   | Both changes are needed, combine them          |
| Re-implement   | Both sides diverged too far, rewrite the block |

Abort with: `git merge --abort` or `git rebase --abort`

## .gitignore Patterns

```gitignore
# Node.js                    # Python                     # Java / Kotlin
node_modules/                 __pycache__/                  *.class
dist/                         *.py[cod]                     target/
*.log                         .venv/                        build/
coverage/                     *.egg-info/                   .gradle/

# IDE and OS                  # Secrets (always ignore)
.idea/                        *.pem
.vscode/                      *.key
.DS_Store                     .env*
Thumbs.db                     !.env.example
```

| Pattern         | Matches                              |
|-----------------|--------------------------------------|
| `*.log`         | All .log files in any directory      |
| `/build`        | build directory in repo root only    |
| `build/`        | build directory anywhere             |
| `**/logs`       | logs directory at any depth          |
| `!important`    | Negate a previous ignore rule        |
| `doc/**/*.txt`  | txt files anywhere under doc/        |

## Git Hooks

| Hook                  | Trigger                    | Common Use                          |
|-----------------------|----------------------------|-------------------------------------|
| `pre-commit`          | Before commit is created   | Lint, format, run fast tests        |
| `commit-msg`          | After message is written   | Validate conventional commit format |
| `pre-push`            | Before push to remote      | Run full test suite                 |
| `prepare-commit-msg`  | Before editor opens        | Add branch name or ticket number    |

```bash
#!/usr/bin/env bash
# .git/hooks/commit-msg
commit_msg=$(cat "$1")
pattern='^(feat|fix|refactor|docs|test|chore|perf|style|ci|revert)(\(.+\))?(!)?: .{1,72}'
if ! echo "$commit_msg" | grep -qE "$pattern"; then
  echo "ERROR: Commit message does not follow conventional format."
  exit 1
fi
```

## Stashing

```bash
git stash push -m "wip: login form validation"   # Save with message
git stash list                                     # List all stashes
git stash apply                                    # Apply most recent (keep in list)
git stash pop                                      # Apply and remove most recent
git stash apply stash@{2}                          # Apply specific stash
git stash drop stash@{0}                           # Drop specific stash
git stash clear                                    # Clear all stashes
git stash push -u -m "include new files"           # Include untracked files
git stash branch feature/from-stash stash@{0}      # Create branch from stash
```

## Cherry-Picking

```bash
git cherry-pick -x abc123              # Always use -x to record source
git cherry-pick abc123..def456         # Cherry-pick a range
git cherry-pick --no-commit abc123     # Stage only, do not commit
git cherry-pick --abort                # Abort a conflicted cherry-pick
```

The `-x` flag appends `(cherry picked from commit ...)` for traceability.

## Git Bisect

```bash
git bisect start
git bisect bad                         # Mark current state as bad
git bisect good v2.1.0                 # Mark a known good commit
# Test each checkout, then: git bisect good / git bisect bad
git bisect start HEAD v2.1.0           # Automate with a test script
git bisect run npm test
git bisect reset                       # When done, return to original state
```

## Amending Commits Safely

```bash
git commit --amend -m "fix(auth): correct token expiry check"
git add forgotten-file.ts && git commit --amend --no-edit
git commit --amend --author="Name <email@example.com>"
```

### Safety Checklist

- [ ] The commit has NOT been pushed to a shared branch
- [ ] No one else has based work on this commit
- [ ] Never amend commits on main, master, develop, or release branches
- [ ] Use `--force-with-lease` instead of `--force` when pushing amended commits

## Daily Workflow

```bash
git checkout main && git pull --rebase
git checkout -b feature/ticket-123-description
git add -p && git commit -m "feat(module): add feature description"
git fetch origin && git rebase origin/main
git rebase -i origin/main              # Clean up before review
git push -u origin feature/ticket-123-description
```
