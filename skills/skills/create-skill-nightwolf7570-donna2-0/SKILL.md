---
name: "Skill Creating"
description: "Used to create a new skill. Used when a user wants to create a new skill "
---

# Create Skill

## Instructions
Invoked when the user requests for a new skill to be created


# Create Skill

## Instructions

When requested to create a new skill, follow these steps:
1. Create a new folder in `.claude/skills` with the skill name `xyz.md` (make name gerund form)
2. Take the requested input to turn into a re-usable skill
3. Be sure to have the description field be very clear on what it does and how to use it - 2-4 sentences max
4. Store documentation and sample inputs/outputs in a new sub-folder there `resources/` if they exceed several lines or will be referenced for depth.
5. Generate minimal, clear, actionable Markdown instructions as the primary workflow guide.
6. If code or scripts are needed, place them in the skill folder and reference their purpose in this file.

## Examples

skill.md
---
name: Generating Commit Messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## Instructions

1. Run `git diff --staged` to see changes
2. I'll suggest a commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best practices

- Use present tense
- Explain what and why, not how


## References

- Additional templates and best practices are in the Claude Skill repo and [Skill authoring best practices][1].

[1]: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices