---
description: "Extract skill candidate from conversation. Use when identifying automatable logic suitable for skill. Keywords: extract, skill, candidate, automatable. Not for command extraction, agent creation, or non-skill logic."
argument-hint: "[<logic-description>]"
---

<mission_control>
<objective>Identify automatable logic for skill creation</objective>
<success_criteria>Skill candidate specified with type and rationale</success_criteria>
</mission_control>

## Quick Start

Use this command when automatable logic needs extraction for skill creation.

## Execution

1. **Analyze**: Trust your conversational memory to identify complex automatable logic
2. **Decide**: Command vs Skill based on freedom and reuse (Commands = low freedom, fixed output; Skills = high freedom, inject knowledge)
3. **Report**: Present skill candidate with name, description (What-When-Not-Includes), and core sections

<critical_constraint>
Trust your conversational memory. Only read session files if context is unclear. Previous sessions available at `.claude/workspace/sessions/previous-session.jsonl` if comparing across sessions.
</critical_constraint>
