---
name: system-review
description: deeply review a system/architecture area and propose a simplification plan (Elon’s Algorithm).
---

Perform a deep system/structure review with the explicit goal of **drastically simplifying**.

## Method: Elon’s 5-Step Algorithm (in order)

1. **Make the requirements less dumb**
   - Challenge assumptions; list what’s unclear; ask the minimum questions to proceed.
2. **Delete**
   - Identify code, layers, features, and processes that should not exist.
   - Prefer removal over “refactor”.
3. **Simplify**
   - Propose the smallest design that satisfies the real requirements.
   - Reduce indirection and config surface area.
4. **Accelerate**
   - Find the current bottleneck and optimize only that.
5. **Automate**
   - Only once the process is simple and stable.

## Tools

- Use repo tooling (`scc`, `knip`, `jscpd`, `rg`) to find hotspots and duplication.
- If appropriate, use `oracle` for independent critique.
- Provide it all relevant context (key files, diagrams, constraints).

## Recurring Things To Check (If Relevant)

- Under-leveraging Convex (especially Components / `convex-helpers`) leading to excess boilerplate
- Re-inventing the wheel instead of using mature npm libraries
- React complexity driven by unnecessary effects
  - See `~/.config/docs/React/ReactEffectsGuide.md`

## Output Format

- Current state (what exists, in 5–10 bullets)
- Proposed target state (what it should become)
- Deletions (explicit list)
- Migration plan (smallest safe steps)
- Risks / open questions
