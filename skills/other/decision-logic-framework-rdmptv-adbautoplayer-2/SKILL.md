---
name: decision-logic-framework
description: Decision rules for Claude Code skills, scripts, MDs, and workflows - project-agnostic patterns
version: 1.0.0
modularized: true
last_updated: 2025-12-02
compliance_score: 100
auto_trigger_keywords:
  - skill creation
  - script vs md
  - naming convention
  - workflow decision
  - tier selection
  - single file rule
  - prefix naming
  - when to use script
  - when to use markdown
color: blue
---

## Quick Reference (30 seconds)

**Core Principle**: Clear separation between Agents (orchestrators) and Skills (capabilities).

| Component | Location | Contains |
|-----------|----------|----------|
| **Agents** | `.claude/agents/` | `workflows/` (TOON + MD steps) |
| **Skills** | `.claude/skills/` | `scripts/` (UV Python) OR `modules/` (single-file MDs) |

**Decision Tree**:
```
Need external Python packages? → UV Script (.py)
Need system commands?          → UV Script (.py)
Reference/documentation?       → Single-File MD (.md)
Simple data/rules?             → Single-File MD (.md)
```

**Naming (Mandatory Prefixes)**:
- Scripts: `{skill}_{action}.py` (underscore)
- Modules: `{category}-{topic}.md` (hyphen)

---

## Architecture Overview

### Agents = Orchestrators with Workflows
```
.claude/agents/{category}/{agent-name}/
├── {agent-name}.md              # Agent definition
└── workflows/                    # Agent-owned workflows
    └── {workflow-name}/
        ├── WORKFLOW.toon        # Structure (TOON tabular)
        ├── instructions.md      # Overall guidance
        ├── checklist.md         # Validation (tier-2+)
        └── steps/
            └── step-NN-{action}.md
```

### Skills = Capabilities with Scripts OR Modules
```
.claude/skills/{skill-name}/
├── SKILL.md                     # Main entry (REQUIRED)
├── scripts/                     # For complex automation (OPTIONAL)
│   └── {skill}_{action}.py      # UV scripts with prefix
└── modules/                     # For simple reference MDs (OPTIONAL)
    └── {category}-{topic}.md    # Single-file MDs with prefix
```

---

## When to Use This Skill

Use this skill when:
- Creating a new skill and deciding between scripts vs modules
- Choosing workflow complexity tier (0-3)
- Naming new files (scripts or modules)
- Understanding the architecture separation
- Reverse-engineering third-party apps

**Load Order**: This skill should be loaded FIRST when creating any new skill, agent, or workflow.

---

## Available Modules

| Module | Purpose | When to Load |
|--------|---------|--------------|
| `rule-script-vs-md.md` | Decision logic for script vs MD | Creating new skill content |
| `rule-naming-convention.md` | Prefix naming system | Naming any new file |
| `rule-skill-tiers.md` | Tier 1-4 skill complexity | Assessing skill scope |
| `rule-workflow-complexity.md` | Tier 0-3 workflow selection | Creating workflows |
| `pattern-single-file.md` | Universal single-file rules | Reviewing file constraints |

## Available Schemas

| Schema | Purpose | When to Load |
|--------|---------|--------------|
| `workflow-schema.toon` | Canonical WORKFLOW.toon format | Creating any workflow |
| `step-schema.md` | Template for step-NN-{action}.md | Creating workflow steps |

---

## Decision Flowcharts

### Script vs MD Decision

```
┌─────────────────────────────────────┐
│     NEW SKILL CONTENT NEEDED        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Requires external Python packages?  │
│ (httpx, pandas, click, psutil...)   │
├─────────────┬───────────────────────┤
│     YES     │          NO           │
│     ↓       │          ↓            │
│  UV SCRIPT  │  Requires shell/sys?  │
└─────────────┴───────────┬───────────┘
                          │
              ┌───────────┴───────────┐
              │     YES     │    NO   │
              │     ↓       │    ↓    │
              │  UV SCRIPT  │  MD OK  │
              └─────────────┴─────────┘
```

### Workflow Tier Selection

```
┌─────────────────────────────────────┐
│      WORKFLOW COMPLEXITY            │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────┬───────────┐
    ▼          ▼          ▼           ▼
┌───────┐ ┌───────┐ ┌─────────┐ ┌─────────┐
│Tier 0 │ │Tier 1 │ │ Tier 2  │ │ Tier 3  │
│1 step │ │3-5    │ │ 5-10    │ │ 10+     │
│hotfix │ │simple │ │ medium  │ │ complex │
└───────┘ └───────┘ └─────────┘ └─────────┘
```

---

## Prefix Naming Quick Reference

### Scripts (UV Python)
```
Pattern: {skill-name}_{action}.py
Separator: underscore (_)

Examples:
  kalshi_get-market.py
  kalshi_search-events.py
  system_analyze-cpu.py
  builder_generate-skill.py
```

### Modules (Single-File MDs)
```
Pattern: {category}-{topic}.md
Separator: hyphen (-)

Categories: api, pattern, rule, guide, schema, example

Examples:
  api-endpoints.md
  pattern-authentication.md
  rule-naming-convention.md
  guide-quick-start.md
```

---

## Works Well With

**Agents**:
- `builder-skill` - Skill creation with tier system
- `builder-workflow` - TOON + MD workflow generation
- `builder-agent` - Agent with workflows/ generation

**Skills**:
- `moai-library-toon` - TOON format reference
- `moai-foundation-core` - Core execution rules
- `builder-skill-uvscript` - UV script examples

**Commands**:
- `/moai:1-plan` - SPEC generation with decision framework
- `/builder:generate-skill` - Skill creation workflow

---

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-12-02
