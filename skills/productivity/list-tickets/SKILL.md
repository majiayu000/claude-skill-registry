---
name: list-tickets
description: List all open (non-archived) tickets
---

# List Tickets

## Purpose

This skill provides commands for discovering and listing open tickets. Open tickets are those in `.ushabti/tickets/` that have not been archived.

## Listing Open Tickets

### Basic List Command

List all ticket files in `.ushabti/tickets/`:

```bash
ls .ushabti/tickets/*.yaml 2>/dev/null || echo "No tickets found"
```

This shows filenames only. Example output:
```
.ushabti/tickets/T0001-add-search-functionality.yaml
.ushabti/tickets/T0005-improve-error-messages.yaml
.ushabti/tickets/T0008-refactor-agent-roles.yaml
```

### List with Details

Show ticket files with modification times:

```bash
ls -lh .ushabti/tickets/*.yaml 2>/dev/null || echo "No tickets found"
```

### Extract Ticket IDs

Get just the ticket IDs:

```bash
ls .ushabti/tickets/T[0-9][0-9][0-9][0-9]-*.yaml 2>/dev/null | \
  sed -E 's/.*\/(T[0-9]{4})-.*/\1/' || echo "No tickets found"
```

Example output:
```
T0001
T0005
T0008
```

### Count Tickets

Count how many open tickets exist:

```bash
ls .ushabti/tickets/*.yaml 2>/dev/null | wc -l
```

## Reading Ticket Contents

To read a specific ticket:

```bash
cat .ushabti/tickets/T0001-*.yaml
```

To read all tickets (useful for searching):

```bash
for ticket in .ushabti/tickets/*.yaml; do
  echo "=== $ticket ==="
  cat "$ticket"
  echo ""
done
```

## Important Notes

### Exclusions

These commands explicitly ignore:
- **Archived tickets**: Files in `.ushabti/tickets/.archived/` are never listed
- **Non-YAML files**: Only `.yaml` files are considered tickets
- **Subdirectories**: Only files directly in `.ushabti/tickets/` are listed

### Empty Directory

If no tickets exist, the commands handle this gracefully:
- `ls` with `2>/dev/null` suppresses error messages
- `|| echo "No tickets found"` provides user-friendly output

### Sorting

By default, `ls` sorts alphanumerically, which matches ticket ID order due to zero-padding (T0001, T0002, T0010).

## Example Usage

### Scenario: User asks "What tickets are open?"

Run:
```bash
ls .ushabti/tickets/*.yaml 2>/dev/null || echo "No tickets found"
```

If tickets exist, show filenames. If no tickets exist, respond "No tickets found".

### Scenario: Agent needs to check if any tickets exist

Run:
```bash
ls .ushabti/tickets/*.yaml 2>/dev/null | wc -l
```

If result is 0, no tickets exist. If greater than 0, tickets exist.

### Scenario: User asks for ticket details

Run:
```bash
for ticket in .ushabti/tickets/*.yaml; do
  echo "=== $ticket ==="
  cat "$ticket"
  echo ""
done
```

This displays all ticket contents with clear separation.

## Integration with Other Skills

- Use `find-next-ticket-number` to determine the next ID when creating a ticket
- Use `create-ticket` to add a new ticket to the list
- Use `archive-ticket` to remove a ticket from the active list (moves to `.archived/`)
- Use `describe-tickets` to understand ticket schema and workflows

## Output Format

The skill intentionally provides raw output (filenames, counts, YAML content) rather than formatted reports. This keeps the skill simple and allows agents to format output based on context.
