---
name: list-rfcs
description: List all RFCs with status, progress, and metadata
argument-hint: [--status <status>] [--all]
---

# list-rfcs

**Category**: Technical Architecture

## Usage

```bash
/list-rfcs [options]
```

## Options

| Option | Description |
|--------|-------------|
| `--status <status>` | Filter by status (DRAFT, REVIEW, APPROVED, IN_PROGRESS, COMPLETED) |
| `--all` | Include archived RFCs |
| `--author <name>` | Filter by author |
| `--format table|list` | Output format (default: table) |

## Execution Instructions

When this command is run, Claude Code should:

1. **Scan RFC Directories**
   ```
   rfcs/
   ├── draft/           → DRAFT
   ├── review/          → REVIEW
   ├── approved/        → APPROVED
   │   └── in-progress/ → IN_PROGRESS
   ├── completed/       → COMPLETED
   └── archive/         → (only with --all)
   ```

2. **Extract Metadata from Each RFC**
   - RFC ID (from filename or frontmatter)
   - Title
   - Status
   - Author
   - Created date
   - Last updated date
   - Reviewers and their status

3. **Apply Filters** (if specified)
   - Filter by status
   - Filter by author
   - Exclude archive unless `--all`

4. **Display Results**

### Table Format (default)

```
RFC Management Summary
======================

Active RFCs: 5 | In Review: 2 | Completed: 12

| RFC ID    | Title                      | Status      | Author    | Updated    |
|-----------|----------------------------|-------------|-----------|------------|
| RFC-0045  | API Gateway Selection      | REVIEW      | Jane Doe  | 2025-12-05 |
| RFC-0044  | Cache Strategy             | IN_PROGRESS | John Doe  | 2025-12-04 |
| RFC-0043  | Auth Redesign              | APPROVED    | Jane Doe  | 2025-12-01 |
| RFC-0042  | Database Migration         | DRAFT       | Bob Smith | 2025-11-28 |
| RFC-0041  | Logging Architecture       | DRAFT       | Jane Doe  | 2025-11-25 |

Use '/rfc-status RFC-XXXX' to see details or update status.
```

### List Format

```
RFC-0045: API Gateway Selection
  Status: REVIEW
  Author: Jane Doe
  Created: 2025-12-01
  Updated: 2025-12-05
  Reviewers: Alice (approved), Bob (pending)
  Location: rfcs/review/RFC-0045-api-gateway-selection.md

RFC-0044: Cache Strategy
  Status: IN_PROGRESS
  Author: John Doe
  ...
```

## Status Summary

Always show a summary at the top:

```
RFC Status Summary
==================
DRAFT:       3
REVIEW:      2
APPROVED:    1
IN_PROGRESS: 2
COMPLETED:   12
ARCHIVED:    8 (use --all to include)
```

## Sorting

Default sort order:
1. REVIEW (needs attention)
2. IN_PROGRESS
3. APPROVED
4. DRAFT
5. COMPLETED

Within each status, sort by last_updated (newest first).

## Example Usage

```bash
# List all active RFCs
/list-rfcs

# List only RFCs in review
/list-rfcs --status REVIEW

# List all including archived
/list-rfcs --all

# List RFCs by specific author
/list-rfcs --author "Jane Doe"
```

## Empty State

If no RFCs exist:

```
No RFCs found.

To create a new RFC:
  /create-rfc <title>

RFC documentation:
  See plugins/devops-data/skills/rfc-specification/SKILL.md
```

## Error Handling

- If `rfcs/` directory doesn't exist, show empty state message
- If RFC file has invalid frontmatter, show warning but continue
- Handle missing metadata gracefully (show "N/A")
