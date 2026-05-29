---
name: rfc-status
description: Show RFC details or update RFC status through lifecycle
argument-hint: <rfc-id> [--set <status>]
---

# rfc-status

**Category**: Technical Architecture

## Usage

```bash
/rfc-status <rfc-id> [options]
```

## Arguments

- `<rfc-id>`: Required - RFC identifier (e.g., RFC-0042 or just 0042)

## Options

| Option | Description |
|--------|-------------|
| `--set <status>` | Transition to new status |
| `--reviewer <name>` | Add or update reviewer |
| `--comment <text>` | Add status change comment |

## Valid Statuses

- `DRAFT` - Initial writing
- `REVIEW` - Open for feedback
- `APPROVED` - Decision made
- `IN_PROGRESS` - Implementation started
- `COMPLETED` - Implementation finished
- `REJECTED` - Proposal declined
- `ABANDONED` - Author withdrew
- `SUPERSEDED` - Replaced by newer RFC

## Execution Instructions

### View Status (no --set)

When viewing an RFC:

1. **Find the RFC file**
   - Search all `rfcs/` subdirectories
   - Match by RFC ID in filename or frontmatter

2. **Display RFC Details**

```
RFC-0042: Database Migration Strategy
======================================

Status:      REVIEW
Author:      Jane Doe
Created:     2025-12-01
Updated:     2025-12-05
Location:    rfcs/review/RFC-0042-database-migration-strategy.md

Reviewers:
  - Alice Chen: approved (2025-12-04)
  - Bob Smith: pending
  - Carol Wu: in-progress

Overview:
  [First 2-3 sentences of the Overview section]

Valid Transitions:
  → APPROVED  (requires all reviewers approved)
  → DRAFT     (needs revision)
  → REJECTED  (proposal declined)

Commands:
  /rfc-status RFC-0042 --set APPROVED
  /rfc-status RFC-0042 --reviewer "Bob Smith:approved"
```

### Update Status (with --set)

When updating status:

1. **Validate Transition**

   Valid transitions:
   | From | To |
   |------|-----|
   | DRAFT | REVIEW, ABANDONED |
   | REVIEW | APPROVED, REJECTED, DRAFT |
   | APPROVED | IN_PROGRESS, SUPERSEDED |
   | IN_PROGRESS | COMPLETED, SUPERSEDED |
   | Any | SUPERSEDED (with link to new RFC) |

2. **Perform Pre-transition Checks**

   For REVIEW → APPROVED:
   - Warn if not all reviewers approved
   - Require at least one approved reviewer

   For APPROVED → IN_PROGRESS:
   - Verify Technical Design section exists
   - Verify Implementation Plan section exists

   For IN_PROGRESS → COMPLETED:
   - Prompt for completion notes
   - Ask about lessons learned

3. **Update RFC File**
   - Update `status` in frontmatter
   - Update `last_updated` to today
   - Add `decision_date` if transitioning to APPROVED
   - Add `archive_date` if archiving

4. **Move File to Correct Directory**

   | Status | Directory |
   |--------|-----------|
   | DRAFT | `rfcs/draft/` |
   | REVIEW | `rfcs/review/` |
   | APPROVED | `rfcs/approved/` |
   | IN_PROGRESS | `rfcs/approved/in-progress/` |
   | COMPLETED | `rfcs/completed/` |
   | REJECTED | `rfcs/archive/YYYY/rejected/` |
   | ABANDONED | `rfcs/archive/YYYY/abandoned/` |
   | SUPERSEDED | `rfcs/archive/YYYY/superseded/` |

5. **Confirm Update**

```
RFC-0042 status updated: REVIEW → APPROVED

Updated:
  - Status: APPROVED
  - Decision Date: 2025-12-06
  - Location: rfcs/approved/RFC-0042-database-migration-strategy.md

Next steps:
  1. Create implementation tasks
  2. When starting work: /rfc-status RFC-0042 --set IN_PROGRESS
```

## Reviewer Management

Update reviewer status:

```bash
/rfc-status RFC-0042 --reviewer "Bob Smith:approved"
/rfc-status RFC-0042 --reviewer "Carol Wu:declined"
```

Reviewer statuses:
- `pending` - Not yet reviewed
- `in-progress` - Currently reviewing
- `approved` - Approved the RFC
- `declined` - Requested changes or rejected

## Example Usage

```bash
# View RFC details
/rfc-status RFC-0042

# Submit for review
/rfc-status RFC-0042 --set REVIEW

# Approve RFC
/rfc-status RFC-0042 --set APPROVED --comment "All concerns addressed"

# Start implementation
/rfc-status RFC-0042 --set IN_PROGRESS

# Mark complete
/rfc-status RFC-0042 --set COMPLETED

# Mark as superseded
/rfc-status RFC-0042 --set SUPERSEDED --comment "Replaced by RFC-0050"
```

## Error Handling

- If RFC not found, show search suggestions
- If invalid transition, show valid options
- If file move fails, show manual instructions
- Preserve git history when moving files (use `git mv`)

## Integration

When transitioning to IN_PROGRESS:
- Suggest creating tasks with `/generate-tasks` if PRD linked
- Remind to update related PRD status

When transitioning to COMPLETED:
- Prompt for implementation summary
- Ask about deviations from original plan
