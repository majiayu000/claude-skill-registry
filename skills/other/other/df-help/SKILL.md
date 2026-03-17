---
name: df:help
description: |
  Show available DevFlow commands and usage guide.
  Use when the user asks about DevFlow capabilities, available commands, or how to use the system.
  Triggers on: "what can you do?", "how do I use DevFlow?", "show commands", "help", "what commands are available?"
---
<objective>
Display the complete DevFlow command reference.

Output ONLY the reference content below. Do NOT add:
- Project-specific analysis
- Git status or file context
- Next-step suggestions
- Any commentary beyond the reference
</objective>

<execution_context>
@~/.claude/devflow/workflows/help.md
</execution_context>

<process>
Output the complete DevFlow command reference from @~/.claude/devflow/workflows/help.md.
Display the reference content directly — no additions or modifications.
</process>
