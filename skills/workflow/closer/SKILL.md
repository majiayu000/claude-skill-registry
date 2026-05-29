---
name: closer
description: This skill should be used when the user asks to "close feature", "archive feature", "complete feature N", "move feature to completed", or wants to move a finished feature to the _completed/ directory.
---
# Feature Closer

## Primary Directive

Close and archive a completed feature, moving it from active backlog to completed.

## Input

Feature identifier: **${input:FeatureID (e.g., 003 or 003-my-feature)}**

## Step 1: Resolve Feature

Determine the feature to close:

1. If input provided, use it to find the feature folder
2. If no input, try to detect from current branch name (`feature/{NNN}-{slug}`)

```bash
# List active features in backlog (not in completed/)
ls -d backlog/plans/[0-9][0-9][0-9]-*/ 2>/dev/null | head -20
```

```bash
# Get current branch
git branch --show-current
```

Match the feature ID (NNN or NNN-slug) to a folder in `backlog/plans/`.

**If no matching feature found**: Report error and stop.

## Step 2: Validate Completion

Read the feature's `tasks.md` and check for incomplete tasks.

```bash
# Check for unchecked tasks (- [ ] pattern)
grep -c '^\s*- \[ \]' backlog/plans/{NNN}-{slug}/tasks.md 2>/dev/null || echo "0"
```

**If incomplete tasks exist**:
Use the AskUserQuestion tool to ask the user how to proceed:
- "Close anyway (mark as incomplete)"
- "Cancel and finish tasks first"

Only proceed if user chooses to close anyway or all tasks are complete.

## Step 3: Move Feature Folder

```bash
# Ensure completed/features directory exists
mkdir -p backlog/plans/_completed

# Move the feature folder
mv backlog/plans/{NNN}-{slug} backlog/plans/_completed/
```

## Step 4: Update Documentation References

Search for and update any references to the old path in documentation files.

### 4a: Find References

```bash
# Find files referencing the old backlog path (excluding completed/ and .ai/ logs)
grep -rl "backlog/plans/{NNN}-{slug}" . --include="*.md" 2>/dev/null | grep -v -e "^./backlog/plans/_completed/" -e "^./.ai/"
```

### 4b: Update References

For each file found, update paths from:
- `backlog/plans/{NNN}-{slug}/` → `backlog/plans/_completed/{NNN}-{slug}/`
- `../backlog/plans/{NNN}-{slug}/` → `../backlog/plans/_completed/{NNN}-{slug}/`

Common files to check:
- `.claude/commands/planner.md` (Reference section examples)
- `aidocs/feature-planning-methodology.md`
- Any README files referencing the feature

**Important**: Do NOT update paths in:
- `specs/tests/` (spec tests stay in place)
- `.ai/` (progress logs are historical records)
- The feature's own docs (they moved, so relative paths may still work)

## Step 5: Commit Changes

Stage and commit all changes from the move and path updates.

```bash
# Stage the move and any updated docs
git add -A

# Commit with descriptive message
git commit -m "chore: close feature {NNN}-{slug}

- Move backlog/plans/{NNN}-{slug}/ to backlog/plans/_completed/
- Update documentation references

Co-Authored-By: Claude Sonnet <noreply@anthropic.com>"
```

## Step 6: Summary

Output a summary:

```
Feature Closed: {NNN}-{slug}

Actions Taken:
✅ Moved backlog/plans/{NNN}-{slug}/ → backlog/plans/_completed/{NNN}-{slug}/
✅ Updated N documentation references
✅ Committed changes

Spec Tests: specs/tests/{NNN}-{slug}.md (unchanged)

Next Steps:
1. Review the commit: git show HEAD
2. Merge to master when ready: git checkout master && git merge feature/{NNN}-{slug}
3. Delete feature branch after merge: git branch -d feature/{NNN}-{slug}
```

## Error Handling

- **Feature not found**: List available features and ask user to specify
- **Already in completed/**: Report that feature is already closed
- **Git dirty state**: Warn user about uncommitted changes before proceeding
- **Move fails**: Report error, do not proceed with doc updates
