---
name: cfn-operations
description: File and log operations for CFN
version: 1.0.0
tags: [mega-skill, file-io, logging, operations]
status: production
---

# Operations Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** File and log operations for CFN
**Status:** Production
**Consolidates:** cfn-file-operations, cfn-log-operations

---

## Overview

This mega-skill provides I/O operations:
- **File** - File read/write/copy operations
- **Log** - Log file management and rotation

---

## Directory Structure

```
operations/
├── SKILL.md
├── lib/
│   ├── file/             # From cfn-file-operations
│   └── log/              # From cfn-log-operations
└── cli/
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-file-operations/ | operations/lib/file/ |
| cfn-log-operations/ | operations/lib/log/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 2 operations skills into mega-skill

