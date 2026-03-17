---
name: plan-list
description: List and filter plan documents. Use when exploring plans, checking
  status, finding plans by module, or reviewing plan health.
allowed-tools: Read, Bash
agent: design-doc-agent
---

# Plan Listing

Lists and filters plan documents with flexible filtering and output options.

## Overview

This skill lists plan documents by:

1. Reading all plan files from `.claude/plans/`
2. Parsing frontmatter to extract metadata
3. Applying filters (status, module, owner)
4. Sorting results by specified field
5. Formatting output (summary, detailed, timeline)
6. Displaying results with color-coded status

## Quick Start

**List all plans:**

```bash
/plan-list
```

**List by status:**

```bash
/plan-list --status=in-progress
```

**List by module:**

```bash
/plan-list --module=effect-type-registry
```

**Detailed view:**

```bash
/plan-list --format=detailed
```

## How It Works

### 1. Parse Parameters

- `--status`: Filter by status (ready, in-progress, blocked, completed,
  abandoned)
- `--module`: Filter by module name
- `--owner`: Filter by plan owner
- `--format`: Output format (summary, detailed, timeline) [default: summary]
- `--sort`: Sort field (created, updated, progress, status) [default: updated]
- `--order`: Sort order (asc, desc) [default: desc]
- `--include-archived`: Include archived plans from `_archive/`
- `--stale`: Show only stale plans (updated > 30 days)

### 2. Read Plan Directory

Scan for plan files:

- Read `.claude/plans/*.md`
- Optionally read `.claude/plans/_archive/*.md`
- Exclude template files (`_templates/`)
- Report error if directory doesn't exist

### 3. Parse Plan Metadata

For each plan file:

- Extract YAML frontmatter
- Parse required fields: name, title, status, progress
- Parse optional fields: modules, owner, created, updated, started
- Calculate derived fields: age, stale status

### 4. Apply Filters

Filter plans based on parameters:

**Status Filter:**

- Single status: `--status=in-progress`
- Multiple statuses: `--status=ready,in-progress`
- Comma-separated list

**Module Filter:**

- Single module: `--module=effect-type-registry`
- Plans with module in `modules` array

**Owner Filter:**

- Single owner: `--owner=@spencerbeggs`
- Plans with matching `owner` field

**Stale Filter:**

- `--stale`: Show plans with `updated` > 30 days ago
- Configurable threshold in design.config.json

### 5. Sort Results

Sort plans by specified field:

**Sort Fields:**

- `created`: Plan creation date
- `updated`: Last update date (default)
- `progress`: Progress percentage
- `status`: Status value (alphabetical)
- `name`: Plan name (alphabetical)

**Sort Order:**

- `desc`: Newest/highest first (default)
- `asc`: Oldest/lowest first

### 6. Format Output

Three output formats:

**Summary (default):**

```text
Plans (5 active, 2 completed):

Active Plans:
  📋 cache-optimization-plan [in-progress, 45%]
     Updated: 2 days ago
     Module: effect-type-registry

  📋 observability-phase-2 [ready, 0%]
     Updated: 1 day ago
     Module: effect-type-registry

Completed Plans:
  ✅ design-linking-phase-1 [completed, 100%]
     Completed: 3 days ago
```

**Detailed:**

```text
Plan: cache-optimization-plan
  Title: Cache Optimization Implementation
  Status: in-progress (45%)
  Module: effect-type-registry
  Created: 2026-01-10 (8 days ago)
  Updated: 2026-01-16 (2 days ago)
  Started: 2026-01-11 (7 days ago)
  Owner: @spencerbeggs
  Estimated: 2-3 weeks
  Implements: effect-type-registry/cache-optimization.md

  Phases:
    ✓ Phase 1: Initial Implementation (100%)
    → Phase 2: Performance Testing (30%)
    ○ Phase 3: Documentation (0%)
```

**Timeline:**

```text
Timeline View (sorted by started date):

Jan 10 ━━━━━━━━━━●━━━━━━━━━━ Jan 31
       cache-optimization-plan [45%]
         ├─ Phase 1 (done)
         ├─ Phase 2 (active)
         └─ Phase 3 (pending)

Jan 12 ━━━━━━━━━━━━━━━━━●━━━ Feb 05
       observability-phase-2 [20%]
         └─ Phase 1 (active)
```

### 7. Generate Report

Output listing results with:

- Summary statistics (total, active, completed)
- Filtered plan list with color-coded status
- Optional health warnings (stale plans)
- Next action suggestions

## Usage Patterns

### List All Plans

```bash
/plan-list
```

Shows all plans sorted by last update.

### Filter by Status

```bash
# Active plans only
/plan-list --status=in-progress

# Multiple statuses
/plan-list --status=ready,in-progress
```

### Filter by Module

```bash
/plan-list --module=effect-type-registry
```

Shows only plans for specific module.

### Show Stale Plans

```bash
/plan-list --stale
```

Shows plans not updated in 30+ days.

### Detailed View

```bash
/plan-list --format=detailed --status=in-progress
```

Shows full metadata for filtered plans.

### Timeline View

```bash
/plan-list --format=timeline --status=in-progress
```

Shows Gantt-style timeline of active plans.

### Include Archived Plans

```bash
/plan-list --include-archived
```

Shows both active and archived plans.

### Sort by Progress

```bash
/plan-list --sort=progress --order=asc
```

Shows plans sorted by progress (lowest first).

### Sort by Creation Date

```bash
/plan-list --sort=created --order=desc
```

Shows newest plans first.

## Implementation Steps

1. **Parse arguments** from user input (filters, format, sort)
2. **Read config** from `.claude/design/design.config.json`
3. **Scan plan directory** for `.md` files
4. **Parse each plan** to extract frontmatter
5. **Apply filters** based on status, module, owner, stale
6. **Sort results** by specified field and order
7. **Calculate statistics** (total, active, completed, stale)
8. **Format output** based on format parameter
9. **Generate report** with color-coded status
10. **Return exit code** (0 = success)

## Output Format Details

### Status Icons

- `📋` - Active plan (ready, in-progress, blocked)
- `✅` - Completed plan
- `❌` - Abandoned plan
- `⚠️` - Stale plan (warning)

### Status Colors

- `ready` - Blue
- `in-progress` - Yellow
- `blocked` - Red
- `completed` - Green
- `abandoned` - Gray

### Age Formatting

- "1 day ago"
- "5 days ago"
- "2 weeks ago"
- "3 months ago"

### Progress Bar (detailed format)

```text
Progress: [████████░░] 45%
```

## Error Messages

### No Plans Found

```text
No plans found matching filters

Filters:
  Status: in-progress
  Module: effect-type-registry

Suggestions:
  1. Remove filters: /plan-list
  2. Create new plan: /plan-create "My Feature"
  3. Check archived plans: /plan-list --include-archived
```

### Invalid Status

```text
✗ Invalid status: {status}

Valid statuses:
  - ready
  - in-progress
  - blocked
  - completed
  - abandoned

Fix: Use --status={valid-status}
```

### Invalid Module

```text
✗ Module not found: {module}

Available modules:
  - effect-type-registry
  - rspress-plugin-api-extractor
  - design-doc-system

Fix: Use --module={valid-module} or omit --module flag
```

### Plans Directory Missing

```text
✗ Plans directory not found: .claude/plans/

The plans directory doesn't exist yet.

Create it with:
  mkdir -p .claude/plans

Or create your first plan:
  /plan-create "My First Plan"
```

## Statistics

The summary format includes statistics:

```text
Plans: 12 total (7 active, 4 completed, 1 abandoned)

Status Breakdown:
  Ready:        3 plans
  In Progress:  4 plans
  Blocked:      0 plans
  Completed:    4 plans
  Abandoned:    1 plan

Health:
  Stale:        2 plans (updated > 30 days)
  On Schedule:  5 plans
  Behind:       2 plans
```

## Examples

See [examples.md](./examples.md) for detailed usage examples.

## Related Skills

- `plan-validate` - Validate plan structure
- `plan-create` - Create new plans
- `plan-update` - Update plan status/progress
- `plan-explore` - Comprehensive plan exploration (Phase 2)
- `design-list` - List design docs
