---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

Skills are modular packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools.

## Core Principles

### Conciseness
The context window is shared. Only add information Claude doesn't already have. Challenge each piece: "Does this justify its token cost?"

### Degrees of Freedom
- **High freedom** (text instructions): Multiple valid approaches, context-dependent decisions
- **Medium freedom** (pseudocode/scripts with params): Preferred pattern exists, some variation acceptable
- **Low freedom** (specific scripts): Fragile operations, consistency critical

## Skill Anatomy

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name, description (required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/     # Executable code for deterministic tasks
    ├── references/  # Documentation loaded as needed
    └── assets/      # Files used in output (templates, icons)
```

### What NOT to Include
- README.md, CHANGELOG.md, INSTALLATION_GUIDE.md
- User-facing documentation
- Setup/testing procedures

## Progressive Disclosure

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words, <500 lines)
3. **Bundled resources** - As needed by Claude

For design patterns, see:
- `references/workflows.md` - Multi-step processes and conditional logic
- `references/output-patterns.md` - Template and example patterns

## Creation Process

### Step 1: Understand with Examples
Gather concrete examples of how the skill will be used. Ask:
- What functionality should it support?
- What would trigger this skill?

### Step 2: Plan Reusable Contents
For each example, identify:
- Scripts for repetitive code
- References for domain knowledge
- Assets for templates/boilerplate

### Step 3: Initialize
```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

### Step 4: Edit
- Implement resources (scripts, references, assets)
- Write SKILL.md with proper frontmatter
- Delete unused example files

**Frontmatter guidelines:**
- `description` is the primary triggering mechanism
- Include both what skill does AND when to use it
- All "when to use" info goes in description, not body

### Step 5: Package
```bash
python scripts/package_skill.py <path/to/skill-folder> [output-dir]
```

Validates and creates a distributable .skill file.

### Step 6: Iterate
Use the skill on real tasks, notice struggles, update, and test again.
