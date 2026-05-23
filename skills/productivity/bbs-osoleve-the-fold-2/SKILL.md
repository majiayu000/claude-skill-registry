---
name: bbs
description: Manage issues with The Fold's CAS-native BBS (Bulletin Board System). Use for creating, updating, searching, and tracking issues. Invoke when the user wants to create tickets, find work, check issue status, or manage dependencies.
allowed-tools: Bash(./fold:*), Read, Grep, Glob
---

# BBS (Bulletin Board System) Skill

## Overview

BBS is The Fold's CAS-native issue tracker built on block primitives. All issues are content-addressed, with full history preserved in the store.

Use BBS for:
- Creating and tracking issues (bugs, features, tasks, epics)
- Finding available work (unblocked issues)
- Managing dependencies between issues
- Reviewing issue history and status

## Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `bbs-list` | List issues | `(bbs-list)` |
| `bbs-show` | View issue details | `(bbs-show 'fold-001)` |
| `bbs-create` | Create new issue | `(bbs-create "Title")` |
| `bbs-update` | Update issue fields | `(bbs-update 'fold-001 'status 'in_progress)` |
| `bbs-close` | Close an issue | `(bbs-close 'fold-001)` |
| `bbs-find` | Search issue titles | `(bbs-find "query")` |
| `bbs-search` | Search titles + descriptions | `(bbs-search "query")` |
| `bbs-ready` | Show unblocked work | `(bbs-ready)` |
| `bbs-blocked` | Show blocked issues | `(bbs-blocked)` |
| `bbs-dep` | Add dependency | `(bbs-dep 'blocker 'blocked)` |
| `bbs-add-blocker` | Add dependency (alias) | `(bbs-add-blocker 'fold-001 'fold-002)` |
| `bbs-list-by-label` | Filter by label | `(bbs-list-by-label 'topology)` |
| `bbs-list-by-type` | Filter by type | `(bbs-list-by-type 'epic)` |
| `bbs-label-report` | Show all labels | `(bbs-label-report)` |
| `bbs-stats` | Database statistics | `(bbs-stats)` |

## Instructions

### Listing Issues

```bash
# List open issues (default)
./fold "(bbs-list)"

# List closed issues
./fold "(bbs-list 'status 'closed)"

# List all issues regardless of status
./fold "(bbs-list 'status 'all)"
```

### Viewing Issues

```bash
# View issue details
./fold "(bbs-show 'fold-001)"

# Search issue titles
./fold "(bbs-find \"auth\")"

# Search titles AND descriptions (more comprehensive)
./fold "(bbs-search \"authentication\")"

# Show unblocked work (ready to start)
./fold "(bbs-ready)"

# Show blocked issues
./fold "(bbs-blocked)"
```

### Filtering Issues

```bash
# Filter by label
./fold "(bbs-list-by-label 'topology)"

# Filter by type (task, bug, feature, epic)
./fold "(bbs-list-by-type 'epic)"

# Get programmatic list of IDs with label (not displayed)
./fold "(bbs-by-label 'refactor)"

# Show all labels in use
./fold "(bbs-label-report)"
```

### Creating Issues

```bash
# Basic create (just title)
./fold "(bbs-create \"Fix authentication bug\")"

# With priority (0=critical, 2=medium, 4=backlog)
./fold "(bbs-create \"Urgent fix\" 'priority 0)"

# With type (task, bug, feature, epic)
./fold "(bbs-create \"Add dark mode\" 'type 'feature)"

# Full creation with all options
./fold "(bbs-create \"Refactor auth\" 'description \"Detailed description here\" 'priority 1 'type 'task 'labels '(core security))"
```

### Updating Issues

```bash
# Update status
./fold "(bbs-update 'fold-001 'status 'in_progress)"

# Change priority
./fold "(bbs-update 'fold-001 'priority 0)"

# Add labels
./fold "(bbs-update 'fold-001 'labels '(urgent core))"

# Update description
./fold "(bbs-update 'fold-001 'description \"New description\")"
```

### Closing Issues

```bash
# Simple close
./fold "(bbs-close 'fold-001)"

# Close with reason
./fold "(bbs-close 'fold-001 'reason \"Fixed in commit abc123\")"
```

### Managing Dependencies

```bash
# fold-001 blocks fold-002 (fold-002 depends on fold-001)
./fold "(bbs-dep 'fold-001 'fold-002)"

# What blocks this issue?
./fold "(bbs-blockers 'fold-002)"

# What does this issue block?
./fold "(bbs-blocking 'fold-001)"

# All unblocked open issues (ready for work)
./fold "(bbs-ready)"
```

### History & Statistics

```bash
# Show version history for an issue
./fold "(bbs-history 'fold-001)"

# Database statistics
./fold "(bbs-stats)"
```

## Field Reference

### Priority Levels

| Priority | Meaning |
|----------|---------|
| 0 | Critical - drop everything |
| 1 | High - do soon |
| 2 | Medium (default) |
| 3 | Low - when time permits |
| 4 | Backlog - someday maybe |

### Issue Types

| Type | Use For |
|------|---------|
| `task` | General work items |
| `bug` | Defects to fix |
| `feature` | New functionality |
| `epic` | Large multi-issue efforts |

### Status Values

| Status | Meaning |
|--------|---------|
| `open` | Not yet started |
| `in_progress` | Currently being worked |
| `closed` | Completed or won't fix |

## Examples

### Example 1: Typical Bug Fix Workflow

```bash
# Find the bug
./fold "(bbs-find \"auth\")"

# Check details
./fold "(bbs-show 'fold-042)"

# Start working on it
./fold "(bbs-update 'fold-042 'status 'in_progress)"

# ... fix the bug ...

# Close it
./fold "(bbs-close 'fold-042 'reason \"Fixed token refresh logic\")"
```

### Example 2: Creating a Feature with Dependencies

```bash
# Create the main feature
./fold "(bbs-create \"Add export functionality\" 'type 'feature 'priority 1)"
# Returns: fold-100

# Create sub-tasks
./fold "(bbs-create \"Design export API\" 'type 'task)"
# Returns: fold-101

./fold "(bbs-create \"Implement CSV export\" 'type 'task)"
# Returns: fold-102

# Set up dependencies (design must complete before implementation)
./fold "(bbs-dep 'fold-101 'fold-102)"

# Main feature blocked by implementation
./fold "(bbs-dep 'fold-102 'fold-100)"
```

### Example 3: Finding Available Work

```bash
# What's ready to work on?
./fold "(bbs-ready)"

# Get stats overview
./fold "(bbs-stats)"

# See what's currently blocked
./fold "(bbs-blocked)"
```

### Example 4: Triaging Issues

```bash
# List all open issues
./fold "(bbs-list)"

# Bump priority on critical item
./fold "(bbs-update 'fold-050 'priority 0)"

# Add labels for categorization
./fold "(bbs-update 'fold-050 'labels '(security urgent))"
```

### Example 5: Finding Related Work by Label

```bash
# See what labels exist
./fold "(bbs-label-report)"

# Find all topology-related issues
./fold "(bbs-list-by-label 'topology)"

# Find all epics to see big-picture work
./fold "(bbs-list-by-type 'epic)"

# Deep search in descriptions
./fold "(bbs-search \"homology\")"
```

## Notes

- **Issue IDs**: Can be symbols (`'fold-001`) or strings (`"fold-001"`)
- **Auto-initialization**: BBS initializes automatically when the REPL starts
- **CAS Storage**: All issues are content-addressed in `.store/`
- **Head files**: Current issue state tracked in `.store/heads/bbs/`
- **Counter**: Issue counter in `.bbs/counter`

## Pipeline Integration

BBS effects are available in agent pipelines (`lattice/pipeline/effects.ss`):

```scheme
(bbs-create "title")              ; Create issue, return ID
(bbs-create-full title desc type priority)
(bbs-update id updates-alist)     ; Update issue fields
(bbs-close id)                    ; Close issue
(bbs-ready)                       ; Get unblocked issues
(bbs-show id)                     ; Get issue details
```

## File Locations

| Path | Purpose |
|------|---------|
| `.store/heads/bbs/` | Issue head files (current hash per issue) |
| `.bbs/counter` | Next issue number |
| `.bbs/deps` | Dependency relationships |
| `boundary/bbs/bbs.ss` | Core BBS implementation |
| `boundary/bbs/ops.ss` | BBS operations |
| `boundary/bbs/index.ss` | BBS indexing |
