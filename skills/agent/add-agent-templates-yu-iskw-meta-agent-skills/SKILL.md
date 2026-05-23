---
name: add-agent-templates
description: Add new Agent templates to the meta-agent-skills framework.
---

# Add Agent Templates

## Purpose

This skill standardizes the process of adding new Agent templates to the `meta-agent-skills` framework. It ensures that new agents follow the required structure for automatic generation and skill binding by the Meta-Agent.

## When to Use

- When you want to add a new specialized agent (e.g., `cloud-deployer-agent`, `perf-optimizer-agent`) to the framework.
- When you want to define a new set of capabilities that a subagent should possess.

## Instructions

1.  **Define Agent Persona**:
    - Identify the agent's name (e.g., `sre-agent`).
    - Define its primary purpose and responsibilities.

2.  **Select Required Skills**:
    - List the skills from `skills/meta-agent-skills/assets/templates/skills/` that this agent will need.
    - These should be listed in the YAML frontmatter.

3.  **Use Boilerplate**:
    - Read `assets/agent-template-boilerplate.md` for the standard structure.
    - Create a new file in `skills/meta-agent-skills/assets/templates/agents/` named `<agent-name>.md`.

4.  **Configure Template**:
    - Fill in the YAML frontmatter (`name`, `description`, `skills`).
    - Use the `<!-- SKILLS_START -->` and `<!-- SKILLS_END -->` markers in the **Capabilities** section.
    - Refer to [references/agent-conventions.md](references/agent-conventions.md) for detailed formatting rules.

5.  **Register Capability**:
    - Update the `Capabilities Generated` section in `skills/meta-agent-skills/SKILL.md` to include the new agent.

6.  **Verify**:
    - Ensure the template is readable and follows the format of existing agents like `codebase-maintainer-agent.md`.

## References

- [Agent Conventions](references/agent-conventions.md)
- [Agent Skills Standard](https://agentskills.io)
