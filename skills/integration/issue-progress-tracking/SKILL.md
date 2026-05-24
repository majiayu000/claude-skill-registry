---
name: issue-progress-tracking
description: Automatic GitHub issue progress updates from commits and sub-task completion. Use when tracking issue progress from commits or automating status updates.
tags: [github, issues, progress, tracking, automation, commits]
user-invocable: false
---

# Issue Progress Tracking

Automatic GitHub issue progress tracking that updates issues based on commits and marks sub-tasks as complete.

## Overview

- Working on GitHub issues with checkbox sub-tasks
- Making commits that reference issue numbers
- Using issue-prefixed branches (e.g., `issue/123-feature`, `fix/456-bug`)
- Wanting automatic progress visibility without manual updates

## How It Works

### Automatic Progress Tracking

The plugin automatically tracks your work through three coordinated hooks:

1. **Commit Detection** (`issue-progress-commenter.sh`)
   - Extracts issue number from branch name or commit message
   - Queues commit info for batch commenting
   - Supports patterns: `issue/123-*`, `fix/123-*`, `feature/123-*`, `#123`

2. **Sub-task Updates** (`issue-subtask-updater.sh`)
   - Parses commit messages for task completion keywords
   - Matches against unchecked `- [ ]` items in issue body
   - Automatically checks off matching tasks via GitHub API

3. **Session Summary** (`issue-work-summary.sh`)
   - Posts consolidated progress comment when session ends
   - Includes: commits, files changed, sub-tasks completed, PR link

### Issue Number Extraction

```bash
# From branch name (priority)
issue/123-implement-feature  # Extracts: 123
fix/456-resolve-bug          # Extracts: 456
feature/789-add-tests        # Extracts: 789
123-some-description         # Extracts: 123

# From commit message (fallback)
"feat(#123): Add user validation"     # Extracts: 123
"fix: Resolve bug (closes #456)"      # Extracts: 456
```

### Sub-task Matching

Commit messages are matched against issue checkboxes using:
- Normalized text comparison (case-insensitive)
- Partial matching for task descriptions
- Keyword detection (Add, Implement, Fix, Test, etc.)

**Example:**
```markdown
# Issue body
- [ ] Add input validation
- [ ] Write unit tests
- [ ] Update documentation

# Commit message
"feat(#123): Add input validation"

# Result: First checkbox auto-checked
- [x] Add input validation
- [ ] Write unit tests
- [ ] Update documentation
```

## Progress Comment Format

```markdown
## Claude Code Progress Update

**Session**: `abc12345...`
**Branch**: `issue/123-implement-feature`

### Commits (3)
- `abc1234`: feat(#123): Add input validation
- `def5678`: test(#123): Add unit tests
- `ghi9012`: docs(#123): Update README

### Files Changed
- `src/validation.ts` (+45, -12)
- `tests/validation.test.ts` (+89, -0)
- `README.md` (+5, -2)

### Sub-tasks Completed
- [x] Add input validation
- [x] Write unit tests

### Pull Request
https://github.com/owner/repo/pull/42

---
*Automated by SkillForge*
```

## Requirements

- `gh` CLI installed and authenticated
- Repository with GitHub remote
- Issue must exist and be accessible

## Configuration

Disable individual hooks in `.claude/config.json`:

```json
{
  "hooks": {
    "issue-progress-commenter.sh": false,
    "issue-subtask-updater.sh": false,
    "issue-work-summary.sh": false
  }
}
```

## Best Practices

1. **Use Issue Branches**: Start branches with `issue/N-` for automatic detection
2. **Reference Issues in Commits**: Include `#N` or `(#N)` in commit messages
3. **Match Checkbox Text**: Commit messages that match issue checkboxes get auto-checked
4. **Use Conventional Commits**: `feat(#123):`, `fix(#123):`, `test(#123):` patterns work well

## Related Skills

- `commit` - Commit creation with conventional format
- `github-operations` - GitHub CLI patterns and workflows
- `fix-issue` - Issue resolution workflow

## References

- [Branch Naming](references/branch-naming.md) - Supported branch patterns for issue extraction
- [GitHub CLI Commands](references/gh-api-commands.md) - gh commands used by the hooks
