---
name: skills-ksmuvva-ai-playwright-framewor
description: 'Skill: e73customskill'
---

# E7.3 - Custom Skills

**Skill:** `e7_3_custom_skill`
**Version:** 1.0.0
**Author:** Claude Playwright Agent Team

## Overview

Support for creating and managing custom user-defined skills.

## Capabilities

- Create custom skills
- Validate skill structure
- Register custom skills
- Load user skills

## Usage

```python
# Create custom skill at .cpa/skills/my_skill/
# skill.yaml + main.py + __init__.py
```

## Skill Structure

```
.cpa/skills/my_skill/
├── skill.yaml
├── __init__.py
└── main.py
```

## See Also

- [E7.1 - Skill Registry](./e7_1_registry.md)
- [E7.2 - Manifest Parser](./e7_2_manifest_parser.md)
