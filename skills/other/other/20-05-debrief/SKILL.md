---
name: 20-05-debrief
description: Write a full-fidelity post-mortem after completing development work. Use after any merge, feature completion, or significant work session.
---

# 20.05 Post-Mortem

Write a post-mortem after every significant piece of development work. This is NOT just for incidents — it's a full-fidelity account of what happened during the work so future agents and humans understand the real story.

⛔ **Post-mortems MUST be committed to `main`.** They are project history, not branch artifacts. If you're on a feature branch, switch to main (or finish your merge first via `20.04`) before creating the post-mortem.

## When to Write

- After every merge (triggered by `20.04`)
- After completing a feature or significant refactor
- After any work session where decisions were made, problems were hit, or lessons were learned

**There is no threshold.** Don't skip because "nothing went wrong" or "it was straightforward." Straightforward work still has decisions, context, and lessons worth capturing.

## Create the Post-Mortem

1. Make sure you're on `main`
2. Create a `tk` ticket tagged `post-mortem` with the template below filled in
3. Commit to `main`

## Template

```markdown
# Post-Mortem: <title>

**Date:** <date>
**Branch/Feature:** <branch or feature name>
**Duration:** <rough time spent>

## Goal

What were we trying to accomplish? One or two sentences.

## What Actually Happened

Factual replay of the work in sequence. Include:
- What was tried first
- What changed along the way
- Key timestamps or commits if relevant
- Links, quotes, error messages — concrete evidence

This section is calm and factual. No analysis yet.

## Decisions Made

For each significant choice:
- **Decision:** What we chose
- **Alternatives considered:** What else was on the table
- **Why:** The reasoning at the time
- **In hindsight:** Would we choose the same? Why or why not?

## Problems Hit

What went wrong or was harder than expected:
- What the problem was
- How it manifested (error messages, unexpected behavior, confusion)
- How it was resolved
- How long it took vs how long it should have taken

## What Worked

What went smoothly:
- Tools, patterns, or approaches that were effective
- Decisions that paid off
- Things to repeat next time

## What We'd Do Differently

Hindsight improvements — not blame, but honest reflection:
- Process changes
- Different technical approaches
- Better preparation or research
- Things that were over-engineered or under-engineered

## One Binding Improvement

Pick exactly ONE concrete, actionable improvement. Not five aspirational ideas — one thing that will actually get done.

- **What:** <specific change>
- **Who:** <person or agent responsible>
- **When:** <deadline or trigger>
```

## Rules

1. **Commit to `main`.** Post-mortems are project history. Never leave them on a feature branch or worktree.
2. **Write with full fidelity.** Don't sanitize, don't summarize into nothing. The goal is that someone reading this in 3 months understands what really happened.
3. **Blameless.** Describe what happened and why, not whose fault it was. People (and agents) make decisions under uncertainty — document the context, not the blame.
4. **One binding improvement.** Many post-mortems produce a list of 10 action items that nobody does. Pick one. It must actually happen. If you're motivated to do more, great — but only one is required.
5. **Do it now.** Don't defer "until later" — memory fades fast. The best post-mortem is written immediately after the work while context is fresh.
6. **Include the ugly parts.** Dead ends, wrong approaches, wasted time, confusion — these are the most valuable parts for future readers. A post-mortem that only describes success is useless.
