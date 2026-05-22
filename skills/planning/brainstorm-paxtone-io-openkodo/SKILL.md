---
name: brainstorm
description: >
  Turn ideas into fully formed designs through collaborative questioning.
  Use before any creative work to explore user intent, requirements, and design.
---

# Brainstorming Ideas Into Designs

## Overview

Transform vague ideas into concrete, implementable designs through structured dialogue.
Ask questions one at a time, present designs in digestible sections, and validate
incrementally before committing to implementation.

**Core principle:** One question at a time. Never overwhelm with multiple questions.

**Announce at start:** "I'm using the brainstorm skill to explore this idea."

## When to Use

- Starting a new feature or project
- Exploring design alternatives
- Clarifying requirements before implementation
- Breaking down complex problems
- Any creative work that modifies behavior

## The Process

### Phase 1: Understanding the Idea

**Before asking questions:**
1. Run `kodo query "<topic>"` to check existing patterns and context
2. Check project state (files, docs, recent commits)
3. Review any related learnings from past sessions

**Asking questions:**
- **One question per message** - If topic needs more exploration, break into multiple questions
- **Prefer multiple choice** when possible - easier to answer than open-ended
- Focus on: purpose, constraints, success criteria, edge cases
- If user gives vague answer, follow up to clarify

**Question types (prefer in this order):**
1. Multiple choice: "Which approach: A, B, or C?"
2. Yes/No confirmation: "Should it also handle X?"
3. Open-ended only when necessary: "What happens when...?"

### Phase 2: Exploring Approaches

When requirements are clear:
1. **Propose 2-3 approaches** with clear trade-offs
2. Lead with your recommendation and explain why
3. Present options conversationally, not as bullet lists
4. Wait for user to choose before proceeding

**Format:**
```
I'd recommend approach A because [reasoning].

Alternatively:
- Approach B would [trade-off]
- Approach C would [trade-off]

Which direction feels right?
```

### Phase 3: Presenting the Design

**Once approach is chosen:**
1. Present in sections of **200-300 words**
2. After each section ask: "Does this look right so far?"
3. Cover: architecture, components, data flow, error handling, testing
4. Be ready to revise if something doesn't fit

**Sections to cover:**
- High-level architecture
- Key components and their responsibilities
- Data flow and state management
- Error handling strategy
- Testing approach
- Edge cases

### Phase 4: Documentation

**After design is validated:**
1. Write to `docs/plans/YYYY-MM-DD-<topic>-design.md`
2. Commit the design document
3. **Auto-extract learnings from the design doc:**
   ```bash
   kodo extract docs/plans/YYYY-MM-DD-<topic>-design.md
   ```
   This will:
   - Parse the design doc for learnings (rules, decisions, tech choices, workflows)
   - Add them to `.kodo/learnings/` with HIGH confidence (user-created design)
   - Create a context entry in `.kodo/context-tree/`
4. Capture any additional key decisions: `kodo reflect --signal "Decided to use X because Y"`

## Handoff to Implementation

After saving the design, offer:

**"Design saved to `docs/plans/<filename>.md`. Ready to create implementation plan?"**

If yes:
- Use `kodo:plan` skill to create detailed implementation plan
- Link to GitHub issue if exists: `kodo track link #123`

## Key Principles

- **One question at a time** - Never multiple questions in same message
- **Multiple choice preferred** - When possible, offer options
- **YAGNI ruthlessly** - Remove unnecessary features from designs
- **Incremental validation** - Present in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't fit

## Red Flags

**You're doing it wrong if:**
- Asking 3+ questions at once
- Presenting full design without checkpoints
- Skipping existing context check (`kodo query`)
- Not offering multiple approaches
- Moving to implementation without documenting design
