---
name: list-tech-specs
description: List all Technical Specifications with status and metadata
argument-hint: [--status <status>] [--all]
---

# list-tech-specs

**Category**: Technical Architecture

## Usage

```bash
/list-tech-specs [options]
```

## Options

| Option | Description |
|--------|-------------|
| `--status <status>` | Filter by status (DRAFT, APPROVED, REFERENCE) |
| `--all` | Include archived specs |
| `--rfc <RFC-XXXX>` | Filter by linked RFC |
| `--format table|list` | Output format (default: table) |

## Execution Instructions

When this command is run, Claude Code should:

1. **Scan Tech Spec Directories**
   ```
   tech-specs/
   ├── draft/      → DRAFT
   ├── approved/   → APPROVED
   ├── reference/  → REFERENCE
   └── archive/    → (only with --all)
   ```

2. **Extract Metadata from Each Spec**
   - Tech Spec ID (from filename or frontmatter)
   - Title
   - Status
   - Author
   - Linked RFC (if any)
   - Created date
   - Last updated date

3. **Apply Filters** (if specified)
   - Filter by status
   - Filter by linked RFC
   - Exclude archive unless `--all`

4. **Display Results**

### Table Format (default)

```
Tech Spec Summary
=================

Active: 8 | Reference: 15 | Archived: 5

| Spec ID   | Title                      | Status    | RFC Link  | Updated    |
|-----------|----------------------------|-----------|-----------|------------|
| TS-0045   | Payment Gateway API        | APPROVED  | RFC-0042  | 2025-12-05 |
| TS-0044   | User Auth Implementation   | DRAFT     | -         | 2025-12-04 |
| TS-0043   | Cache Layer Design         | REFERENCE | RFC-0038  | 2025-12-01 |
| TS-0042   | Search Service             | APPROVED  | -         | 2025-11-28 |

Use '/tech-spec-status TS-XXXX' to see details or update status.
```

### List Format

```
TS-0045: Payment Gateway API
  Status: APPROVED
  Author: Jane Doe
  RFC: RFC-0042
  Created: 2025-12-01
  Updated: 2025-12-05
  Location: tech-specs/approved/TS-0045-payment-gateway-api.md

TS-0044: User Auth Implementation
  Status: DRAFT
  Author: John Doe
  RFC: -
  ...
```

## Status Summary

Always show a summary at the top:

```
Tech Spec Status Summary
========================
DRAFT:     3
APPROVED:  5
REFERENCE: 15
ARCHIVED:  5 (use --all to include)
```

## Sorting

Default sort order:
1. DRAFT (work in progress)
2. APPROVED (ready to implement)
3. REFERENCE (implemented)

Within each status, sort by last_updated (newest first).

## Example Usage

```bash
# List all active tech specs
/list-tech-specs

# List only specs in draft
/list-tech-specs --status DRAFT

# List specs linked to specific RFC
/list-tech-specs --rfc RFC-0042

# List all including archived
/list-tech-specs --all
```

## Empty State

If no Tech Specs exist:

```
No Technical Specifications found.

To create a new Tech Spec:
  /create-tech-spec <title>

Tech Spec documentation:
  See plugins/devops-data/skills/technical-specification/SKILL.md
```

## Error Handling

- If `tech-specs/` directory doesn't exist, show empty state message
- If spec file has invalid frontmatter, show warning but continue
- Handle missing metadata gracefully (show "N/A")
