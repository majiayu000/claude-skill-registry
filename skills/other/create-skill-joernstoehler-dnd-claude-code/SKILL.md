---
name: create-skill
description: Create a new Claude Code skill. Use when adding reusable knowledge or workflows to the repository, when the user asks to "add a skill", or when a repeated pattern should be captured as a skill.
---

# Creating a New Skill

## Official Documentation

- **Primary**: https://code.claude.com/docs/en/skills.md
- **Best Practices**: https://code.claude.com/docs/en/best-practices.md

## File Structure

Create a directory in `.claude/skills/<skill-name>/` with:

```
<skill-name>/
├── SKILL.md           # Required: main instructions with YAML frontmatter
├── references/        # Optional: detailed reference material
│   └── *.md
├── examples/          # Optional: example outputs
│   └── *.md
└── scripts/           # Optional: executable scripts
    └── *.sh
```

## SKILL.md Format

```yaml
---
name: skill-name                    # lowercase-with-dashes, max 64 chars
description: What it does and when to use it. Include trigger phrases users would naturally say.
# Optional fields below:
disable-model-invocation: false     # true = manual /skill-name only
user-invocable: true                # false = Claude-only, hidden from menu
allowed-tools: Read, Grep, Glob     # restrict tool access
context: fork                       # run in isolated subagent
agent: Explore                      # subagent type if context: fork
---

# Skill content here

Instructions Claude follows when this skill is active.
Keep under 500 lines; move details to references/.
```

## Writing Good Descriptions

The description determines when Claude auto-invokes the skill. Include:
- What the skill does
- Keywords users would naturally say
- Specific trigger conditions

**Good**: "Create an NPC with personality, motivation, and stats. Use when the user asks for a new character, needs an NPC, or says 'create a character'."

**Bad**: "NPC creation skill."

## Progressive Disclosure

- SKILL.md description is always loaded (counts toward 15k char budget)
- Full SKILL.md body loads only when skill is invoked
- Reference files load only when Claude decides to read them

Structure knowledge accordingly:
- Description: when to use, brief summary
- Body: step-by-step instructions, key facts
- References: detailed tables, extensive examples, full specifications

## Checklist

Before committing a new skill:

1. [ ] Name is lowercase-with-dashes
2. [ ] Description explains what AND when
3. [ ] Body is under 500 lines
4. [ ] Instructions are clear and actionable
5. [ ] Large reference material is in separate files
6. [ ] Tested with `/skill-name` invocation
