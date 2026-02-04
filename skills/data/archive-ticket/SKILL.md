---
name: archive-ticket
description: Archive completed tickets by moving them to .archived/
---

# Archive Ticket

## Purpose

This skill provides instructions for archiving tickets when their derived phases complete. Archiving moves a ticket from `.ushabti/tickets/` to `.ushabti/tickets/.archived/`, making it invisible to agents.

## When to Archive

Archive a ticket when:

1. A phase was derived from the ticket (phase.md contains `ticket: TNNNN` metadata)
2. The phase has been reviewed and approved by Overseer
3. Overseer is declaring the phase complete (status: complete)

Archival is part of Overseer's phase completion workflow.

## Archive Procedure

### Step 1: Identify the Ticket

When completing a phase:

1. Read the phase.md file
2. Look for a `ticket` metadata field
3. Extract the ticket ID (e.g., `ticket: T0042` means ticket ID is T0042)

If no `ticket` field exists, skip archival (the phase was not derived from a ticket).

### Step 2: Locate the Ticket File

The ticket file is in `.ushabti/tickets/` with a filename matching `TNNNN-*.yaml`

For ticket ID T0042, the filename might be `T0042-improve-error-messages.yaml`

Use glob pattern to find the exact filename:
```bash
ls .ushabti/tickets/T0042-*.yaml
```

### Step 3: Ensure Archive Directory Exists

Ensure the archive directory exists by running:

```bash
mkdir -p .ushabti/tickets/.archived
```

This is idempotent and handles cases where the directory was not created during bootstrap.

### Step 4: Move to Archive

Move the ticket file from `.ushabti/tickets/` to `.ushabti/tickets/.archived/`

```bash
mv .ushabti/tickets/T0042-improve-error-messages.yaml .ushabti/tickets/.archived/
```

The filename remains unchanged, only the location changes.

### Step 5: Verify

Confirm the ticket file:
- No longer exists in `.ushabti/tickets/`
- Now exists in `.ushabti/tickets/.archived/`

### Step 6: Log the Action

In review.md, document the archival:

```markdown
## Completion Actions

- Archived ticket T0042 (improve-error-messages) as phase is complete
```

## Filesystem Operations

### Command Template

```bash
# Ensure archive directory exists
mkdir -p .ushabti/tickets/.archived

# Find the ticket file
TICKET_FILE=$(ls .ushabti/tickets/TNNNN-*.yaml)

# Move to archive
mv "$TICKET_FILE" .ushabti/tickets/.archived/

# Verify
ls .ushabti/tickets/.archived/TNNNN-*.yaml
```

Replace `TNNNN` with the actual ticket ID from phase.md.

## Example: Complete Archival Workflow

Phase file (`.ushabti/phases/0012-ticketing-system/phase.md`) contains:

```markdown
# Phase 0012: Ticketing System

ticket: T0008

## Intent
...
```

Overseer completes the phase and archives the ticket:

```bash
# Ensure archive directory exists
mkdir -p .ushabti/tickets/.archived

# Find ticket T0008
TICKET_FILE=$(ls .ushabti/tickets/T0008-*.yaml)
echo "Found: $TICKET_FILE"
# Output: .ushabti/tickets/T0008-add-ticketing-system.yaml

# Move to archive
mv .ushabti/tickets/T0008-add-ticketing-system.yaml .ushabti/tickets/.archived/

# Verify
ls .ushabti/tickets/.archived/T0008-*.yaml
# Output: .ushabti/tickets/.archived/T0008-add-ticketing-system.yaml
```

Overseer logs in review.md:

```markdown
## Completion Actions

- Archived ticket T0008 (add-ticketing-system) as phase is complete
```

## Notes

- Only Overseer archives tickets, as part of phase completion
- Archived tickets are invisible to agents (agents only read `.ushabti/tickets/`, not `.archived/`)
- If a ticket file is missing, log the issue but don't fail the phase completion
- Archival is a one-way operation; archived tickets are not meant to be restored
- The ticket ID and filename do not change, only the directory location
