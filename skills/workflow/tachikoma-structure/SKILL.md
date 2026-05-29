---
name: tachikoma-structure
description: Analyze Context Lake file organization and propose structural changes. Use when asked to run structure cleanup, find misplaced files, identify orphans, archive old content, or merge duplicates.
allowed-tools: Read, Write, Glob, Grep
---

# Tachikoma Structure Cleanup

You are running structure cleanup on a Context Lake workspace. Your job is to analyze file organization and propose structural changes by creating decision files.

## Context Lake Structure

The workspace IS the Context Lake. Entity directories live at the workspace root:
- `.claude/schema.yaml` - Entity type definitions
- `.claude/tachikoma-summary.yaml` - Previous observations
- `{entity_type}/` - Entity directories (tasks/, notes/, roles/, etc.)
- `decisions/` - Where you write proposals

## What to Look For

1. **Wrong directory**: Files that belong in a different entity type
   - Example: Note with action items and status → relocate to tasks/

2. **Orphan files**: Files outside the schema structure
   - Example: Random .md in workspace root → relocate or delete

3. **Stale content**: Old files that may need archiving
   - Example: Task completed 6+ months ago → archive

4. **Duplicates**: Multiple files covering the same topic
   - Example: Two notes about 'API design' → merge

5. **Naming issues**: Files not matching naming conventions
   - Example: Journal named 'notes-jan.md' → rename to '2024-01-15.md'

6. **Junk/system files**: Files that should never be in a workspace
   - .DS_Store, Thumbs.db (OS junk)
   - __pycache__/, *.pyc (Python cache)
   - *.swp, *.swo, *~ (editor backup files)
   - *.bak, *.tmp (temporary files)
   - Delete with HIGH confidence (0.95+)

7. **Sync divergence**: Local and remote have diverged
   - Check with: `git fetch origin && git status`
   - If "diverged" or "ahead/behind": propose sync_merge strategy
   - Analyze which files conflict and recommend resolution

## Process

1. Read `.claude/schema.yaml` to understand expected structure
2. Read `.claude/tachikoma-summary.yaml` for previous observations
3. Explore all directories in the workspace
4. Identify misplaced, orphaned, stale, or duplicate files
5. Create appropriate decision files
6. Update `.claude/tachikoma-summary.yaml` with findings

## Decision Types

### relocate
Move file to correct location:
```markdown
---
title: "relocate: voice-samples.md to songs/"
status: pending
decision_type: relocate
subject_path: voice-samples-to-record.md
suggested_path: songs/voice-samples-to-record.md
confidence: 0.85
---

## Current State
File `voice-samples-to-record.md` is in workspace root but contains song-related content.

## Suggested Change
Move to `songs/voice-samples-to-record.md`

## Reasoning
Content is about vocal samples for specific songs, belongs with other song materials.
```

### archive
Move to archive for historical reference:
```markdown
---
title: "archive: completed tasks from 2024"
status: pending
decision_type: archive
subject_path: tasks/old-completed-task.md
suggested_path: archive/tasks/old-completed-task.md
confidence: 0.7
---
```

### delete
Remove file (use sparingly, high confidence required):
```markdown
---
title: "delete: empty placeholder file"
status: pending
decision_type: delete
subject_path: notes/placeholder.md
confidence: 0.95
---
```

### merge
Combine multiple files:
```markdown
---
title: "merge: api-design files"
status: pending
decision_type: merge
subject_path: notes/api-design-v1.md, notes/api-design-v2.md
suggested_path: notes/api-design.md
confidence: 0.8
---
```

### sync_merge
Propose strategy for merging divergent local/remote workspaces:
```markdown
---
title: "sync: merge remote changes from VM"
status: pending
decision_type: sync_merge
local_branch: main
remote_branch: origin/main
confidence: 0.85
---

## Divergence Detected

Local and remote have diverged:
- Local ahead by: [N] commits
- Remote ahead by: [M] commits

## Files in Conflict

- `roles/01-creative-lead.md` - modified both sides
- `tasks/new-task.md` - exists only on remote
- `.claude/schema.yaml` - modified locally

## Proposed Strategy

1. **Fetch remote:** `git fetch origin`
2. **Rebase local on remote:** `git rebase origin/main`
   - Or merge if rebase too complex: `git merge origin/main`
3. **Resolve conflicts:**
   - `roles/01-creative-lead.md`: Keep local (more recent curation)
   - `.claude/schema.yaml`: Manual merge needed
4. **Push to sync:** `git push origin main`

## Commands

```bash
git fetch origin
git rebase origin/main
# resolve conflicts if any
git push origin main
```

## Reasoning

Remote has new content from VM auto-commits. Local has role updates from learning.
Rebase preferred to keep linear history.
```

Use `sync_merge` when workspace has both local and remote changes that need reconciliation.

## Confidence Guidelines

- **relocate**: 0.7+ (clear evidence file belongs elsewhere)
- **archive**: 0.6+ (old content, completed tasks)
- **delete**: 0.9+ (duplicates, truly unnecessary, empty)
- **merge**: 0.8+ (clear overlap, same topic)
- **sync_merge**: 0.8+ (clear divergence, strategy makes sense)

## Guidelines

- Don't relocate files that are intentionally in their location
- Check file content, not just names, before proposing changes
- Prefer archive over delete for completed work
- Be conservative with delete proposals

## Output

When done, update `.claude/tachikoma-summary.yaml`:

```yaml
last_scan: {ISO timestamp}
cleanup_mode: structure
entity_counts:
  tasks: 10
  notes: 5
  orphan_files: 2
observations:
  - Found 2 files in root that belong in entity directories
  - 3 completed tasks from 2024 could be archived
pending_decisions:
  - relocate-voice-samples.md
  - archive-old-tasks.md
```
