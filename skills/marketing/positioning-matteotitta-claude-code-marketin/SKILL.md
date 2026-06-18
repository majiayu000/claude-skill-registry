---
name: positioning
version: '1.0'
last_updated: 2026-05-19
author: genesys-growth
description: Develop positioning strategy with anchor, differentiators, status-quo alternatives, and a positioning statement. Reads from marketing/icp/ICP.md + marketing/competitors/aggregate.md. Writes to marketing/positioning/positioning.md as the canonical positioning every downstream skill reads. Triggers - "positioning", "category definition", "how do we position", "positioning strategy", "anchor + differentiators"
goal: Develop positioning strategy with anchor, differentiators, status-quo alternatives, and positioning statement.
outcome: marketing/positioning/positioning.md — the foundational PMM artifact every other strategy + execution skill reads.
primitive: product-marketing
ontology_type: positioning
review_gate: 2
inputs:
  required: []
  recommended:
    - icp-research
    - competitor-aggregate
outputs:
  - type: positioning
    feeds_into:
      - product-messaging
      - landing-page-copy
      - sales-enablement
owned_by_agent: pmm
mcps_used:
  - exa
triggers:
  slash_commands:
    - /positioning
status: draft
---

# positioning — Stage 2 synthesis skill (PMM spine)

Reads the canonical ICP + the canonical competitor aggregate and produces the positioning strategy. This is the foundational PMM spine artifact — every other strategy + execution skill reads from positioning.

---

## When to use

- After ICP + competitor aggregate are both locked
- Quarterly refresh
- After major competitive shift (new entrant, repositioning move) that invalidates current anchor
- After major ICP shift that changes who you're positioning for

## When NOT to use

- For messaging libraries or taglines (use `/product-messaging` after positioning locks)
- For battlecards (use `/sales-enablement`)
- For landing-page copy (use `/landing-page-copy` after messaging locks)

## How it works

1. Inputs: none required (skill reads canonical files automatically)
2. Reads: `marketing/icp/ICP.md` (champion JTBD + pain points + decision criteria), `marketing/competitors/aggregate.md` (threat matrix + where category doesn't compete), optionally `marketing/brand/brand-voice.md` (applies voice rules to the positioning statement)
3. Produces a positioning doc with these sections (matches the PulseAnalytics example at `marketing/positioning/positioning.md`):
   - **Anchor** — what category your product anchors to (or creates)
   - **Target customer** — pointer to ICP.md
   - **Status-quo alternatives** — what the customer does today + why each falls short
   - **Key differentiators** — what makes you different + why it matters to the ICP
   - **Value propositions (per priority)** — outcome-shaped statements ordered by ICP pain
   - **What we are NOT** — anti-positioning (explicit exclusions)
   - **Pricing positioning** — premium / mid-market / self-serve framing
   - **Tagline candidates** — 3-5 options + working tagline
4. Marks the file `status: locked` once approved
5. Writes to `marketing/positioning/positioning.md` (overwrites prior canonical; git history preserves prior versions)

## Invoke

```
/positioning
```

Or with focus:
```
/positioning refresh — competitor X just launched, anchor may need to shift
```

## Example output

See [`marketing/positioning/positioning.md`](../../../marketing/positioning/positioning.md) for the PulseAnalytics seed. Notice the anchor leads ("the marketing analytics layer that traces revenue without an engineering quarter"); status-quo alternatives are named with concrete fail-modes; value props are outcome-shaped ("stop owning the pipeline-review prep") not feature-shaped.

## Dependencies

- **Reads from:** `marketing/icp/ICP.md` (required, must be locked); `marketing/competitors/aggregate.md` (required, must be locked); `marketing/brand/brand-voice.md` (optional — applies voice to the positioning statement)
- **Writes to:** `marketing/positioning/positioning.md` (canonical)
- **Downstream readers:** `/product-messaging`, `/landing-page-copy`, `/linkedin-content`, `/outreach-emails`, `/ad-creative-brief`, every execution skill in the 5 workstreams

## Customization

The default "binary anchor" framing comes from the Genesys positioning ontology — pick ONE primary anchor, optionally one secondary. If you're operating in a category where you genuinely need to claim two anchors (rare; usually a positioning weakness), extend the body.

The status-quo-alternatives section is the most important — most B2B SaaS positioning fails by positioning against direct competitors when the real competition is "the spreadsheet" or "doing nothing." Spend extra cycles on this section.

## Where this fits in the Example 1 chain

```
Week 1: /competitor-research × N → /competitor-aggregate → competitor canonical locked
Week 1: /icp-research → ICP canonical locked
Week 2: /positioning (THIS SKILL) → positioning canonical
Week 2: /product-messaging reads positioning → messaging canonical
Week 3+: /landing-page-copy, /linkedin-content, /outreach-emails read messaging + positioning
```

## Refresh cadence

Quarterly. Trigger sooner on competitive shift, ICP shift, or value-prop validation falling apart in customer conversations.
