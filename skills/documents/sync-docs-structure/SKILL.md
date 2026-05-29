---
name: sync-docs-structure
description: Automatically sync the documentation structure from docs/content/{en,uk}/ to CLAUDE.md when changes are detected in the docs directory. This skill should be triggered when documentation files are added, removed, or reorganized, or when explicitly requested by the user or agents.
---

# Sync Documentation Structure

## Overview

Keep CLAUDE.md synchronized with the current documentation structure by scanning `docs/content/{en,uk}/` and updating the Documentation section with the latest file tree and titles.

## When to Use

Trigger this skill when:
- New documentation files or directories are added to `docs/`
- Documentation structure is reorganized or renamed
- User explicitly requests documentation sync
- After significant changes to docs/ are detected

## Workflow

### 1. Scan Documentation Structure

Run the bundled scanner script to extract the current docs structure:

```bash
uv run .claude/skills/sync-docs-structure/scripts/scan_docs.py
```

The script:
- Scans `docs/content/en/` and `docs/content/uk/` directories
- Builds a tree structure showing files and folders
- Extracts titles from markdown frontmatter when available
- Outputs clean markdown-formatted tree

### 2. Update CLAUDE.md

Locate or create the `## Documentation` section in CLAUDE.md (should be after `## Code Quality Standards`).

Replace the entire Documentation section with:

```markdown
## Documentation

**Source**: Bilingual markdown files in `docs/content/{en,uk}/`

```
[OUTPUT FROM SCAN SCRIPT]
```
```

### 3. Verify and Report

After updating:
- Confirm what sections were found (en, uk)
- Report number of documentation files discovered
- Preserve all other sections in CLAUDE.md unchanged

## Example Output

After running the skill, CLAUDE.md should contain:

```markdown
## Documentation

**Source**: Bilingual markdown files in `docs/content/{en,uk}/`

```
docs/content/
├── en/
│   ├── api/
│   │   └── endpoints.md - API Endpoints
│   └── architecture/
│       ├── overview.md - System Architecture
│       └── analysis-system.md - Analysis System
└── uk/
    ├── api/
    │   └── endpoints.md - API точки доступу
    └── architecture/
        ├── overview.md - Архітектура системи
        └── analysis-system.md - Система аналізу
```
```

## Notes

- Keep updates lightweight - structure only, not file contents
- The script extracts titles from markdown frontmatter automatically
- Skip `docs/site/` and other generated directories
- Preserve exact formatting for consistency