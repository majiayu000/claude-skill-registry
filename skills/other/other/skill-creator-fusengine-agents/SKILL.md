---
name: skill-creator
description: Use when creating new skills, restructuring existing skills, or improving skill documentation. Generates SKILL.md + references/ structure with proper patterns.
versions:
  claude-plugins: "1.35"
user-invocable: true
references: references/workflow.md, references/architecture.md, references/content-rules.md, references/registration.md, references/adaptation.md, references/templates/SKILL-template.md, references/templates/reference-template.md, references/templates/template-template.md
related-skills: research, exploration
---

# Skill Creator

## Agent Workflow (MANDATORY)

Before ANY skill creation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Check existing skills, analyze structure
2. **fuse-ai-pilot:research-expert** - Fetch latest official documentation online
3. **mcp__context7__query-docs** - Get code examples from official sources

After creation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Action | When to Use |
|--------|-------------|
| **New Skill** | Library/framework not yet documented |
| **Restructure** | Existing skill doesn't follow pattern |
| **Improve** | Missing references or outdated content |
| **Adapt** | Copy from similar skill (Next.js → React) |

---

## Critical Rules

1. **ALL content in English** - Never French or other languages
2. **SKILL.md is descriptive** - Guides agent to references/templates
3. **References are conceptual** - WHY + WHEN, max 150 lines
4. **Templates are complete** - Copy-paste ready code
5. **Register in agent + marketplace.json** - Or skill won't load
6. **Run sniper after creation** - Validate all files

---

## Architecture

```
skills/<skill-name>/
├── SKILL.md                    # Entry point (guides agent)
└── references/                 # All documentation
    ├── installation.md         # Setup, configuration (conceptual)
    ├── patterns.md             # Core patterns (conceptual)
    ├── ...                     # Other references
    └── templates/              # Complete code examples
        ├── basic-setup.md      # Full project setup
        └── feature-example.md  # Feature implementation
```

→ See [architecture.md](references/architecture.md) for details

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Workflow** | [workflow.md](references/workflow.md) | Creating/improving skills |
| **Architecture** | [architecture.md](references/architecture.md) | Understanding skill structure |
| **Content Rules** | [content-rules.md](references/content-rules.md) | Writing references/templates |
| **Registration** | [registration.md](references/registration.md) | Making skill available |
| **Adaptation** | [adaptation.md](references/adaptation.md) | Converting between frameworks |

### Templates

| Template | When to Use |
|----------|-------------|
| [SKILL-template.md](references/templates/SKILL-template.md) | Creating new SKILL.md |
| [reference-template.md](references/templates/reference-template.md) | Creating reference files |
| [template-template.md](references/templates/template-template.md) | Creating code templates |

---

## Quick Reference

### Create New Skill

```bash
# 1. Research documentation
→ research-expert + context7/exa

# 2. Create structure
mkdir -p plugins/<agent>/skills/<name>/references/templates

# 3. Create files
→ SKILL.md (from template)
→ references/*.md (conceptual)
→ references/templates/*.md (code)

# 4. Register
→ agent frontmatter + marketplace.json

# 5. Validate
→ sniper
```

### Improve Existing Skill

```bash
# 1. Analyze
→ explore-codebase

# 2. Research updates
→ research-expert (latest docs)

# 3. Add missing files
→ references + templates

# 4. Validate
→ sniper
```

---

## Validation Checklist

- [ ] ALL content in English
- [ ] SKILL.md has proper frontmatter
- [ ] All references listed in frontmatter
- [ ] Agent Workflow section present
- [ ] Reference Guide has Concepts + Templates tables
- [ ] References < 150 lines each
- [ ] Templates have complete, working code
- [ ] Registered in agent + marketplace.json

---

## Best Practices

### DO
- Research official docs before writing
- Use tables for organization
- Link references to templates
- Keep references conceptual
- Make templates copy-paste ready

### DON'T
- Write in French (English only)
- Copy-paste raw documentation
- Exceed 150 lines in references
- Forget registration step
- Skip sniper validation
