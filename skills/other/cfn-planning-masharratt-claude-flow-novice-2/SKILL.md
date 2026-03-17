---
name: cfn-planning
description: "Epic decomposition, coordinator planning, and scope management. Use when breaking down epics into sprints and tasks, coordinating multi-coordinator workflows, or simplifying and managing project scope boundaries."
version: 1.0.0
tags: [mega-skill, epic, planning, scope, decomposition]
status: production
---

# Planning Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Epic decomposition, coordinator planning, and scope management
**Status:** Production
**Consolidates:** cfn-epic-decomposer, cfn-multi-coordinator-planning, cfn-scope-simplifier

---

## Overview

This mega-skill provides planning capabilities:
- **Epic** - Epic decomposition into sprints/tasks
- **Coordinator** - Multi-coordinator planning and orchestration
- **Scope** - Scope simplification and boundary management

---

## Directory Structure

```
planning/
├── SKILL.md
├── lib/
│   ├── epic/             # From cfn-epic-decomposer
│   ├── coordinator/      # From cfn-multi-coordinator-planning
│   └── scope/            # From cfn-scope-simplifier
└── cli/
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-epic-decomposer/ | planning/lib/epic/ |
| cfn-multi-coordinator-planning/ | planning/lib/coordinator/ |
| cfn-scope-simplifier/ | planning/lib/scope/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 3 planning skills into mega-skill

