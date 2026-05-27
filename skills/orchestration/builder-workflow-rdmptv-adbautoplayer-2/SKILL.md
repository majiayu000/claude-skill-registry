---
name: builder-workflow
description: Workflow orchestration skill for builder ecosystem - repo analysis, SPEC creation, and generation workflows for skills, agents, and UV scripts
version: 1.0.0
modularized: false
scripts_enabled: false
last_updated: 2025-12-01
auto_trigger_keywords:
  - builder-workflow
  - reverse-engineer
  - workflow-designer
  - generate-skill
  - generate-agent
  - generate-script
color: yellow
---

---

## Quick Reference (30 seconds)

**Builder Ecosystem Workflow Orchestration**

**What It Does**: Orchestrates the builder agent ecosystem for repository analysis, pattern extraction, SPEC/diagram creation, and automated generation of skills, agents, and UV scripts.

**Core Capabilities**:
- Repository Analysis & Pattern Extraction
- SPEC Document & Diagram Creation
- Skill Generation Workflows
- Agent Blueprint Creation
- UV Script Generation (IndieDevDan patterns)

**Agent Ecosystem**:
| Agent | Role | Trigger Command |
|-------|------|-----------------|
| builder-reverse-engineer | Repo analysis, pattern extraction | `/builder:reverse-engineer` |
| builder-workflow-designer | SPEC creation, workflow diagrams | `/builder:workflow-designer` |
| builder-workflow | UV script generation | `/builder:generate-script` |
| builder-skill | Skill creation | `/builder:generate-skill` |
| builder-agent | Agent blueprint creation | `/builder:generate-workflow` |

**When to Use**:
- Analyzing external repositories for automation opportunities
- Creating SPECs from pattern analysis
- Generating new skills with proper structure
- Creating UV CLI scripts following IndieDevDan patterns
- Building complete workflows (skill + agents + scripts)

---

## Agent Relationship Flow

The builder ecosystem follows a clear delegation chain:

```
┌─────────────────────────────┐
│  builder-reverse-engineer   │ ← FIRST: Analyze repo, extract patterns
│  (moai-builder/)            │
└──────────────┬──────────────┘
               │
               ▼ identifies automation opportunities
┌─────────────────────────────┐
│  builder-workflow-designer  │ ← THEN: Creates SPECs, diagrams
│  (moai-builder/)            │
└──────────────┬──────────────┘
               │
               ▼ delegates script generation
┌─────────────────────────────┐
│  builder-workflow           │ ← FINALLY: Creates UV scripts
│  (moai-builder/)            │
└─────────────────────────────┘
```

### Workflow Stages

**Stage 1: Repository Analysis** (builder-reverse-engineer)
- Scan repository structure and file organization
- Identify technology stack and dependencies
- Extract design patterns and conventions
- Discover automation opportunities
- Output: TOON-formatted analysis report

**Stage 2: SPEC & Diagram Creation** (builder-workflow-designer)
- Parse analysis report
- Create EARS-style SPEC documents
- Generate workflow diagrams
- Design agent coordination patterns
- Output: SPEC documents, Mermaid diagrams

**Stage 3: Implementation** (builder-workflow, builder-skill, builder-agent)
- Generate UV CLI scripts from patterns
- Create skill structures with SKILL.md
- Build agent blueprints with proper frontmatter
- Output: Production-ready code and configurations

---

## Available Commands

The builder ecosystem exposes these commands:

### `/builder:reverse-engineer [repo-path]`
Analyze repository for patterns and automation opportunities.

```bash
# Analyze local repository
/builder:reverse-engineer /path/to/repo

# Analyze GitHub repository
/builder:reverse-engineer https://github.com/owner/repo
```

### `/builder:workflow-designer [analysis-output]`
Create SPECs and diagrams from analysis.

```bash
# Design workflow from analysis
/builder:workflow-designer .moai/reports/analysis-report.md
```

### `/builder:generate-script [skill-name] [script-name]`
Generate UV CLI script for existing skill.

```bash
# Generate analysis script
/builder:generate-script moai-foundation-core analyze-compliance
```

### `/builder:generate-skill [skill-name] [description]`
Generate new skill with SKILL.md structure.

```bash
# Generate new skill
/builder:generate-skill moai-connector-slack "Slack integration with MCP"
```

### `/builder:generate-workflow [workflow-name]`
Generate complete workflow (skill + agents + scripts).

```bash
# Generate complete workflow
/builder:generate-workflow api-testing-automation
```

---

## Integration with builder-skill-uvscript

This skill works alongside `builder-skill-uvscript` which contains 23 production UV scripts:

**Script Categories in builder-skill-uvscript**:
- System Analysis: 12 scripts (analyze_*, monitor_*, optimize_*)
- Code Generation: 4 scripts (generate_agent, generate_skill, generate_command, scaffold_test)
- Development Tools: 2 scripts (debug_code, analyze_performance)
- Documentation: 2 scripts (lint_docs, validate_diagrams)
- BaaS Integration: 2 scripts (select_provider, migrate_provider)
- Template Tools: 1 script (generate_template)

**Relationship**:
- `builder-workflow` (this skill) - Orchestration patterns and agent coordination
- `builder-skill-uvscript` - Reference implementations and production scripts

---

## Workflow Patterns

### Pattern 1: Repository-to-Skill Pipeline

```yaml
pipeline:
  input: Repository URL or path
  stages:
    - builder-reverse-engineer → Analysis Report
    - builder-workflow-designer → SPEC + Diagrams
    - builder-skill → Skill Structure
    - builder-workflow → UV Scripts
  output: Complete skill with scripts
```

### Pattern 2: Quick Script Generation

```yaml
pipeline:
  input: Skill name + Script requirements
  stages:
    - builder-workflow → UV Script
  output: Single production script
```

### Pattern 3: Agent Blueprint Creation

```yaml
pipeline:
  input: Agent requirements
  stages:
    - builder-reverse-engineer → Pattern analysis
    - builder-agent → Agent YAML with frontmatter
  output: Agent definition file
```

---

## Quality Standards

All generated artifacts follow:

**TRUST 5 Principles**:
- Testable: Includes test patterns
- Readable: Clear documentation
- Understandable: Self-documenting code
- Secure: No hardcoded secrets
- Traceable: Version history

**IndieDevDan 13 Rules** (for UV scripts):
- 200-300 line target
- PEP 723 dependencies
- Zero shared imports
- Dual output modes
- Project-root detection

**MoAI Standards**:
- YAML frontmatter
- Color coding (yellow = custom)
- Agent hierarchy compliance
- Command naming conventions

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| builder-skill-uvscript | 23 reference UV scripts |
| moai-foundation-core | Execution rules, TRUST 5 |
| moai-lang-unified | Multi-language patterns |
| moai-library-toon | TOON format specification |

---

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-12-01
**Color**: Yellow (Custom Superdisco)
