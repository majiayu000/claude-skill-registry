---
name: using-linear
description: Query, create, and manage Linear issues from the command line. Use when checking assigned work, viewing issue details, creating new issues, or updating issue status.
---

# Linear CLI

Query, create, and update Linear issues without leaving the terminal.

## Quick Examples

```bash
# Check your assigned work
linear-cli my-work

# View issue details
linear-cli issue ENG-456

# Create a new issue
linear-cli create --title "Production bug" --priority 1 --team ENG

# Update status and add comment
linear-cli update ENG-456 --status "Done"
linear-cli comment ENG-456 "Shipped in v2.1.0"
```

## Key Flags

- `--team ENG` - Specify or filter by team
- `--status "In Progress"` - Set or filter by status
- `--priority 1` - Set priority (1-4, 1 is highest)
- `--assignee name` - Assign to team member
- `--description` - Add issue description

## More Info

See REFERENCE.md for complete flag documentation, advanced examples, and workflow patterns. Use `linear-cli --help` or `linear-cli <command> --help` for all options.

## Authentication

```bash
linear-cli login    # OAuth login (stores credentials)
linear-cli logout   # Clear stored credentials
linear-cli status   # Verify connection
```
