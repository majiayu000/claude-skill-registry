---
name: add-skill-templates
description: Add new Agent Skill templates to the meta-agent-skills framework.
---

# Add Skill Templates

## Purpose

This skill standardizes the process of adding new Agent Skill templates to the `meta-agent-skills` framework. It ensures that new templates follow the required structure for automatic instantiation by the Meta-Agent.

## When to Use

- When you want to add a new standard capability (e.g., `deploy-k8s`, `performance-bench`) to the `meta-agent-skills` framework.
- When existing templates need to be cloned or used as a basis for a new one.

## Instructions

1.  **Identify New Skill Requirements**:
    - Determine the name and purpose of the new skill.
    - Identify the primary commands that should be included in its **Commands** table.

2.  **Use Boilerplate**:
    - Read the boilerplate template from `assets/skill-template-boilerplate.md`.
    - Create a new file in `skills/meta-agent-skills/assets/templates/skills/` named `<skill-name>.md`.

3.  **Configure Template**:
    - Fill in the YAML frontmatter (`name`, `description`).
    - Use placeholders like `{{ order }}`, `{{ component }}`, `{{ path }}`, `{{ layer }}`, `{{ command }}`, and `{{ description }}` in the **Commands** table.
    - Refer to [references/conventions.md](references/conventions.md) for guidance on placeholder usage and layer naming.

4.  **Register Capability**:
    - Update the `Capabilities Generated` section in `skills/meta-agent-skills/SKILL.md` to include the new skill.

5.  **Verify**:
    - Ensure the template is readable and follows the format of existing templates like `lint-fix.md`.

## References

- [Conventions](references/conventions.md)
- [Agent Skills Specification](https://agentskills.io/specification)
