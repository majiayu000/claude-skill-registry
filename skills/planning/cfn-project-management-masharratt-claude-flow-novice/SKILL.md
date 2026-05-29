---
name: cfn-project-management
description: Backlog and changelog management for CFN projects
version: 1.0.0
tags: [mega-skill, backlog, changelog, tracking]
status: production
---

# Project Management Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Backlog and changelog management for CFN projects
**Status:** Production
**Consolidates:** cfn-backlog-management, cfn-changelog-management

---

## Overview

This mega-skill provides project tracking:
- **Backlog** - Issue and task backlog management
- **Changelog** - Version changelog generation and maintenance

---

## Directory Structure

```
project-management/
├── SKILL.md
├── lib/
│   ├── backlog/          # From cfn-backlog-management
│   └── changelog/        # From cfn-changelog-management
└── cli/
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-backlog-management/ | project-management/lib/backlog/ |
| cfn-changelog-management/ | project-management/lib/changelog/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 2 project management skills into mega-skill

## Known Issues

- ⚠️ **Missing Implementation**: The `lib/backlog/` and `lib/changelog/` directories referenced in the documentation do not exist
- ⚠️ **Old Paths Missing**: The old paths referenced for migration (`cfn-backlog-management/`, `cfn-changelog-management/`) also do not exist
- ⚠️ **Planned Consolidation**: This skill appears to be a planned consolidation that hasn't been implemented
- ⚠️ **Use Alternative Commands**: Users should look for backlog and changelog functionality in other skills or slash commands
- ⚠️ **Implementation Required**: This is a documentation-only skill until the consolidation is implemented

