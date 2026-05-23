---
name: cfn-loop-orchestration-v2
description: "CFN Loop coordination and orchestration - gate checks, validation, consensus, coordination patterns. Use when orchestrating multi-agent workflows, managing iteration cycles, or coordinating Loop 2/Loop 3 dependencies."
version: 1.0.0
tags: [mega-skill, cfn-loop, orchestration, coordination]
status: production
---

# Loop Orchestration Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** CFN Loop coordination and orchestration
**Status:** Production
**Consolidates:** cfn-loop-orchestration, cfn-loop-output-processing, cfn-loop-validation, cfn-coordination

---

## Overview

This mega-skill provides complete CFN Loop orchestration:
- **Orchestrator** - Main loop execution and gate checks
- **Output** - Agent output parsing and consensus calculation
- **Validation** - Multi-layer validation framework
- **Coordination** - Agent coordination patterns (chain, broadcast, mesh)

---

## Directory Structure

```
loop-orchestration/
├── SKILL.md
├── lib/
│   ├── orchestrator/     # From cfn-loop-orchestration
│   ├── output/           # From cfn-loop-output-processing
│   ├── validation/       # From cfn-loop-validation
│   └── coordination/     # From cfn-coordination
└── cli/
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| cfn-loop-orchestration/ | loop-orchestration/lib/orchestrator/ |
| cfn-loop-output-processing/ | loop-orchestration/lib/output/ |
| cfn-loop-validation/ | loop-orchestration/lib/validation/ |
| cfn-coordination/ | loop-orchestration/lib/coordination/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 4 loop orchestration skills into mega-skill
