---
name: example-skill
description: Example skill template for AgentForge. Demonstrates proper SKILL.md structure with references and scripts.
version: 1.0.0
tags:
  - example
  - template
  - demo
author: AgentForge
category: utilities
---

# Example Skill

This is an example skill template that demonstrates the proper structure for AgentForge skills.

## Purpose

This skill serves as a template for creating new skills. It shows how to:
- Write proper SKILL.md frontmatter
- Organize supporting documentation in `references/`
- Include executable scripts in `scripts/`
- Add assets in `assets/`

## Usage

When creating a new skill:
1. Copy this template structure
2. Edit SKILL.md with your skill's instructions
3. Add reference documentation to `references/`
4. Include helper scripts in `scripts/`
5. Place any images or data files in `assets/`

## Files Structure

```
example-skill/
├── SKILL.md          # Main skill instructions (this file)
├── references/       # Supporting documentation
│   └── guide.md
├── scripts/          # Executable scripts
│   └── helper.ts
└── assets/           # Images, data files, etc.
```

## Next Steps

1. Rename `example-skill` to your skill name
2. Update frontmatter metadata
3. Write detailed instructions in this file
4. Add references and scripts as needed
