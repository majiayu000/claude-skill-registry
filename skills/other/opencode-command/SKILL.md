---
name: opencode-command
description: Use this skill when creating, modifying, or understanding OpenCode commands stored in `~/.config/opencode/command/`.
---

# OpenCode Commands

Use this skill when creating, modifying, or understanding OpenCode commands stored in `~/.config/opencode/command/`.

## Location

Commands directory: `~/.config/opencode/command/`
Vault root: `/Users/alexismanuel/.config/opencode/`

## Command Structure

Commands are stored user prompts - markdown files with YAML frontmatter.

### File Format

```yaml
---
description: Short description of what command does
---

[Instructions for agent - what to do when command is invoked]

Load relevant skills if needed.

Arguments: $ARGUMENTS
```

### Required Fields

- `description` (YAML frontmatter): Short, action-oriented summary
- `$ARGUMENTS`: Placeholder for command arguments (if needed)

### Naming

- Use kebab-case: `bootstrap-daily-note.md`
- Descriptive, concise names matching the command's purpose

## Creating Commands

1. Choose a descriptive name (kebab-case)
2. Create markdown file in `~/.config/opencode/command/`
3. Add YAML frontmatter with description
4. Write clear instructions for the agent
5. Reference relevant skills to load
6. Include `$ARGUMENTS` placeholder if command accepts arguments

## Examples

Existing commands to reference:
- `diary.md` - Update daily note with session summary
- `save-session.md` - Save OpenCode session to vault
- `bootstrap-daily-note.md` - Bootstrap daily note from yesterday

## Best Practices

- Keep instructions concise and actionable
- Always reference relevant skills
- Test commands after creation
- Use consistent formatting across commands
