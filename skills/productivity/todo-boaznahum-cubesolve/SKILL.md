---
name: todo
user_invocable: true
description: |
  Manage and track all TODOs from code comments and todo files. Provides quick reports
  of open tasks, scans for untracked TODOs, and integrates with GitHub Issues.
  Triggered by "/todo", "show todos", "list todos", or "todo status".
---

# Todo Management Skill

This skill consolidates all TODOs from two sources:
1. **Code comments** - `TODO:` and `CLAUDE:` markers in src/, tests/, docs/
2. **Todo files** - Files with "todo" in the filename

## Quick Start - Run Scan Script First

**ALWAYS run this script first to save tokens:**

```bash
python .claude/skills/todo/todo_scan.py
```

This outputs a complete report showing:
- Tracked vs untracked code TODOs
- Todo files and their status
- GitHub Issues with `todo` label

## Quick Report (Default Action)

When user runs `/todo`, provide a quick summary:

1. Run the scan script
2. Query GitHub Issues: `gh issue list --label todo --state open --json number,title,labels`
3. Present combined report

**Output format:**

```
=== TODO Quick Report ===

Open Issues: X (Y high, Z medium, W low)
In Progress: N
Untracked in code: M

| #   | Pri  | Category | Title                    | Status      |
|-----|------|----------|--------------------------|-------------|
| #45 | HIGH | bug      | GUI Animation Bug        | in-progress |
| #32 | MED  | arch     | Circular imports         | analyzed    |
...

Untracked Code TODOs: M
  src/file.py:123 - TODO: description
  ...

Run `/todo scan` for full scan
Run `/todo track` to create issues for untracked items
```

## Commands

### `/todo help`
Show quick reference of available commands:

```
/todo              Quick report (open issues, priorities, in-progress)
/todo scan         Full codebase scan for TODOs
/todo sync         Find inconsistencies between code and GitHub
/todo search       Search issues by keyword or label
/todo track        Create GitHub Issues for untracked TODOs
/todo analyze #id  Analyze TODO and update its GitHub Issue
/todo start #id    Mark issue as in-progress
/todo done #id     Close the issue
/todo reject #id   Close with wontfix label
```

### `/todo` or `/todo report`
Quick report from script output and GitHub Issues.

### `/todo scan`
Full scan with detailed output:
```bash
python .claude/skills/todo/todo_scan.py
```

### `/todo sync`
Find inconsistencies between code/files and GitHub Issues:
```bash
python .claude/skills/todo/todo_scan.py --sync
```

**Checks performed:**

**Code TODOs:**
1. **Missing in GitHub** - Code TODO has `[#X]` but issue doesn't exist or lacks `todo` label
2. **Missing in Code** - GitHub Issue with `todo:code` label has no matching code TODO
3. **Stale TODOs** - Code TODO references a CLOSED issue (should be removed)

**File Entries:**
4. **Missing in GitHub** - File entry references issue that doesn't exist or lacks `todo` label
5. **Missing in File** - GitHub Issue with `todo:file` label has no matching file entry
6. **Stale Entries** - File entry references a CLOSED issue (should be removed)
7. **Status Mismatch** - File says `in-progress` but GitHub lacks label, or vice versa

**Output format:**
```
=== SYNC REPORT ===

Code: Missing in GitHub (1):
  src/file.py:42 - [#999] issue does not exist

Code: Stale TODOs (1):
  src/old.py:20 - [#30] issue is CLOSED - remove this TODO

File: Status Mismatch (2):
  todo/todo_open.md:5 - [#16] file says 'investigating' but GitHub has 'in-progress' label
  todo/todo_open.md:15 - [#23] file says 'in-progress' but GitHub lacks label

Synced: 13 code TODOs, 25 file entries
```

**Interactive Resolution:**

When inconsistencies are found, ask the user how to resolve each one:

1. **Status Mismatch** - Ask: "Update file to match GitHub, or update GitHub to match file?"
   - Option A: Update file entry status to match GitHub label
   - Option B: Add/remove `in-progress` label on GitHub to match file
   - Option C: Skip (do nothing)

2. **Stale TODOs/Entries** - Ask: "Issue is closed. Remove the TODO/entry?"
   - Option A: Remove the code comment or file entry
   - Option B: Skip (keep it)

3. **Missing in GitHub** - Ask: "Create GitHub Issue for this TODO?"
   - Option A: Create issue with `todo` label
   - Option B: Skip

4. **Missing in Code/File** - Ask: "GitHub Issue has label but no local reference. What to do?"
   - Option A: Remove the `todo:code` or `todo:file` label from GitHub
   - Option B: Skip (leave as is)

**Example interaction:**
```
Found 1 inconsistency:

[1] Status Mismatch: todo/todo_open.md:5
    Issue #16: file says 'investigating' but GitHub has 'in-progress' label

    How to resolve?
    A) Update file to 'in-progress'
    B) Remove 'in-progress' label from GitHub
    C) Skip
```

### `/todo search [query] [--label <label>]`
Search GitHub Issues by keyword and/or label filter.

**Usage:**
```bash
/todo search animation          # Search for "animation" in title/body
/todo search --label bug        # Filter by label
/todo search gui --label high   # Combined: keyword + label
/todo search --label in-progress  # Find all in-progress issues
```

**Implementation:**
```bash
# Keyword search (searches title and body)
gh issue list --label todo --search "animation" --state open --json number,title,labels,state

# Label filter (can use partial match)
gh issue list --label todo --label "priority:high" --state open --json number,title,labels,state

# Combined
gh issue list --label todo --label bug --search "animation" --state open --json number,title,labels,state

# Include closed issues
gh issue list --label todo --search "animation" --state all --json number,title,labels,state
```

**Output format:**
```
=== Search Results: "animation" ===

| #   | State  | Labels                  | Title                    |
|-----|--------|-------------------------|--------------------------|
| #45 | open   | bug, priority:high      | GUI Animation Bug        |
| #12 | closed | enhancement             | Animation speed control  |

Found 2 issues. Use `/todo start #id`, `/todo done #id`, or `/todo analyze #id` to operate on results.
```

**Common label filters:**
- `--label bug` - Bug issues
- `--label enhancement` - Feature requests
- `--label priority:high` / `priority:medium` / `priority:low` - By priority
- `--label in-progress` - Currently being worked on
- `--label analyzed` - Already analyzed by Claude
- `--label todo:code` - From code comments
- `--label todo:file` - From todo files

**Options:**
- `--all` - Include closed issues (default: open only)
- `--limit N` - Limit results (default: 30)

### `/todo track`
For each untracked code TODO:
1. Assign next available ID (check existing TC# numbers)
2. Create GitHub Issue with `todo` and `todo:code` labels
3. Update code comment with issue number: `# TODO [#123]: text`

### `/todo analyze [#id]`
Read the code context around a TODO, update the GitHub Issue description with analysis, and add `analyzed` label.

### `/todo start #id`
Add `in-progress` label to the GitHub Issue.

### `/todo done #id`
Close the GitHub Issue. Optionally remove or update the code comment.

### `/todo reject #id [reason]`
Add `wontfix` label and close the issue with reason.

## ID Schema

### Code Comments
Format: `# TODO [ID]: description`

Examples:
- `# TODO [TC1]: Move single step mode into operator`
- `# TODO [#45]: Fix animation bug`
- `# CLAUDE [#123]: Review this logic`

### GitHub Labels

| Label | Purpose |
|-------|---------|
| `todo` | All tracked TODOs |
| `todo:code` | From code comments |
| `todo:file` | From todo files |
| `analyzed` | Claude has reviewed and understands |
| `in-progress` | Currently being worked on |
| `priority:high` | High priority |
| `priority:medium` | Medium priority |
| `priority:low` | Low priority |

## Status Flow

```
new → analyzed → in_progress → completed
                     │
                     └──────────▶ rejected (wontfix)
```

## Todo Files

Files with "todo" in filename are tracked:
- Should be moved to `todo/` folder
- Files with "new entries" section need processing
- Each entry should become a GitHub Issue

### Processing New Entries

1. Find files with `has_new_entries: true` in scan output
2. Read the new entries section
3. Create GitHub Issues for each entry
4. Update file to mark entries as processed

## Token-Saving Strategy

1. **Always run Python script first** - It does the file scanning
2. **Use --json flag** for programmatic parsing: `python .claude/skills/todo/todo_scan.py --json`
3. **Only read specific files** when analyzing individual TODOs
4. **Cache GitHub queries** - The script already queries once

## Migration Notes

Existing tracked items use these ID formats:
- `TC1-TC6` - Code TODOs
- `B#, G#, A#, Q#, S#, D#` - Categorized tasks in todo_open.md

These will be migrated to GitHub Issues when `/todo track` is run.

## Important

- **NEVER create issues without user approval** - Show what will be created first
- **Ask before modifying code** - Confirm before updating TODO comments with IDs
- **Preserve existing IDs** - Don't reassign TC1-TC6 to new numbers