---
name: create-ticket
description: Create a new ticket with schema validation
---

# Create Ticket

## Purpose

This skill provides step-by-step instructions for creating a new ticket with proper schema validation. Tickets are YAML files stored in `.ushabti/tickets/` that capture ideas for future work.

## Prerequisites

Before creating a ticket, invoke the `find-next-ticket-number` skill to determine the next ticket ID.

## Required Fields

Every ticket MUST include these fields:

- **id**: Sequential ticket ID in TNNNN format (e.g., T0001)
- **title**: Short, descriptive title (used to generate filename slug)
- **created**: ISO 8601 date in YYYY-MM-DD format (today's date)
- **priority**: Must be exactly one of: `low`, `medium`, `high`
- **context**: Multi-line string explaining why this ticket exists
- **proposed_work**: Multi-line string describing what should be done

## Filename Format

Ticket filenames follow the pattern: `TNNNN-short-description.yaml`

- `TNNNN`: The ticket ID (zero-padded 4 digits)
- `short-description`: Lowercase, hyphenated slug derived from the title
  - Convert title to lowercase
  - Replace spaces with hyphens
  - Remove special characters except hyphens
  - Limit to ~5 words for brevity

Example: Title "Improve error messages" becomes `T0042-improve-error-messages.yaml`

## Creation Procedure

### Step 1: Determine Next ID

Use the `find-next-ticket-number` skill to get the next ticket ID.

### Step 2: Gather Information

Collect the required information:
- Title (brief, descriptive)
- Priority (low, medium, or high)
- Context (why does this ticket exist?)
- Proposed work (what should be done?)

### Step 3: Validate Priority

Ensure priority is exactly one of: `low`, `medium`, `high` (all lowercase).

If priority is not valid, stop and report the error.

### Step 4: Generate Filename

Convert the title to a slug:
- Lowercase all characters
- Replace spaces with hyphens
- Remove special characters (keep letters, numbers, hyphens)
- Limit to approximately 5 words

Combine with ticket ID: `TNNNN-slug.yaml`

### Step 5: Create YAML Content

Construct the YAML file with all required fields:

```yaml
id: T0042
title: Improve error messages
created: 2026-02-01
priority: medium
context: |
  Current error messages are vague and don't help users understand
  what went wrong or how to fix issues. This makes debugging difficult
  and reduces the usability of Ushabti.
proposed_work: |
  - Audit all error messages across agents
  - Replace vague messages with specific, actionable guidance
  - Add error codes for programmatic error handling
  - Update documentation with common errors and solutions
```

### Step 6: Ensure Directory Exists

Ensure the ticket directory exists by running: `mkdir -p .ushabti/tickets`

This is idempotent and handles cases where bootstrap or onboarding didn't create the directory.

### Step 7: Write File

Write the YAML content to `.ushabti/tickets/TNNNN-slug.yaml`

### Step 8: Verify

Confirm the file was written successfully and is valid YAML.

## Validation Checklist

Before considering the ticket created, verify:

- [ ] File exists in `.ushabti/tickets/` (NOT in `.archived/`)
- [ ] Filename matches `TNNNN-slug.yaml` pattern
- [ ] YAML is syntactically valid
- [ ] All six required fields are present
- [ ] `id` field matches the TNNNN in the filename
- [ ] `created` field is today's date in YYYY-MM-DD format
- [ ] `priority` field is exactly `low`, `medium`, or `high`
- [ ] `context` and `proposed_work` fields have meaningful content

## Example: Complete Ticket Creation

```yaml
id: T0001
title: Add search functionality to ticket list
created: 2026-02-01
priority: low
context: |
  As the number of tickets grows, finding specific tickets becomes
  harder. Currently users must read through all ticket files manually.
proposed_work: |
  Create a new skill (search-tickets) that allows filtering tickets by:
  - Title substring match
  - Priority level
  - Date range
  Update list-tickets to optionally use search criteria.
```

Filename: `T0001-add-search-functionality.yaml`

Location: `.ushabti/tickets/T0001-add-search-functionality.yaml`

## Notes

- Tickets are create-only. Once created, they are not edited.
- If a ticket needs correction, create a new ticket and archive the incorrect one.
- Tickets remain in `.ushabti/tickets/` until a derived phase completes, then they are archived.
- Archived tickets are moved to `.ushabti/tickets/.archived/` and become invisible to agents.
