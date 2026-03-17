---
name: skill-creation-guide
description: "Guide for creating Agent Skills: structure, best practices, and SKILL.md format for Claude Code, Codex, Gemini CLI, and other AI agents."
---

# Skill Creation Guide

## Scope

Use this skill when:

- Creating new Agent Skills
- Understanding SKILL.md format and conventions
- Learning best practices for skill authoring

## Skill Structure

```
skill-name/
├── SKILL.md          # Required: Instructions and metadata
├── scripts/          # Optional: Helper scripts
├── templates/        # Optional: Document templates
└── resources/        # Optional: Reference files
```

## SKILL.md Format

### Required Frontmatter

```yaml
---
name: my-skill-name
description: A clear description of what this skill does and when to use it.
---
```

### Body Structure

```markdown
# Skill Name

Detailed description of the skill's purpose.

## When to Use This Skill

- Use case 1
- Use case 2

## Instructions

[Detailed instructions for the agent]

## Examples

[Real-world examples]
```

## Best Practices

1. **Keep descriptions exhaustive**: The frontmatter description helps agents decide when to trigger the skill.
2. **Focus on execution**: The body should contain clear, actionable steps.
3. **Use progressive disclosure**: Put detailed references in `references/` folder.
4. **Include scripts for automation**: Use helper scripts for deterministic operations.
5. **Keep SKILL.md under 500 lines**: For optimal performance.
6. **Test across platforms**: Verify skills work with Claude Code, Codex, etc.

## Token Efficiency

Skills employ progressive disclosure architecture:

1. **Metadata loading** (~100 tokens): Agent scans available skills
2. **Full instructions** (<5k tokens): Load when skill is activated
3. **Bundled resources**: Only load as needed

## Platform-Specific Paths

| Platform | Project Path | Global Path |
|----------|--------------|-------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.codex/skills/` | `~/.codex/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |

## Quality Checklist

- [ ] Clear, actionable instructions
- [ ] Includes real-world examples
- [ ] Written for AI agents, not end users
- [ ] Documents prerequisites and dependencies
- [ ] Includes error handling guidance
- [ ] Tested on target platform(s)

## Full Resource List

For more detailed skill creation resources, complete link lists, or the latest information, use WebFetch to retrieve the full README.md:

```
https://raw.githubusercontent.com/gmh5225/awesome-skills/refs/heads/main/README.md
```

The README.md contains the complete categorized resource list with all links.
