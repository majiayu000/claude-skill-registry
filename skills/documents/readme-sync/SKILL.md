---
name: readme-sync
description: Synchronizes the list of Agent Skills in the root README.md with the actual skills present in the codebase.
---

# README Sync

## Purpose

Ensures that the `## Agents` and `## Agent Skills` sections in the root `README.md` accurately reflect all available agents in `agents/` and skills in `skills/`.

## Workflow

1.  **Identify Items**:
    - Locate all agents: Files ending in `.md` in `agents/` (excluding `.gitkeep`).
    - Locate all skills: Directories in `skills/` containing a `SKILL.md` file.
2.  **Extract Information**:
    - For **skills**: Use `uv run skills-ref read-properties <skill-directory>` to get the `name` and `description`.
    - For **agents**: Read the YAML frontmatter directly from the `.md` file to extract `name` and `description`.
3.  **Generate Markdown**: Format the collected information as sorted lists:
    - Format: `- **[name](relative/path/to/item)**: description`
    - Note: For agents, the link should point to the `.md` file. For skills, the link should point to the directory.
4.  **Update README.md**:
    - Replace content between `<!-- START-AGENTS -->` and `<!-- END-AGENTS -->` with the agents list.
    - Replace content between `<!-- START-SKILLS -->` and `<!-- END-SKILLS -->` with the skills list.

## Implementation Notes

- The `skills-ref` tool is used for skills in `skills/`.
- For agents in `agents/`, extract the `name` and `description` from the YAML frontmatter (lines between `---`).
- Always maintain alphabetical order of the items in each section.
- Ensure the relative paths in the markdown links correctly point to the items from the root.
- **Do not** include items from `.cursor/skills/` or `.cursor/agents/`.

## Examples

### Scenario: Updating README.md after adding a new skill

1. Find all skills in the directory `skills/`.
2. Get properties for each skill: `uv run skills-ref read-properties skills/claude-code-cli`.
3. Update `README.md` within the `<!-- START-SKILLS -->` block.
