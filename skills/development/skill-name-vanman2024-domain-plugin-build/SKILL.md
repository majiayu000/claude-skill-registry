---
name: skill-name-vanman2024-domain-plugin-build
description: '{{DESCRIPTION_WHAT_IT_DOES}}. Use when {{TRIGGER_KEYWORDS_AND_CONTEXT}}.'
---

---
name: {{SKILL_NAME}}
description: {{DESCRIPTION_WHAT_IT_DOES}}. Use when {{TRIGGER_KEYWORDS_AND_CONTEXT}}.
{{ALLOWED_TOOLS}}
---

# {{SKILL_NAME}}

**CRITICAL: The description field above controls when Claude auto-loads this skill.**

**Description Template:**
```yaml
description: [What it does]. Use when [building/creating/validating/analyzing] [specific things], [related activities], or when user mentions [keywords], [terms], [phrases].
```

**Good Examples:**
```yaml
# Validator Skill
description: Validate and auto-fix MCP server structure. Use when building MCP servers, validating server code, fixing server issues, or when user mentions MCP validation, server structure, or FastMCP compliance.

# Generator Skill
description: Generate React components with validation. Use when creating React components, building UI elements, scaffolding components, or when user mentions React, components, or UI generation.

# Analyzer Skill
description: Detect framework and project structure. Use when initializing projects, analyzing codebases, identifying frameworks, or when user mentions project detection, framework identification, or stack analysis.
```

**Bad Examples (too vague - won't trigger):**
```yaml
description: Helps with files  # ❌ Too vague
description: Development skill  # ❌ No triggers
description: Use when needed  # ❌ No specifics
```

## Instructions

{{STEP_BY_STEP_INSTRUCTIONS}}

## Examples

{{CONCRETE_EXAMPLES}}

## Requirements

{{REQUIREMENTS}}

---

**Generated from**: $HOME/.claude/marketplaces/multiagent-dev/plugins/multiagent-build/skills/build-assistant/templates/skills/SKILL.md.template
**Template Version**: 1.0.0
