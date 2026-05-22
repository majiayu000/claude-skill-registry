---
name: brainstorming
model: reasoning
version: 1.0.0
description: >
  Explore ideas before implementation through collaborative dialogue. Use before any
  creative work — creating features, building components, adding functionality, or
  modifying behavior. Turns ideas into fully formed designs and specs through structured
  conversation.
tags: [brainstorming, design, ideation, planning, creative, specification]
---

# Brainstorming Ideas Into Designs

Turn ideas into fully formed designs and specs through natural collaborative dialogue. This skill ensures you explore the problem space before jumping to solutions.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install brainstorming
```


## When to Use

Use this before any creative work:

- Creating new features or components
- Adding significant functionality
- Modifying existing behavior or architecture
- When the user has an idea but no clear spec
- When requirements are ambiguous or incomplete
- Before any implementation that involves design decisions

## The Process

### Phase 1: Understand the Idea

Start by understanding what exists and what's being proposed.

**Gather context first:**
- Check the current project state (files, docs, recent commits)
- Read existing documentation, README, or design docs
- Understand the current architecture and constraints

**Ask questions to refine the idea:**
- Ask questions **one at a time** — never overwhelm with multiple questions
- Prefer **multiple-choice questions** when possible — easier to answer than open-ended
- Focus on understanding: purpose, constraints, success criteria
- If a topic needs deeper exploration, use follow-up questions

**Good questions to ask:**
- "What problem does this solve for the user?"
- "What does success look like?"
- "Are there existing patterns in the codebase we should follow?"
- "What constraints do we need to work within?" (time, tech stack, compatibility)
- "Who is the audience for this feature?"

### Phase 2: Explore Approaches

Once you understand the problem, propose solutions — never settle on the first idea.

- **Always propose 2-3 different approaches** with clear trade-offs
- **Lead with your recommendation** and explain why
- Present options conversationally with pros/cons
- Wait for the user to choose before proceeding

**Format for presenting approaches:**

```markdown
## Approach A: [Name] — Recommended
- Pros: ...
- Cons: ...
- Why I recommend this: ...

## Approach B: [Name]
- Pros: ...
- Cons: ...

## Approach C: [Name]
- Pros: ...
- Cons: ...
```

### Phase 3: Present the Design

Once the approach is chosen, present the detailed design incrementally.

- **Break the design into sections of 200-300 words**
- **Ask after each section:** "Does this look right so far?"
- Cover these aspects:
  - Architecture and component structure
  - Data flow and state management
  - API contracts and interfaces
  - Error handling and edge cases
  - Testing strategy
- Be ready to go back and revise earlier sections if something doesn't fit

### Phase 4: After the Design

**Documentation:**
- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Commit the design document to git
- Include: problem statement, chosen approach, design details, open questions

**Implementation (if continuing):**
- Ask: "Ready to set up for implementation?"
- Create an isolated workspace if available
- Create a detailed implementation plan with ordered tasks

## Key Principles

| Principle | Why |
|-----------|-----|
| One question at a time | Multiple questions overwhelm and get partial answers |
| Multiple choice preferred | Faster to answer; reveals options the user hadn't considered |
| YAGNI ruthlessly | Remove features from designs before they become code |
| Explore alternatives | The first idea is rarely the best; always consider 2-3 |
| Incremental validation | Present design in sections; validate each before moving on |
| Be flexible | Go back and clarify when something doesn't make sense |
| Start with why | Understanding the problem prevents building the wrong solution |

## Common Brainstorming Contexts

### New Feature
Focus on: user need, scope boundaries, integration with existing system, MVP vs full vision

### Refactoring
Focus on: what's wrong with current approach, risk assessment, migration path, backwards compatibility

### Architecture Decision
Focus on: requirements driving the change, evaluation criteria, long-term implications, reversibility

### Bug Fix (Complex)
Focus on: root cause vs symptoms, scope of impact, regression risk, testing strategy

## Platform Templates

Ready-to-use brainstorming instructions for different AI platforms:

- `templates/platforms/claude-knowledge.md` — Claude project knowledge format
- `templates/platforms/copilot-instructions.md` — GitHub Copilot instructions format
- `templates/platforms/cursorrules.md` — Cursor rules format

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Jumping to code | No design validation, leads to rework | Complete all 3 phases before implementation |
| Asking 5 questions at once | User answers 2, skips 3 | One question per message |
| Only one approach | No comparison, no confidence in choice | Always present 2-3 alternatives |
| Design as monologue | User disengages, misses problems | Check in after every 200-300 words |
| Gold-plating | Feature creep in design phase | Apply YAGNI; cut anything not essential for v1 |
| Skipping context | Design doesn't fit existing system | Read the codebase before proposing architecture |

## NEVER Do

1. **NEVER skip brainstorming for creative work** — jumping to implementation without exploring the problem leads to rework
2. **NEVER present the full design at once** — break it into sections and validate each one
3. **NEVER assume requirements** — ask when uncertain; wrong assumptions compound
4. **NEVER implement before the design is validated** — code is expensive to change; designs are cheap
5. **NEVER ask more than one question per message** — batch questions get partial or confused answers
6. **NEVER settle on the first approach** — always explore at least 2-3 alternatives before committing
7. **NEVER design without understanding the existing system** — check the codebase first; your design must fit what exists
