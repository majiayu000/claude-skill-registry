---
description: "Create a new Atlas skill"
argument-hint: "[skill-name]"
allowed-tools: [Write, Bash, Read]
---

# Create New PAI Skill

Create a new skill for the PAI system.

## Skill to Create

**Skill name:** $ARGUMENTS

## Creation Process

Please create a new skill following these steps:

1. **Skill Directory:**
   - Create `~/.claude/skills/$1/`
   - Create the main SKILL.md file

2. **Skill Structure:**
   Follow this template:

```markdown
---
name: SkillName
description: Brief description (one line, what triggers this skill)
---

# SkillName - Full Title

Brief overview of what this skill does.

## When to Use

- Trigger condition 1
- Trigger condition 2
- Trigger condition 3

## Capabilities

What this skill can do:
- Capability 1
- Capability 2
- Capability 3

## Usage

How to invoke and use this skill.

## Examples

<example>
User: [Example user request]
Assistant: [How the skill responds]
</example>

## Technical Details

Any implementation details, dependencies, or requirements.
```

3. **Register the Skill:**
   - Verify the skill is in ~/.claude/skills/
   - Test by listing with `/atlas:skills`

4. **Provide Usage:**
   - Show how to invoke the skill
   - Provide example use cases

Would you like me to create a skill? Provide the name and description.
