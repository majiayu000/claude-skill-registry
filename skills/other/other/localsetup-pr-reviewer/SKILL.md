---
name: localsetup-pr-reviewer
description: Automated GitHub PR code review with diff analysis, lint integration, and structured reports. Use when reviewing pull requests, checking for security issues, error handling gaps, test coverage, or code style problems. Supports Go, Python, and JavaScript/TypeScript. Requires gh CLI authenticated with repo access.
metadata:
  version: "1.1"
---

# PR Reviewer

Automated code review for GitHub pull requests. Analyzes diffs for security issues, error handling gaps, style problems, and test coverage.

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`)
- Repository access (read at minimum, write for posting comments)
- Optional: `golangci-lint` for Go linting, `ruff` for Python linting

## Quick Start

```bash
# Review all open PRs in current repo
python scripts/pr_review.py check

# Review a specific PR
python scripts/pr_review.py review 42

# Post review as GitHub comment
python scripts/pr_review.py post 42

# Check status of all open PRs
python scripts/pr_review.py status

# List unreviewed PRs (useful for heartbeat/cron integration)
python scripts/pr_review.py list-unreviewed
```

## Configuration

Set these environment variables or the script auto-detects from the current git repo:

- `PR_REVIEW_REPO` — GitHub repo in `owner/repo` format (default: detected from `gh repo view`)
- `PR_REVIEW_DIR` — Local checkout path for lint (default: git root of cwd)
- `PR_REVIEW_STATE` — State file path (default: `./data/pr-reviews.json`)
- `PR_REVIEW_OUTDIR` — Report output directory (default: `./data/pr-reviews/`)

## What It Checks

| Category | Marker | Examples |
|----------|--------|----------|
| Security | [FAIL] | Hardcoded credentials, AWS keys, secrets in code |
| Error Handling | [WARNING] | Discarded errors (Go `_ :=`), bare `except:` (Python), unchecked `Close()` |
| Risk | [WARNING] | `panic()` calls, `process.exit()` |
| Style | [NOTE] | `fmt.Print`/`print()`/`console.log` in prod, very long lines |
| TODOs | [NOTE] | TODO, FIXME, HACK, XXX markers |
| Test Coverage | [NOTE] | Source files changed without corresponding test changes |

## Smart Re-Review

Tracks HEAD SHA per PR. Only re-reviews when new commits are pushed. Use `review <PR#>` to force re-review.

## Report Format

Reports are saved as markdown files in the output directory. Each report includes:

- PR metadata (author, branch, changes)
- Commit list
- Changed file categorization by language/type
- Automated diff findings with file, line, category, and context
- Test coverage analysis
- Local lint results (when repo is checked out locally)
- Summary verdict: [FAIL] SECURITY / [WARNING] NEEDS ATTENTION / [NOTE] MINOR NOTES / [OK] LOOKS GOOD

## Heartbeat/Cron Integration

Add to a periodic check (heartbeat, cron job, or CI):

```bash
UNREVIEWED=$(python scripts/pr_review.py list-unreviewed)
if [ -n "$UNREVIEWED" ]; then
  python scripts/pr_review.py check
fi
```

## Extending

The analysis patterns in `pr_review.py` are organized by language. Add new patterns by appending to the relevant pattern list in the `analyze_diff()` function:

```python
# Add a new Go pattern
go_patterns.append((r'^\+.*os\.Exit\(', 'RISK', 'Direct os.Exit() — consider returning error'))
```
