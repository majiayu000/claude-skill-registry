---
name: worktree
description: |
  Manage git worktrees for parallel issue development - list, switch, clean, and prune.
version: "1.0.0"

  TRIGGER when: User wants to list worktrees, switch between worktrees, clean up worktrees, or manage worktrees ("list worktrees", "/worktree", "switch to worktree", "clean worktrees").

  DO NOT TRIGGER when: User wants to start issues (use /start-issue) or finish issues (use /finish-issue).
argument-hint: "[list|switch|clean|prune]"
allowed-tools: Bash, Read, Write
disable-model-invocation: false
user-invocable: true
---

# Worktree - Git Worktree Management

Manage git worktrees for parallel issue development with interactive selection and cleanup.

## Overview

This skill provides comprehensive worktree management for the issue workflow:

**What it does:**
- **List** all worktrees with status (active/merged/stale)
- **Interactive selection** to switch between worktrees
- **Clean** merged or stale worktrees automatically
- **Prune** orphaned worktree references

**Why it's needed:**
When working on multiple issues in parallel using worktrees, you need an easy way to see all active work, switch between issues, and clean up completed work. This skill provides a unified interface for all worktree operations.

**When to use:**
- View all active worktrees and their status
- Quickly switch to a different issue's worktree
- Clean up after merging PRs
- Manage worktree references

## Commands

```bash
/worktree              # Interactive: list + select worktree to switch
/worktree list         # List all worktrees with details
/worktree switch <n>   # Switch to worktree by number or issue#
/worktree clean        # Remove merged/stale worktrees
/worktree prune        # Clean up orphaned references
```

## Usage

### List Worktrees

**Command**: `/worktree` or `/worktree list`

**Output**:
```
📋 Git Worktrees:

┌────┬────────┬──────────────────────────────────┬─────────────────────────────┬──────────┐
│ #  │ Issue  │ Branch                           │ Path                        │ Status   │
├────┼────────┼──────────────────────────────────┼─────────────────────────────┼──────────┤
│ 1  │ main   │ main                             │ ~/dev/ai-dev                │ 🏠 Main  │
│ 2  │ #101   │ feature/101-remove-taskcreate... │ ~/dev/ai-dev-101-remove...  │ 🟢 Active│
│ 3  │ #110   │ feature/110-compliance...        │ ~/dev/ai-dev-110-compli...  │ ✅ Merged│
│ 4  │ #113   │ feature/113-worktree...          │ ~/dev/ai-dev-113-worktree...│ 🟡 Current│
└────┴────────┴──────────────────────────────────┴─────────────────────────────┴──────────┘

💡 Current: #4 (Issue #113)
```

**Status indicators**:
- 🏠 Main - Main repository worktree
- 🟢 Active - Issue in progress
- ✅ Merged - PR merged, ready for cleanup
- 🟡 Current - You are here
- 🔴 Stale - No activity for >30 days

### Interactive Switch

**Command**: `/worktree` (when run without arguments)

**Behavior**:
1. Show list of all worktrees
2. Prompt: "Select worktree to switch (1-4) or 'q' to quit: _"
3. User selects number
4. Output cd command for easy execution

**Example**:
```
Select worktree to switch (1-4) or 'q' to quit: 2

📍 To switch to worktree #2 (Issue #101), run:

   cd ~/dev/ai-dev-101-remove-taskcreate-pattern

Or in a new terminal:
   Terminal → New Tab → cd ~/dev/ai-dev-101-remove-taskcreate-pattern
```

### Switch by Number

**Command**: `/worktree switch 2` or `/worktree switch #101`

**Behavior**:
- Accept either worktree number (from list) or issue number
- Output cd command for the selected worktree

### Clean Merged Worktrees

**Command**: `/worktree clean`

**Behavior**:
1. Find all worktrees with status="merged" or "stale"
2. Show list and prompt for confirmation
3. Remove confirmed worktrees
4. Update metadata

**Example**:
```
🧹 Found 2 worktrees ready for cleanup:

  #110 - Fix skills compliance (merged 2 days ago)
  #108 - Update docs (merged 1 week ago)

Remove these worktrees? [y/N]: y

✅ Removed worktree for issue #110
✅ Removed worktree for issue #108

💾 Disk space freed: ~45 MB
```

### Prune References

**Command**: `/worktree prune`

**Behavior**:
- Run `git worktree prune` to clean up orphaned references
- Update metadata to remove cleaned entries

## Implementation

### Script: list_worktrees.py

```python
#!/usr/bin/env python3
"""List all git worktrees with metadata."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "scripts"))

from worktree_manager import list_worktrees

def format_table(worktrees):
    """Format worktrees as ASCII table."""
    # Implementation in scripts/worktree_manager.py
    ...

if __name__ == "__main__":
    worktrees = list_worktrees()
    format_table(worktrees)
```

### Script: select_worktree.py

```python
#!/usr/bin/env python3
"""Interactive worktree selection."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "scripts"))

from worktree_manager import list_worktrees, detect_current_worktree

def prompt_selection(worktrees):
    """Show list and prompt for selection."""
    # Display table
    print_table(worktrees)

    # Prompt
    choice = input("\nSelect worktree (1-{}) or 'q' to quit: ".format(len(worktrees)))

    if choice.lower() == 'q':
        return None

    try:
        idx = int(choice) - 1
        return worktrees[idx]
    except (ValueError, IndexError):
        print("Invalid selection")
        return None

if __name__ == "__main__":
    worktrees = list_worktrees()
    selected = prompt_selection(worktrees)

    if selected:
        print(f"\n📍 To switch to worktree, run:\n")
        print(f"   cd {selected['path']}\n")
```

### Script: clean_worktrees.py

```python
#!/usr/bin/env python3
"""Clean up merged/stale worktrees."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "scripts"))

from worktree_manager import list_worktrees, cleanup_worktree

def find_cleanable(worktrees):
    """Find worktrees that can be cleaned up."""
    return [wt for wt in worktrees if wt['status'] in ['merged', 'stale']]

def confirm_cleanup(worktrees):
    """Prompt user to confirm cleanup."""
    if not worktrees:
        print("No worktrees to clean up")
        return []

    print(f"🧹 Found {len(worktrees)} worktrees ready for cleanup:\n")
    for wt in worktrees:
        print(f"  #{wt['issue_number']} - {wt['issue_title']}")

    response = input("\nRemove these worktrees? [y/N]: ")
    return worktrees if response.lower() == 'y' else []

if __name__ == "__main__":
    all_worktrees = list_worktrees()
    cleanable = find_cleanable(all_worktrees)
    to_remove = confirm_cleanup(cleanable)

    for wt in to_remove:
        cleanup_worktree(wt['issue_number'])
        print(f"✅ Removed worktree for issue #{wt['issue_number']}")
```

## Error Handling

**No worktrees found**:
```
📋 No worktrees found

Create one with: /start-issue <number>
```

**Invalid selection**:
```
❌ Invalid selection

Please enter a number between 1 and 4, or 'q' to quit
```

**Cleanup failed**:
```
❌ Failed to remove worktree for issue #101

Reasons:
  - Directory has uncommitted changes
  - Directory is currently in use

Try:
  1. Commit or stash changes
  2. Close any programs using the directory
  3. Run: /worktree clean --force
```

## Examples

### Example 1: List and Switch

**User says:**
> "show me all worktrees"

**Output**:
```
📋 Git Worktrees:
[table showing 3 worktrees]

Select worktree to switch (1-3) or 'q' to quit: 2

📍 To switch to worktree #2 (Issue #101), run:
   cd ~/dev/ai-dev-101-remove-taskcreate-pattern
```

### Example 2: Clean Merged Worktrees

**User says:**
> "clean up worktrees"

**Output**:
```
🧹 Found 1 worktree ready for cleanup:
  #110 - Fix skills compliance (merged 2 days ago)

Remove these worktrees? [y/N]: y
✅ Removed worktree for issue #110
```

### Example 3: Quick Switch

**User says:**
> "switch to issue 101 worktree"

**Output**:
```
📍 To switch to Issue #101 worktree, run:
   cd ~/dev/ai-dev-101-remove-taskcreate-pattern
```

## Integration

**Created by**: `/start-issue` - Automatically creates worktree metadata
**Used by**: Developers working on multiple issues in parallel
**Cleaned by**: `/finish-issue` - Optionally removes worktree after merge

**Workflow**:
```
/start-issue #101    → Creates worktree #1
/start-issue #102    → Creates worktree #2
/worktree            → List and switch between #1 and #2
/finish-issue #101   → Removes worktree #1
/worktree clean      → Cleanup remaining merged worktrees
```

## Best Practices

1. **List regularly** - Use `/worktree` to see all active work
2. **Clean after merge** - Remove worktrees once PR is merged
3. **Switch via number** - Faster than typing full path
4. **Prune periodically** - Clean up orphaned references

## Related Skills

- **/start-issue** - Creates worktrees for new issues
- **/finish-issue** - Cleans up worktrees after completion
- **/status** - Shows active work across all worktrees

---

**Version:** 1.0.0
**Last Updated:** 2026-03-10
**Changelog:**
- v1.0.0 (2026-03-10): Initial release - git worktree management for parallel development
**Pattern:** Tool-Reference (guides Claude through workflow)
**Compliance:** ADR-001 Section 4 ✅
