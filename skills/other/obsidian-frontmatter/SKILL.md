---
name: obsidian-frontmatter
description: Frontmatter management in Obsidian for metadata and organisation
category: Session Knowledge
---

# Skill: obsidian-frontmatter

## What I do

I provide expertise in managing YAML frontmatter within Obsidian notes. I ensure that metadata is structured, consistent, and optimised for both manual organisation and automated querying via Dataview. I specialise in defining standard schemas for different note types to maintain vault-wide data integrity.

## When to use me

- When creating templates for new notes (e.g. daily notes, project notes, or skills).
- When standardising metadata across a cluster of existing notes.
- When defining custom fields that will be used in Dataview dashboards or charts.
- When troubleshooting YAML syntax errors that prevent notes from being indexed correctly.

## Core principles

1. **Standardisation** — Use a consistent set of core fields (e.g. \`title\`, \`created\`, \`tags\`, \`status\`) across all notes to ensure predictable query results.
2. **ISO 8601 Compliance** — Always use the \`YYYY-MM-DD\` format for dates to maintain compatibility with Obsidian's core features and Dataview.
3. **Kebab-Case Tags** — Prefer \`kebab-case\` for tag values and hierarchical structures (e.g. \`#project/active\`) for better readability and filtering.
4. **Minimality** — Keep frontmatter lean; only include metadata that is genuinely useful for automation or organisation. Avoid cluttering notes with unused fields.

## Patterns & examples

### Standard Note Frontmatter
A baseline schema for a general knowledge note.
```yaml
---
title: Advanced Git Workflows
created: 2024-03-25
tags: [git, workflow, advanced]
aliases: [Git Master, Git Expert]
status: permanent
---
```

### Project-Specific Metadata
Extended fields for tracking project progress and ownership.
```yaml
---
type: project
client: Baphled Corp
deadline: 2024-12-31
priority: high
assigned_to: [[Sisyphus]]
progress: 45
---
```

### Hierarchical Tags
Using slashes to create nested categories within the \`tags\` field.
```yaml
---
tags:
  - knowledge/technical/obsidian
  - status/in-progress
---
```

## Anti-patterns to avoid

- ❌ **Malformed YAML** — Missing colons, inconsistent indentation, or unquoted special characters that break the frontmatter block.
- ❌ **Duplicate Fields** — Defining the same metadata key multiple times in a single note, leading to unpredictable behaviour.
- ❌ **Non-Standard Dates** — Using formats like \`DD/MM/YY\` which are not natively supported for date-based sorting in many plugins.
- ❌ **Over-Categorisation** — Adding dozens of tags or custom fields that are never used for filtering or querying.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Session-Knowledge/Obsidian Frontmatter.md`

## Related skills

- `obsidian-dataview-expert` — The primary consumer of frontmatter metadata for dynamic indexing.
- `obsidian-structure` — For deciding which notes require specific frontmatter schemas based on their PARA location.
- `obsidian-customjs-expert` — For writing scripts that read and update note frontmatter programmatically.
- `information-architecture` — For designing the high-level metadata schema of the vault.
