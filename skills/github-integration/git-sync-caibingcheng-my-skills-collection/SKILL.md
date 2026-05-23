---
name: git-sync
description: USE WHEN syncing code changes with git, creating commits with intelligent messages, pushing to remote repositories, or automating git workflows. Triggers on 'sync my changes', 'commit and push', 'git sync', 'sync to remote'.
---

# Git Sync Skill

Automate git workflow with smart commit message generation and email verification.

## Quick Start

```bash
python scripts/sync.py
```

This will:
1. Check email consistency with recent commits
2. Analyze commit message patterns
3. Generate an appropriate commit message
4. Stage, commit, and push

## Core Features

### 1. Email Consistency Check

Before committing, verifies your `user.email` matches recent commits:

- If last 5 commits use `@company.com`, your config must too
- Prevents mixing personal/work emails
- Use `--force` to skip

**Example:**
```
⚠️  Email domain mismatch detected!

Recent commits use: @company.com
Your config uses: @gmail.com

To fix, run:
  git config user.email 'your.name@company.com'

Or if this is intentional, use --force to continue anyway.
```

### 2. Intelligent Commit Messages

Analyzes your repo's commit history to match style:

| Pattern Detected | Applied to New Message |
|-----------------|----------------------|
| Conventional commits | Adds `feat:`/`fix:` prefix |
| Capitalization | "Add feature" vs "add feature" |
| Punctuation | Period at end or not |
| Common verbs | Uses repository's preferred verbs |

**Auto-generated based on changes:**
- Adding files → "Add {files}"
- Modifying files → "Update {files}"
- Deleting files → "Remove {files}"
- Mixed changes → "Update {N} files"

### 3. Workflow Options

```bash
# Dry run - preview without changes
python scripts/sync.py --dry-run

# Commit only, don't push
python scripts/sync.py --no-push

# Skip email verification
python scripts/sync.py --force

# Custom message (formatted to match repo style)
python scripts/sync.py -m "Implement user authentication"

# Analyze more commits for pattern detection
python scripts/sync.py --pattern-count 10
```

## Workflow

```
┌─────────────────────────────┐
│ Check email consistency     │──Fail──▶ Show fix suggestion, exit
└─────────────────────────────┘
              │ Pass
              ▼
┌─────────────────────────────┐
│ Analyze commit patterns     │
│ (style, verbs, format)      │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Categorize changes          │
│ (add/modify/delete)         │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Generate matching message   │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Stage → Commit → Push       │
└─────────────────────────────┘
```

## Scripts

### `scripts/sync.py` - Main Entry

| Flag | Description |
|------|-------------|
| `-m, --message` | Custom commit message |
| `--no-push` | Commit only, skip push |
| `-f, --force` | Skip email verification |
| `-n, --dry-run` | Preview without changes |
| `--email-count N` | Check last N commits for email (default: 5) |
| `--pattern-count N` | Analyze last N commits for patterns (default: 5) |

### `scripts/check_email.py` - Standalone Email Check

```bash
python scripts/check_email.py           # Check and exit with status
python scripts/check_email.py --json    # JSON output
python scripts/check_email.py -f        # Force skip
```

### `scripts/analyze_commits.py` - Pattern Analysis

```bash
python scripts/analyze_commits.py          # Human-readable
python scripts/analyze_commits.py --json   # JSON output
```

## Example Output

```bash
$ python scripts/sync.py

📧 Checking email consistency...
  ✓ Email consistency check passed. Domain: @company.com

📊 Analyzing commit message patterns...
  Pattern: simple messages
  Capitalization: first letter uppercase

📝 Changes to be committed:
   M  src/main.py
  ??  src/utils.py

💬 Generated commit message: "Update src/main.py and add 1 file"

📦 Staging changes...
🚀 Committing...
  ✓ Committed: Update src/main.py and add 1 file

☁️  Pushing to main...
  ✓ Pushed to origin/main

✅ Sync complete!
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (email mismatch, git error, etc.) |

## Requirements

- Python 3.7+
- Git repository with at least 1 commit
- Git `user.name` and `user.email` configured