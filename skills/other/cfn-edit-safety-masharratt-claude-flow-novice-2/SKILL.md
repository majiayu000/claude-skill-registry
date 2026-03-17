---
name: cfn-edit-safety
description: "Pre-edit backup and post-edit validation for safe file modifications. Use when you need to capture file state before edits, validate changes after modifications, revert files to previous state, or ensure edit safety with automatic backup and validation hooks."
version: 1.0.0
tags: [mega-skill, backup, hooks, validation, safety]
status: production
---

# Edit Safety Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Pre-edit backup and post-edit validation
**Status:** Production
**Consolidates:** cfn-hook-pipeline, pre-edit-backup
**Confidence:** 8.5/10 (mandatory paired workflow in CLAUDE.md)

---

## Overview

This mega-skill provides complete edit safety:
- **Backup** - Pre-edit file state capture for revert capability
- **Hooks** - Post-edit validation and feedback pipeline

---

## Directory Structure

```
edit-safety/
├── SKILL.md
├── lib/
│   ├── backup/           # From pre-edit-backup
│   └── hooks/            # From cfn-hook-pipeline
└── cli/
```

---

## Workflow

1. Pre-edit: `edit-safety/lib/backup/` captures file state
2. Edit occurs
3. Post-edit: `edit-safety/lib/hooks/` validates changes
4. If needed: Revert via backup

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| pre-edit-backup/ | edit-safety/lib/backup/ |
| cfn-hook-pipeline/ | edit-safety/lib/hooks/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated backup + hooks into unified edit safety skill

