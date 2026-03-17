---
name: awesome-skills-overview
description: Guide for understanding and contributing to the awesome-skills curated resource list. Use this skill when adding resources, organizing categories, or maintaining README.md consistency (no duplicates).
---

# Awesome Skills - Project Overview

## Purpose

This is a curated collection of Agent Skills, resources, and tools for AI coding agents like Claude Code, Codex, Gemini CLI, GitHub Copilot, Cursor, and more. The goal is to keep the list **high-signal**, **well-categorized**, and **non-duplicated**.

## Project Structure

```
awesome-skills/
├── README.md                # Main resource list (curated)
├── LICENSE                  # License
├── .claude/
│   └── skills/              # Claude skills (this directory)
└── ref/                     # Reference repositories (not curated)
    ├── awesome-agent-skills-*/
    ├── awesome-claude-skills-*/
    ├── awesome-codex-skills/
    ├── awesome-copilot-agents/
    └── ...
```

## README.md Format Convention

### Heading Structure

- Top-level categories use `##`.
- Subcategories use `###` (e.g., inside `Community Skills`).
- Use tables for skill listings with `| Skill | Description |` format.

### Link Format

- Use full URLs in table cells.
- Add a short description in the Description column.
- Keep descriptions **English** and concise.
- Do not add the same URL in multiple places.

### Example Entry

```markdown
### Development & Code Tools

| Skill | Description |
|-------|-------------|
| [skill-name](https://github.com/...) | Short description of the skill |
```

## Categorization Rules (How to Place a New Link)

- **Official Skills**: Skills from Anthropic, OpenAI, HuggingFace official repositories.
- **Skills by Teams**: Skills from recognized teams (Vercel, Trail of Bits, Sentry, Expo).
- **Community Skills**: Community-contributed skills organized by category.
- **Supporting Tools**: CLI tools, installers, and management utilities.
- **Tutorials & Resources**: Documentation, videos, articles, and learning materials.

## Duplicate Policy

**No duplicate URLs in README.md.** If a link fits multiple categories, pick the primary one.

## Contribution Checklist

1. Check for duplicates in `README.md` before adding.
2. Verify the link points to the canonical source (avoid low-value forks).
3. Keep the description English and useful.
4. Put it into the most appropriate category.
5. Prefer minimal changes over reformatting large sections.

## Full Resource List

For more detailed skill resources, complete link lists, or the latest information, use WebFetch to retrieve the full README.md:

```
https://raw.githubusercontent.com/gmh5225/awesome-skills/refs/heads/main/README.md
```

The README.md contains the complete categorized resource list with all links.
