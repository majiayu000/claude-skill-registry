---
name: git
description: Git workflow management including branch validation, commit conventions, PR preparation, and repository health checks. Auto-activates on keywords git, branch, commit, pull request, PR, merge, rebase, workflow, conventional commits, branch strategy.
allowed-tools: Bash(git:*), Read, Grep, mcp__zen-core__pr_prepare
---

# Git Workflow Management Skill

Comprehensive git workflow assistance including branch validation, commit conventions, PR preparation, and repository health checks.

## When This Skill Activates

This skill automatically activates when user mentions:
- "git" or "git workflow"
- "branch" or "branch validation" or "branch naming"
- "commit" or "commit message" or "conventional commits"
- "pull request" or "PR" or "create PR"
- "merge" or "rebase"
- "git status" or "repository status"
- "workflow" or "git workflow helpers"
- "milestone" or "start feature" or "start work"
- "worktree" or "parallel work" or "parallel development"
- "semantic release" or "version bump"

## What This Skill Does

Provides comprehensive git workflow management:

- **Milestone Management**: Auto-detect branch vs worktree, semantic release alignment, parallel work
- **Branch Management**: Validate branch names, create feature branches, manage strategy
- **Worktree Orchestration**: Create, manage, and cleanup worktrees for parallel development
- **Commit Conventions**: Validate conventional commits, ensure signing, check formatting
- **PR Preparation**: Automated PR creation with GitHub integration and What the Diff
- **Repository Health**: Status checks, conflict detection, PR readiness validation
- **Workflow Automation**: Pre-commit checks, secrets detection, file size validation

## User Intent Detection and Routing

### Branch Validation
**Triggers**: "validate branch", "check branch name", "branch naming conventions"

**Route to**: [/git/branch](workflows/branch.md) workflow

**Examples**:
- "validate my branch name"
- "check if branch follows conventions"
- "create a feature branch"

### Commit Message Validation
**Triggers**: "validate commit", "check commit message", "conventional commits"

**Route to**: [/git/commit](workflows/commit.md) workflow

**Examples**:
- "validate my last commit message"
- "check commit conventions"
- "does my commit follow standards?"

### PR Readiness Check
**Triggers**: "check PR", "ready for PR", "PR readiness", "can I create a PR"

**Route to**: [/git/pr-check](workflows/pr-check.md) workflow

**Examples**:
- "is my branch ready for a pull request?"
- "check if I can create a PR"
- "validate PR readiness"

### PR Preparation (Automated)
**Triggers**: "create PR", "prepare PR", "make pull request", "generate PR description"

**Route to**: [/git/pr-prepare](workflows/pr-prepare.md) workflow (MCP integration)

**Examples**:
- "create a pull request"
- "prepare PR with What the Diff"
- "generate PR description for my changes"

### Repository Status
**Triggers**: "git status", "repo status", "check repository", "what changed"

**Route to**: [/git/status](workflows/status.md) workflow

**Examples**:
- "show me git status"
- "what files have changed?"
- "summarize repository status"

### Milestone Branch Management (RECOMMENDED)
**Triggers**: "start feature", "start work", "new milestone", "begin implementation", "start fix"

**Route to**: [/git/milestone](workflows/milestone.md) workflow

**Examples**:
- "start working on user authentication feature"
- "begin implementing the dashboard"
- "I need to fix a bug while working on this feature"
- "start a new milestone for API refactoring"

**Key Feature**: Auto-detects when to use worktree vs simple branch based on:
- Current uncommitted changes
- Whether already on a feature branch
- Type of work (hotfix requires isolation)

### Worktree Management
**Triggers**: "worktree", "parallel work", "parallel branch", "need isolation"

**Route to**: [/git/milestone](workflows/milestone.md) workflow (worktree subcommand)

**Examples**:
- "create worktree for parallel development"
- "I need to review a PR while keeping my changes"
- "set up isolated workspace for hotfix"
- "list my active worktrees"

### General Git Questions
**Triggers**: "git workflow", "git best practices", "branch strategy", "commit standards"

**Action**: Load relevant context files and explain concepts

**Examples**:
- "explain git workflow best practices"
- "what are the branch naming conventions?"
- "how should I format commit messages?"

## Quick Command Reference

```bash
# === MILESTONE MANAGEMENT (RECOMMENDED) ===

# Start new feature (auto-detects branch vs worktree)
/git/milestone start feat/user-dashboard

# Start bug fix
/git/milestone start fix/api-timeout

# Force worktree for parallel work
/git/milestone worktree feat/parallel-feature

# Complete milestone (validates, suggests PR)
/git/milestone complete

# List active branches and worktrees
/git/milestone list

# === BRANCH MANAGEMENT ===

# Validate branch name
/git/branch validate

# Create feature branch
/git/branch create feature/123-add-auth

# === COMMIT VALIDATION ===

# Validate last commit
/git/commit validate

# === PR WORKFLOW ===

# Check PR readiness
/git/pr-check

# Create PR with What the Diff (RECOMMENDED)
/git/pr-prepare --include_wtd=true --target_branch=main

# Force WTD for large PRs
/git/pr-prepare --include_wtd=true --force_wtd=true

# === STATUS ===

# Repository status summary
/git/status
```

## Git Workflow Standards

### Branch Naming Conventions

Follow this pattern: `<type>/<issue-number>-<short-description>`

**Valid types**:
- `feature/` - New features
- `fix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `chore/` - Maintenance tasks

**Examples**:
- `feature/123-user-authentication`
- `fix/456-memory-leak`
- `hotfix/789-security-patch`
- `chore/101-update-dependencies`

### Conventional Commit Format

Follow Conventional Commits specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Valid types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`

**Examples**:
```bash
feat(auth): add user login functionality
fix(api): resolve timeout issue in payment endpoint
docs(readme): update installation instructions
chore(deps): upgrade dependencies to latest versions
```

### PR Preparation Workflow (AUTOMATED)

**ALWAYS use `mcp__zen-core__pr_prepare` for PR creation**:

1. **Branch Safety Validation**: Ensures proper branch strategy
2. **Dependency Updates**: Regenerates requirements files automatically
3. **Security Scanning**: Checks for dependency vulnerabilities
4. **What the Diff Integration**: Includes AI-generated summary
5. **GitHub Integration**: Creates draft PR with comprehensive description

**Default behavior**:
- Includes What the Diff shortcode (`<!-- wtd:summary -->`)
- Validates branch targeting and naming
- Updates dependency files if needed
- Runs security checks
- Generates comprehensive PR description

**What the Diff Integration**:
- **Shortcode**: `<!-- wtd:summary -->` (HTML comment format)
- **Placement**: Inserted where AI summary is desired
- **Additional options**: `<!-- wtd:joke -->`, `<!-- wtd:poem -->`
- **Disable**: Use `--include_wtd=false` (rare)

### Signing Configuration

All commits MUST be signed:

```bash
# Configure signing key
git config --get user.signingkey  # Must be configured

# Check SSH signing
ssh-add -l  # Must show SSH key

# Check GPG signing
gpg --list-secret-keys  # Must show GPG key
```

## Integration with Other Skills

### Pre-Commit Validation
Works with [quality skill](../quality/SKILL.md):
```bash
/quality/precommit  # Runs before commit
/git/commit validate  # Validates after commit
```

### Security Validation
Complements [security skill](../security/SKILL.md):
```bash
/security/validate-env  # Check signing keys
/git/pr-prepare  # Includes security scan
```

### Assumption Verification
Integrates with [RAD skill](../rad/SKILL.md):
```bash
/rad/verify --scope=changed-files  # Before PR
/git/pr-prepare  # After verification
```

## Common Workflows

### Starting a New Milestone (RECOMMENDED)

```bash
# 1. Start milestone with automatic branch/worktree detection
/git/milestone start feat/user-dashboard

# 2. Work through your TODO items with proper commits
git add .
git commit -m "feat(dashboard): add initial component"
git commit -m "feat(dashboard): implement data fetching"
git commit -m "test(dashboard): add unit tests"

# 3. Complete milestone validation
/git/milestone complete

# 4. Create PR
/git/pr-prepare --include_wtd=true
```

### Parallel Feature Development

```bash
# 1. Start first feature
/git/milestone start feat/feature-a

# 2. Need to work on something else? Start parallel worktree
/git/milestone worktree fix/urgent-bug

# 3. Switch between worktrees as needed
cd ../project-worktrees/fix-urgent-bug
# ... work on fix ...
/git/milestone complete

# 4. Return to original feature
cd ../project
# ... continue feature work ...
/git/milestone complete

# 5. Clean up
git worktree list
git worktree remove ../project-worktrees/fix-urgent-bug
```

### Creating a Feature Branch (Manual)
```bash
# 1. Create and checkout feature branch
git checkout -b feature/123-add-feature

# 2. Validate branch name
/git/branch validate

# 3. Make changes and commit
git add .
git commit -m "feat(module): add new feature"

# 4. Validate commit
/git/commit validate
```

### Preparing a Pull Request
```bash
# 1. Check PR readiness
/git/pr-check

# 2. Verify assumptions (if using RAD)
/rad/verify --scope=changed-files

# 3. Run pre-commit validation
/quality/precommit

# 4. Create PR with What the Diff
/git/pr-prepare --include_wtd=true --target_branch=main

# 5. Review generated PR description and push
```

### Fixing Commit Issues
```bash
# 1. Check last commit
/git/commit validate

# 2. If invalid, amend commit message
git commit --amend -m "feat(auth): add user login"

# 3. Re-validate
/git/commit validate
```

### Updating Feature Branch
```bash
# 1. Fetch latest changes
git fetch origin

# 2. Rebase on main
git rebase origin/main

# 3. Resolve conflicts if any
# 4. Force push (if already pushed)
git push --force-with-lease
```

## Workflow Best Practices

### Branch Management
- Keep branches focused on single features/fixes
- Use descriptive branch names with issue numbers
- Delete branches after merging
- Never work directly on main/master

### Commit Practices
- Write clear, conventional commit messages
- Keep commits atomic (one logical change per commit)
- Sign all commits for security
- Never commit secrets or sensitive data

### PR Guidelines
- Keep PRs under 400 lines when possible
- Include comprehensive description
- Link to related issues
- Use What the Diff for AI-generated summaries
- Request appropriate reviewers

### Repository Hygiene
- Run pre-commit hooks before every commit
- Keep dependencies up to date
- Address security vulnerabilities promptly
- Maintain clean commit history with rebase

## MCP Integration

### PR Prepare Tool

The `mcp__zen-core__pr_prepare` tool provides comprehensive PR preparation:

**Features**:
- Branch strategy validation and migration assistance
- Automatic dependency file updates (requirements.txt, poetry.lock)
- Security vulnerability scanning
- What the Diff shortcode integration
- GitHub PR creation with rich descriptions
- Size analysis and splitting suggestions

**Usage**:
```bash
# Standard PR with WTD
mcp__zen-core__pr_prepare --include_wtd=true

# Custom parameters
mcp__zen-core__pr_prepare \
  --include_wtd=true \
  --target_branch=develop \
  --change_type=feat \
  --title="Add new authentication system"

# Force WTD for large PRs
mcp__zen-core__pr_prepare --force_wtd=true
```

## Resources

- **Milestone Management**: See [workflows/milestone.md](workflows/milestone.md) (RECOMMENDED)
- **Branch Strategies**: See [context/branch-strategies.md](context/branch-strategies.md)
- **Commit Standards**: See [context/conventional-commits.md](context/conventional-commits.md)
- **PR Preparation**: See [workflows/pr-prepare.md](workflows/pr-prepare.md)
- **Global Standards**: See `CLAUDE.md > Automated Branch Creation Strategy`
- **Worktree Reference**: See `~/.claude/standards/git-worktree.md`

---

*Consolidated from workflow-git-helpers command and MCP pr_prepare integration.*
