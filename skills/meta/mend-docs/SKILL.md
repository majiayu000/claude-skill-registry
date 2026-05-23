---
name: mend-docs
description: Maintain and synchronize documentation files with the actual codebase (agents and skills).
---

# Mend Docs

This skill enables the automatic synchronization of documentation files with the available agents and skills in the repository.

## Purpose

To ensure that `README.md`, `CONTRIBUTING.md`, and other public documentation files accurately list the capabilities of the agent without manual updates.

## Instructions

1.  **Discovery**: Scan the following directories and categorize them:
    - **Reusable Skills**: Look for all `SKILL.md` files in `skills/` (recursive).
    - **Project Skills**: Look for all `SKILL.md` files in `.claude/skills/` (recursive).
    - **Agents**: Look for agent definitions or metadata in `agents/` and `.claude/agents/`.
2.  **Extraction**: For each skill/agent found, extract:
    - `name`: From YAML frontmatter or directory name.
    - `description`: From YAML frontmatter or first paragraph.
    - `path`: Relative path from the workspace root.
3.  **Target Identification**: Identify documentation files and their respective markers:
    - **README.md**: Use `<!-- REUSABLE_SKILLS_START -->` and `<!-- REUSABLE_SKILLS_END -->`.
    - **CONTRIBUTING.md**: Use `<!-- PROJECT_SKILLS_START -->` and `<!-- PROJECT_SKILLS_END -->`.
4.  **Formatting**: Generate a table for each category.
    - Recommended format: A table with columns for Name, Description, and Link.
5.  **Synchronization**: Replace the content between the specific markers in the target documentation files.
    - Reusable skills go into `README.md`.
    - Project skills go into `CONTRIBUTING.md`.
    - **CRITICAL**: `README.md` MUST be written in English. Translate any non-English metadata (name, description) to English during the extraction/formatting phase for `README.md`.
6.  **Verification**: Ensure that the formatting is correct and all discovered skills are included in the correct file.

## Markers

### Reusable Skills (README.md)

```html
<!-- REUSABLE_SKILLS_START -->
<!-- REUSABLE_SKILLS_END -->
```

### Project Skills (CONTRIBUTING.md)

```html
<!-- PROJECT_SKILLS_START -->
<!-- PROJECT_SKILLS_END -->
```

## Example Table Format

<!-- markdown-link-check-disable -->

| Name     | Description                                                              | Link                                                                 |
| :------- | :----------------------------------------------------------------------- | :------------------------------------------------------------------- |
| lint-fix | Iteratively run linters, apply auto-fixes, and resolve remaining issues. | [.claude/skills/lint-fix/SKILL.md](.claude/skills/lint-fix/SKILL.md) |

<!-- markdown-link-check-enable -->
