---
name: mend-agent-rules
description: Synchronize CLAUDE.md and AGENTS.md with available agents and skills.
---

# Mend Agent Rules

This skill automates the synchronization of `CLAUDE.md` and `AGENTS.md` using AI / LLM to ensure they always reflect the current state of the repository's agents and skills.

## Purpose

To provide AI agents with up-to-date instructions and context about available specialized capabilities without manual maintenance.

## Instructions

1.  **Discovery**: Scan the following directories and categorize them:
    - **Project Skills**: All `SKILL.md` files in `.claude/skills/` (recursive).
    - **Agents**: Agent definitions or metadata in `.claude/agents/`.
2.  **Extraction**: For each skill/agent found, extract:
    - `name`: From YAML frontmatter or directory name.
    - `description`: From YAML frontmatter or first paragraph.
    - `path`: Relative path from the workspace root.
3.  **Target Identification**: Identify documentation files and their respective markers:
    - **CLAUDE.md** and **AGENTS.md**:
      - `<!-- AVAILABLE_SKILLS_START -->` and `<!-- AVAILABLE_SKILLS_END -->`
      - `<!-- AVAILABLE_AGENTS_START -->` and `<!-- AVAILABLE_AGENTS_END -->`
      - `<!-- FRAMEWORK_DOCS_START -->` and `<!-- FRAMEWORK_DOCS_END -->`
4.  **Formatting**:
    - **Skills List**: Generate a table of all discovered project skills.
    - **Agents List**: Generate a table of discovered agents.
5.  **Synchronization**: Replace the content between the specific markers in BOTH target files.
    - Update BOTH `CLAUDE.md` and `AGENTS.md` with the project skills table, agents table, and framework documentation.
    - **CRITICAL**: The framework documentation (explaining what Agent Skills are, directory structure, and guidelines) MUST be present in both files between the `FRAMEWORK_DOCS` markers. If it is missing from one but present in the other, synchronize it.
6.  **Verification**: Confirm that both files are identical except for their top-level headers (`# CLAUDE.md` vs `# AGENTS.md`) and that all markers are preserved.

## Markers

### CLAUDE.md

```html
<!-- AVAILABLE_SKILLS_START -->
<!-- AVAILABLE_SKILLS_END -->

<!-- AVAILABLE_AGENTS_START -->
<!-- AVAILABLE_AGENTS_END -->

<!-- FRAMEWORK_DOCS_START -->
<!-- FRAMEWORK_DOCS_END -->
```

### AGENTS.md

```html
<!-- AVAILABLE_SKILLS_START -->
<!-- AVAILABLE_SKILLS_END -->

<!-- AVAILABLE_AGENTS_START -->
<!-- AVAILABLE_AGENTS_END -->

<!-- FRAMEWORK_DOCS_START -->
<!-- FRAMEWORK_DOCS_END -->
```

## Example Table Format

<!-- markdown-link-check-disable -->

| Name     | Description                                                              | Link                                                                 |
| :------- | :----------------------------------------------------------------------- | :------------------------------------------------------------------- |
| lint-fix | Iteratively run linters, apply auto-fixes, and resolve remaining issues. | [.claude/skills/lint-fix/SKILL.md](.claude/skills/lint-fix/SKILL.md) |

<!-- markdown-link-check-disable -->
