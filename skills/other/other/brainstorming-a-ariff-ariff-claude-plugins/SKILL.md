---
name: brainstorming
description: Transform rough ideas into solid designs through structured questioning
version: 1.0.0
author: Ariff
when_to_use: Before any feature implementation, when user describes an idea
---

# Brainstorming → Design

## Purpose
Turn vague ideas into actionable designs through Socratic questioning.

> "I'm using the Brainstorming skill to refine your idea into a design."

## The Flow

```
[Idea] → Phase 1: Understand → Phase 2: Explore → Phase 3: Design → [Plan]
```

## Phase 1: Understanding (Ask Questions)

**One question at a time. Prefer multiple choice.**

Questions to ask:
- What problem does this solve?
- Who's the user?
- What's success look like?
- Any constraints (time, tech, integrations)?
- What's already built that this touches?

**Before asking:** Check working directory for existing context.

## Phase 2: Exploration (Present Options)

Present 2-3 approaches:

```markdown
### Approach A: [Name]
- Architecture: [how it works]
- Pros: [benefits]
- Cons: [tradeoffs]
- Complexity: [low/medium/high]

### Approach B: [Name]
...
```

Ask: "Which approach resonates? Or should we explore others?"

## Phase 3: Design (Incremental)

Present design in 200-300 word chunks:
1. Architecture overview
2. Key components
3. Data flow
4. Error handling
5. Testing strategy

After each chunk: "Does this look right?"

## Phase 4: Handoff

When design approved:

> "Ready to create the implementation plan?"

If yes → Use `writing-plans` skill

## Going Backwards

**It's okay to revisit earlier phases:**
- New constraint discovered → Back to Phase 1
- Design doesn't feel right → Back to Phase 2
- Missing requirements → Back to Phase 1

Don't force linear progress.

## Principles

- **YAGNI** - Don't design what's not needed
- **Explore alternatives** - Never settle on first idea
- **Validate incrementally** - Small chunks, frequent feedback
- **Document decisions** - Why, not just what
