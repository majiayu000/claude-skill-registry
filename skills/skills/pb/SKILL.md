---
description: Create a new skill with proper SKILL.md structure and frontmatter
argument-hint: <skill-name> [plugin-path]
allowed-tools: Read, Write, Glob
---

# Create New Skill

Create a new Claude Code skill with the name: $1
Target plugin path: $2 (defaults to current directory)

## Process

1. **Validate skill name**
   - Must be lowercase
   - Only alphanumeric and hyphens
   - Max 64 characters

2. **Create directory structure**
   ```
   skills/
   └── $1/
       └── SKILL.md
   ```

3. **Generate SKILL.md with template**

```yaml
---
name: $1
description: [Ask user for description - must be specific with trigger phrases, max 1024 chars]
allowed-tools: Read, Grep, Glob
---

# [Skill Title]

## Overview

[Brief explanation of what this skill provides]

## Instructions

[Step-by-step instructions for Claude when this skill is active]

## Examples

[Concrete examples of using this skill]
```

4. **Ask user for:**
   - Description (with guidance on making it specific)
   - Which tools should be allowed (or all)
   - Main purpose/instructions

5. **Create optional reference.md if needed**

## Validation

After creation, verify:
- [ ] Directory `skills/$1/` exists
- [ ] `SKILL.md` has valid YAML frontmatter
- [ ] Description includes trigger phrases
- [ ] Description under 1024 characters
