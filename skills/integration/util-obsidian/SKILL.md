---
name: _util-obsidian
description: Obsidian CLI for vault search, backlinks, links, tags, and file operations. Use when fetching related content or interacting with Obsidian programmatically. Requires Obsidian v1.12+ with CLI enabled.
---

# Obsidian CLI

Interact with a running Obsidian instance. Requires Obsidian open with CLI enabled (Settings > General > Command line interface).

## Availability Check

Before any operation, verify CLI is available:

```bash
obsidian version 2>/dev/null
```

If this fails (non-zero exit), skip CLI operations and continue without enhanced context. Never block workflows because Obsidian is unavailable.

## Syntax

**Parameters** take a value with `=`. Quote values with spaces:

```bash
obsidian search query="project notes" limit=10
```

**Flags** are boolean switches with no value:

```bash
obsidian create name="Note" silent
```

**File targeting:**
- `file=<name>` — resolves like a wikilink (name only)
- `path=<path>` — exact path from vault root

**Vault targeting:** Commands target the most recently focused vault. Use `vault=<name>` to target a specific vault.

## Quick Start

### Search notes by content

```bash
obsidian search query="meeting notes" limit=10
```

### Find backlinks (notes linking TO a file)

```bash
obsidian backlinks file="Projects/Q2-Launch"
```

### Find outgoing links (notes this file links TO)

```bash
obsidian links file="Projects/Q2-Launch"
```

### Find notes by tag

```bash
obsidian tag name="project" limit=20
```

### List all tags with counts

```bash
obsidian tags sort=count counts
```

## Common Patterns

Use `--copy` on any command to copy output to clipboard. Use `silent` to prevent files from opening. Use `total` on list commands to get a count.

```bash
obsidian search query="leadership" limit=5 --copy
obsidian backlinks file="People/Marcus" total
```

## References

For complete CLI command reference: [references/commands.md](references/commands.md)

Full documentation: https://help.obsidian.md/cli
