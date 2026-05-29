---
name: discover-history
description: Search archived tickets by keywords to find related historical context.
allowed-tools: Bash
user-invocable: false
---

# Discover History

Search archived tickets to find related past work.

## Instructions

Run the bundled script with keywords extracted from the ticket request:

```bash
bash .claude/skills/discover-history/sh/search.sh <keyword1> [keyword2] ...
```

### Keyword Extraction

Extract 3-5 keywords from:
- Key file paths (e.g., `ticket.md`, `drive.md`)
- Domain terms (e.g., `branch`, `commit`, `archive`)
- Layer names (e.g., `Config`, `UX`)

### Output Format

The script returns matches sorted by relevance (match count):

```
5 .workaholic/tickets/archive/feat-xxx/ticket-a.md
3 .workaholic/tickets/archive/feat-yyy/ticket-b.md
```

### Interpreting Results

- Higher count = more keyword matches = more relevant
- Read top 5 tickets to understand context
- Extract: title, overview, key files, layer
