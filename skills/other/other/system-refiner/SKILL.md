---
name: system-refiner
description: "Autonomously correct project rules when negative feedback occurs. Use PROACTIVELY when user says 'no', 'wrong', 'wait', 'not that', or 'actually'. Identifies the root cause in commands, agents, skills, or documentation and rewrites the offending instruction to prevent recurrence."
---

<mission_control>
<objective>Analyze the mistake, find the instruction that caused it, and patch the relevant file.</objective>
<success_criteria>offending rule identified; atomic patch applied; user informed of the change</success_criteria>
</mission_control>

## Workflow

1. **Detect**: User correction ("No," "Wait," "Wrong," "Not what I meant")
2. **Trace**: Ask "Which instruction allowed this mistake?"
   - Project documentation? → Update the source
   - Skill workflow? → Edit the skill
   - Command logic? → Fix the command
   - Agent prompt? → Refine the agent
3. **Identify the Gap**: Why did the instruction fail? Was it missing, vague, or contradictory?
4. **Patch**: Apply targeted edit to the relevant file
5. **Report**: "I've updated [file] to ensure I [new behavior]."

## Root Cause Mapping

| If the mistake reveals... | Target... |
| :--- | :--- |
| Missing or wrong project rule | Documentation, CLAUDE.md, .claude/rules/ |
| Wrong procedural pattern | Relevant skill in .claude/skills/ |
| Command logic issue | Command file in .claude/commands/ |
| Agent behavior problem | Agent config in .claude/agents/ |
| Hook or tool mismatch | Hook definition or tool schema |

## Patching Principles

- **Be specific**: Patch the exact instruction that failed, not surrounding content
- **Generalize**: Extract principle from the specific mistake
- **Respect structure**: Follow each file's existing conventions (XML tags, tables, etc.)
- **Place strategically**: Put new constraints where they'll be noticed (file bottoms for recency)

---

<critical_constraint>
- NEVER create new files for corrections; ALWAYS edit existing rules/skills/commands/agents.
- Use the Delta Standard: Only add rules for things you actually got wrong.
- Keep patches atomic. Change the logic, not the formatting.
- If unsure where the rule belongs, trace from effect to cause before editing.
</critical_constraint>
