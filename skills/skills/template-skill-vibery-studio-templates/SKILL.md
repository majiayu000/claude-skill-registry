---
name: template-skill
description: Replace with description of the skill and when Claude should use it.
license: MIT
---

# Template Skill

This is a basic template for creating new skills.

## Structure

```
skill-name/
├── SKILL.md          # Main skill file (required)
├── references/       # Additional documentation (optional)
├── scripts/          # Utility scripts (optional)
└── assets/           # Output files, templates (optional)
```

## SKILL.md Format

```markdown
---
name: skill-name
description: Brief description of what this skill does and when to use it.
license: MIT
---

# Skill Name

[Skill instructions and documentation here]
```

## Best Practices

1. Keep SKILL.md under 200 lines
2. Use references/ for detailed documentation
3. Follow progressive disclosure principles
4. Use Python/Node for scripts (cross-platform)

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
