---
name: mend-agent-templates
description: Maintain and synchronize agent templates with their associated skill templates.
---

# Mend Agent Templates

This skill automates the synchronization of agent templates in `skills/meta-agent-skills/assets/templates/agents/` with the actual metadata and descriptions of skill templates in `skills/meta-agent-skills/assets/templates/skills/`.

## Purpose

To ensure that agent templates always accurately reflect the current capabilities, names, and descriptions of the skills they reference in their YAML frontmatter.

## Instructions

1.  **Discovery**:
    - List all skill templates in `skills/meta-agent-skills/assets/templates/skills/*.md`.
    - List all agent templates in `skills/meta-agent-skills/assets/templates/agents/*.md`.

2.  **Extraction**:
    - For each **skill template**, extract:
      - `name`: From YAML frontmatter.
      - `description`: From YAML frontmatter.
    - For each **agent template**, extract:
      - `skills`: The list of skill names from YAML frontmatter.

3.  **Synchronization**:
    - For each agent template:
      - Locate the `Capabilities` section marked by `<!-- SKILLS_START -->` and `<!-- SKILLS_END -->`.
      - Generate a bulleted list of the agent's skills.
      - Each bullet should follow the format: `- **Skill Title**: description from the skill template.`
      - Note: "Skill Title" should be a title-cased version of the skill's machine `name` or its display name if available.
      - Replace the content between the markers with this generated list.

4.  **Verification**:
    - Ensure that all skills listed in the agent's frontmatter are represented in the `Capabilities` section.
    - Confirm that the descriptions match the source skill templates exactly.

## Markers

```html
<!-- SKILLS_START -->
<!-- SKILLS_END -->
```
