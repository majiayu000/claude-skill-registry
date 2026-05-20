---
name: git-commit
description: Git workflow automation for commits, branches, and PRs. Triggers on "commit", "push", "create PR", "git workflow".
---

# Git Commit

Structured git workflow for commits, branch management, and PR creation.

## When to Use

- Committing completed work
- Creating feature branches
- Pushing to remote
- Creating pull requests

## Core Principles

- Write descriptive commit messages (why, not what)
- One logical change per commit
- Never commit secrets (.env, credentials)
- Always verify changes before committing

## Commit Workflow

### Step 1: Review Changes

```bash
git status                    # See all changes
git diff                      # See unstaged changes
git diff --staged             # See staged changes
```

### Step 2: Stage Changes

```bash
git add <specific-files>      # Stage specific files
# or
git add .                     # Stage all (verify no secrets first)
```

**Never commit**:
- `.env` files
- `node_modules/`
- `.next/` build output
- Credential files

### Step 3: Commit

**Message format**:

```
<type>: <description>

[optional body explaining why]
```

**Types**:
- `feat`: New feature or page
- `fix`: Bug fix
- `style`: Visual/styling changes
- `refactor`: Code restructuring (no behavior change)
- `docs`: Documentation only
- `chore`: Build, config, dependency updates

**Examples**:
```
feat: add mentors listing page with search and filter

fix: resolve navbar scroll detection on mobile Safari

style: update hero gradient to match new brand guidelines

refactor: extract reusable SectionHeading component
```

### Step 4: Push

```bash
git push -u origin HEAD       # Push and set upstream
```

## Branch Naming

```
feat/description              # New features
fix/description               # Bug fixes
style/description             # Visual changes
refactor/description          # Code restructuring
```

## PR Creation

```bash
gh pr create --title "feat: description" --body "$(cat <<'EOF'
## Summary
- [Change 1]
- [Change 2]

## Test Plan
- [ ] Verify on mobile
- [ ] Verify on desktop
- [ ] Check all links
EOF
)"
```

## Related Skills

| Skill | When to Chain |
|-------|--------------|
| review-pr | Review before committing |
| feature-dev | Commit after feature implementation |
