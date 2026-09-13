---
name: ux-grill
description: Use when a running web app's UX has to be audited reproducibly rather than by feel — a deterministic mechanical pass over routes and viewports (axe, target size, horizontal overflow, page title, scripted journeys) followed by a screenshot-grounded interrogation of the operator, journey by journey, with two persona lenses from the target repo's manifest. Triggered by "grill the UX", "roast the dashboard", "UX-Audit", "/ux-grill". Bootstraps its own manifest from a loopback URL on the first run, so it never requires a hand-written file to start.
metadata:
  model: inherit
  color: magenta
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
---

# ux-grill

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/ux-grill/SKILL.md`](../../../skills/ux-grill/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
