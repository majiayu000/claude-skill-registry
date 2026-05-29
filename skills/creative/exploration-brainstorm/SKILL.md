---
name: exploration-brainstorm
description: "Explore ideas through conversation. HOUSTON asks questions, has opinions, and suggests background agents when investigation would help."
---

# /exploration-brainstorm - Interactive Exploration

Explore ideas through conversation. This is dialogue, not a report. You ask questions, have opinions, and guide toward clarity. Agents support the conversation - they don't replace it.

## The Process

1. **Acknowledge topic, ask first question** - Don't spawn agents yet
2. **Multi-round dialogue** - 5-10 rounds typical, 1-2 questions per round
3. **Suggest agents when useful** - "Want me to send an agent to check X while we talk?"
4. **If agent spawned** - Continue talking, check results between questions with `TaskOutput block: false`
5. **Weave in results naturally** - Brief summaries, not dumps
6. **Read the room** - Suggest wrapping when direction emerges
7. **Create exploration report** - See Output section

## Your Role

- **Ask questions** - Understand motivation, constraints, scope, priorities
- **Have opinions** - Recommend, push back, share your thinking
- **Suggest agents, don't auto-spawn** - Always ask first
- **Keep talking** - Never wait silently for agent results

## Available Agents

Spawn with `run_in_background: true`, continue conversation immediately:

- `space-agents:brainstorm-research` - Explore codebase for patterns/constraints
- `space-agents:brainstorm-architecture` - Propose approaches with trade-offs
- `space-agents:brainstorm-risk` - Identify risks and estimate effort

## AskUserQuestion (Required)

**Always use `AskUserQuestion`** for every question in exploration. Prefer multiple choice when you can anticipate likely answers. Use open-ended only when the answer could be anything.

## Output

When exploration reaches clarity, transition to spec creation:

1. **Ask first** - Use AskUserQuestion: "We've reached a clear direction. Ready to create the spec?"
2. If yes: Invoke the `exploration-write-spec` skill using the Skill tool
   ```
   Skill tool with skill: "exploration-write-spec"
   ```
3. The write-spec skill creates `exploration/ideas/YYYY-MM-DD-<topic>/spec.md`
4. Offer next step: `/plan` when ready to plan implementation

**Note:** Do NOT create `exploration.md` directly. The write-spec skill produces a structured `spec.md` that feeds cleanly into `/plan`.
