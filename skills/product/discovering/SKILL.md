---
name: discovering
description:
  Use when idea is vague, multiple interpretations exist, scope is undefined, or
  stakeholders need alignment before technical work begins
---

# Discovering Skill

Use when the what/why is unclear; output is a direction, not a solution.

## When to Use vs Researching

```
What's unclear?
├── What/Why (goal, scope, requirements) → Discovering
└── How (technical approach, implementation) → Researching
```

## When to Use

- Idea is vague or underspecified
- Multiple interpretations exist
- Need to align on scope and goals
- Stakeholders have different expectations

Skip if: request is clear and decision-ready (use **researching** skill
instead).

## Quick Reference

| Phase      | Focus                          | Output          |
| ---------- | ------------------------------ | --------------- |
| Context    | Code, docs, recent changes     | Current state   |
| Intent     | Purpose, constraints, criteria | Requirements    |
| Directions | 2-3 approaches + trade-offs    | Recommendation  |
| Confirm    | Sign-off                       | Discovery brief |

## Core Rules

- Gather project context first
- One question at a time
- Prefer multiple choice
- High-level directions, not technical solutions

## Flow

1. **Context** — Check code, docs, recent changes

2. **Intent** — Purpose, constraints, success criteria, scope

3. **Directions** — 2-3 high-level approaches with trade-offs; recommend one

4. **Confirm & Output** — Discovery brief:
   - Goal (1 sentence)
   - Non-goals
   - Direction/approach
   - Open questions (1-3 bullets)

Get sign-off before proceeding.

## Common Mistakes

| Mistake                           | Fix                                       |
| --------------------------------- | ----------------------------------------- |
| Jumping to technical solutions    | Stay high-level; how comes later          |
| Asking multiple questions at once | One question, wait for answer             |
| Skipping context gathering        | Always check existing code/docs first     |
| No clear recommendation           | Always pick one direction and explain why |
| Proceeding without sign-off       | Get explicit confirmation                 |

## After Discovery

- Technical uncertainty? → Use **researching** skill
- Direction clear? → Proceed to implementation
