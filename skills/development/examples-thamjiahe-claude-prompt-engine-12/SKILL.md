---
name: "Git Workflow"
description: "Enforces Conventional Commits, PR standards, merge conflict resolution, and branch management. Apply when committing code, opening PRs, resolving conflicts, managing branches, or handling Git operations."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
version: 2.1.0
compatibility: Claude Opus 4.5, Claude Code v2.x
updated: 2026-01-24
---

# Git Workflow

Systematic Git and GitHub workflows following Conventional Commits and your project's commit standards.

## Overview

This skill enforces:
- Atomic commits with clear intent (GH-3)
- Conventional Commits format (GH-1)
- Safe branch management and PR workflows
- Conflict resolution without data loss
- Issue linking and auto-close patterns

Apply when committing, branching, merging, or opening PRs.

## Commit Message Structure

Use this exact format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

- `feat`: New feature (MINOR version bump)
- `fix`: Bug patch (PATCH version bump)
- `docs`: Documentation only
- `style`: Formatting, whitespace (no logic change)
- `refactor`: Code restructure (no bug fix or feature)
- `perf`: Performance improvement
- `test`: Add or fix tests
- `build`: Build system or dependencies
- `ci`: CI/CD configuration
- `chore`: Maintenance (gitignore, etc.)
- `revert`: Revert previous commit

### Breaking Changes

Mark with `!` or footer:

```
feat!: drop Node 12 support

BREAKING CHANGE: requires Node 14+
```

### Rules

**GH-1 (MUST)**: Use Conventional Commits format
**GH-2 (SHOULD NOT)**: Never mention Claude or Anthropic
**GH-3 (MUST)**: Commits must be atomic and communicate intent
**GH-4 (MUST)**: Verbose beats ambiguous

### Good Examples

```
feat(auth): add password reset via email
fix(api): prevent race condition in user creation
docs: update README environment variables
refactor(db): extract user queries to separate module
test(payments): add Stripe webhook integration tests
```

### Anti-Patterns

```
update stuff           # ❌ What stuff?
fix bug                # ❌ Which bug?
wip                    # ❌ Work in progress is not a commit
asdfasdf               # ❌ Keyboard mashing
final version          # ❌ Meaningless
Claude helped me       # ❌ Violates GH-2
```

## Branching Strategy

### Branch Types and Naming

```
main                    # Production-ready, always stable
develop                 # Integration (if using Gitflow)
feature/user-auth       # New features
fix/payment-validation  # Bug fixes
hotfix/security-cors    # Critical production fixes
release/v2.1.0          # Release preparation
```

### Feature Branch Workflow

```bash
# 1. Create branch from main
git checkout main
git pull origin main
git checkout -b feature/my-feature

# 2. Work and commit atomically
git add file1.ts file2.ts
git commit -m "feat(feature): implement core logic"

# 3. Push and open PR
git push origin feature/my-feature

# 4. After merge, cleanup
git checkout main
git pull origin main
git branch -d feature/my-feature
```

## Pull Request Workflow

### Opening a PR

**Title**: Use Conventional Commit format

```
feat(payments): integrate Stripe payment processing
```

**Description template**:

```markdown
## Description
[What changed and why]

## Related Issues
Closes #123

## Changes Made
- Added X
- Fixed Y  
- Refactored Z

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing complete

## Breaking Changes
[If any]
```

### Pre-Merge Checklist

Before merging, verify:

- [ ] CI checks pass (prettier, eslint, TypeScript, tests)
- [ ] At least one approval (team policy)
- [ ] All conversations resolved
- [ ] Branch up-to-date with base
- [ ] Commit messages follow conventions

### Merge Strategy

**Squash and merge** (recommended): Clean history, single commit per feature
**Rebase and merge**: Linear history, preserve commit details
**Merge commit**: Full branch history preserved

## Merge Conflict Resolution

### Detection

Conflicts occur during:
- `git merge`
- `git pull`
- `git rebase`

Check status:
```bash
git status  # Shows conflicted files
```

### Manual Resolution Process

**Step 1**: Open conflicted file

Git marks conflicts with:
```
const value = 20;
```

**Step 2**: Resolve conflict

Edit file, remove markers, keep desired code:
```ts
const value = 20;
```

**Step 3**: Stage resolved file

```bash
git add path/to/file
```

**Step 4**: Complete merge

```bash
git commit -m "fix: resolve merge conflict in [file]"
```

### Strategy Options

Accept one side entirely:

```bash
# Keep current branch changes
git merge -s recursive -Xours feature-branch

# Keep incoming branch changes
git merge -s recursive -Xtheirs feature-branch
```

### Abort Merge

If stuck:
```bash
git merge --abort  # Resets to pre-merge state
```

### GitHub Web Resolution

For simple conflicts:
1. Open PR → "Resolve conflicts"
2. Edit in web editor
3. Remove `<<<<<<<`, `=======`, `>>>>>>>`
4. "Mark as resolved" → "Commit merge"

Note: Complex conflicts need command line.

## Issue Management

### Linking Issues to PRs

Use auto-close keywords in commit messages or PR description:

```
Closes #123
Fixes #456
Resolves #789
```

Multiple issues:
```
Closes #123, #456, #789
```

### Standard Labels

- `bug`: Something broken
- `feature`: New functionality
- `enhancement`: Improvement to existing
- `documentation`: Docs updates
- `good first issue`: Beginner-friendly
- `help wanted`: Need assistance
- `wontfix`: Won't be addressed
- `duplicate`: Already reported

## Pre-Commit Checklist

Before every commit, verify:

- [ ] Code follows CLAUDE.md guidelines
- [ ] Tests written and passing
- [ ] TypeScript compiles (`npx tsc --noEmit`)
- [ ] Linting passes (`pnpm lint`)
- [ ] Formatting applied (`npx prettier --write .`)
- [ ] No sensitive data (API keys, passwords)
- [ ] Commit message uses Conventional Commits
- [ ] Changes are atomic and focused

## Common Workflows

### Scenario 1: Feature Development

```bash
git checkout main
git pull origin main
git checkout -b feature/new-dashboard

# Work and commit
git add .
git commit -m "feat(dashboard): add user analytics view"

# Push and open PR
git push origin feature/new-dashboard
# Open PR on GitHub

# After merge
git checkout main
git pull origin main
git branch -d feature/new-dashboard
```

### Scenario 2: Hotfix

```bash
git checkout main
git pull origin main
git checkout -b hotfix/security-patch

# Fix and commit
git add .
git commit -m "fix(auth): patch JWT validation vulnerability"

# Push and merge urgently
git push origin hotfix/security-patch
# Create and merge PR immediately

# Cleanup
git checkout main
git pull origin main
git branch -d hotfix/security-patch
```

### Scenario 3: Sync Feature Branch

```bash
# Update main
git checkout main
git pull origin main

# Rebase feature on main
git checkout feature/my-feature
git rebase main

# Resolve conflicts if any, then:
git add .
git rebase --continue

# Force push (rewrites history)
git push --force-with-lease origin feature/my-feature
```

### Scenario 4: Undo Last Commit (Not Pushed)

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Edit files as needed

# Commit with better message
git commit -m "feat(api): improved description"
```

## Verification Before Completion

Before claiming Git work is done:

- [ ] All commits use Conventional Commits format
- [ ] No commits mention Claude/Anthropic
- [ ] Each commit is atomic (one logical change)
- [ ] Commit messages are verbose and clear
- [ ] Branch follows naming conventions
- [ ] PR has clear description and links issues
- [ ] No merge conflicts
- [ ] CI checks pass

## Anti-Patterns

**Avoid these**:

```bash
# ❌ Massive single commit
git add .
git commit -m "feat: add everything"

# ❌ Force push to main
git push --force origin main

# ❌ Ambiguous commit
git commit -m "updates"

# ❌ Mixed concerns in one commit
git commit -m "feat: add auth and fix database and update docs"

# ❌ No message
git commit --no-edit
```

## Helpful Commands

### Status and History

```bash
git status                    # Current state
git log --oneline            # Commit history
git log --merge              # Merge conflicts
git diff                     # Unstaged changes
git diff --staged            # Staged changes
```

### Undoing Changes

```bash
git checkout -- <file>       # Discard working changes
git reset HEAD <file>        # Unstage file
git reset --soft HEAD~1      # Undo commit, keep changes
git reset --hard HEAD~1      # Undo commit, discard changes
git reset --hard <commit>    # Reset to specific commit
```

### Branch Management

```bash
git branch -a                # List all branches
git branch -d feature/name   # Delete local branch
git push origin --delete feature/name  # Delete remote
git branch -m new-name       # Rename current branch
```

## Integration with CLAUDE.md

Enforces CLAUDE.md Section 7:
- **GH-1**: Conventional Commits format
- **GH-2**: No Claude/Anthropic mentions
- **GH-3**: Atomic commits with clear intent
- **GH-4**: Verbose over ambiguous

## Compliance & Attribution

- MUST NOT: Add or include any phrase like "🤖 Generated with Claude Code", "Generated by Claude", "Created with Claude", or mention of Claude/Anthropic in any output, comment, doc, or artifact.
- Commit messages, diff logs, footers, and visible/documented outputs must never automatically or manually attribute work to Claude or Anthropic.
- All project outputs should appear as crafted by the team, following project and team branding only.
---

**Last Updated:** January 24, 2026
**Compatibility:** Claude Opus 4.5, Claude Code v2.x
**Status:** Production Ready

> **January 2026 Update:** This skill is compatible with Claude Opus 4.5 and Claude Code v2.x. For complex tasks, use the `effort: high` parameter for thorough analysis.
