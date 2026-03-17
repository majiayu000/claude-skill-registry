---
name: cfn-sprint-execution
description: Sprint planning, execution, and checkpointing for CFN Loop
version: 1.0.0
tags: [mega-skill, sprint, planning, execution, checkpoint]
status: production
---

# Sprint Execution Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Sprint planning, execution, and checkpointing for CFN Loop
**Status:** Production
**Consolidates:** cfn-sprint-execution, cfn-sprint-planner, cfn-wave-checkpoint

---

## Overview

This mega-skill provides complete sprint management:
- **Planning** - Sprint decomposition and scheduling
- **Execution** - Sprint task execution and tracking
- **Checkpoint** - Wave-based progress checkpointing

---

## Directory Structure

```
sprint-execution/
├── SKILL.md
├── lib/
│   ├── planning/         # From cfn-sprint-planner
│   ├── execution/        # From cfn-sprint-execution
│   └── checkpoint/       # From cfn-wave-checkpoint
└── cli/
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-sprint-planner/ | sprint-execution/lib/planning/ |
| cfn-sprint-execution/ | sprint-execution/lib/execution/ |
| cfn-wave-checkpoint/ | sprint-execution/lib/checkpoint/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 3 sprint-related skills into mega-skill

