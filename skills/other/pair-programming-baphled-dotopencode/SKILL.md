---
name: pair-programming
description: Collaborate effectively through pairing - driver/navigator, mob programming
category: General Cross Cutting
---

# Skill: pair-programming

## What I do

I facilitate effective collaborative coding. I manage the roles of driver and navigator, ensuring both participants stay engaged, maintain high focus, and produce higher quality code than they would solo.

## When to use me

- When tackling complex logic or architectural transitions
- To onboard a new developer or share domain knowledge
- When debugging a particularly stubborn or opaque issue
- During high-stakes sessions where two sets of eyes are critical

## Core principles

1. **Driver vs Navigator** — The driver focuses on the immediate implementation (the "keyboard"); the navigator focuses on the bigger picture (potential bugs, edge cases, upcoming steps).
2. **Rotate frequently** — Swap roles every 30-60 minutes to maintain energy and prevent fatigue.
3. **Think aloud** — Both participants must vocalise their thought processes to ensure alignment.
4. **Mobbing for the win** — Use mob programming (3+ people) for architectural decisions or team-wide knowledge sharing.

## Patterns & examples

**Ping-Pong TDD:**
- **Developer A:** Writes a failing test.
- **Developer B:** Writes the code to make it pass, then writes the next failing test.
- **Developer A:** Makes the test pass, refactors, then writes the next failing test.

**Navigator Checklist:**
- Is there a simpler way to write this?
- Are we missing an edge case (e.g. null/empty inputs)?
- Does this align with our existing architectural patterns?
- Is the naming clear and descriptive?

## Anti-patterns to avoid

- ❌ **The passive navigator** — Checking emails or zoning out while the driver codes.
- ❌ **Keyboard hogging** — One person driving for hours without swapping.
- ❌ **Watch-the-master** — Senior developer driving while the junior just watches (not true pairing).

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/General-Cross-Cutting/Pair Programming.md`

## Related skills

- `bdd-workflow` — Natural fit for Ping-Pong TDD
- `clean-code` — Easier to enforce with two people
- `code-reviewer` — Real-time code review during pairing
- `mentoring` — Sharing knowledge through collaboration
