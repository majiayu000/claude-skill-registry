---
name: df:progress
description: |
  Check project progress, show context, and route to next action.
  Use when the user asks about project status, what's next, or where things stand.
  Triggers on: "where are we?", "what's the status?", "show progress", "what's next?", "project status", "how far along are we?"
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - SlashCommand
---
<objective>
Check project progress, summarize recent work and what's ahead, then intelligently route to the next action - either executing an existing job or creating the next one.

Provides situational awareness before continuing work.
</objective>

<execution_context>
@~/.claude/devflow/workflows/progress.md
</execution_context>

<process>
Execute the progress workflow from @~/.claude/devflow/workflows/progress.md end-to-end.
Preserve all routing logic (Routes A through F) and edge case handling.
</process>
