---
name: git-workflows
description: Execute git and GitHub operations through Grove Wrap (gw) with safety-tiered commands, Conventional Commits, and agent-safe defaults. Use when making commits, managing branches, working with PRs/issues, or performing any version control operations.
---

# Git & GitHub Workflows (via Grove Wrap)

**All git and GitHub operations go through `gw`** — never use raw `git` or `gh` commands directly.
Grove Wrap adds safety tiers, Conventional Commits enforcement, protected branch guards, and agent-safe defaults.

## When to Activate

Activate this skill when:

- Making git commits, pushing, pulling, branching, or stashing
- Creating, reviewing, or merging pull requests
- Creating, viewing, or closing GitHub issues
- Checking CI/workflow run status
- Reviewing git history, diffs, or blame
- Resolving merge conflicts
- Any version control operation

## Safety System

gw enforces a three-tier safety model:

| Tier          | Flag Required     | Examples                                                         |
| ------------- | ----------------- | ---------------------------------------------------------------- |
| **READ**      | None              | `gw git status`, `gw git log`, `gw gh pr list`                   |
| **WRITE**     | `--write`         | `gw git commit`, `gw git push`, `gw git pull`, `gw gh pr create` |
| **DANGEROUS** | `--write --force` | `gw git reset`, `gw git force-push`, `gw git rebase`             |

**Protected branches** (`main`, `master`, `production`, `staging`) can NEVER be force-pushed, even with `--force`.

**Agent mode** (auto-detected for Claude Code): stricter row limits, force operations blocked, all operations audit-logged.

**Dry run** any command with `--dry-run` to preview what would happen.

## Conventional Commits Format

gw validates commit messages against Conventional Commits automatically. Format:

```
<type>(<optional scope>): <brief description>

<optional body>

<optional footer>
```

### Commit Types

| Type       | Purpose          | Example                             |
| ---------- | ---------------- | ----------------------------------- |
| `feat`     | New feature      | `feat: add user authentication`     |
| `fix`      | Bug fix          | `fix: correct validation error`     |
| `docs`     | Documentation    | `docs: update README`               |
| `style`    | Code formatting  | `style: format with prettier`       |
| `refactor` | Code restructure | `refactor: extract helper function` |
| `test`     | Add/modify tests | `test: add auth tests`              |
| `chore`    | Maintenance      | `chore: update dependencies`        |
| `perf`     | Performance      | `perf: optimize query speed`        |
| `ci`       | CI/CD changes    | `ci: fix deploy workflow`           |

**Breaking changes**: Add an exclamation mark after the type, e.g. **feat!: replace XML config with YAML**

## Git Commands — Reading (Always Safe)

```bash
gw git status                  # Enhanced git status
gw git log                     # Formatted commit history
gw git log --limit 20          # Last 20 commits
gw git diff                    # Show changes
gw git diff --staged           # Show staged changes
gw git blame file.ts           # Blame with context
gw git show abc123             # Show commit details
```

## Git Commands — Writing (Needs `--write`)

```bash
gw git add --write .                              # Stage files
gw git add --write src/lib/thing.ts               # Stage specific file
gw git commit --write -m "feat: add new feature"  # Commit (validates conventional commits!)
gw git push --write                               # Push to remote
gw git pull --write                               # Pull from remote
gw git pull --write --rebase                      # Pull with rebase strategy
gw git branch --write feature/new-thing           # Create branch
gw git switch --write feature/new-thing           # Switch branches
gw git stash --write                              # Stash changes
gw git stash --write pop                          # Pop stash
gw git unstage --write file.ts                    # Unstage files
```

## Git Commands — Dangerous (Needs `--write --force`)

```bash
gw git push --write --force          # Force push (blocked to protected branches!)
gw git reset --write --force HEAD~1  # Hard reset
gw git rebase --write --force main   # Rebase onto main
gw git merge --write --force feature # Merge branches
```

## Grove Shortcuts

These combine common multi-step operations into single commands:

```bash
# Quick save: stage all + WIP commit
gw git save --write

# Quick sync: fetch + rebase + push
gw git sync --write

# WIP commit that skips hooks
gw git wip --write

# Undo last commit (keeps changes staged)
gw git undo --write

# Amend last commit message
gw git amend --write -m "better message"

# FAST MODE: skip ALL hooks, commit + push in one shot
gw git fast --write -m "fix: emergency hotfix"
```

## Branching Strategy

### Branch Naming

```
feature/feature-name    # New features
fix/bug-description     # Bug fixes
experiment/new-idea     # Experiments
release/v1.0.0          # Releases
```

### Feature Branch Workflow

```bash
# Create and switch to feature branch
gw git branch --write feature/user-auth
gw git switch --write feature/user-auth

# Work and commit
gw git add --write .
gw git commit --write -m "feat: add JWT authentication"

# Push and create PR
gw git push --write
gw gh pr create --write --title "feat: add JWT authentication"
```

## GitHub — Pull Requests

```bash
# Reading (always safe)
gw gh pr list                   # List open PRs
gw gh pr view 123               # View PR details
gw gh pr status                 # PR status (CI, reviews, etc.)

# Writing (needs --write)
gw gh pr create --write --title "feat: new thing" --body "Description"
gw gh pr comment --write 123 "LGTM!"
gw gh pr merge --write 123      # Merge PR (prompts for confirmation)
```

## GitHub — Issues

```bash
# Reading (always safe)
gw gh issue list                # List open issues
gw gh issue view 456            # View issue details

# Writing (needs --write)
gw gh issue create --write --title "Bug: thing broke"
gw gh issue close --write 456
```

## GitHub — Workflow Runs (CI)

```bash
# Reading (always safe)
gw gh run list                  # List recent runs
gw gh run view 12345678         # View run details
gw gh run watch 12345678        # Watch a running workflow

# Writing (needs --write)
gw gh run rerun --write 12345678 --failed  # Rerun failed jobs
gw gh run cancel --write 12345678          # Cancel a run
```

## GitHub — API & Rate Limits

```bash
# GET requests (always safe)
gw gh api repos/AutumnsGrove/GroveEngine

# POST/PATCH (needs --write)
gw gh api --write repos/{owner}/{repo}/labels -X POST -f name="bug"

# DELETE (needs --write --force)
gw gh api --write --force repos/{owner}/{repo}/labels/old -X DELETE

# Check rate limit status
gw gh rate-limit
```

## GitHub — Project Boards

```bash
gw gh project list              # List project boards
gw gh project view              # View current project
```

## Commit Examples

### Feature

```bash
gw git commit --write -m "feat: add dark mode toggle

- Implement theme switching logic
- Add localStorage persistence
- Update CSS variables"
```

### Bug Fix with Issue Link

```bash
gw git commit --write -m "fix: correct timezone handling bug

Fixes off-by-one error in date calculations.

Closes #123"
```

### Breaking Change

```bash
gw git commit --write -m "feat!: replace XML config with YAML

BREAKING CHANGE: XML configuration no longer supported.
See docs/migration.md for upgrade instructions."
```

## Agent-Optimized Commands (NEW)

These commands are specifically designed for agentic workflows:

### Session Start (Always run this first!)

```bash
gw context                      # One-shot session snapshot (rich output)
gw --json context               # JSON snapshot (branch, changes, packages, issues)
```

### Ship with Auto-Stage

```bash
# Stage all + format + check + commit + push in ONE command
gw git ship --write -a -m "feat: implement feature"

# Equivalent to: gw git add --write . && gw git ship --write -m "..."
```

### PR Preparation

```bash
gw git pr-prep                  # Full PR readiness report
gw --json git pr-prep           # JSON: commits, files, packages, suggested title
```

### Targeted CI

```bash
gw ci --affected               # Only check packages with changes
gw ci --affected --fail-fast   # Fast feedback: stop on first failure
gw ci --diagnose               # Structured error output when steps fail
gw --json ci --affected        # JSON with parsed error details
```

### Batch Issue Creation

```bash
# Create multiple issues from JSON
gw gh issue batch --write --from-json issues.json
echo '[{"title":"Bug: thing","labels":["bug"]}]' | gw gh issue batch --write --from-json -
```

### Impact Analysis (via gf)

```bash
gf impact src/lib/auth.ts       # Who imports this? What tests? Which routes?
gf test-for src/lib/auth.ts     # Find tests covering this file
gf diff-summary                 # Structured diff with per-file stats
gf --json impact src/lib/auth.ts  # All of the above as parseable JSON
```

## Common Workflows

### Start a new feature

```bash
gw context                      # Orient: what branch, what's changed?
gw git branch --write feature/my-feature
gw git switch --write feature/my-feature
# ... make changes ...
gw git ship --write -a -m "feat: implement my feature"
gw git pr-prep                  # Check readiness
gw gh pr create --write --title "feat: implement my feature"
```

### Quick fix and ship

```bash
gw git fast --write -m "fix: correct typo in header"
```

### Ship with full checks

```bash
gw git ship --write -a -m "feat: add auth refresh"
# This does: auto-stage all → format → type-check → commit → push
```

### Check CI before merging

```bash
gw ci --affected --fail-fast    # Quick: only changed packages
gw gh pr status                 # See CI status on current PR
gw gh run list                  # See recent workflow runs
gw gh run watch 12345678        # Watch the current run
```

### Pull latest changes

```bash
gw git pull --write             # Pull from remote (merge strategy)
gw git pull --write --rebase    # Pull with rebase (cleaner history)
gw git pull --write origin main # Pull specific remote/branch
```

### Sync branch with main

```bash
gw git sync --write             # Fetch + rebase + push
```

### Save work in progress

```bash
gw git save --write             # Stage all + WIP commit
# or
gw git stash --write            # Stash without committing
```

## Merge Conflicts

When conflicts occur during sync/rebase/merge:

```bash
gw git status                   # See conflicted files

# Edit files to resolve conflicts:
# <<<<<<< HEAD
# Your changes
# =======
# Incoming changes
# >>>>>>> feature-branch

# After resolving:
gw git add --write resolved-file.ts
gw git commit --write -m "fix: resolve merge conflicts"
```

## Worktrees

Work on multiple branches simultaneously without stashing:

```bash
gw git worktree add --write ../grove-hotfix fix/urgent
gw git worktree list
gw git worktree remove --write ../grove-hotfix
```

## Best Practices

### DO

- Start every session with `gw context` (or `gw --json context` for structured data)
- Use `gw` for all git/GitHub operations (never raw `git` or `gh`)
- Use `gf` for all codebase search (never raw `grep` or `rg`)
- Use Conventional Commits format (gw enforces this)
- Use `gw git ship --write -a -m "..."` for the fastest commit+push workflow
- Use `gw ci --affected` instead of full CI when possible
- Use `gw git pr-prep` before creating PRs
- Use `gf impact` before making changes to understand blast radius
- One logical change per commit
- Keep subject under 50 characters
- Use imperative mood ("Add" not "Added")
- Use `--dry-run` to preview destructive operations

### DON'T

- Use raw `git` or `gh` commands directly
- Force-push to protected branches
- Use vague messages ("Update files", "Fix stuff")
- Combine multiple unrelated changes in one commit
- Skip the `--write` flag (even if it seems tedious — it's a safety net)

## Troubleshooting

### "Protected branch"

You tried to force-push to `main`. Create a PR instead:

```bash
gw gh pr create --write --title "My changes"
```

### "Rate limit exhausted"

```bash
gw gh rate-limit               # Check when it resets
```

### Committed to wrong branch

```bash
gw git log --limit 1            # Note the commit hash
gw git switch --write correct-branch
# Cherry-pick the commit, then remove from wrong branch
```

### Need to undo last commit

```bash
gw git undo --write             # Keeps changes staged
```

## Related Resources

- **gw README**: `tools/gw/README.md` — Full command reference
- **gw spec**: `docs/specs/gw-cli-spec.md` — Technical specification
- **Git guide**: `AgentUsage/git_guide.md` — Extended documentation
- **MCP integration**: `gw mcp serve` exposes all commands as MCP tools for Claude Code
