---
name: git-convention
description: Git convention for branch naming, commit messages, and issue labels based on GitFlow and Conventional Commits. Use when creating branches, writing commit messages, or setting up issue labels.
---

# Git Convention

## Branch Naming

Format: `type/[branch/]description[-#issue]`

| Type | Description | Example |
|------|-------------|---------|
| feat | New feature | `feat/login-#123` |
| fix | Bug fix | `fix/button-click-#456` |
| docs | Documentation | `docs/api-docs-#789` |
| style | Code style (no logic change) | `style/css-format-#101` |
| refactor | Code restructure | `refactor/auth-service-#102` |
| test | Add/modify tests | `test/unit-tests-#103` |
| chore | Maintenance | `chore/dependency-update-#104` |

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Rules
- Max 100 characters per line
- Subject: imperative, present tense ("change" not "changed")
- Subject: no capitalize, no period at end
- Body: motivation and contrast with previous behavior

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **style**: Formatting, missing semicolons
- **refactor**: Code restructure without behavior change
- **test**: Adding or updating tests
- **chore**: Build, package manager, no code change

## Setup

### Commit Template
```bash
git config --local commit.template .github/.gitmessage
```

### Issue Labels
```bash
github-label-sync --access-token <token> --labels .github/labels.json <owner>/<repo>
```
