---
name: cfn-intervention-system
description: "Human intervention detection and orchestration for CFN Loop. Use when automated processes need human oversight, when escalation is required, or when managing intervention workflows and approval gates."
version: 1.0.0
tags: [mega-skill, intervention, human-in-the-loop, escalation]
status: production
---

# Intervention System Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Human intervention detection and orchestration for CFN Loop
**Status:** Production
**Consolidates:** cfn-intervention-detector, cfn-intervention-orchestrator

---

## Overview

This mega-skill provides complete intervention management:
- **Detector** - Detect when human intervention is needed
- **Orchestrator** - Manage intervention workflows and escalation

---

## Directory Structure

```
intervention-system/
├── SKILL.md
├── lib/
│   ├── detector/         # From cfn-intervention-detector
│   └── orchestrator/     # From cfn-intervention-orchestrator
└── cli/
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-intervention-detector/ | intervention-system/lib/detector/ |
| cfn-intervention-orchestrator/ | intervention-system/lib/orchestrator/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 2 intervention skills into mega-skill

