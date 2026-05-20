---
name: retrospective
description: Learning from failures and successes, post-mortems, continuous improvement
category: Thinking Analysis
---

# Skill: retrospective

## What I do

I manage the process of reflecting on past work to identify improvements. I facilitate blameless analysis of failures and capture successful patterns to ensure continuous improvement in the development process.

## When to use me

- After completing a major feature or project
- Following a production incident (post-mortem)
- Periodically (e.g. every sprint) to refine team workflows
- When a recurring problem or friction point is identified

## Core principles

1. **Blamelessness** — Focus on system failures rather than individual mistakes. Assume everyone did the best they could with the information they had.
2. **Action-oriented** — Every retrospective must produce specific, owner-assigned, and time-bound action items.
3. **Timeline reconstruction** — For incidents, build a factual timeline before trying to identify causes.
4. **Distinguish root vs contributing** — Use the "5 Whys" to dig past surface symptoms to the underlying system issue.

## Patterns & examples

**4Ls Format:**
- **Liked:** What went well? (e.g. "The new CI pipeline saved us hours.")
- **Learned:** What new knowledge was gained? (e.g. "We learned that library X has a memory leak.")
- **Lacked:** What was missing? (e.g. "We lacked clear requirements for the edge cases.")
- **Longed For:** What do we want next time? (e.g. "I longed for more pair programming during the refactor.")

**Root Cause Analysis (5 Whys Example):**
- **Problem:** Deployment failed.
- **Why?** The database migration timed out.
- **Why?** It was trying to index a 100M row table.
- **Why?** We didn't test the migration on a production-sized dataset.
- **Why?** Our staging database is too small.
- **Root Cause:** Inadequate testing environments for production scale.

## Anti-patterns to avoid

- ❌ **Pointing fingers** — Using the retro to air personal grievances or blame individuals.
- ❌ **Retrospective amnesia** — Identifying the same problems repeatedly without taking action.
- ❌ **Skipping successes** — Only focusing on what went wrong; it's equally important to know why things went well.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Thinking-Analysis/Retrospective.md`

## Related skills

- `critical-thinking` — Analysing the findings of the retro
- `assumption-tracker` — Identifying assumptions that led to failure
- `systems-thinker` — Understanding the system dynamics that led to issues
- `memory-keeper` — Capturing the "Learned" section for future sessions
