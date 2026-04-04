---
name: GitHub Issue Triage
description: Monitor and triage GitHub issues against design docs and implementation status. Use when user asks to "check issues", "triage issues", "sync issues", "what issues are open", or wants to ensure issues are up-to-date with development progress.
---

# GitHub Issue Triage

**Monitor open GitHub issues, match them to design docs, identify closable issues, and keep the issue tracker synchronized with actual development progress.**

## Quick Start

**Most common usage:**
```bash
# Full triage report - shows all issues, matches to design docs, suggests closures
.claude/skills/github-issue-triage/scripts/triage_report.sh

# Just list open issues with labels and age
.claude/skills/github-issue-triage/scripts/list_open_issues.sh

# Find issues that have been implemented (design docs in implemented/)
.claude/skills/github-issue-triage/scripts/find_closable.sh

# Match issues to planned design docs (shows what's being worked on)
.claude/skills/github-issue-triage/scripts/match_design_docs.sh --planned
```

## When to Use This Skill

Invoke this skill when:
- User asks "what issues are open?", "check our issues", "triage issues"
- Starting a new development cycle and need to understand backlog
- After completing a release to identify closable issues
- Periodic housekeeping to keep issue tracker clean
- User wants to understand which issues are covered by design docs

## Available Scripts

### `scripts/check_auth.sh`
Verify GitHub CLI authentication matches expected user.

**Usage:**
```bash
.claude/skills/github-issue-triage/scripts/check_auth.sh
```

**What it checks:**
1. `gh` CLI is installed
2. User is authenticated to github.com
3. Active account matches `github.expected_user` in config

**Exit codes:**
- `0` - Auth OK, correct user active
- `1` - Auth failed or wrong user active

### `scripts/list_open_issues.sh [--json] [--labels LABELS]`
List all open GitHub issues with details.

**Usage:**
```bash
.claude/skills/github-issue-triage/scripts/list_open_issues.sh
.claude/skills/github-issue-triage/scripts/list_open_issues.sh --json
.claude/skills/github-issue-triage/scripts/list_open_issues.sh --labels bug,enhancement
```

**Output includes:**
- Issue number and title
- Labels (bug, enhancement, etc.)
- Age (days since creation)
- Last updated date
- Assignee (if any)

### `scripts/match_design_docs.sh [--planned] [--implemented] [--all]`
Match open issues to design documents.

**Usage:**
```bash
.claude/skills/github-issue-triage/scripts/match_design_docs.sh           # All matches
.claude/skills/github-issue-triage/scripts/match_design_docs.sh --planned # Only planned docs
.claude/skills/github-issue-triage/scripts/match_design_docs.sh --implemented # Only implemented
```

**Matching strategy:**
1. Exact issue number references (`#123` in design doc)
2. Title keyword matching (significant words from issue title)
3. Bug ID matching (`M-BUG-XXX` patterns)

**Output:**
```
Issue #29: Parser crash on empty input
  Status: COVERED
  Design doc: design_docs/planned/v0_6_1/m-bug-parser-crash.md
  Match type: exact_reference (#29)

Issue #31: Add async support
  Status: NOT COVERED
  No matching design doc found
  Suggestion: Create design doc in design_docs/planned/v0_7_0/
```

### `scripts/find_closable.sh [--close] [--dry-run]`
Find issues that have been implemented and can be closed.

**Usage:**
```bash
.claude/skills/github-issue-triage/scripts/find_closable.sh           # Report only
.claude/skills/github-issue-triage/scripts/find_closable.sh --dry-run # Preview close actions
.claude/skills/github-issue-triage/scripts/find_closable.sh --close   # Actually close issues
```

**What it checks:**
1. Issue referenced in `design_docs/implemented/` directory
2. Issue mentioned in CHANGELOG.md
3. Issue keywords match implemented features

### `scripts/triage_report.sh [--output FILE]`
Generate a complete triage report combining all analysis.

**Usage:**
```bash
.claude/skills/github-issue-triage/scripts/triage_report.sh
.claude/skills/github-issue-triage/scripts/triage_report.sh --output /tmp/triage.md
```

**Report includes:**
1. **Summary**: Total open, covered, closable, orphaned
2. **Closable Issues**: Ready to close (implemented)
3. **Covered Issues**: Have design docs (in progress)
4. **Orphaned Issues**: No design doc coverage (need attention)
5. **Stale Issues**: No activity in 30+ days
6. **Recommendations**: Suggested actions

## Triage Workflow

### 1. Check Authentication

**Always verify correct GitHub account:**
```bash
.claude/skills/github-issue-triage/scripts/check_auth.sh
```

If wrong account:
```bash
gh auth switch --user MarkEdmondson1234
```

### 2. Generate Triage Report

```bash
.claude/skills/github-issue-triage/scripts/triage_report.sh
```

### 3. Handle Closable Issues

**Review and close issues that have been implemented:**
```bash
# Preview what would be closed
.claude/skills/github-issue-triage/scripts/find_closable.sh --dry-run

# Close with proper comments
.claude/skills/github-issue-triage/scripts/find_closable.sh --close
```

### 4. Review Orphaned Issues

**For issues without design doc coverage:**
1. Assess priority and feasibility
2. Create design doc if work should proceed: `/design-doc-creator`
3. Close with "won't fix" if out of scope
4. Add to backlog for future versions

### 5. Handle Stale Issues

**For issues with no activity in 30+ days:**
1. Check if still relevant
2. Add comment requesting update from reporter
3. Close if no response after additional time

## Bot User Integration (sunholo-voight-kampff)

**Status: ACTIVE** - Bot is configured and ready to use.

**Bot account:** https://github.com/sunholo-voight-kampff

### What Uses the Bot

| Tool | Uses Bot? |
|------|-----------|
| `gh issue close/comment` | Yes (via `gh auth`) |
| `ailang messages send --github` | Yes (via config) |
| `ailang messages import-github` | Yes (via config) |
| Issue triage scripts | Yes (uses `gh` CLI) |

### Current Configuration

The bot is configured in `~/.ailang/config.yaml`:
```yaml
github:
  expected_user: sunholo-voight-kampff
  default_repo: sunholo-data/ailang
```

### Switching Accounts

```bash
# Use bot (current)
gh auth switch --user sunholo-voight-kampff

# Use personal (update config too if using ailang messages --github)
gh auth switch --user MarkEdmondson1234
```

### Benefits of Bot User

- **Audit trail**: All automated actions attributed to bot
- **Rate limits**: Separate from personal account limits
- **Revocable access**: Easy to disable without affecting personal auth
- **CI/CD integration**: Can use same token in automation
- **Unified**: Both `gh` CLI and `ailang messages` use same account

For detailed setup and troubleshooting, see [`resources/bot_user_guide.md`](resources/bot_user_guide.md)

## Configuration

Current config in `~/.ailang/config.yaml`:

```yaml
github:
  expected_user: sunholo-voight-kampff  # Bot account (active)
  default_repo: sunholo-data/ailang
```

## Integration with Other Skills

### With release-manager
```bash
# Before release: find issues to close
.claude/skills/github-issue-triage/scripts/find_closable.sh

# During release: close issues
.claude/skills/release-manager/scripts/collect_closable_issues.sh 0.6.1 --close
```

### With design-doc-creator
```bash
# Find uncovered issues, then create design doc
.claude/skills/github-issue-triage/scripts/match_design_docs.sh --planned
# For uncovered issue #42:
/design-doc-creator M-ISSUE-42 "Fix for issue #42"
```

### With sprint-planner
```bash
# Use triage report to inform sprint scope
.claude/skills/github-issue-triage/scripts/triage_report.sh --output /tmp/triage.md
# Include high-priority uncovered issues in sprint
```

## Resources

### Bot User Guide
See [`resources/bot_user_guide.md`](resources/bot_user_guide.md) for complete bot account setup.

### Triage Checklist
See [`resources/triage_checklist.md`](resources/triage_checklist.md) for step-by-step checklist.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Correct user active (`gh auth status`)
- Repository access (`sunholo-data/ailang`)
- `~/.ailang/config.yaml` with `github.expected_user`

## Notes

- All scripts check auth before making changes
- Close operations add proper comments with release/commit references
- Designed for AILANG repo but can be adapted for others
- Works with existing `ailang messages` GitHub integration
