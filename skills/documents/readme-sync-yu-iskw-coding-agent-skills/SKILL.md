---
name: readme-sync
description: Synchronizes the list of Agent Skills in the root README.md with the actual skills present in the codebase.
---

# README Sync

## Purpose

Ensures that the `## Agent Skills` section in the root `README.md` accurately reflects all available skills in `skills/`.

## Workflow

1.  **Identify Skills**: Use `Glob` or `find` to locate all `SKILL.md` files in `skills/` and `.cursor/skills/`.
2.  **Extract Information**: For each skill found, use `uv run skills-ref read-properties <skill-directory>` to get the `name` and `description`.
3.  **Generate Markdown**: Format the collected information as a sorted list of markdown items:
    - Format: `- **[name](relative/path/to/skill/)**: description`
4.  **Update README.md**: Replace the content between `<!-- START-SKILLS -->` and `<!-- END-SKILLS -->` markers in the root `README.md` with the newly generated list.

## Implementation Notes

- The `skills-ref` tool is part of the project dependencies and can be run via `uv run`.
- Always maintain alphabetical order of the skills in the `README.md` list.
- Ensure the relative paths in the markdown links correctly point to the skill directories from the root.

## Examples

### Scenario: Updating README.md after adding a new skill

1. Find all skills in the directory `skills/`.
2. Get properties for each skill: `uv run skills-ref read-properties skills/claude-code-cli`.
3. Update `README.md` within the `<!-- START-SKILLS -->` block.
