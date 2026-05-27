---
name: create-persona
description: Create detailed user persona with guided questions
argument-hint: <persona-name>
---

# create-persona

**Category**: Product & Strategy

## Usage

```bash
create-persona <name>
```

## Arguments

- `<name>`: Required argument

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Read the source file at `claude_settings/python/templates/persona-template.md`
2. Read the template content
3. If arguments provided, use them for output filename
4. Generate the file from the template
5. Replace any template variables if needed

## Source Content Location

The full process documentation can be found at:
`claude_settings/python/templates/persona-template.md`

Claude Code should read this file and follow the documented process exactly.

## Example

```bash
create-persona example-name
```
