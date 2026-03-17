---
name: git
description: Git workflow management including branch validation, commit conventions, PR preparation, and repository health checks.
---

# Git Workflow Skill

Git workflow management including branch validation, commit conventions, PR preparation, and repository health checks.

## Activation

Auto-activates on keywords: git, branch, commit, pull request, PR, merge, rebase, workflow, conventional commits, branch strategy

## Workflows

### Branch Management
- **branch.md**: Branch creation, validation, and naming conventions
- **status.md**: Repository status and health checks

### Commit Management
- **commit.md**: Conventional commit message preparation

### PR Workflow
- **pr-prepare.md**: Pull request description generation
- **pr-check.md**: PR validation and checklist

## Context Files

- **conventional-commits.md**: Commit message format standards
- **branch-strategies.md**: Branch naming and workflow patterns

## Commands

```bash
# Check branch status
git branch --show-current
git status

# Validate branch naming
# Branch format: {type}/{descriptive-slug}
# Types: feat, fix, docs, refactor, perf, test, chore, hotfix

# Create conventional commit
git commit -m "$(cat <<'EOF'
{type}({scope}): {description}

{body}

{footer}
EOF
)"
```

## Semantic Release Mapping

| Branch Prefix | Commit Type | Version Impact |
|---------------|-------------|----------------|
| feat/         | feat:       | Minor (0.X.0)  |
| fix/          | fix:        | Patch (0.0.X)  |
| docs/         | docs:       | No release     |
| refactor/     | refactor:   | No release     |
| perf/         | perf:       | Patch (0.0.X)  |
| test/         | test:       | No release     |
| chore/        | chore:      | No release     |
| hotfix/       | fix:        | Patch (0.0.X)  |
