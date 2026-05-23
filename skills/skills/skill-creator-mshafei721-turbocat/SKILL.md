---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

Guide for creating effective skills that extend Claude's capabilities.

## About Skills

Skills are modular, self-contained packages providing:
1. Specialized workflows
2. Tool integrations
3. Domain expertise
4. Bundled resources

## Core Principles

### Concise is Key

The context window is shared. Only add context Claude doesn't already have. Challenge each piece: "Does Claude really need this?"

### Set Appropriate Degrees of Freedom

- **High freedom**: Text instructions for flexible tasks
- **Medium freedom**: Pseudocode/scripts with parameters
- **Low freedom**: Specific scripts for fragile operations

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/          - Executable code
    ├── references/       - Documentation for context
    └── assets/           - Files for output
```

## Progressive Disclosure

Three-level loading:
1. **Metadata** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed (unlimited)

## Skill Creation Process

### Step 1: Understand with Examples
Gather concrete examples of how the skill will be used.

### Step 2: Plan Reusable Contents
Identify scripts, references, and assets needed.

### Step 3: Initialize
```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

### Step 4: Edit the Skill
- Implement scripts, references, assets
- Update SKILL.md with instructions
- Keep SKILL.md under 500 lines

### Step 5: Package
```bash
scripts/package_skill.py <path/to/skill-folder>
```

### Step 6: Iterate
Test on real tasks, notice struggles, improve.

## SKILL.md Guidelines

**Frontmatter:**
- `name`: Skill name
- `description`: What it does AND when to use it

**Body:**
- Use imperative/infinitive form
- Reference bundled resources
- Keep under 500 lines
