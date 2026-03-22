---
name: agentic-share
description: "Shared core logic for importing/exporting reusable assets into the v0.2 plugin architecture. Internal helper for agentic-import and agentic-export."
project-agnostic: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Agentic Asset Share

Core logic for moving reusable assets between projects and this repository.

## Arguments

- **mode**: `import` | `export`
- **asset_type**: `skill` | `template` | `agent`
- **source**: source path or asset name
- **target**: optional destination name/path
- **options**: optional flags (`--plugin`, `--force`, `--dry-run`)

Parsed from: `$ARGUMENTS`

## Canonical Locations (v0.2)

| Type | Project Source | Repository Target |
|------|----------------|-------------------|
| skill | `.claude/skills/<name>/` or explicit skill dir | `plugins/<plugin>/skills/<name>/` |
| template | `templates/<name>/` | `templates/<name>/` |
| agent | explicit agent markdown path | `plugins/ac-workflow/agents/<name>.md` |

Notes:
- There is **no command asset type** in v0.2 (skills-only surface).
- For skills, `--plugin` is required unless destination can be inferred.

## Execution Flow

1. Parse mode, type, source, target, options.
2. Validate mode (`import` or `export`).
3. Validate asset type (`skill`, `template`, `agent`).
4. Validate repository root:
   - must contain `.claude-plugin/marketplace.json`
   - must contain `plugins/`
5. Resolve source and destination paths by type.
6. Read source content (single file or directory tree).
7. Apply sanitization:
   - scrub absolute home paths (`/Users/...`, `/home/...`) -> `{USER_HOME}`
   - scrub secrets/tokens (`api_key`, `token`, `secret`, bearer values) -> `{REDACTED}`
8. Validate sanitized output:
   - block if unresolved secrets remain
   - warn on environment-specific hardcoded values
9. Write output (or preview with `--dry-run`).
10. Report summary and next steps.

## Safety Rules

- Never overwrite existing targets without `--force` or explicit confirmation.
- Never proceed when unresolved secrets remain after sanitization.
- On any failure, abort with a clear error and leave no partial file writes.

## Commit Guidance (Optional)

After successful import/export, offer a commit for only touched asset paths.

Conventional message pattern:

```text
feat(assets): import <asset_type> '<asset_name>'
```

(or `export` accordingly)

## Error Cases

| Error | Action |
|-------|--------|
| Invalid mode/type | Abort with valid choices |
| Repository root not detected | Abort and request running from repo root |
| Source missing | Abort and print source path |
| Sanitization blockers remain | Abort and print blocker lines |
| Target exists without force | Ask for overwrite confirmation |
