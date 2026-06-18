---
name: product-messaging
version: '1.0'
last_updated: 2026-05-19
author: genesys-growth
description: Build a 10-component messaging library from your positioning + ICP + competitor aggregate. Produces positioning statement, value propositions, key differentiators, taglines, CTA variants, proof points, messaging hierarchy, status-quo alternatives. Writes to marketing/messaging/messaging.md as the canonical messaging library every downstream content / paid / outbound / lifecycle skill reads. Triggers - "product messaging", "messaging library", "value props", "messaging framework", "build messaging", "messaging components"
goal: Build a 10-component messaging library from positioning + ICP + competitor aggregate.
outcome: marketing/messaging/messaging.md — the single source of truth for every downstream copy decision.
primitive: product-marketing
ontology_type: messaging
review_gate: 2
inputs:
  required: []
  recommended:
    - positioning
    - icp-research
outputs:
  - type: messaging
    feeds_into:
      - landing-page-copy
      - content-strategy
      - outreach-emails
      - lifecycle-marketing
owned_by_agent: pmm
mcps_used:
  - exa
triggers:
  slash_commands:
    - /product-messaging
status: draft
---

# product-messaging — Stage 2 synthesis skill (PMM spine)

Reads the canonical positioning + ICP and produces the 10-component messaging library. The single source of truth for every downstream copy decision (landing pages, social, paid, outbound, lifecycle, sales enablement).

---

## When to use

- After positioning locks
- Quarterly refresh
- When positioning refreshes (messaging depends on positioning)
- When a value prop stops landing in customer conversations

## When NOT to use

- For positioning strategy (use `/positioning` — messaging depends on positioning, not the reverse)
- For voice rules (use `/tov-guidelines` — voice is in `marketing/brand/`)
- For audience-specific copy variants (use `/landing-page-copy` or downstream content skills — they read this library and produce audience-tailored variants)

## How it works

1. Inputs: none required (skill reads canonical files automatically)
2. Reads: `marketing/positioning/positioning.md` (anchor + differentiators + value props per priority), `marketing/icp/ICP.md` (champion persona + JTBD + pain priority order), `marketing/competitors/aggregate.md` (status quo alternatives synthesized), optionally `marketing/brand/brand-voice.md` (voice applied to messaging output)
3. Produces a 10-component messaging library (matches the PulseAnalytics example at `marketing/messaging/messaging.md`):
   1. **Positioning statement** (1 sentence, the anchor)
   2. **Value propositions** (in priority order — outcome-shaped, not feature-shaped)
   3. **Key differentiators** (what makes you different)
   4. **Status-quo alternatives** (what the buyer does today)
   5. **Taglines** (3-5 candidates + working tagline)
   6. **CTA variants** (primary / secondary / footer)
   7. **Proof points** (real data only; `[UNAVAILABLE]` for what isn't measured)
   8. **Messaging hierarchy** (by audience — champion / economic buyer / sales / end users)
   9. **What we are NOT** (anti-positioning)
   10. **Headlines per channel** (homepage / pricing / LinkedIn / cold email)
4. Marks the file `status: locked` once approved
5. Writes to `marketing/messaging/messaging.md` (overwrites prior canonical; git history preserves prior versions)

## Invoke

```
/product-messaging
```

Or focused:
```
/product-messaging refresh — value prop 1 stopped landing, regenerate
```

## Example output

See [`marketing/messaging/messaging.md`](../../../marketing/messaging/messaging.md) for the PulseAnalytics seed. Notice the value props are outcome-shaped ("stop owning the pipeline-review prep") not feature-shaped ("multi-touch attribution"). The headlines-per-channel section gives downstream skills ready-to-use copy per surface.

## Dependencies

- **Reads from:** `marketing/positioning/positioning.md` (required, must be locked); `marketing/icp/ICP.md` (required); `marketing/competitors/aggregate.md` (recommended); `marketing/brand/brand-voice.md` (optional)
- **Writes to:** `marketing/messaging/messaging.md` (canonical)
- **Downstream readers:** `/landing-page-copy`, `/linkedin-content`, `/outreach-emails`, `/ad-creative-brief`, `/lifecycle-marketing`, `/sales-enablement`, every content / paid / outbound / lifecycle execution skill

## Customization

The 10-component default tracks the Genesys ontology (`.claude/rules/ontology.md` § messaging). Add a component (e.g., "Objection handlers" if the team uses them frequently in sales conversations) by appending to the list.

Value-prop priority order is the most important customization — the order you place value props here is the order downstream content skills will lead with. If pain priority shifts in ICP refreshes, re-prioritize value props.

## Where this fits in the Example 1 chain

```
Week 1: /competitor-aggregate + /icp-research → canonical context
Week 2: /positioning → positioning canonical
Week 2: /product-messaging (THIS SKILL) → messaging canonical
Week 3+: every execution skill reads messaging.md
```

## Refresh cadence

Quarterly, after positioning refreshes. Trigger sooner if value props stop landing in customer conversations.
