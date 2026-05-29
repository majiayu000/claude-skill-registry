---
name: obsidian-vault
description: Manage and navigate Obsidian vault with consistent structure, naming conventions, and linking patterns
skill_type: flexible
---

Use this skill when working with Obsidian notes in `/Users/alexismanuel/workspace/obsidian_notes/notes`.

## Core Principles

- **Location first**: Place notes in the correct folder before creating them (topics/, work/concepts/, work/tickets/, daily/)
- **Naming matters**: Use consistent naming (YYYY-MM-DD.md for daily, RD-XXXX [Title].md for tickets, descriptive for topics)
- **Link everything**: Use [[wikilinks]] to connect related notes; avoid orphaned notes
- **Follow templates**: Use daily template with YAML frontmatter and checkboxes

## Quick Reference

| Note Type | Location | Naming |
|-----------|----------|--------|
| Daily notes | daily/ | YYYY-MM-DD.md |
| Tickets | work/tickets/ | `RD-XXXX [Title]/` (folder containing Ticket.md, PRD.md, Plan.md) |
| Concepts | work/concepts/ | Descriptive title.md |
| Topics | topics/ | Descriptive title.md |
| Objectives | work/ | Y[X]S[X] Objectives.md |

## Ticket Hub Pattern

Tickets in `work/tickets/` use a folder-based structure called "Feature Folder":

```
work/tickets/RD-XXXX [Title]/
├── Ticket.md      # Progress dashboard with links to [[PRD]] and [[Plan]]
├── PRD.md         # Product Requirements Document (Goal, Requirements, Non-Goals)
└── Plan.md        # Implementation plan (Technical Strategy, Tasks, Testing)
```

Each ticket is a folder, not a single file. Use the templates in `templates/` to create each component.

- Start at `topics/Index.md` for vault overview
- Use search for domain-specific content (data engineering, GIS, AI/GenAI)
- Follow wikilinks to discover related notes

## References

- [creating-notes.md](obsidian-vault/creating-notes.md) - Placement, naming, linking decisions
- [finding-notes.md](obsidian-vault/finding-notes.md) - Vault structure and search strategies
- [organizing-content.md](obsidian-vault/organizing-content.md) - Folder structure and git workflow
