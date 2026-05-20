---
name: git-sync-skill
description: Automate git workflow with intelligent commit message generation and email consistency verification. Use when syncing code changes with git, creating commits, or pushing to remote repositories. Triggers on phrases like 'sync my changes', 'commit and push', 'git sync', or any git workflow automation needs.
---

# Git Sync Skill

Automate git workflow with intelligent commit message generation and email consistency verification.

## Overview

This skill streamlines the git commit workflow by:
1. **Analyzing historical commit patterns** to generate messages that match your team's style
2. **Verifying email consistency** to prevent commits with mismatched author information
3. **Automating stage/commit/push** operations in a single command

## Quick Start

Run the sync script from any git repository:

```bash
python /path/to/git-sync-skill/scripts/sync.py
```

This will:
- Check email consistency with recent commits
- Analyze your commit message patterns
- Generate an appropriate commit message
- Stage all changes
- Commit and push

## Core Features

### 1. Email Consistency Check

Before committing, the script verifies that your configured git email matches the domain used in recent commits. This prevents accidental commits with personal emails in work repositories (or vice versa).

**Behavior:**
- If the last 5 commits all use `@company.com`, your config must also use `@company.com`
- If commits have mixed domains, a warning is shown for manual confirmation
- Use `--force` to skip this check when intentionally using a different email

**Example:**
```bash
# Will warn and exit if email domain doesn't match recent commits
python scripts/sync.py

# Skip email check
python scripts/sync.py --force
```

### 2. Intelligent Commit Message Generation

The script analyzes your recent commit history to match your team's style:

- **Conventional commits**: Detects if you use `feat:`, `fix:`, `chore:` prefixes
- **Capitalization**: Follows your pattern ("Add feature" vs "add feature")
- **Punctuation**: Matches period usage at end of messages
- **Verb selection**: Chooses appropriate verbs based on change types

**Message generation logic:**
| Change Type | Generated Message |
|-------------|-------------------|
| Only new files | "Add {file/description}" |
| Only modifications | "Update {files}" |
| Only deletions | "Remove {files}" |
| Mixed changes | "Update {files}" |

**Override with custom message:**
```bash
python scripts/sync.py -m "Implement user authentication"
```

### 3. Workflow Options

```bash
# Dry run - see what would happen without making changes
python scripts/sync.py --dry-run

# Commit only, don't push
python scripts/sync.py --no-push

# Skip email verification
python scripts/sync.py --force

# Analyze more commits for pattern detection
python scripts/sync.py --pattern-count 10
```

## Individual Scripts

### analyze_commits.py

Analyze commit message patterns without making changes:

```bash
python scripts/analyze_commits.py -n 10
```

Output includes:
- Whether conventional commits are used
- Capitalization patterns
- Average message length
- Common first words/verbs

### check_email.py

Verify email consistency:

```bash
# Check and exit with error code if inconsistent
python scripts/check_email.py

# Output as JSON for scripting
python scripts/check_email.py --json

# Skip check
python scripts/check_email.py --force
```

## Usage Examples

### Daily Workflow

```bash
# Make your changes...
vim myfile.py

# Quick sync with auto-generated message
python /path/to/git-sync-skill/scripts/sync.py

# Output:
# 📧 Checking email consistency...
#   ✓ Email consistency check passed. Domain: @company.com
# 📊 Analyzing commit message patterns...
#   Pattern: simple messages
#   Capitalization: first letter uppercase
# 📝 Changes to be committed:
#   M  myfile.py
# 💬 Generated commit message: "Update myfile.py"
# 📦 Staging changes...
# 🚀 Committing...
#   ✓ Committed: Update myfile.py
# ☁️  Pushing to main...
#   ✓ Pushed to origin/main
# ✅ Sync complete!
```

### With Custom Message

```bash
python scripts/sync.py -m "Fix authentication bug in login flow"
```

The custom message will be formatted according to your team's patterns (capitalization, punctuation).

### Email Mismatch Scenario

```bash
python scripts/sync.py

# Output:
# 📧 Checking email consistency...
# ⚠️  Email domain mismatch detected!
#
# Recent commits use: @company.com
# Your config uses: @gmail.com
#
# To fix, run:
#   git config user.email 'your.name@company.com'
#
# Or if this is intentional, use --force to continue anyway.
```

## Resources

### scripts/

- **`sync.py`** - Main automation script. Orchestrates email check, pattern analysis, and git operations.
- **`analyze_commits.py`** - Standalone commit pattern analyzer. Useful for understanding team conventions.
- **`check_email.py`** - Standalone email consistency checker. Can be integrated into CI pipelines.

### Implementation Notes

**Email Check Algorithm:**
1. Extract domains from last N commits
2. If all commits share one domain → current config must match
3. If mixed domains → warning (user must confirm)
4. Exit code 1 on mismatch, 0 on match or `--force`

**Message Generation Algorithm:**
1. Analyze last N commits for:
   - Conventional commit prefixes (feat:, fix:, etc.)
   - Capitalization pattern
   - Punctuation usage
   - Common verbs
2. Categorize current changes (add/modify/delete)
3. Select appropriate verb based on change type
4. Format message according to detected patterns

**Safety Features:**
- Dry-run mode for testing
- Clear preview of changes before commit
- Non-zero exit codes on errors for CI integration
- Respects existing git configurations
name: git-sync-skill
description: Automated git synchronization with intelligent commit message generation and email consistency verification. Use when syncing code changes to git repositories, committing work, or pushing updates. Triggers on requests like 'sync my changes', 'commit and push', 'git sync', or when automatic commit messages matching repository style are needed. Also handles email verification to ensure commits are attributed correctly.
---
name: git-sync-skill
description: Automate git commit and push with intelligent commit message generation and email verification. Use when syncing local changes to remote repository, committing code, or ensuring consistent commit message format and email configuration.
---

# Git Sync Skill

## Overview

Automatically sync git changes with commit messages that match your repository's style and verify email consistency before committing.

## Core Capabilities

### 1. Email Consistency Check

Before committing, the skill verifies your git email configuration matches recent commits:

- Checks the last 5 commits' email domains
- Compares with your current `user.email` config
- **Blocks commit** if domains don't match (prevents misattributed commits)
- **Warns and asks** if recent commits have inconsistent domains

**Example scenarios:**
- If all recent commits use `@company.com`, your config must also use `@company.com`
- If commits mix `@gmail.com` and `@company.com`, you'll be asked to confirm

### 2. Intelligent Commit Message Generation

Analyzes your repository's commit history to generate messages that match your style:

**Pattern analysis includes:**
- Conventional commits (e.g., `feat:`, `fix:`) vs simple messages
- Capitalization preference (first letter upper/lower case)
- Punctuation style (with/without period)
- Common verbs and structure

**Auto-generated messages based on changes:**
- Adding files → "Add {files}"
- Modifying files → "Update {files}"
- Deleting files → "Remove {files}"
- Mixed changes → "Update {N} files"

### 3. One-Command Sync

Stages, commits, and pushes in one operation:

```bash
# Auto-generate message and sync
python scripts/sync.py

# Custom message
python scripts/sync.py -m "Implement user authentication"

# Commit only (no push)
python scripts/sync.py --no-push

# Skip email check (if you know what you're doing)
python scripts/sync.py --force

# Preview without making changes
python scripts/sync.py --dry-run
```

## Quick Start

### Basic Usage

```bash
# Navigate to your git repository
cd /path/to/your/repo

# Run sync (analyzes history, checks email, commits, pushes)
python /path/to/git-sync-skill/scripts/sync.py
```

### Individual Tools

```bash
# Check email consistency only
python scripts/check_email.py

# Analyze commit patterns only
python scripts/analyze_commits.py

# Force continue despite email mismatch
python scripts/sync.py --force
```

## Workflow

### Standard Sync Flow

1. **Email Verification** → Compares current config with last 5 commits
2. **Pattern Analysis** → Examines commit message style from history
3. **Change Detection** → Identifies what files were added/modified/deleted
4. **Message Generation** → Creates message matching your style
5. **Commit** → Stages all changes and commits
6. **Push** → Pushes to origin (unless `--no-push`)

### Handling Email Mismatches

When email check fails:

```
⚠️  Email domain mismatch detected!

Recent commits use: @company.com
Your config uses: @gmail.com

To fix, run:
  git config user.email 'your.name@company.com'

Or if this is intentional, use --force to continue anyway.
```

## Scripts

### `scripts/sync.py`

Main sync script. Run this for the complete workflow.

**Options:**
| Flag | Description |
|------|-------------|
| `-m, --message` | Custom commit message |
| `--no-push` | Commit only, don't push |
| `-f, --force` | Skip email verification |
| `-n, --dry-run` | Preview without changes |
| `--email-count N` | Check last N commits for email (default: 5) |
| `--pattern-count N` | Analyze last N commits for patterns (default: 5) |

### `scripts/check_email.py`

Standalone email verification tool.

**Usage:**
```bash
python scripts/check_email.py              # Check and exit with status
python scripts/check_email.py --json       # JSON output for scripting
python scripts/check_email.py -f           # Force skip
```

### `scripts/analyze_commits.py`

Standalone commit pattern analysis.

**Usage:**
```bash
python scripts/analyze_commits.py          # Human-readable analysis
python scripts/analyze_commits.py --json   # JSON output
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (email mismatch, git error, etc.) |

## Requirements

- Python 3.7+
- Git repository with at least 1 commit
- Git user.name and user.email configured

Automate git workflow with smart commit message generation and email consistency checks.

## Quick Start

```bash
# Basic usage - auto-generates commit message and pushes
python scripts/sync.py

# With custom message
python scripts/sync.py -m "Add new feature"

# Commit only (no push)
python scripts/sync.py --no-push

# Skip email verification
python scripts/sync.py --force

# Dry run (see what would happen)
python scripts/sync.py --dry-run
```

## Features

### 1. Email Consistency Check

Before committing, the script checks if your git config email matches the pattern of recent commits:

- If the last 5 commits all use `@company.com`, your email should too
- If recent commits have inconsistent domains, you'll be warned to verify
- Use `--force` to skip this check

**Why this matters:**
- Prevents mixing personal and work emails in the same repo
- Maintains clean git history attribution
- Catches git misconfigurations early

### 2. Automatic Commit Message Generation

Analyzes recent commit history to match your team's style:

- Detects conventional commits (e.g., `feat:`, `fix:`) vs simple messages
- Matches capitalization patterns ("Add" vs "add")
- Matches punctuation style (period at end or not)
- Uses appropriate verbs based on change types

## Workflow Decision Tree

```
User: "Sync my changes"
  │
  ▼
┌────────────────────────────────┐
│ Are there uncommitted changes? │──No──▶ "✓ No changes to commit"
└────────────────────────────────┘
  │
  Yes
  │
  ▼
┌──────────────────────────────────┐
│ Email check (can skip with       │──Fail──▶ Show mismatch info, suggest fix
│ --force)                         │         Exit with error
└──────────────────────────────────┘
  │
  Pass
  │
  ▼
┌──────────────────────────────────┐
│ Analyze recent commits for       │
│ message format patterns          │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│ Generate commit message matching │
│ historical patterns              │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│ Stage all changes → Commit       │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│ Push to remote (unless           │
│ --no-push specified)             │
└──────────────────────────────────┘
  │
  ▼
"✅ Sync complete!"
```

## Commands

### Main Sync Command

```bash
python scripts/sync.py [options]
```

Options:
- `-m, --message TEXT` - Custom commit message (optional)
- `--no-push` - Commit only, skip push
- `-f, --force` - Skip email verification
- `-n, --dry-run` - Show what would happen without making changes
- `--email-count N` - Number of commits to check for email (default: 5)
- `--pattern-count N` - Number of commits to analyze for patterns (default: 5)

### Email Check Only

```bash
python scripts/check_email.py [options]
```

Options:
- `-n, --count N` - Number of commits to check (default: 5)
- `-f, --force` - Skip check (return success)
- `--json` - Output as JSON

### Commit Pattern Analysis

```bash
python scripts/analyze_commits.py [options]
```

Options:
- `-n, --count N` - Number of commits to analyze (default: 5)
- `--json` - Output as JSON

## Examples

### Example 1: Auto-commit with generated message

```bash
$ python scripts/sync.py

📧 Checking email consistency...
  ✓ Email consistency check passed. Domain: @163.com

📊 Analyzing commit message patterns...
  Pattern: simple messages
  Capitalization: first letter uppercase

📝 Changes to be committed:
   M README.md
  ?? new-file.txt

💬 Generated commit message: "Update README.md and add 1 file"

📦 Staging changes...
🚀 Committing...
  ✓ Committed: Update README.md and add 1 file

☁️  Pushing to main...
  ✓ Pushed to origin/main

✅ Sync complete!
```

### Example 2: Email mismatch detected

```bash
$ python scripts/sync.py

📧 Checking email consistency...
⚠️  Email domain mismatch detected!

Recent commits use: @163.com
Your config uses: @gmail.com

To fix, run:
  git config user.email 'your.name@163.com'

Or if this is intentional, use --force to continue anyway.

To continue anyway, run with --force flag
```

### Example 3: Custom message

```bash
$ python scripts/sync.py -m "Fix critical bug in auth"

📧 Checking email consistency...
  ✓ Email consistency check passed. Domain: @company.com

💬 Using custom commit message: "Fix critical bug in auth"
...
```

## Scripts

### scripts/sync.py

Main synchronization script. Orchestrates the full workflow:
1. Email verification
2. Pattern analysis
3. Message generation
4. Staging and committing
5. Pushing

### scripts/check_email.py

Standalone email verification tool. Can be used independently to check email configuration without committing.

### scripts/analyze_commits.py

Standalone commit pattern analysis tool. Useful for understanding your team's commit conventions.

## Notes

- Scripts must be run from within a git repository
- All changes are staged (`git add -A`) before commit
- The generated message tries to describe what changed based on file modifications
- Use `--dry-run` to preview actions without making changes
