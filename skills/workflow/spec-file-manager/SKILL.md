---
name: spec-file-manager
description: Manage specification files. Use when creating, reading, updating, or listing spec files. Triggers on requests like "create spec", "update spec", "list specs", or "show spec status".
---

# Spec File Manager

Manages specification files in a configurable directory.

## Storage Location

### Directory Detection

Search for spec directory in this order:

1. `specs/`
2. `.specs/`
3. `docs/specs/`
4. `.dev-plans/`

If none found, ask user which directory to create.

### Override

Directory can be specified explicitly via command argument:

```
/spec:create-md docs/specifications
```

## File Naming Convention

```
YYYY-MM-DD-{slug}.md
```

- **Date prefix**: Creation date in ISO format (e.g., `2025-01-22`)
- **Slug**: Kebab-case, English only, max 20 characters
- **Extension**: Always `.md`

Examples:
- `2025-01-22-user-auth.md`
- `2025-01-22-api-pagination.md`

## Structure

Flat structure. No subdirectories.

## Operations

### Create

1. Detect or receive target directory
2. Generate filename with today's date and slug
3. Copy template from `assets/spec-template.md`
4. Save to target directory

### List

List all `.md` files in spec directory sorted by date (newest first).

### Update

Edit existing spec file in spec directory.

### Delete

Remove spec file from spec directory.

## Template

See [assets/spec-template.md](assets/spec-template.md) for the specification file template.
