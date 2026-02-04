---
name: find-next-ticket-number
description: Determine the next sequential ticket ID
---

# Find Next Ticket Number

## Purpose

This skill provides the logic to determine the next sequential ticket ID when creating a new ticket. Ticket IDs follow the format `TNNNN` (e.g., T0001, T0002, T0042).

## Usage

Run the provided bash command to find the highest existing ticket number and calculate the next ID.

## Bash Command

```bash
# Ensure directory exists (defensive, in case bootstrap didn't run)
mkdir -p .ushabti/tickets

# Find the highest ticket number in .ushabti/tickets/
HIGHEST=$(find .ushabti/tickets -maxdepth 1 -type f -name 'T[0-9][0-9][0-9][0-9]-*.yaml' | \
  sed -E 's/.*\/T([0-9]{4})-.*/\1/' | \
  sort -n | \
  tail -1)

# If no tickets exist, start at 1; otherwise increment
if [ -z "$HIGHEST" ]; then
  NEXT=1
else
  NEXT=$((10#$HIGHEST + 1))
fi

# Format as zero-padded 4-digit number
printf "T%04d\n" $NEXT
```

## How It Works

1. **Ensure directory exists**: Creates `.ushabti/tickets/` if it doesn't exist (defensive fallback)
2. **Find ticket files**: Searches `.ushabti/tickets/` for files matching `T[0-9][0-9][0-9][0-9]-*.yaml`
3. **Extract IDs**: Uses `sed` to extract the 4-digit numeric portion from each filename
4. **Sort**: Sorts numerically to find the highest ID
5. **Calculate next**: Increments the highest ID by 1, or starts at 1 if no tickets exist
6. **Format**: Outputs the next ID as zero-padded 4-digit format (TNNNN)

## Example Output

If `.ushabti/tickets/` contains:
- `T0001-first-ticket.yaml`
- `T0002-second-ticket.yaml`
- `T0005-another-ticket.yaml`

The command outputs:
```
T0006
```

If `.ushabti/tickets/` is empty, the command outputs:
```
T0001
```

## Notes

- The command ignores archived tickets in `.ushabti/tickets/.archived/`
- IDs are sequential but may have gaps (e.g., if T0003 and T0004 were created then archived)
- Zero-padding ensures alphanumeric sorting matches numeric order
