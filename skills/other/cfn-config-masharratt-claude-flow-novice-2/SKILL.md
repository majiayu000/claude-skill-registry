---
name: cfn-config
description: "Configuration management and environment sanitization. Use when you need to manage configuration files, validate environment variables, sanitize sensitive data, or update system settings across CFN Loop components."
version: 1.0.0
tags: [mega-skill, config, environment, sanitization]
status: production
---

# Config Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Configuration management and environment sanitization
**Status:** Production
**Consolidates:** cfn-config-management, cfn-environment-sanitization

---

## Overview

This mega-skill provides configuration handling:
- **Management** - Configuration file management and updates
- **Sanitization** - Environment variable sanitization and validation

---

## Directory Structure

```
config/
├── SKILL.md
├── lib/
│   ├── management/       # From cfn-config-management
│   └── sanitization/     # From cfn-environment-sanitization
└── cli/
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-config-management/ | config/lib/management/ |
| cfn-environment-sanitization/ | config/lib/sanitization/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 2 config skills into mega-skill

