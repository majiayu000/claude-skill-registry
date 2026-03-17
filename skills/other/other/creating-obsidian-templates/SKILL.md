---
name: creating-obsidian-templates
description: Create Obsidian templates for the Second Brain vault. Use when asked to "create a template", "make a template for", "add an Obsidian template", or "template for X".
allowed-tools: Read, Write, Glob, Grep, WebFetch, WebSearch, AskUserQuestion
---

# Creating Obsidian Templates

Create templates for the Second Brain Obsidian vault that work with the core Templates plugin.

## Template Location

All templates go in: `content/_obsidian-templates/`

This directory is excluded from Nuxt Content (configured in `content.config.ts`).

## Template Format

Templates use Obsidian's template syntax:
- `{{date}}` - Current date (YYYY-MM-DD)
- `{{date:format}}` - Custom format (e.g., `{{date:YYYY-MM-DD}}`)
- `{{time}}` - Current time
- `{{title}}` - Note title

## Workflow

1. **Understand the use case**: Ask what the template is for if unclear
2. **Check existing templates**: `ls content/_obsidian-templates/`
3. **Research structure** (if external format): Fetch examples from the web
4. **Create template**: Write to `content/_obsidian-templates/{name}.md`
5. **Verify**: Confirm template is valid markdown

## Template Structure

```markdown
---
title: "Template Name - {{date:YYYY-MM-DD}}"
draft: true
---

## Section 1

<!-- Guidance comment -->

## Section 2

<!-- Guidance comment -->
```

## Existing Templates

| Template | Purpose |
|----------|---------|
| `newsletter.md` | Weekly newsletter draft for beehiiv |

## User Setup

Remind user to configure Obsidian:
1. Settings → Core plugins → Enable Templates
2. Template folder: `_obsidian-templates`
3. Shortcut: Cmd/Ctrl + T to insert
