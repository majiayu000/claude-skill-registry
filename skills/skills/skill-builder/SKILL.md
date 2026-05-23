---
name: "Skill Builder"
version: "1.0.0"
description: "Create new Claude Code Skills with proper YAML frontmatter, progressive disclosure structure, and complete directory organization. Use when you need to build custom skills for specific workflows, generate skill templates, or understand the Claude Skills specification."
category: development
tags:
  - skill-authoring
  - templates
  - yaml
  - claude-code
  - scaffolding
author: Smith Horn
---

# Skill Builder

## Behavioral Classification

**Type**: Guided Decision

This skill guides you through key decisions when creating skills, then generates appropriate templates and structure.

**Decision Points**:
1. What type of skill? (basic, intermediate, advanced)
2. Behavioral classification? (autonomous, guided, interactive, configurable)
3. Include scripts? (yes/no)

After decisions are made, skill generation proceeds automatically.

---

## What This Skill Does

Creates production-ready Claude Code Skills with proper YAML frontmatter, progressive disclosure architecture, and complete file/folder structure. This skill guides you through building skills that Claude can autonomously discover and use across all surfaces (Claude.ai, Claude Code, SDK, API).

**Key Features**:
- Proper YAML frontmatter with required `name` and `description` fields
- Progressive disclosure (3-level system for scaling to 100+ skills)
- Directory structure templates for minimal to full-featured skills
- Scripts and resources organization patterns

---

## Prerequisites

- Claude Code 2.0+ or Claude.ai with Skills support
- Basic understanding of Markdown and YAML
- Text editor or IDE

---

## Quick Start

### Creating Your First Skill

```bash
# 1. Create skill directory (MUST be at top level, NOT in subdirectories!)
mkdir -p ~/.claude/skills/my-first-skill

# 2. Create SKILL.md with proper format
cat > ~/.claude/skills/my-first-skill/SKILL.md << 'EOF'
---
name: "My First Skill"
description: "Brief description of what this skill does and when Claude should use it. Maximum 1024 characters."
---

# My First Skill

## What This Skill Does
[Your instructions here]

## Quick Start
[Basic usage]
EOF

# 3. Verify skill is detected
# Restart Claude Code or refresh Claude.ai
```

---

## Sub-Documentation

For detailed information, see the following files:

| Document | Contents |
|----------|----------|
| [Specification](./specification.md) | YAML frontmatter, directory structure, progressive disclosure |
| [Templates](./templates.md) | Basic, intermediate, and advanced skill templates |
| [Best Practices](./best-practices.md) | Content writing guidelines, validation checklist |
| [Skill Locations](./skill-locations.md) | User vs project skills, precedence, migration |

---

## Quick Reference

### YAML Frontmatter (Required)

```yaml
---
name: "Skill Name"                    # REQUIRED: Max 64 chars
description: "What this skill does    # REQUIRED: Max 1024 chars
and when Claude should use it."       # Include BOTH what & when
---
```

### Directory Structure

**Minimal (Required)**:
```
~/.claude/skills/my-skill/
└── SKILL.md                     # REQUIRED
```

**Full-Featured (Recommended)**:
```
~/.claude/skills/my-skill/
├── SKILL.md                     # REQUIRED: Main skill file
├── README.md                    # Optional: Human-readable docs
├── scripts/                     # Optional: Executable scripts
├── resources/                   # Optional: Templates, examples
└── docs/                        # Optional: Additional documentation
```

### Skills Locations

| Location | Scope | Use Case |
|----------|-------|----------|
| `~/.claude/skills/` | Personal (all projects) | Personal productivity tools |
| `.claude/skills/` | Project (team-shared) | Team workflows, committed to git |

### Behavioral Classifications

| Classification | Directive | When to Use |
|----------------|-----------|-------------|
| **Autonomous Execution** | EXECUTE, DON'T ASK | Prescribed workflows, no decisions needed |
| **Guided Decision** | ASK, THEN EXECUTE | Requires user input on specific choices |
| **Interactive Exploration** | ASK THROUGHOUT | Ongoing dialogue is the value |
| **Configurable Enforcement** | USER-CONFIGURED | Behavior depends on project settings |

### Progressive Disclosure

| Level | Loaded When | Size | Content |
|-------|-------------|------|---------|
| 1: Metadata | Always (startup) | ~200 chars | Name + description |
| 2: SKILL.md | Skill triggered | 1-10KB | Main instructions |
| 3+: References | On-demand | Variable | Deep reference, examples |

---

## Learn More

### Official Resources
- [Anthropic Agent Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills)
- [GitHub Skills Repository](https://github.com/anthropics/skills)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)

### Community
- [Skills Marketplace](https://github.com/anthropics/skills) - Browse community skills
- [Anthropic Discord](https://discord.gg/anthropic) - Get help from community

---

**Created**: 2025-10-19
**Version**: 1.0.0
**Maintained By**: agentic-flow team
