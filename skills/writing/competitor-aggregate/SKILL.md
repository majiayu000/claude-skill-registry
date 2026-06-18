---
name: competitor-aggregate
version: '1.0'
last_updated: 2026-05-19
author: genesys-growth
description: Synthesize multiple per-competitor research files (produced by /competitor-research) into a single canonical threat matrix. Writes to marketing/competitors/aggregate.md as the locked canonical version every downstream skill reads. Triggers - "competitor aggregate", "synthesize competitors", "competitor matrix", "threat matrix", "lock competitor canonical"
goal: Synthesize multiple per-competitor research files into a single canonical threat matrix.
outcome: marketing/competitors/aggregate.md — the locked canonical version every downstream skill reads.
primitive: research
ontology_type: competitor-intel
review_gate: 2
inputs:
  required: []
  recommended:
    - competitor-research
outputs:
  - type: competitor-intel
    feeds_into:
      - positioning
      - product-messaging
      - sales-enablement
owned_by_agent: researcher
mcps_used:
  - exa
triggers:
  slash_commands:
    - /competitor-aggregate
status: draft
---

# competitor-aggregate — Stage 2 synthesis skill

Reads every file under `marketing/competitors/*.md` (per-competitor research files produced by `/competitor-research`) and synthesizes them into a single canonical threat matrix. The output is the locked file that downstream skills (positioning, messaging, landing-page-copy, sales-enablement) read.

This is the **Stage 2 synthesis** step in the article's research → context loop. Stage 1 produces per-item research; Stage 2 locks the canonical version.

---

## When to use

- Day 3 of Example 1: after running `/competitor-research` on 3-5 competitors, synthesize them
- Quarterly refresh: re-run after individual competitor dossiers update
- Before refreshing `/positioning` — positioning reads the aggregate, not per-competitor files

## When NOT to use

- When fewer than 2 per-competitor files exist (no aggregation needed yet)
- For deep-diving a single competitor (use `/competitor-research`)
- For sales battlecards (use `/sales-enablement` after aggregate is locked)

## How it works

1. Inputs: none required (skill auto-discovers all files under `marketing/competitors/*.md` except `aggregate.md` itself)
2. Reads: every per-competitor dossier in the folder. Excludes the prior `aggregate.md` if one exists (we're rebuilding it).
3. Produces an aggregate threat matrix with these sections:
   - **Threat ranking** — ordered table: competitor name | threat level | category | primary axis of competition
   - **Common positioning patterns** — themes shared across competitors (e.g., all 3 lead on "model sophistication")
   - **Where the category competes** — the axes the category implicitly accepts as the playing field
   - **Where the category doesn't compete** — gaps in the collective positioning that your wedge can exploit
   - **Status-quo alternatives synthesized** — single deduplicated list across all competitors
   - **Per-competitor wedge summary** — one row per competitor: "where they lose / your wedge against them"
   - **Watch list** — events across the set that would change the matrix
4. Marks the file with `status: locked` frontmatter — signals downstream skills that this is the canonical version
5. Writes to `marketing/competitors/aggregate.md` (overwrites prior canonical; the prior version is preserved in git history)

## Invoke

```
/competitor-aggregate
```

Or scoped to a subset:
```
/competitor-aggregate synthesize only 0526-bizible.md and 0526-dreamdata.md
```

## Example output structure

```markdown
---
status: locked
locked_date: 2026-05-26
sources: [0526-competitor-a.md, 0526-competitor-b.md, 0526-competitor-c.md]
---

# Competitor aggregate — threat matrix (canonical)

## Threat ranking

| Competitor | Threat | Category | Primary axis |
|---|---|---|---|
| Bizible-style | PRIMARY | Multi-touch attribution | Model sophistication |
| Dreamdata-style | PRIMARY | Multi-touch attribution | Salesforce-native depth |
| HockeyStack-style | DIRECT | Marketing attribution | Self-serve mid-market |

## Common positioning patterns
... (3-5 bullet themes)

## Where the category doesn't compete (your wedge)
... (the gap your positioning exploits)

## Per-competitor wedge summary
... (one row per competitor)
```

## Dependencies

- **Reads from:** every `marketing/competitors/MMYY-*.md` file (per-competitor dossiers from `/competitor-research`)
- **Writes to:** `marketing/competitors/aggregate.md` (canonical, locked)
- **Downstream readers:** `/positioning`, `/product-messaging`, `/landing-page-copy`, `/sales-enablement`

## Customization

Add a custom dimension to the threat matrix (e.g., "Mid-market vs enterprise split") by editing the section list in this SKILL.md body. The aggregate adapts to whatever sections you specify.

## Where this fits in the Example 1 chain

```
Day 1-3: /competitor-research × N → per-competitor files
Day 3:   /competitor-aggregate (THIS SKILL) → canonical threat matrix
Day 5:   /icp-research reads aggregate.md
Week 2:  /positioning reads aggregate.md
```

## Refresh cadence

Re-run whenever any per-competitor file updates. Quarterly minimum; fortnightly if you're in a fast-moving category.
