---
name: example-workflow
description: Use when demonstrating plugin workflow features - shows how skills can guide multi-step processes
---

# Example Workflow Skill

## Overview

This skill demonstrates how to create a workflow-based skill that guides Claude through a multi-step process. It serves as a reference implementation for plugin developers.

## When to Use

This is an example skill for learning purposes. In a real plugin, you would:
- Use when specific conditions match the skill's domain
- Provide clear triggering criteria
- Guide through complex multi-step workflows

## Example Workflow

When invoked, this skill would guide through these steps:

1. **Gather requirements** - Ask clarifying questions
2. **Plan approach** - Create a structured plan using TodoWrite
3. **Execute systematically** - Follow the plan step-by-step
4. **Verify results** - Confirm the outcome matches requirements

## Integration with Other Components

This skill demonstrates how skills can:
- Reference bundled documentation in `references/`
- Call executable scripts in `scripts/`
- Use MCP server tools provided by the plugin
- Trigger or respond to plugin hooks

## For Plugin Developers

Key points this example demonstrates:
- Clear YAML frontmatter with name and description
- Structured workflow with numbered steps
- Integration points with other plugin components
- Documentation of when/how to use the skill
