---
name: create-ticket
description: Create implementation tickets with proper format and conventions.
user-invocable: false
---

# Create Ticket

Guidelines for creating implementation tickets in `.workaholic/tickets/`.

## Frontmatter Template (REQUIRED - DO NOT SKIP)

```yaml
---
created_at: <run: date -Iseconds>
author: <run: git config user.email>
type: <enhancement | bugfix | refactoring | housekeeping>
layer: [<UX | Domain | Infrastructure | DB | Config>]
effort: <leave empty - filled after implementation>
commit_hash: <leave empty - filled when archived>
category: <leave empty - filled when archived>
---
```

**All fields are mandatory.** Run the shell commands to fill `created_at` and `author`.

## Filename Convention

Format: `YYYYMMDDHHmmss-<short-description>.md`

Use current timestamp: `date +%Y%m%d%H%M%S`

Example: `20260114153042-add-dark-mode.md`

## File Structure

```markdown
---
created_at: YYYY-MM-DDTHH:MM:SS+TZ
author: <git user.email>
type: enhancement | bugfix | refactoring | housekeeping
layer: [<layers affected>]
effort: <filled after implementation>
commit_hash: <filled when archived>
category: <filled when archived>
---

# <Title>

## Overview

<Brief description of what will be implemented>

## Key Files

- `path/to/file.ts` - <why this file is relevant>

## Related History

<1-2 sentence summary synthesizing what historical tickets reveal about this area>

Past tickets that touched similar areas:

- [20260127010716-rename-terminology-to-terms.md](.workaholic/tickets/archive/<branch>/20260127010716-rename-terminology-to-terms.md) - Renamed terminology directory (same layer: Config)
- [20260125113858-auto-commit-ticket-on-creation.md](.workaholic/tickets/archive/<branch>/20260125113858-auto-commit-ticket-on-creation.md) - Modified ticket.md (same file)

## Implementation Steps

1. <Step 1>
2. <Step 2>
   ...

## Considerations

- <Any trade-offs, risks, or things to watch out for>
```

## Frontmatter Fields

### Required at Creation

- **created_at**: Creation timestamp in ISO 8601 format. Use `date -Iseconds`
- **author**: Git email. Use `git config user.email`
- **type**: Infer from request context:
  - `enhancement` - New features or capabilities (keywords: add, create, implement, new)
  - `bugfix` - Fixing broken behavior (keywords: fix, bug, broken, error)
  - `refactoring` - Restructuring without changing behavior (keywords: refactor, restructure, reorganize)
  - `housekeeping` - Maintenance, cleanup, documentation (keywords: clean, update, remove, deprecate)
- **layer**: Architectural layers affected (YAML array, can specify multiple):
  - `UX` - User interface, components, styling
  - `Domain` - Business logic, models, services
  - `Infrastructure` - External integrations, APIs, networking
  - `DB` - Database, storage, migrations
  - `Config` - Configuration, build, tooling

### Filled After Implementation

- **effort**: Time spent in numeric hours. Valid: `0.1h`, `0.25h`, `0.5h`, `1h`, `2h`, `4h`. Invalid: `XS`, `S`, `M`, `10m`. Leave empty when creating ticket.
- **commit_hash**: Short git commit hash. Set automatically by archive script.
- **category**: Change category (Added, Changed, or Removed). Set automatically by archive script based on commit message verb.

## Exploring the Codebase

Before writing a ticket:

- Use Glob, Grep, and Read tools to find relevant files
- Understand existing patterns, architecture, and conventions
- Identify files that will need to be modified or created

## Related History

The Related History section is populated by the `history-discoverer` subagent (invoked by `/ticket` command).

**Link format**: Use markdown links with repository-relative paths:
```markdown
- [filename.md](.workaholic/tickets/archive/<branch>/filename.md) - Description (match reason)
```

The full path includes the branch directory from the search results (e.g., `feat-20260126-214833`).

If the subagent returns no matches, omit the Related History section entirely.

## Writing Guidelines

- Focus on the "why" and "what", not just "how"
- Keep implementation steps actionable and specific
- Reference existing code patterns when applicable
- Use the Write tool directly - it creates parent directories automatically
