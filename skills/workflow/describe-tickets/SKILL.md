---
name: describe-tickets
description: Ticket system overview, schema, and workflows
---

# Ticket System

## Purpose

Tickets provide a lightweight, file-backed way to capture ideas for future work within the Ushabti repository. They complement the phase-driven workflow by allowing agents and users to record ideas that are out-of-scope for the current phase without losing them.

Tickets are deliberately simple: create, derive a phase from, archive. No editing, no complex state transitions, no prioritization logic.

## Directory Structure

```
.ushabti/tickets/           # Active tickets
.ushabti/tickets/.archived/ # Completed tickets (invisible to agents)
```

Agents read tickets from `.ushabti/tickets/` but ignore `.ushabti/tickets/.archived/`. Archived tickets are effectively invisible once moved.

## Ticket YAML Schema

Each ticket is a YAML file with the following required fields:

```yaml
id: T0001                    # Sequential ticket ID (TNNNN format)
title: Short description     # Brief, descriptive title
created: 2026-02-01          # ISO 8601 date (YYYY-MM-DD)
priority: medium             # Must be: low, medium, or high
context: |
  Multi-line context explaining why this ticket exists.
  What observation or need led to its creation?
proposed_work: |
  Multi-line description of what should be done.
  What would a phase derived from this ticket accomplish?
```

All fields are required. The `priority` field must be one of: `low`, `medium`, `high`.

## Ticket Filename Format

Ticket files are named: `TNNNN-short-description.yaml`

- `TNNNN`: Zero-padded 4-digit sequential ID (T0001, T0002, etc.)
- `short-description`: Lowercase, hyphenated slug derived from title
- Extension: `.yaml`

Example: `T0042-improve-error-messages.yaml`

## Workflows

### Creating a Ticket

1. Determine next ticket ID (use `find-next-ticket-number` skill)
2. Create YAML file with all required fields
3. Validate schema (all fields present, priority is valid)
4. Write file to `.ushabti/tickets/TNNNN-slug.yaml`

### Deriving a Phase from a Ticket

When a ticket is ready to become a phase:

1. Scribe reads the ticket YAML from `.ushabti/tickets/`
2. Scribe uses `context` and `proposed_work` to inform phase planning
3. Scribe adds `ticket: TNNNN` metadata to the phase.md file
4. The ticket remains in `.ushabti/tickets/` until the phase completes

### Archiving a Ticket

When a ticket-derived phase completes:

1. Overseer reads the `ticket` field from phase.md
2. Overseer moves the ticket file from `.ushabti/tickets/` to `.ushabti/tickets/.archived/`
3. Overseer logs the archival action in review findings
4. The archived ticket is now invisible to agents

## Agent Responsibilities

### Vizier (Advisory)

- Can read active tickets from `.ushabti/tickets/`
- Ignores archived tickets in `.ushabti/tickets/.archived/`
- May offer to create tickets when good ideas for future work arise during conversation
- Should offer ticket creation sparingly, only for genuine future work

### Scribe (Planning)

- Reads tickets when user requests a phase derived from a ticket
- Uses ticket `context` and `proposed_work` to inform phase intent and scope
- Adds `ticket: TNNNN` metadata to phase.md when deriving from a ticket

### Overseer (Review)

- Checks phase.md for `ticket` field when completing a phase
- Archives the corresponding ticket by moving it to `.ushabti/tickets/.archived/`
- Logs archival action in review findings

### Builder, Lawgiver, Artisan, Surveyor

- No specific ticket responsibilities
- May create tickets if they observe out-of-scope work during their duties

## Design Principles

- **Simple lifecycle**: Create → derive phase → archive. No intermediate states.
- **File-backed**: Everything lives in the repository, no external dependencies.
- **Agent-friendly**: Clear schema, clear locations, clear workflows.
- **Complementary**: Tickets support phases, they don't replace planning or become a backlog management tool.
- **Invisible when done**: Archived tickets are moved out of the active directory and ignored by agents.
