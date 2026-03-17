---
name: cfn-memory-persistence
description: Data persistence for CFN Loop - SQLite storage, Redis coordination, automatic memory persistence
version: 1.0.0
tags: [mega-skill, persistence, sqlite, redis, memory]
status: production
---

# Memory Persistence Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Data persistence for CFN Loop (SQLite, Redis, auto-persistence)
**Status:** Production
**Consolidates:** cfn-sqlite-memory, cfn-sqlite-cfn-loop, cfn-redis-coordination, cfn-automatic-memory-persistence, cfn-memory-management

---

## Overview

This mega-skill provides complete data persistence:
- **SQLite** - Local database storage with ACL
- **Redis** - Pub/sub coordination and state
- **Auto** - Automatic confidence persistence
- **Management** - Memory limits and heap profiling

---

## Directory Structure

```
memory-persistence/
├── SKILL.md
├── lib/
│   ├── sqlite/           # From cfn-sqlite-memory
│   │   └── cfn-loop/     # From cfn-sqlite-cfn-loop
│   ├── redis/            # From cfn-redis-coordination
│   ├── auto/             # From cfn-automatic-memory-persistence
│   └── management/       # From cfn-memory-management
└── cli/
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-sqlite-memory/ | memory-persistence/lib/sqlite/ |
| cfn-sqlite-cfn-loop/ | memory-persistence/lib/sqlite/cfn-loop/ |
| cfn-redis-coordination/ | memory-persistence/lib/redis/ |
| cfn-automatic-memory-persistence/ | memory-persistence/lib/auto/ |
| cfn-memory-management/ | memory-persistence/lib/management/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 5 memory/persistence skills into mega-skill
