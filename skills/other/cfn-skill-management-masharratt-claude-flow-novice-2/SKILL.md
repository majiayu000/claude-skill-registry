---
name: cfn-skill-management
description: "Skill loading, propagation, and building for CFN. Use when dynamically discovering and loading skills, deploying skills across environments, or creating new skill scaffolding."
version: 1.0.0
tags: [mega-skill, skills, loader, builder, deployment]
status: production
---

# Skill Management Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Skill loading, propagation, and building for CFN
**Status:** Production
**Consolidates:** cfn-skill-loader, cfn-skill-propagation, cfn-skill-builder

---

## Overview

This mega-skill provides complete skill lifecycle management:
- **Loader** - Dynamic skill discovery and loading
- **Propagation** - Skill deployment across environments
- **Builder** - New skill creation and scaffolding

---

## Directory Structure

```
skill-management/
├── SKILL.md
├── lib/
│   ├── loader/           # From cfn-skill-loader
│   ├── propagation/      # From cfn-skill-propagation
│   └── builder/          # From cfn-skill-builder
└── cli/
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-skill-loader/ | skill-management/lib/loader/ |
| cfn-skill-propagation/ | skill-management/lib/propagation/ |
| cfn-skill-builder/ | skill-management/lib/builder/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 3 skill management skills into mega-skill

