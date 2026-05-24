---
name: git-storytelling-branch-strategy
description: Use when planning git branching strategies or managing branches for development. Helps create clear development narratives through effective branch organization and workflow patterns.
allowed-tools:
  - Bash
  - Read
---

# Git Storytelling - Branch Strategy

This skill helps you implement effective branching strategies that tell the story of your development process through organized, purposeful branch management. Good branching creates a clear narrative of parallel development efforts.

## Core Concepts

### Why Branch Strategy Matters

A good branching strategy:

- **Creates clear development narratives** - Each branch tells a specific story
- **Enables parallel work** - Multiple features can develop simultaneously
- **Facilitates code review** - Changes are isolated and reviewable
- **Supports deployment workflows** - Different branches for different environments
- **Reduces merge conflicts** - Smaller, focused branches are easier to merge
- **Documents development history** - Branch names and structure show intent

### The Story of Branches

Think of branches as parallel storylines in your codebase:

- **Main branch**: The canonical story, always working and deployable
- **Feature branches**: Side quests that eventually merge into the main story
- **Release branches**: Chapters being prepared for publication
- **Hotfix branches**: Emergency patches to the published story
- **Development branch**: The staging area where stories come together

## Branch Naming Conventions

### Standard Prefixes

Use consistent prefixes to categorize branches:

```
feature/    - New features
fix/        - Bug fixes
hotfix/     - Production emergency fixes
refactor/   - Code refactoring
test/       - Testing changes
docs/       - Documentation
chore/      - Maintenance tasks
release/    - Release preparation
```

### Naming Best Practices

Good branch names are:

```bash
# GOOD: Clear, descriptive, kebab-case
feature/user-authentication
fix/payment-processing-timeout
refactor/extract-validation-logic
hotfix/critical-security-patch

# BAD: Vague, unclear, inconsistent
feature/new-stuff
fix-thing
my-branch
temp
```

### Including Issue Numbers

Reference tracking system issues:

```bash
feature/123-add-user-authentication
fix/456-resolve-memory-leak
hotfix/789-patch-security-vulnerability
```

### Branch Name Format

Follow a consistent pattern:

```
<type>/<issue-number>-<short-description>

Examples:
feature/234-oauth-integration
fix/567-null-pointer-exception
refactor/890-simplify-error-handling
```

## Common Branching Strategies

### Git Flow

A robust branching model for release-based software:

```bash
# Main branches (permanent)
main        # Production-ready code
develop     # Integration branch for features

# Supporting branches (temporary)
feature/*   # New features
release/*   # Release preparation
hotfix/*    # Production fixes
```

**Git Flow Workflow:**

```bash
# Start new feature
git checkout develop
git checkout -b feature/user-profile

# Work on feature with commits
git commit -m "feat: add user profile model"
git commit -m "feat: add profile update endpoint"

# Finish feature
git checkout develop
git merge --no-ff feature/user-profile
git branch -d feature/user-profile

# Start release
git checkout develop
git checkout -b release/v1.2.0

# Prepare release
git commit -m "chore: bump version to 1.2.0"
git commit -m "docs: update CHANGELOG"

# Finish release
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git checkout develop
git merge --no-ff release/v1.2.0
git branch -d release/v1.2.0

# Emergency hotfix
git checkout main
git checkout -b hotfix/v1.2.1

# Fix and release
git commit -m "fix: critical security issue"
git checkout main
git merge --no-ff hotfix/v1.2.1
git tag -a v1.2.1 -m "Hotfix version 1.2.1"
git checkout develop
git merge --no-ff hotfix/v1.2.1
git branch -d hotfix/v1.2.1
```

### GitHub Flow

A simpler model for continuous deployment:

```bash
# Only one main branch
main        # Always deployable

# All work in feature branches
feature/*   # Features, fixes, everything
```

**GitHub Flow Workflow:**

```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/add-search

# Make commits
git commit -m "feat: add search component"
git commit -m "test: add search tests"
git commit -m "docs: document search API"

# Push and create pull request
git push -u origin feature/add-search

# After review and CI passes, merge via PR
# Then deploy main branch

# Clean up
git checkout main
git pull origin main
git branch -d feature/add-search
```

### Trunk-Based Development

Minimal branching with short-lived feature branches:

```bash
# Main branch
main        # The trunk, always deployable

# Short-lived feature branches (< 1 day)
feature/*   # Small, quick features
```

**Trunk-Based Workflow:**

```bash
# Create short-lived feature branch
git checkout main
git pull origin main
git checkout -b feature/update-button-text

# Make focused change
git commit -m "feat: update CTA button text"

# Push and merge same day
git push -u origin feature/update-button-text

# Merge via PR or direct merge
git checkout main
git merge feature/update-button-text
git push origin main

# Delete branch immediately
git branch -d feature/update-button-text
```

### GitLab Flow

Environment branches for deployment stages:

```bash
# Main development branch
main              # Integration branch

# Environment branches
staging           # Staging environment
production        # Production environment

# Feature branches
feature/*         # Features merge to main
```

**GitLab Flow Workflow:**

```bash
# Develop feature
git checkout main
git checkout -b feature/notification-system
git commit -m "feat: add notification system"

# Merge to main
git checkout main
git merge feature/notification-system

# Deploy to staging
git checkout staging
git merge main
git push origin staging  # Triggers staging deployment

# After testing, deploy to production
git checkout production
git merge staging
git push origin production  # Triggers production deployment
```

## Code Examples

### Example 1: Starting a Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch with descriptive name
git checkout -b feature/456-implement-two-factor-auth

# Verify you're on new branch
git branch --show-current
# Output: feature/456-implement-two-factor-auth

# Make initial commit
git commit --allow-empty -m "feat: initialize two-factor authentication feature"

# Push branch to remote
git push -u origin feature/456-implement-two-factor-auth

# Continue development
git commit -m "feat: add TOTP token generation"
git commit -m "feat: add token verification endpoint"
git commit -m "test: add 2FA integration tests"
```

### Example 2: Keeping Feature Branch Updated

```bash
# While working on feature branch, main has moved forward
git checkout feature/789-user-dashboard

# Option 1: Rebase (creates linear history)
git fetch origin
git rebase origin/main

# If conflicts occur
git status  # See conflicting files
# Fix conflicts in editor
git add .
git rebase --continue

# Option 2: Merge (preserves branch history)
git fetch origin
git merge origin/main

# Resolve any merge conflicts
git add .
git commit -m "merge: resolve conflicts with main"

# Push updated branch
git push --force-with-lease origin feature/789-user-dashboard
```

### Example 3: Release Branch Workflow

```bash
# Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v2.0.0

# Prepare release
git commit -m "chore: bump version to 2.0.0"
git commit -m "docs: update CHANGELOG for v2.0.0"
git commit -m "chore: update dependencies"

# Fix bugs found during release testing
git commit -m "fix: resolve edge case in user validation"
git commit -m "fix: correct API response format"

# Merge to main and tag
git checkout main
git merge --no-ff release/v2.0.0
git tag -a v2.0.0 -m "Release version 2.0.0

Major changes:
- New user authentication system
- Improved performance
- Updated API endpoints

See CHANGELOG.md for details."

# Merge back to develop
git checkout develop
git merge --no-ff release/v2.0.0

# Push everything
git push origin main
git push origin develop
git push origin v2.0.0

# Clean up
git branch -d release/v2.0.0
```

### Example 4: Emergency Hotfix

```bash
# Production is broken, need immediate fix
git checkout main
git pull origin main

# Create hotfix branch
git checkout -b hotfix/critical-login-bug

# Make the fix
git commit -m "fix: resolve null pointer in login handler

Users unable to log in when email field contains trailing
whitespace. Add trim() to email input processing.

Critical production issue affecting 15% of login attempts.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Test the fix
npm test

# Merge to main
git checkout main
git merge --no-ff hotfix/critical-login-bug
git tag -a v1.5.1 -m "Hotfix: Login bug fix"

# Deploy immediately
git push origin main
git push origin v1.5.1

# Merge to develop so fix isn't lost
git checkout develop
git merge --no-ff hotfix/critical-login-bug
git push origin develop

# Clean up
git branch -d hotfix/critical-login-bug
git push origin --delete hotfix/critical-login-bug
```

### Example 5: Collaborative Feature Branch

```bash
# Developer A starts feature
git checkout -b feature/payment-integration
git commit -m "feat: add payment gateway client"
git push -u origin feature/payment-integration

# Developer B joins the work
git fetch origin
git checkout feature/payment-integration

# Developer B makes changes
git commit -m "feat: add webhook handler"
git pull --rebase origin feature/payment-integration
git push origin feature/payment-integration

# Developer A pulls updates
git checkout feature/payment-integration
git pull --rebase origin feature/payment-integration

# Continue collaborating until complete
git commit -m "test: add payment integration tests"
git commit -m "docs: document payment webhook API"

# Create pull request for review
git push origin feature/payment-integration
```

### Example 6: Experimental Branch

```bash
# Trying a risky approach
git checkout -b experiment/new-architecture

# Make experimental commits
git commit -m "experiment: try event-driven architecture"
git commit -m "experiment: add message queue integration"

# Test the approach
npm test
npm run benchmark

# Decision 1: Experiment failed, abandon it
git checkout main
git branch -D experiment/new-architecture

# Decision 2: Experiment succeeded, integrate it
git checkout -b feature/event-driven-refactor
git merge experiment/new-architecture
git commit -m "refactor: migrate to event-driven architecture"
git push -u origin feature/event-driven-refactor

# Clean up experiment branch
git branch -d experiment/new-architecture
```

### Example 7: Stacked Branches

```bash
# Large feature requires multiple PRs
git checkout main

# First part: Database schema
git checkout -b feature/schema-updates
git commit -m "feat: add new database tables"
git commit -m "feat: add migration scripts"
git push -u origin feature/schema-updates

# Second part: API (depends on schema)
git checkout -b feature/api-endpoints
git commit -m "feat: add user API endpoints"
git commit -m "test: add API integration tests"
git push -u origin feature/api-endpoints

# Third part: UI (depends on API)
git checkout -b feature/user-interface
git commit -m "feat: add user management UI"
git commit -m "test: add UI component tests"
git push -u origin feature/user-interface

# Merge order: schema -> API -> UI
# As each PR is approved and merged, rebase next branch onto main
```

### Example 8: Branch Cleanup

```bash
# List all branches
git branch -a

# Delete local branches that are merged
git branch --merged main | grep -v "main" | xargs git branch -d

# Delete remote branch
git push origin --delete feature/old-feature

# Prune remote tracking branches
git fetch --prune

# Delete local branches that no longer exist on remote
git remote prune origin

# Interactive cleanup
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -D

# See stale branches
git for-each-ref --sort=-committerdate refs/heads/ \
  --format='%(committerdate:short) %(refname:short)'
```

## When to Use This Skill

Use this skill when:

- Starting a new project and establishing branching conventions
- Planning feature development across multiple developers
- Setting up CI/CD pipelines with branch-based deployments
- Coordinating release schedules and version management
- Managing hotfixes to production environments
- Onboarding new team members to git workflow
- Resolving complex merge situations
- Refactoring large portions of codebase
- Experimenting with architectural changes
- Maintaining multiple versions of software simultaneously

## Best Practices

1. **Keep branches short-lived** - Merge within days, not weeks, to reduce merge conflicts

2. **Use descriptive branch names** - Future you will thank present you

3. **Delete merged branches** - Keep repository clean and navigable

4. **One purpose per branch** - Don't mix features, fixes, and refactoring

5. **Update from main regularly** - Frequent rebasing/merging reduces conflict pain

6. **Protect main branch** - Require PR reviews, passing tests before merge

7. **Use branch prefixes consistently** - Enables automation and filtering

8. **Include issue numbers** - Creates traceability to requirements

9. **Push branches early** - Enables collaboration and provides backup

10. **Create PR early as draft** - Get early feedback on approach

11. **Review changes before creating PR** - Use `git diff main...HEAD`

12. **Write meaningful merge commits** - Explain what the branch accomplished

13. **Tag releases** - Mark important points in history

14. **Document branching strategy** - In README or CONTRIBUTING guide

15. **Automate branch cleanup** - Use tools to delete stale branches

## Common Pitfalls

1. **Long-lived branches** - Weeks-old branches become nightmare to merge

2. **Inconsistent naming** - Mix of conventions confuses everyone

3. **Working directly on main** - Bypasses review and CI checks

4. **Forgetting to pull before branching** - Start from stale base

5. **Creating branches from wrong base** - Feature from feature instead of main

6. **Not updating feature branches** - Drift from main causes conflicts

7. **Keeping too many local branches** - Clutters workspace

8. **Force pushing shared branches** - Destroys collaborator's work

9. **Mixing unrelated changes** - One branch does too many things

10. **Not cleaning up merged branches** - Repository becomes graveyard

11. **Creating nested branch hierarchies** - Overly complex dependencies

12. **Merging without testing** - Breaks main branch

13. **No branch protection rules** - Anyone can push to main

14. **Using generic branch names** - "fix" or "update" tells nothing

15. **Forgetting to push branches** - Work exists only locally

## Resources

### Git Commands for Branch Management

```bash
# Create and switch to new branch
git checkout -b <branch-name>
git switch -c <branch-name>  # Modern alternative

# Switch branches
git checkout <branch-name>
git switch <branch-name>     # Modern alternative

# List branches
git branch              # Local branches
git branch -r           # Remote branches
git branch -a           # All branches
git branch -vv          # Verbose with tracking info

# Delete branches
git branch -d <branch>          # Delete if merged
git branch -D <branch>          # Force delete
git push origin --delete <branch>  # Delete remote

# Rename branch
git branch -m <old> <new>       # Rename local
git push origin -u <new>        # Push renamed
git push origin --delete <old>  # Delete old remote

# Track remote branch
git branch -u origin/<branch>
git checkout --track origin/<branch>

# Compare branches
git diff main...feature-branch
git log main..feature-branch
git log --graph --oneline --all

# Merge strategies
git merge <branch>              # Regular merge
git merge --no-ff <branch>      # Force merge commit
git merge --squash <branch>     # Squash into one commit

# Rebase
git rebase main                 # Rebase onto main
git rebase -i main              # Interactive rebase
git rebase --continue           # Continue after conflicts
git rebase --abort              # Abandon rebase

# Cherry-pick
git cherry-pick <commit-hash>   # Apply specific commit
```

### Branch Protection Rules

Configure on GitHub/GitLab:

```yaml
Protected Branch: main
- Require pull request reviews: 2 reviewers
- Require status checks to pass: true
  - Tests
  - Linting
  - Build
- Require branches to be up to date: true
- Include administrators: true
- Restrict push: true
- Allow force pushes: false
- Allow deletions: false
```

### Git Aliases for Branch Management

Add to `.gitconfig`:

```bash
[alias]
    # Branch management
    br = branch
    co = checkout
    cob = checkout -b

    # Branch cleanup
    bclean = "!f() { git branch --merged ${1-main} | grep -v " ${1-main}$" | xargs git branch -d; }; f"

    # Branch status
    bstat = branch -vv

    # Recent branches
    recent = branch --sort=-committerdate --format='%(committerdate:short) %(refname:short)'

    # Current branch name
    current = branch --show-current

    # Push current branch
    pub = "!git push -u origin $(git current)"

    # Update branch from main
    update = "!git fetch origin && git rebase origin/main"
```

### Visualization Tools

```bash
# View branch structure
git log --graph --oneline --all --decorate

# Detailed branch graph
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --all

# See all branches with last commit
git branch -v

# Branch topology
git show-branch

# Visual git tools
gitk --all          # Built-in visualizer
git gui             # Built-in GUI
```

### Related Skills

- **git-storytelling-commit-strategy**: When to commit on branches
- **git-storytelling-commit-messages**: Writing clear commit messages
- **code-reviewer**: How branches facilitate code review

## Advanced Patterns

### Feature Flags for Trunk-Based Development

Instead of long-lived branches, use feature flags:

```javascript
// feature-flags.js
export const features = {
  newUserDashboard: process.env.ENABLE_NEW_DASHBOARD === 'true',
  betaPaymentFlow: process.env.ENABLE_BETA_PAYMENT === 'true',
};

// component.jsx
import { features } from './feature-flags';

function Dashboard() {
  if (features.newUserDashboard) {
    return <NewDashboard />;
  }
  return <LegacyDashboard />;
}
```

This allows merging incomplete features to main without exposing them:

```bash
# Commit partial feature to main
git checkout main
git commit -m "feat: add new dashboard (behind feature flag)"
git push origin main

# Feature is deployed but not active
# Enable when ready via environment variable
```

### Branch Strategy Documentation

Document in `CONTRIBUTING.md`:

```markdown
## Branching Strategy

We use GitHub Flow with the following conventions:

### Branch Types

- `feature/*` - New features
- `fix/*` - Bug fixes
- `hotfix/*` - Production emergency fixes
- `refactor/*` - Code improvements
- `docs/*` - Documentation

### Workflow

1. Create branch from `main`: `git checkout -b feature/123-description`
2. Make commits following our commit message guidelines
3. Keep branch updated: `git rebase origin/main`
4. Push and create PR: `git push -u origin feature/123-description`
5. After approval and CI passes, merge via PR
6. Delete branch after merge

### Branch Naming

Format: `<type>/<issue>-<description>`

Examples:
- `feature/456-user-authentication`
- `fix/789-memory-leak`
- `hotfix/101-critical-security-patch`

### Branch Lifecycle

- Create branches from up-to-date `main`
- Keep branches under 3 days old
- Delete immediately after merge
- Never force push to `main`
```

## Conclusion

Effective branch strategy is essential for telling a clear development story. By following consistent naming conventions, keeping branches focused and short-lived, and choosing the right branching model for your team's needs, you create a git history that is navigable, understandable, and valuable.

Remember: Branches are temporary workspaces for focused development. Use them to isolate changes, enable parallel work, and facilitate code review. Then merge them and clean them up. A clean branch structure is a sign of a healthy, well-managed codebase.
