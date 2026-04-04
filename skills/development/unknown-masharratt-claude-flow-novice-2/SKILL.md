---
name: cfn-agent-tooling
description: "Agent development tools - generation and validation. Use when creating new agent templates from scaffolding, or validating and linting existing agent profiles for correctness and completeness."
version: 1.0.0
tags: [mega-skill, agents, templates, validation, development]
status: production
---

# Agent Tooling Skill (Mega-Skill)

**Version:** 1.0.0
**Purpose:** Agent development tools - generation and validation
**Status:** Production
**Consolidates:** agent-template-generator, agent-validation-linter

---

## Overview

This mega-skill provides agent development tools:
- **Generator** - Agent template scaffolding and generation
- **Linter** - Agent profile validation and linting

---

## Directory Structure

```
agent-tooling/
├── SKILL.md
├── lib/
│   ├── generator/        # From agent-template-generator
│   └── linter/           # From agent-validation-linter
└── cli/
```

---

## Migration Paths

| Old Path | New Path |
|----------|----------|
| agent-template-generator/ | agent-tooling/lib/generator/ |
| agent-validation-linter/ | agent-tooling/lib/linter/ |

---

## Version History

### 1.0.0 (2025-12-02)
- Consolidated 2 agent tooling skills into mega-skill

