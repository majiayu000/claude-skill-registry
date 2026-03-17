---
name: codex-git
description: Git-aware development workflows with Codex CLI including intelligent commits, PR automation, branch management, and diff application. Use for git operations, PR reviews, or automated git workflows.
---

# Codex Git Integration

Comprehensive git-aware development workflows with Codex CLI, featuring intelligent commit generation and full automation.

**Last Updated**: December 2025 (GPT-5.2 Release)

## Quick Start

```bash
# Apply Codex changes as git patch
codex apply
# or
codex a

# Generate intelligent commits
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Review all changes and create meaningful git commits"

# Automated PR workflow
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Create feature branch, implement auth, commit, and create PR"
```

## Apply Codex Changes

Codex generates diffs that can be applied as git patches:

```bash
# After Codex makes changes in a session
codex apply

# Short form
codex a

# Review what will be applied
git diff  # Shows Codex's proposed changes

# Apply selectively
git add -p  # Stage only desired changes

# Revert if needed
git checkout .
```

## Intelligent Commit Generation

Codex analyzes changes and generates meaningful commits:

```bash
# Analyze changes and create commits
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Review all uncommitted changes and create semantic commits:
  1. Group related changes
  2. Write clear commit messages
  3. Follow conventional commits format
  4. Create separate commits for different concerns"

# With specific commit style
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Create commits using Angular commit convention"

# Quick commit for simple changes
codex exec --full-auto "Commit current changes with appropriate message"
```

## Git-Aware Development

Codex respects and understands git context:

```bash
# Codex automatically:
# - Respects .gitignore
# - Understands git history
# - Avoids modifying committed files unnecessarily
# - Creates clean, atomic commits
# - Understands branch context

# Work on feature branch
git checkout -b feature/new-auth
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Implement OAuth2 with clean git commits throughout"

# Codex will create logical commit points during implementation
```

## PR Automation

Complete pull request workflows:

```bash
# Create PR from current work
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Create PR for current feature:
  1. Review all commits
  2. Generate PR title and description
  3. List all changes
  4. Create PR via gh CLI"

# Automated feature branch + PR
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Complete PR workflow:
  1. Create feature branch feature/user-profiles
  2. Implement user profile system
  3. Write tests
  4. Create commits for each logical change
  5. Push branch
  6. Create PR with detailed description"
```

## Branch Management

```bash
# Create and work on branch
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Create branch 'refactor/auth' and refactor authentication module"

# Merge branches intelligently
codex exec --full-auto \
  "Merge feature/new-api into main, resolving conflicts"

# Clean up branches
codex exec --dangerously-bypass-approvals-and-sandbox \
  "List merged branches and delete them"
```

## Git History Analysis

```bash
# Analyze commit history
codex exec --json \
  "Analyze last 20 commits and identify:
  1. Common change patterns
  2. Areas of high activity
  3. Potential refactoring targets" \
  > git-analysis.json

# Find related changes
codex exec \
  "Find all commits related to authentication in last 6 months"

# Identify breaking changes
codex exec --search \
  "Review commits and identify potential breaking changes for changelog"
```

## Automated Git Workflows

### Complete Feature Development

```bash
#!/bin/bash
# Fully automated feature development with git workflow

develop_feature() {
  local feature_name="$1"
  local description="$2"

  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Complete feature development workflow:

    1. Create feature branch: feature/$feature_name
    2. Implement: $description
    3. Write comprehensive tests
    4. Create semantic commits for:
       - Initial implementation
       - Test addition
       - Documentation updates
    5. Run all tests
    6. Fix any failures
    7. Push branch
    8. Create PR with detailed description
    9. Provide summary of all changes"
}

# Usage
develop_feature "user-notifications" "Real-time notification system with WebSocket"
```

### Automated Code Review Response

```bash
#!/bin/bash
# Respond to PR feedback automatically

respond_to_pr_feedback() {
  local pr_number="$1"

  # Get PR comments
  gh pr view "$pr_number" --json comments > pr-comments.json

  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Review PR comments in @pr-comments.json and:
    1. Address all feedback
    2. Make requested changes
    3. Create commits for each feedback item
    4. Run tests
    5. Push updates
    6. Reply to comments explaining changes"
}

# Usage
respond_to_pr_feedback 123
```

### Automated Hotfix Workflow

```bash
#!/bin/bash
# Complete hotfix workflow with git safety

create_hotfix() {
  local issue="$1"
  local description="$2"

  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Hotfix workflow:

    1. Create hotfix branch from main
    2. Fix: $description (issue #$issue)
    3. Write targeted test for the fix
    4. Run all tests
    5. Create commit: 'fix: $description (closes #$issue)'
    6. Push branch
    7. Create PR with:
       - Clear description of bug
       - Explanation of fix
       - Test results
    8. Tag for review"
}

# Usage
create_hotfix 456 "Fix race condition in user session handling"
```

## Commit Message Generation

Codex generates high-quality commit messages:

```bash
# Conventional commits
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Create commits using conventional commits:
  feat: new features
  fix: bug fixes
  docs: documentation
  refactor: code refactoring
  test: test additions
  chore: maintenance"

# Detailed commit messages
codex exec --full-auto \
  "Create commits with:
  - Clear subject line (50 chars)
  - Blank line
  - Detailed body explaining WHY (not what)
  - References to issues"

# Example output:
# feat: add real-time notifications
#
# Implements WebSocket-based notification system to provide
# users with instant updates on important events.
#
# - Connects to notification service on login
# - Handles reconnection automatically
# - Queues notifications when offline
#
# Closes #123
```

## Git Safety Patterns

### Backup Before Automation

```bash
#!/bin/bash
# Safe automation with git backups

safe_codex_automation() {
  local task="$1"

  # Create git stash backup
  git stash push -m "pre-codex-$(date +%s)"

  if codex exec --dangerously-bypass-approvals-and-sandbox "$task"; then
    echo "✓ Success! Backup available: git stash list"
    git stash drop  # Optional: remove backup if confident
  else
    echo "✗ Failed! Restoring backup..."
    git stash pop
    return 1
  fi
}

# Usage
safe_codex_automation "Refactor entire authentication module"
```

### Dry-Run Mode

```bash
# Generate changes without applying
codex exec \
  "Implement user caching system and show me the complete diff" \
  > proposed-changes.diff

# Review proposed changes
git apply --check proposed-changes.diff

# Apply manually
git apply proposed-changes.diff
```

### Checkpoint Commits

```bash
#!/bin/bash
# Create checkpoints during long refactoring

checkpoint_refactoring() {
  local scope="$1"

  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Refactor $scope with checkpoint commits:
    1. Create WIP commit before starting
    2. Make incremental changes
    3. Create checkpoint commit every logical step
    4. Run tests after each checkpoint
    5. If tests fail, revert last checkpoint
    6. Continue until complete
    7. Squash WIP commits into clean history"
}

# Usage
checkpoint_refactoring "./src/auth"
```

## Git History Cleanup

```bash
# Interactive rebase automation
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Clean up last 5 commits:
  1. Squash WIP commits
  2. Rewrite unclear messages
  3. Reorder for logical flow
  4. Preserve semantic meaning"

# Amend last commit
codex exec --full-auto \
  "Amend last commit to include forgotten test file"

# Fixup commits
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Create fixup commits for TODO items in last 3 commits"
```

## Conflict Resolution

```bash
# Automated merge conflict resolution
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Resolve merge conflicts in current branch:
  1. Analyze conflicts
  2. Understand intent of both changes
  3. Resolve preserving functionality from both
  4. Run tests
  5. Create merge commit"

# Complex merges
codex exec --search --dangerously-bypass-approvals-and-sandbox \
  "Research best practices for this conflict type and resolve intelligently"
```

## Git Hooks Integration

```bash
# Generate pre-commit hook
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Create pre-commit hook that:
  1. Runs linter
  2. Runs type checking
  3. Runs quick tests
  4. Prevents commit if failures"

# Generate commit-msg hook
codex exec --full-auto \
  "Create commit-msg hook enforcing conventional commits format"
```

## Changelog Generation

```bash
# Automated changelog from commits
codex exec --dangerously-bypass-approvals-and-sandbox \
  --json \
  "Generate CHANGELOG.md from git history:
  1. Group by version/tag
  2. Categorize: Features, Fixes, Breaking Changes
  3. Link to commits and PRs
  4. Format as Keep a Changelog" \
  > CHANGELOG.md

# Release notes
codex exec --search --full-auto \
  "Generate release notes for v2.0.0 from commits since v1.9.0"
```

## Advanced Git Workflows

### Automated Release Process

```bash
#!/bin/bash
# Complete release automation

automate_release() {
  local version="$1"

  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Complete release workflow for v$version:

    1. Update version in package.json
    2. Generate CHANGELOG.md
    3. Run full test suite
    4. Create commit: 'chore: release v$version'
    5. Create git tag v$version
    6. Generate release notes
    7. Push commits and tags
    8. Create GitHub release with notes"
}

# Usage
automate_release "2.1.0"
```

### Git Bisect Automation

```bash
# Automated bug hunting with git bisect
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Use git bisect to find commit that introduced test failure in auth.test.js:
  1. Start bisect between v1.0.0 and HEAD
  2. Run test at each commit
  3. Mark good/bad automatically
  4. Identify breaking commit
  5. Analyze changes in that commit
  6. Suggest fix"
```

### Submodule Management

```bash
# Automated submodule updates
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Update all git submodules:
  1. Update to latest remote
  2. Run tests
  3. If pass, commit updates
  4. If fail, report issues"
```

## CI/CD Integration

### GitHub Actions with Codex

```yaml
# .github/workflows/codex-git-automation.yml
name: Codex Git Automation
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  codex-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for git analysis

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install Codex CLI
        run: npm install -g @openai/codex

      - name: Codex PR Analysis
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex exec --dangerously-bypass-approvals-and-sandbox \
            --json \
            "Analyze this PR:
            1. Review commit history
            2. Check commit message quality
            3. Analyze code changes
            4. Check for breaking changes
            5. Verify test coverage
            6. Generate review comments" \
            > pr-analysis.json

      - name: Post PR Comment
        uses: actions/github-script@v6
        with:
          script: |
            const analysis = require('./pr-analysis.json');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: analysis.summary
            });
```

### Automated Commit Cleanup

```yaml
# .github/workflows/commit-cleanup.yml
name: Commit Message Cleanup
on:
  pull_request:
    types: [opened]

jobs:
  check-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Codex CLI
        run: npm install -g @openai/codex

      - name: Validate Commit Messages
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex exec --dangerously-bypass-approvals-and-sandbox \
            "Check all commits in PR:
            1. Verify conventional commits format
            2. Check message clarity
            3. Suggest improvements
            4. Fail if critical issues found"
```

## Best Practices

### Git Workflow with Codex

1. **Always Use Feature Branches**
   ```bash
   codex exec --dangerously-bypass-approvals-and-sandbox \
     -C ./feature-branch \
     "Work only on feature branches, never main"
   ```

2. **Atomic Commits**
   ```bash
   codex exec --full-auto \
     "Create atomic commits - one logical change per commit"
   ```

3. **Test Before Commit**
   ```bash
   codex exec --dangerously-bypass-approvals-and-sandbox \
     "Always run tests before committing changes"
   ```

4. **Review Diffs**
   ```bash
   # Always review what Codex changed
   git diff
   codex apply  # Only after review
   ```

### Safety with Automation

```bash
# 1. Use git stash for safety
git stash push -m "backup"
codex exec --dangerously-bypass-approvals-and-sandbox "task"

# 2. Work on branches
git checkout -b experiment
codex exec --dangerously-bypass-approvals-and-sandbox "try new approach"

# 3. Use codex apply for control
codex apply  # Review changes before applying

# 4. Checkpoint frequently
codex exec --full-auto "Create checkpoint commits during long tasks"
```

## Configuration

### Git-Specific Codex Config

```toml
# ~/.codex/config.toml (December 2025)

# Default model for git operations
model = "gpt-5.1-codex-max"  # Best for agentic coding
# model = "gpt-5.2"          # For large repo analysis (400K context)

[git]
# Always respect .gitignore
respect_gitignore = true

# Create commits automatically
auto_commit = false  # Set true for full automation

# Commit message style
commit_style = "conventional"  # or "angular", "semantic"

# Git safety
require_clean_worktree = false
create_backup_stash = true

[profiles.git-auto]
model = "gpt-5.1-codex-max"
ask_for_approval = "never"
sandbox = "workspace-write"
auto_commit = true
commit_style = "conventional"

[profiles.git-large-repo]
model = "gpt-5.2"
compact = true  # Enable context compaction for large repos
ask_for_approval = "never"
sandbox = "workspace-write"
```

## Troubleshooting

### Common Git Issues

**Uncommitted Changes**
```bash
# Save work before Codex operations
git stash push -m "wip"
codex exec --dangerously-bypass-approvals-and-sandbox "task"
git stash pop
```

**Merge Conflicts**
```bash
# Let Codex resolve
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Resolve all merge conflicts intelligently"
```

**Bad Commits**
```bash
# Rewrite history
codex exec --full-auto \
  "Fix last 3 commits - improve messages and combine related changes"
```

**Lost Changes**
```bash
# Recover with git reflog
codex exec \
  "Use git reflog to find and recover lost commits from last 2 hours"
```

## Related Skills

- `codex-cli`: Main integration
- `codex-review`: Code review workflows
- `codex-tools`: Tool execution
- `codex-chat`: Interactive sessions
- `codex-auth`: Authentication

---

**Created for Claude Code** - Git-aware automation for seamless development workflows
