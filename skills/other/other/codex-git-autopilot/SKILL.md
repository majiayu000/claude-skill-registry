---
name: codex-git-autopilot
description: Automated git commit with CI/CD gate, GPG signing, and conventional commits
version: 8.0.0
---

# Git Autopilot

Automates the commit-push cycle with production-grade safety.

## Pipeline

1. **Collect** - Only task-related files (explicit `--files` list)
2. **Stage** - `git add` specified files
3. **Gate** - Run `pre_commit_check.py` (lint, secret scan, debug check, tests)
4. **Message** - Auto-generate Conventional Commit (`feat(scope): description`)
5. **Sign** - GPG sign for GitHub Verified badge (auto-detect config)
6. **Push** - Auto-push to origin (never force push)

## Quick Commands

### Commit task-related files

```bash
python auto_commit.py --project-root ./ --files src/models/User.js src/routes/user.routes.js
```

### Commit with custom message

```bash
python auto_commit.py --project-root ./ --files src/models/User.js -m "feat(user): add email validation"
```

### Dry-run (preview)

```bash
python auto_commit.py --project-root ./ --files README.md --dry-run
```

### Setup GPG for Verified badge

```bash
python auto_commit.py --setup-gpg
```

## Safety Guarantees

- `NEVER` commits if pre-commit gate fails
- `NEVER` force pushes
- Unstages files on gate failure (clean state)
- Falls back to unsigned commit if GPG fails
- Timeout on all git operations (60s)
- Conventional Commits format (CI/CD compatible)

## GPG Setup (One-Time)

Run `python auto_commit.py --setup-gpg` for interactive guide, or:

```bash
winget install GnuPG.GnuPG
gpg --quick-generate-key "your@email.com" rsa4096 sign never
gpg --list-secret-keys --keyid-format=long
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
gpg --armor --export YOUR_KEY_ID
```

Paste the exported key in GitHub Settings > SSH and GPG Keys > New GPG Key.

## Integration

This skill integrates with:

- `codex-execution-quality-gate/scripts/pre_commit_check.py` (CI gate)
- `codex-project-memory/scripts/generate_changelog.py` (reads commit history)
