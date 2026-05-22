---
name: agent-ops-code-review-interactive
description: "Interactive code review for agent iterations. Captures comments, tracks resolution status, and integrates with git diffs."
category: utility
invokes: [agent-ops-git, agent-ops-critical-review]
invoked_by: [agent-ops-implementation, agent-ops-validation]
state_files:
  read: [constitution.md, focus.md, issues/*.md]
  write: [focus.md, reviews/*.md]
---

# Interactive Code Review Skill

## Purpose

Provide structured code review workflow after agent implementation iterations. Allows capturing comments with categories and tracking resolution status.

## Storage Format

Reviews are stored in `.agent/reviews/`:

```
.agent/reviews/
├── YYYY-MM-DD-<short_hash>.md    # Review for specific commit
├── active-review.md               # Currently open review
└── README.md                      # Review folder documentation
```

## Review Document Format

```markdown
# Code Review: <commit_hash>

**Date**: YYYY-MM-DD HH:MM
**Author**: [user|agent]
**Commit**: <full_hash>
**Branch**: <branch_name>

## Summary

<brief description of changes reviewed>

## Changed Files

| File | Lines Changed | Status |
|------|---------------|--------|
| src/foo.py | +15 -3 | reviewed |
| tests/test_foo.py | +25 | pending |

## Comments

### [CATEGORY] File:Line — Comment Title

**File**: `path/to/file.py`
**Line**: 42-45
**Category**: fix | question | suggestion | concern | praise
**Status**: open | addressed | wont_fix | deferred
**Priority**: critical | high | normal | low

<comment body>

#### Response (if any)

<agent or user response>

---

### [SUGGESTION] src/utils.py:78 — Consider extracting helper

**File**: `src/utils.py`
**Line**: 78
**Category**: suggestion
**Status**: addressed
**Priority**: normal

This block of code appears in multiple places. Consider extracting to a helper function.

#### Response

Extracted to `_format_output()` helper in commit abc123.

---

## Metrics

- Total Comments: X
- Open: X
- Addressed: X
- Won't Fix: X
- Deferred: X
```

## Comment Categories

| Category | Icon | Use For |
|----------|------|---------|
| `fix` | 🔧 | Required changes, bugs, errors |
| `question` | ❓ | Clarification needed |
| `suggestion` | 💡 | Optional improvements |
| `concern` | ⚠️ | Potential issues, risks |
| `praise` | 👍 | Good patterns, well done |

## Status Transitions

```
open → addressed    (when fix is committed)
open → wont_fix     (when decided not to fix with reason)
open → deferred     (when moved to future work)
```

## CLI Integration (Proposed)

```bash
# Start review for current changes
aoc review start

# Start review for specific commit
aoc review start <commit>

# View current review
aoc review show

# Add a comment
aoc review comment --file src/foo.py --line 42 --category fix "Fix null check"

# Mark comment as addressed
aoc review resolve <comment_id>

# Mark as won't fix
aoc review wontfix <comment_id> --reason "Out of scope"

# Defer to issue
aoc review defer <comment_id> --issue FEAT-0123

# Complete review
aoc review complete

# Generate summary
aoc review summary
```

## Workflow Integration

### After Implementation

```
User: Review the changes

Agent:
1. Get diff since last commit/baseline
2. Apply agent-ops-critical-review analysis
3. Create review document
4. Present findings organized by category
5. Ask for user feedback

User: [Provides comments]

Agent:
1. Record comments in review document
2. Address fix/question items
3. Commit changes
4. Update comment statuses
5. Present updated review
```

### Integration with Validation

The validation skill can check for unresolved review comments:

```markdown
## Pre-Commit Checklist

- [ ] All tests pass
- [ ] No lint errors
- [ ] Coverage maintained
- [x] Review comments addressed (3 open → requires resolution)
```

## Review Templates

### Quick Review (for small changes)

```markdown
# Quick Review: <hash>

**Changes**: <summary>

## Comments

- **src/foo.py:23**: [fix] Missing null check
- **src/bar.py:45**: [suggestion] Could simplify with list comprehension

## Status: open/complete
```

### Detailed Review (for PRs/major changes)

Full format as shown above.

## Best Practices

1. **Review early, review often** — Don't let comments accumulate
2. **Be specific** — Include file paths and line numbers
3. **Categorize correctly** — Helps prioritize response
4. **Track everything** — All decisions should be captured
5. **Close the loop** — Every comment should reach a final status
