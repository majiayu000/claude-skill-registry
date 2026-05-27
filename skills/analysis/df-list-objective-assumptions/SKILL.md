---
name: df:list-objective-assumptions
description: |
  Surface Claude's assumptions about an objective approach before planning.
  Specialized diagnostic tool for reviewing AI assumptions.
argument-hint: "[objective]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

<objective>
Analyze an objective and present Claude's assumptions about technical approach, implementation order, scope boundaries, risk areas, and dependencies.

Purpose: Help users see what Claude thinks BEFORE planning begins - enabling course correction early when assumptions are wrong.
Output: Conversational output only (no file creation) - ends with "What do you think?" prompt
</objective>

<execution_context>
@~/.claude/devflow/workflows/list-objective-assumptions.md
</execution_context>

<context>
Objective number: $ARGUMENTS (required)

**Load project state first:**
@.planning/STATE.md

**Load roadmap:**
@.planning/ROADMAP.md
</context>

<process>
1. Validate objective number argument (error if missing or invalid)
2. Check if objective exists in roadmap
3. Follow list-objective-assumptions.md workflow:
   - Analyze roadmap description
   - Surface assumptions about: technical approach, implementation order, scope, risks, dependencies
   - Present assumptions clearly
   - Prompt "What do you think?"
4. Gather feedback and offer next steps
</process>

<success_criteria>

- Objective validated against roadmap
- Assumptions surfaced across five areas
- User prompted for feedback
- User knows next steps (discuss context, plan objective, or correct assumptions)
  </success_criteria>
