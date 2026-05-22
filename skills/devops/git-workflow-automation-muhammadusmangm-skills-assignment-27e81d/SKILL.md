---
name: git-workflow-automation
description: Comprehensive Git workflow automation including branching strategies, pull request creation, code reviews, merge strategies, and release management. Use when Claude needs to help with Git operations, branching models (Git Flow, GitHub Flow), pull request creation, code reviews, merge conflicts, or release processes.
---

# Git Workflow Automation

## Overview
This skill automates common Git workflows and provides expert guidance on best practices for version control.

## When to Use This Skill
- Creating feature branches with proper naming conventions
- Managing merge conflicts and resolution strategies
- Following Git Flow or GitHub Flow methodologies
- Creating and reviewing pull requests
- Performing release and hotfix operations
- Automating repetitive Git tasks

## Branching Strategies

### Git Flow
```
main (production-ready code)
├── develop (integration branch)
│   ├── feature/* (feature branches)
│   └── release/* (release preparation)
└── hotfix/* (urgent fixes)
```

### GitHub Flow
```
main (always deployable)
└── feature/* (short-lived branches)
```

## Common Operations

### Creating a Feature Branch
```bash
git checkout -b feature/user-authentication
```

### Syncing with Upstream
```bash
git checkout main
git pull origin main
git checkout feature/user-authentication
git rebase main
```

### Resolving Merge Conflicts
1. Identify conflicted files: `git status`
2. Open files and look for conflict markers: `<<<<<<<`, `=======`, `>>>>>>>`
3. Manually resolve conflicts by keeping desired changes
4. Stage resolved files: `git add .`
5. Complete the merge: `git rebase --continue` or `git merge --continue`

## Pull Request Best Practices
- Write clear, descriptive titles and descriptions
- Link to related issues
- Include testing instructions
- Specify reviewers
- Follow conventional commit messages

## Release Management
- Tag releases with semantic versioning (v1.2.3)
- Create release notes highlighting changes
- Verify CI/CD pipelines pass before merging
- Coordinate with stakeholders for deployment timing

## Scripts Available
- `scripts/create-feature-branch.sh` - Automated feature branch creation
- `scripts/sync-with-main.sh` - Sync current branch with main
- `scripts/prepare-release.sh` - Prepare a new release branch

## References
- `references/naming-conventions.md` - Git branch naming conventions and best practices
- `references/workflow-patterns.md` - Detailed workflow patterns and commands for different Git strategies