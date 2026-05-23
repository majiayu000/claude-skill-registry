---
name: skill-builder-generic
description: Universal guide for creating production-ready Claude Code skills for any project. Includes 6-step workflow (understand, plan, initialize, edit, package, iterate), progressive disclosure design, YAML frontmatter templates, validation scripts, reference organization patterns, and 10 community-proven innovations. Use when creating new Claude Code skills, converting documentation to skills, improving existing skills, or learning skill development best practices for any domain.
---

# Universal Claude Code Skill Builder

## Overview

Complete guide for creating production-ready Claude Code skills following Anthropic best practices and community innovations. Provides templates, validation tools, step-by-step workflows, and comprehensive references for building effective, discoverable skills.

## When to Use This Skill

- Creating new Claude Code skills from scratch
- Converting existing documentation into skills
- Improving existing skills
- Understanding skill structure
- Validating skills before packaging
- Learning best practices

## Quick Start: Create Skill in 5 Minutes

### 1. Choose Name
```bash
my-skill-name  # hyphen-case only
```

### 2. Create Directory
```bash
mkdir -p .claude/skills/my-skill-name
```

### 3. Create SKILL.md
```yaml
---
name: my-skill-name
description: [What it does]. Use when [triggers].
---

# My Skill

## Overview
[Purpose in 1-2 sentences]

## Quick Start
[Basic usage]
```

### 4. Validate
```bash
python scripts/validate-skill.py my-skill-name/
```

### 5. Package
```bash
bash scripts/package-skill.sh my-skill-name/
```

Done!

## The 6-Step Process

Detailed documentation in references. See [references/yaml-frontmatter-complete-guide.md](references/yaml-frontmatter-complete-guide.md) for comprehensive guidance.

---

**Version:** 1.0
**Research:** 11 sources
**Last Updated:** October 25, 2025
